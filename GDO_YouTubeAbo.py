from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.Render import Render
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
    async def announce(cls, video, origin_channel=None, origin_user=None):
        from gdo.youtube.module_youtube import module_youtube
        for abo in cls.table().select().exec().fetch_all():
            if channel := abo.gdo_value('yta_channel'):
                announcement = module_youtube.render_announcement(video, channel.get_render_mode())
                if origin_channel and channel.get_id() == origin_channel.get_id():
                    await channel.send_text('msg_youtube_peeked', (announcement, video.gdo_val('yt_url')))
                elif origin_user:
                    submitter = Render.bold(origin_user.render_name(), channel.get_render_mode())
                    await channel.send_text('msg_youtube_shared_by', (submitter, announcement, video.gdo_val('yt_url')))
                else:
                    await channel.send_text('msg_youtube_shared', (announcement, video.gdo_val('yt_url')))
            elif user := abo.gdo_value('yta_user'):
                key = 'msg_youtube_peeked' if not origin_channel and origin_user and user.get_id() == origin_user.get_id() else 'msg_youtube_shared'
                await user.send(key, (
                    module_youtube.render_announcement(video, user.get_server().get_connector().get_render_mode()),
                    video.gdo_val('yt_url')))
