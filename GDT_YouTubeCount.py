from gdo.core.GDT_UInt import GDT_UInt


class GDT_YouTubeCount(GDT_UInt):
    """A public video counter with a readable thousands separator."""

    @classmethod
    def display_var(cls, val: str | int) -> str:
        return f'{int(val or 0):,}'
