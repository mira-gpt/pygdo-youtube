from gdo.vote.MethodVote import MethodVote
from gdo.base.GDT import GDT
from gdo.youtube.GDO_YouTubeVideo import GDO_YouTubeVideo
from gdo.youtube.GDO_YouTubeVote import GDO_YouTubeVote
from gdo.youtube.GDT_YouTubeVideo import GDT_YouTubeVideo


class vote(MethodVote):
    @classmethod
    def gdo_trigger(cls) -> str:
        return 'youtube.like'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'ytl'

    def gdo_votes_table(self):
        return GDO_YouTubeVote.table()

    def gdo_vote_object_table(self):
        return GDO_YouTubeVideo.table()

    def gdo_parameters(self) -> list[GDT]:
        table = self.gdo_votes_table()
        return [
            table.column('vote_reason').copy_as('reason'),
            table.column('vote_score').copy_as('score').initial(str(table.gdo_max_vote_score())),
            GDT_YouTubeVideo('id').not_null(),
        ]
