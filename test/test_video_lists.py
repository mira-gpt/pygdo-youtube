import unittest
from unittest.mock import MagicMock, patch

from gdo.youtube.method.ads import ads
from gdo.youtube.method.videos import videos
from gdo.ui.IconUTF8 import IconUTF8


class TestVideoLists(unittest.TestCase):
    def test_each_list_filters_its_own_kind(self):
        for method, expected in ((videos, 'yt_is_add=0'), (ads, 'yt_is_add=1')):
            query = MagicMock()
            table = MagicMock()
            table.select.return_value = query
            with self.subTest(method=method), patch.object(method, 'gdo_table', return_value=table):
                method.gdo_table_query(object.__new__(method))
            query.where.assert_called_once_with(expected)

    def test_ad_trigger_does_not_override_subscription(self):
        self.assertEqual('ytads', ads.gdo_trig())
        self.assertEqual('yt', videos.gdo_trig())

    def test_sidebar_icon_has_fallback(self):
        self.assertIn('link', IconUTF8.MAP())
