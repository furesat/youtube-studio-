import io
import json
import unittest
from engine.tools.opportunity_engine.storage import save_report

class StorageTests(unittest.TestCase):
    def test_receipt(self):
        env = {"SUPABASE_SECRET_KEY":"sb_secret_unit_test","GITHUB_RUN_ID":"123"}
        report = {"videos": {}}
        def opener(request, timeout):
            self.assertEqual(request.full_url,"https://niihqywncuwxfxipkgte.supabase.co/rest/v1/rpc/fasulye_save_report")
            self.assertEqual(json.loads(request.data)["p_run_id"], "123")
            return io.BytesIO(b'{"saved":true,"run_id":"123","videos":0}')
        self.assertTrue(save_report(report,environ=env,opener=opener)["saved"])

    def test_wrong_project_rejected(self):
        with self.assertRaises(ValueError):
            save_report({},environ={"SUPABASE_URL":"https://other.example","SUPABASE_SECRET_KEY":"sb_secret_test","GITHUB_RUN_ID":"123"})
