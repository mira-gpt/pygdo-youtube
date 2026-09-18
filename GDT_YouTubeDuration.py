from gdo.core.GDT_UInt import GDT_UInt


class GDT_YouTubeDuration(GDT_UInt):
    """A stored duration in seconds, rendered as a compact video clock."""

    @classmethod
    def display_var(cls, val: str | int) -> str:
        seconds = max(0, int(val or 0))
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f'{hours}:{minutes:02d}:{seconds:02d}' if hours else f'{minutes}:{seconds:02d}'
