from unittest import TestCase
from engine.tools.opportunity_engine.channel_samples import collect_channel_samples
from engine.tools.opportunity_engine.youtube import ApiError

class Client:
    def request(self, endpoint, **params):
        assert endpoint == "playlistItems"
        assert params["maxResults"] == 25
        return {"items":[{"contentDetails":{"videoId":"a"}},{"contentDetails":{"videoId":"b"}},{"contentDetails":{"videoId":"a"}}],"nextPageToken":"next"}
    def enrich(self, endpoint, ids, part, fields):
        assert ids == ["a","b"]
        assert "defaultAudioLanguage" in fields
        return {"a":{"snippet":{"title":"Fixture","defaultAudioLanguage":"de"},"statistics":{"viewCount":"0"},"contentDetails":{"duration":"PT30S"}}},["fixture_partial"]

class ChannelTests(TestCase):
    def test_raw_upload_metadata_and_missing_detail(self):
        rows=collect_channel_samples(Client(),{"x":{"channel_id":"c","subscribers":10,"uploads_playlist":"p"}})
        self.assertEqual(len(rows),1)
        self.assertTrue(rows[0]["playlist_has_more"])
        self.assertEqual(rows[0]["missing_video_details"],1)
        self.assertEqual(rows[0]["videos"][0]["views"],0)
        self.assertEqual(rows[0]["videos"][0]["audio_language"],"de")
        self.assertEqual(rows[0]["format_classification"],"unverified")
        self.assertEqual(rows[0]["error"],"fixture_partial")
    def test_failed_playlist_does_not_invent_zero(self):
        class Failed(Client):
            def request(self,*a,**kw): raise ApiError("youtube_rate_limited")
        row=collect_channel_samples(Failed(),{"x":{"channel_id":"c","subscribers":0,"uploads_playlist":"p"}})[0]
        self.assertIsNone(row["playlist_has_more"])
        self.assertIsNone(row["missing_video_details"])
        self.assertEqual(row["error"],"youtube_rate_limited")
