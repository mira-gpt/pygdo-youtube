import unittest
from unittest.mock import MagicMock, patch

from gdo.core.GDT_Bool import GDT_Bool
from gdo.youtube.GDO_YouTubeVideo import GDO_YouTubeVideo


class VideoAdFieldTest(unittest.TestCase):
    def test_ad_flag_is_false_by_default(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None), \
             patch('gdo.core.GDO_User.GDO_User.table', return_value=MagicMock()):
            field = next(column for column in GDO_YouTubeVideo().gdo_columns()
                         if column.get_name() == 'yt_is_add')
        self.assertIsInstance(field, GDT_Bool)
        self.assertTrue(field.is_not_null())
        self.assertEqual('0', field.get_initial())
