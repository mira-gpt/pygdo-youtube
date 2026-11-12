from gdo.youtube.method.videos import videos


class ads(videos):
    @classmethod
    def gdo_trigger(cls) -> str:
        return 'youtube.ads'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'ytads'

    def is_ad_list(self) -> bool:
        return True
