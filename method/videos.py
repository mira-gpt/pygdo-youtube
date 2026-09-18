from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.Query import Query
from gdo.base.Render import Mode
from gdo.table.MethodQueryTable import MethodQueryTable
from gdo.table.GDT_Table import TableMode
from gdo.message.GDT_HTML import GDT_HTML
from gdo.youtube.GDO_YouTubeVideo import GDO_YouTubeVideo


class videos(MethodQueryTable):
    @classmethod
    def gdo_trigger(cls) -> str:
        return 'youtube'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'yt'

    def gdo_table(self) -> GDO:
        return GDO_YouTubeVideo.table()

    def gdo_execute(self) -> GDT:
        if not self._env_http and not self._raw_args.pargs and not self._raw_args.args:
            return GDT_HTML().text(self.gdo_module().t('msg_youtube_commands'))
        return super().gdo_execute()

    def gdo_table_mode(self) -> TableMode:
        return TableMode.CARDS

    def gdo_table_search_query(self, query: Query, term: str):
        if term:
            escaped = GDT.escape_search(term)
            query.search_where(f"yt_title LIKE '%{escaped}%' OR yt_description LIKE '%{escaped}%'")

    def render_gdo(self, gdo: GDO, mode: Mode):
        return gdo.render_card() if mode == Mode.render_html else f'{gdo.get_id()}-{gdo.render_name()}'
