from gdo.base.Application import Application
from gdo.base.GDO import GDO
from gdo.base.GDO_Module import GDO_Module
from gdo.base.Logger import Logger
from gdo.base.Message import Message
from gdo.youtube.GDO_YouTubeVideo import GDO_YouTubeVideo
from gdo.youtube.GDO_YouTubeVote import GDO_YouTubeVote
from gdo.youtube.VideoResolver import VideoResolver


class module_youtube(GDO_Module):
    """Persist and announce YouTube links posted to a PyGDO connector."""

    def gdo_dependencies(self) -> list[str]:
        return ['vote', 'net']

    def gdo_classes(self) -> list[type[GDO]]:
        return [GDO_YouTubeVideo, GDO_YouTubeVote]

    def gdo_subscribe_events(self):
        Application.EVENTS.subscribe('new_message', self.on_new_message)

    async def on_new_message(self, message: Message):
        if message.message().startswith(message.get_trigger()):
            return
        video_id = VideoResolver.video_id(message.message())
        if not video_id:
            return
        video, created = await self.store_video(video_id)
        if not created:
            return
        message.result(self.render_announcement(video))
        await message.deliver(with_events=False)

    async def store_video(self, video_id: str) -> tuple[GDO_YouTubeVideo, bool]:
        table = GDO_YouTubeVideo.table()
        if existing := table.get_by_val('yt_video_id', video_id):
            existing.increase('yt_times_added')
            return existing, False
        try:
            metadata = await VideoResolver.resolve(video_id)
        except Exception as error:
            Logger.exception(error)
            return table.blank({
                'yt_video_id': video_id,
                'yt_url': VideoResolver.canonical_url(video_id),
                'yt_title': video_id,
            }).insert(), True
        return table.blank({
            'yt_video_id': metadata.video_id,
            'yt_url': metadata.url,
            'yt_title': metadata.title,
            'yt_description': metadata.description,
            'yt_channel': metadata.channel,
            'yt_thumbnail': metadata.thumbnail,
        }).insert(), True

    @staticmethod
    def render_announcement(video: GDO_YouTubeVideo) -> str:
        channel = video.gdo_val('yt_channel')
        suffix = f' — {channel}' if channel else ''
        return f'YouTube: {video.render_name()}{suffix}'
