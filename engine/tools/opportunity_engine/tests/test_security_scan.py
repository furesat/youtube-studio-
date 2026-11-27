from unittest import TestCase
from engine.tools.opportunity_engine.security_scan import match_types

class ScanTest(TestCase):
    def test_patterns_without_real_credentials(self):
        self.assertIn("github_token",match_types("gh"+"p_"+"x"*35))
        self.assertIn("supabase_secret",match_types("sb_"+"secret_"+"y"*30))
        self.assertIn("credential_url",match_types("https://" + "user" + ":" + "fixture" + "@" + "internal.invalid/path"))
        self.assertNotIn("credential_url",match_types("https://user:fixture@example.test/path"))
        self.assertIn("email_shaped",match_types("fixture"+"@sample.invalid.com"))
        self.assertEqual(match_types("FASULYE_ACCESS_TOKEN=\nSUPABASE_SECRET_KEY="),set())
