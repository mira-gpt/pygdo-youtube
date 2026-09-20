import unittest
from unittest.mock import patch

from gdo.youtube.VideoResolver import VideoResolver
from gdo.youtube.module_youtube import module_youtube


class VideoResolverTest(unittest.TestCase):
    def test_extracts_common_youtube_urls(self):
        video_id = 'dQw4w9WgXcQ'
        urls = [
            f'https://www.youtube.com/watch?v={video_id}',
            f'https://youtu.be/{video_id}?feature=share',
            f'https://www.youtube.com/shorts/{video_id}',
            f'https://www.youtube.com/live/{video_id}',
            f'https://www.youtube.com/embed/{video_id}',
        ]
        for url in urls:
            self.assertEqual(video_id, VideoResolver.video_id(url))

    def test_rejects_non_youtube_and_invalid_ids(self):
        self.assertIsNone(VideoResolver.video_id('https://example.com/watch?v=dQw4w9WgXcQ'))
        with self.assertRaises(ValueError):
            VideoResolver.canonical_url('nope')

    def test_extracts_player_response_counts(self):
        document = 'prefix ytInitialPlayerResponse = {"videoDetails":{"lengthSeconds":"303","viewCount":"42"},"microformat":{"playerMicroformatRenderer":{"likeCount":"7"}}}; suffix'
        data = VideoResolver._player_response(document)
        self.assertEqual('303', data['videoDetails']['lengthSeconds'])
        self.assertEqual(42, VideoResolver._number(data['videoDetails']['viewCount']))
        self.assertEqual(7, VideoResolver._number(data['microformat']['playerMicroformatRenderer']['likeCount']))

    def test_announcement_uses_the_short_like_prompt(self):
        class Video:
            def gdo_val(self, field):
                return {'yt_duration': 151, 'yt_views': 29414845, 'yt_likes': 216809}.get(field)

            def get_id(self):
                return 35

            def render_name(self):
                return 'Touch The Sky'

        with patch('gdo.youtube.module_youtube.Render.bold', side_effect=lambda text, mode: text):
            text = module_youtube.render_announcement(Video())

        self.assertEqual(
            'YouTube #35: Touch The Sky - 2:31 - 216,809 YouTube likes - 29,414,845 views - Like with $ytl 35',
            text,
        )
