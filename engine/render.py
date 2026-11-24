"""render.py - SVG/HTML -> PNG (Playwright + Chrome). Fontlar yerel dosyadan @font-face ile."""
import os, asyncio, shutil
CHROME = next((p for p in [os.environ.get("CHROME_PATH", ""), "/usr/bin/google-chrome", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium", shutil.which("chromium") or "", shutil.which("google-chrome") or ""] if p and os.path.exists(p)), None)
from playwright.async_api import async_playwright
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
FONTS = {
  "Shantell": "ShantellSans[BNCE,INFM,SPAC,wght].ttf", "Nunito": "Nunito[wght].ttf",
  "KalamB": "Kalam-Bold.ttf", "Kalam": "Kalam-Regular.ttf", "Mali": "Mali-SemiBold.ttf",
  "Playpen": "PlaypenSans[wght].ttf", "Baloo": "Baloo2[wght].ttf", "Caveat": "Caveat[wght].ttf",
  "Patrick": "PatrickHand-Regular.ttf", "Itim": "Itim-Regular.ttf", "Gochi": "GochiHand-Regular.ttf",
  "Fredoka": "Fredoka[wdth,wght].ttf", "Delius": "Delius-Regular.ttf", "Amatic": "AmaticSC-Bold.ttf",
}
CSS = "".join(f"@font-face{{font-family:'{k}';src:url('file://{FD}/{v}');}}" for k, v in FONTS.items())

def page(svg, w, h):
    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{CSS}
    html,body{{margin:0;padding:0;background:transparent}} svg{{display:block}}</style></head>
    <body><svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{svg}</svg></body></html>"""

async def _render(jobs, transparent=False):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=["--allow-file-access-from-files", "--no-sandbox"])
        pg = await b.new_page(device_scale_factor=1)
        for svg, path, w, h in jobs:
            await pg.set_viewport_size({"width": w, "height": h})
            html = path.rsplit(".", 1)[0] + ".html"
            open(html, "w").write(page(svg, w, h))
            await pg.goto("file://" + os.path.abspath(html))
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(120)
            await pg.screenshot(path=path, full_page=False, omit_background=transparent and ('/objects/' in path or '/text/' in path or path.endswith('_txt.png')))
            os.remove(html)
        await b.close()

def render(jobs, transparent=False):
    asyncio.run(_render(jobs, transparent))
