from gdo.vote.WithVotes import WithVotes


class WithYouTubeVotes(WithVotes):
    def gdo_votes_table(self):
        from gdo.youtube.GDO_YouTubeVote import GDO_YouTubeVote
        return GDO_YouTubeVote.table()

    def gdo_vote_object_table(self):
        from gdo.youtube.GDO_YouTubeVideo import GDO_YouTubeVideo
        return GDO_YouTubeVideo.table()
