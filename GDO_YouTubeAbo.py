from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Channel import GDT_Channel
from gdo.core.GDT_Creator import GDT_Creator
from gdo.core.GDT_Unique import GDT_Unique
from gdo.core.GDT_User import GDT_User
from gdo.date.GDT_Created import GDT_Created


class GDO_YouTubeAbo(GDO):
    """A context which wants announcements for newly shared videos."""

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('yta_id'),
            GDT_User('yta_user'),
            GDT_Channel('yta_channel'),
            GDT_Created('yta_created'),
            GDT_Creator('yta_creator'),
            GDT_Unique('unique_user').unique_columns('yta_user'),
            GDT_Unique('unique_channel').unique_columns('yta_channel'),
        ]

    @classmethod
    def for_context(cls, user, channel):
        key = 'yta_channel' if channel else 'yta_user'
        value = channel.get_id() if channel else user.get_id()
        return cls.table().get_by_vals({key: value})

    @classmethod
    async def announce(cls, text: str, url: str, origin_channel=None, origin_user=None):
        for abo in cls.table().select().exec().fetch_all():
            if channel := abo.gdo_value('yta_channel'):
                if origin_channel and channel.get_id() == origin_channel.get_id():
                    continue
                await channel.send_text('msg_youtube_shared', (text, url))
            elif user := abo.gdo_value('yta_user'):
                if not origin_channel and origin_user and user.get_id() == origin_user.get_id():
                    continue
                await user.send('msg_youtube_shared', (text, url))
