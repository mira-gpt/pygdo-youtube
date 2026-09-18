import unittest

from gdo.youtube.VideoResolver import VideoResolver


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
