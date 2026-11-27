from threading import Event
from unittest import TestCase
from engine.tools.opportunity_engine.standalone_worker import execution_id,main

class StandaloneTest(TestCase):
    def env(self):
        return {"YOUTUBE_API_KEY":"test","SUPABASE_SECRET_KEY":"sb_secret_test","FASULYE_ATOMIC_QUEUE":"1"}
    def test_unique_local_ids(self):
        ids={execution_id() for _ in range(100)}
        self.assertEqual(len(ids),100)
        self.assertTrue(all(i.isdigit() and i.startswith("9") and len(i)==16 for i in ids))
    def test_missing_credentials_and_disabled_atomic_mode(self):
        self.assertEqual(main(["--check-config"],env={}),2)
        env=self.env()
        del env["FASULYE_ATOMIC_QUEUE"]
        self.assertEqual(main(["--check-config"],env=env),2)
    def test_check_config_does_not_call_worker(self):
        self.assertEqual(main(["--check-config"],env=self.env(),worker=lambda _:self.fail()),0)
    def test_once_uses_local_id_and_passes_exit_code(self):
        def work(env):
            self.assertRegex(env["GITHUB_RUN_ID"],r"^9[0-9]{15}$")
            self.assertEqual(env["GITHUB_RUN_ATTEMPT"],"1")
            return 2
        self.assertEqual(main(["--once"],env=self.env(),stop=Event(),worker=work),2)
    def test_graceful_stop(self):
        stop=Event()
        stop.set()
        self.assertEqual(main([],env=self.env(),stop=stop,worker=lambda _:self.fail()),0)
