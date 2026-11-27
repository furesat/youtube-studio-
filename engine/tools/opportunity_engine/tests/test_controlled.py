from datetime import datetime, timezone
from unittest import TestCase
from collections import Counter
from engine.tools.opportunity_engine.queue_worker import prepare
from engine.tools.opportunity_engine.research import collect

class Client:
    def __init__(self):
        self.calls=[]
    def search(self, market, query, after, before, limit, token):
        self.calls.append((query,after,before))
        return {"items":[]}
    def enrich(self,*args):
        return {},[]

class ControlledTest(TestCase):
    def test_fixed_anchor_and_zero_result_provenance(self):
        task=dict(id=1,topic="history",query="history",market_id="de",region="DE",language="de",lookback_days=7,search_order="relevance",window_anchor="2026-11-20T00:00:00.000Z",comparison_axis="window",query_variant=0,methodology_version="controlled-v1")
        client=Client()
        rows,_,_=collect(client,prepare([task]),dict(lookback_days=365,pages_per_query=1,results_per_page=50),datetime(2026,11,27,tzinfo=timezone.utc))
        self.assertEqual(client.calls,[("history","2026-11-13T00:00:00+00:00","2026-11-20T00:00:00+00:00")])
        q=rows[0][2][0]
        self.assertEqual(q["observation_status"],"zero_results")
        self.assertEqual(q["methodology_version"],"controlled-v1")
        self.assertEqual(q["observed_at"],"2026-11-27T00:00:00+00:00")
