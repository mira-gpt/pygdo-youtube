from gdo.vote.MethodVote import MethodVote
from gdo.youtube.GDO_YouTubeVideo import GDO_YouTubeVideo
from gdo.youtube.GDO_YouTubeVote import GDO_YouTubeVote


class vote(MethodVote):
    @classmethod
    def gdo_trigger(cls) -> str:
        return 'youtube.up'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'ytup'

    def gdo_votes_table(self):
        return GDO_YouTubeVote.table()

    def gdo_vote_object_table(self):
        return GDO_YouTubeVideo.table()
