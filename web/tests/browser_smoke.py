"""Real Chromium browser checks against local static UI; network API responses are fixtures."""
import functools
from datetime import datetime, timedelta, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
import unittest
from urllib.parse import urlparse, parse_qs

from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/"engine/tools/opportunity_engine"

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

class BrowserSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler=functools.partial(QuietHandler,directory=str(ROOT/"web"))
        cls.http=ThreadingHTTPServer(("127.0.0.1",0),handler)
        cls.thread=threading.Thread(target=cls.http.serve_forever,daemon=True)
        cls.thread.start()
        cls.origin="http://127.0.0.1:"+str(cls.http.server_port)
        cls.pw=sync_playwright().start()
        cls.browser=cls.pw.chromium.launch(headless=True)
        cfg=json.loads((ENGINE/"config.json").read_text())
        cls.catalog={"topics":[{k:t[k] for k in ("id","label")} for t in cfg["topics"]],"markets":[{k:m[k] for k in ("id","label","language","region")} for m in cfg["markets"]]}
        cls.discovery={**json.loads((ENGINE/"catalog_v2.json").read_text()),"campaign":json.loads((ENGINE/"catalog_v3.json").read_text()),"features":{"queue_controls":False,"editorial_workflow":False,"wikimedia_evidence":False,"controlled_campaigns":False}}

    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.pw.stop();cls.http.shutdown();cls.http.server_close()

    def fixture_report(self,expired=False):
        now=datetime.now(timezone.utc)
        return {"schema_version":1,"collected_at":(now-timedelta(days=31 if expired else 1)).isoformat(),
                "expires_at":(now+timedelta(days=-1 if expired else 29)).isoformat(),
                "opportunities":[],"videos":{},"detail_errors":{},"revenue_by_market":{},
                "quota":{"successes":{"search":1},"attempts":{"search":1}},
                "channel_samples":[{"channel_id":"fixture","channel_title":"Fixture channel","channel_created_at":"2020-01-01","current_subscribers":42,"playlist_has_more":True,"missing_video_details":1,
                   "videos":[{"video_id":"a","title":"Fixture short-duration","published_at":(now-timedelta(days=2)).isoformat(),"duration":"PT30S","views":0,"audio_language":"de"},
                             {"video_id":"b","title":"Fixture long-duration","published_at":(now-timedelta(days=4)).isoformat(),"duration":"PT8M","views":None,"audio_language":"tr"}]}]}

    def open(self,viewport):
        context=self.browser.new_context(viewport=viewport)
        self.addCleanup(context.close)
        page=context.new_page()
        errors=[];unknown=[];calls=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        session={"authenticated":False}
        def handler(route):
            url=urlparse(route.request.url)
            if route.request.url.startswith(self.origin+"/") and not url.path.startswith("/api/"):
                return route.continue_()
            if not route.request.url.startswith(self.origin+"/api/"):
                unknown.append(route.request.url);return route.abort()
            calls.append((route.request.method,url.path))
            query=parse_qs(url.query)
            if url.path=="/api/session": data={"authenticated":session["authenticated"],"admin":False,"admin_configured":True,"audit_configured":True}
            elif url.path=="/api/login":session["authenticated"]=True;data={"authenticated":True,"admin":False,"admin_configured":True,"audit_configured":True}
            elif url.path=="/api/logout":session["authenticated"]=False;data={"authenticated":False}
            elif url.path=="/api/catalog":data=self.catalog
            elif url.path=="/api/discovery-catalog":data=self.discovery
            elif url.path=="/api/research":
                if query.get("result")==["report"]:data=self.fixture_report(query.get("id")==["124"])
                else:data={"id":query.get("id",["123"])[0],"status":"completed","conclusion":"success"}
            else:
                unknown.append(url.path);return route.fulfill(status=404,json={"error":"Unexpected fixture route"})
            return route.fulfill(json=data)
        page.route("**/*",handler)
        page.goto(self.origin+"/")
        expect(page.locator("#login-password")).to_be_visible()
        page.locator("#login-password").fill("fixture-password")
        page.locator("#login-submit").click()
        expect(page.locator("#page-search")).to_be_visible()
        expect(page.locator("#region")).to_have_value("TR")
        return page,errors,unknown,calls

    def open_report(self,page,run_id):
        page.locator("details").filter(has=page.locator("#resume")).locator("summary").click()
        page.locator("#run-id").fill(run_id)
        page.locator("#resume button[type=submit], #resume button:not([type])").first.click()

    def test_desktop_channel_filters_logout_and_expiry(self):
        page,errors,unknown,calls=self.open({"width":1280,"height":900})
        self.open_report(page,"123")
        expect(page.locator("#results")).to_be_visible()
        expect(page.locator("#channel-library")).to_contain_text("Fixture short-duration")
        expect(page.locator("#channel-library")).to_contain_text("Fixture long-duration")
        before=len(calls)
        page.locator("#channel-duration").select_option("short")
        expect(page.locator("#channel-library")).not_to_contain_text("Fixture long-duration")
        expect(page.locator("#channel-library")).to_contain_text("0 izlenme")
        self.assertEqual(len(calls),before,"Local filtering must not call any API")
        page.locator("#channel-refresh").click()
        expect(page.locator("#query")).to_be_focused()
        page.locator("#run-id").fill("124")
        page.locator("#resume button[type=submit], #resume button:not([type])").first.click()
        expect(page.locator("#status")).to_contain_text("saklama süresi")
        expect(page.locator("#results")).to_be_hidden()
        page.locator("#logout").click()
        expect(page.locator("#login-password")).to_be_visible()
        self.assertFalse(errors,errors);self.assertFalse(unknown,unknown)

    def test_mobile_navigation_and_keyboard(self):
        page,errors,unknown,_=self.open({"width":390,"height":844})
        nav=page.locator('[data-page="discover"]')
        nav.focus();page.keyboard.press("Enter")
        expect(page.locator("#page-discover")).to_be_visible()
        expect(nav).to_have_attribute("aria-current","page")
        expect(page.locator("#discover-category")).not_to_be_empty()
        self.assertTrue(page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"),"Mobile horizontal page overflow")
        self.assertFalse(errors,errors);self.assertFalse(unknown,unknown)

if __name__=="__main__":
    unittest.main(verbosity=2)
