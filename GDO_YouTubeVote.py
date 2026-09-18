from gdo.vote.GDO_VoteTable import GDO_VoteTable


class GDO_YouTubeVote(GDO_VoteTable):
    def gdo_votes_table(self) -> GDO_VoteTable:
        return self.table()

    def gdo_vote_object_table(self):
        from gdo.youtube.GDO_YouTubeVideo import GDO_YouTubeVideo
        return GDO_YouTubeVideo.table()
