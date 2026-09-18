from gdo.base.GDO import GDO
from gdo.core.GDT_Object import GDT_Object
from gdo.youtube.GDO_YouTubeVideo import GDO_YouTubeVideo


class GDT_YouTubeVideo(GDT_Object):
    """Resolve a video reference by numeric id or its human-facing title."""

    def __init__(self, name: str = 'id'):
        super().__init__(name)
        self.table(GDO_YouTubeVideo.table())

    def query_gdos(self, val: str):
        if val.isdigit():
            if video := self._table.get_by_aid(val):
                return [video]
        escaped = GDO.escape(val)
        return self._table.select().where(
            f"yt_title LIKE '%{escaped}%'"
        ).exec().fetch_all()
