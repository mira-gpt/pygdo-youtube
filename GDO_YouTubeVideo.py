from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Creator import GDT_Creator
from gdo.core.GDT_String import GDT_String
from gdo.core.GDT_Text import GDT_Text
from gdo.core.GDT_UInt import GDT_UInt
from gdo.core.GDT_Unique import GDT_Unique
from gdo.date.GDT_Created import GDT_Created
from gdo.net.GDT_Url import GDT_Url
from gdo.ui.GDT_Card import GDT_Card
from gdo.ui.GDT_Link import GDT_Link
from gdo.ui.GDT_Title import GDT_Title
from gdo.vote.GDT_VoteCount import GDT_VoteCount
from gdo.vote.GDT_VoteOutcome import GDT_VoteOutcome
from gdo.youtube.WithYouTubeVotes import WithYouTubeVotes


class GDO_YouTubeVideo(WithYouTubeVotes, GDO):
    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('yt_id'),
            GDT_String('yt_video_id').ascii().not_null().maxlen(11),
            GDT_Url('yt_url').not_null().maxlen(1024),
            GDT_Title('yt_title').not_null().maxlen(512),
            GDT_Text('yt_description').maxlen(4096),
            GDT_String('yt_channel').maxlen(256),
            GDT_Url('yt_thumbnail').maxlen(1024),
            GDT_UInt('yt_duration').bytes(4).not_null().initial('0'),
            GDT_UInt('yt_views').bytes(8).not_null().initial('0'),
            GDT_UInt('yt_likes').bytes(8).not_null().initial('0'),
            GDT_UInt('yt_times_added').not_null().initial('1'),
            GDT_Creator('yt_creator'),
            GDT_Created('yt_created'),
            GDT_VoteCount('yt_vote_count'),
            GDT_VoteOutcome('yt_vote_score'),
            GDT_Unique('unique_video').unique_columns('yt_video_id'),
        ]

    def render_name(self) -> str:
        return self.gdo_val('yt_title')

    def render_card(self) -> str:
        card = GDT_Card().gdo(self).creator_header()
        card.get_header().add_field(GDT_Link().href(self.gdo_val('yt_url')).text_raw(self.render_name()))
        card.get_content().add_fields(
            self.column('yt_description'), self.column('yt_channel'),
            self.column('yt_duration'), self.column('yt_views'), self.column('yt_likes'),
            self.column('yt_times_added'),
            self.column('yt_vote_count'), self.column('yt_vote_score'),
        )
        return card.render_html()
