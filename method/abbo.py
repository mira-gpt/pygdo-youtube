from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_Bool import GDT_Bool
from gdo.youtube.GDO_YouTubeAbo import GDO_YouTubeAbo


class abbo(Method):
    @classmethod
    def gdo_trigger(cls) -> str:
        return 'youtube.abbo'

    @classmethod
    def gdo_trig(cls) -> str:
        return 'yta'

    def gdo_parameters(self) -> list[GDT]:
        return [GDT_Bool('enabled').initial('1').positional()]

    def gdo_execute(self) -> GDT:
        enabled = self.param_value('enabled')
        abo = GDO_YouTubeAbo.for_context(self._env_user, self._env_channel)
        if enabled:
            if not abo:
                GDO_YouTubeAbo.blank({
                    'yta_user': self._env_user.get_id() if not self._env_channel else None,
                    'yta_channel': self._env_channel.get_id() if self._env_channel else None,
                    'yta_creator': self._env_user.get_id(),
                }).insert()
            return self.reply('msg_youtube_subscribed')
        if abo:
            abo.delete()
        return self.reply('msg_youtube_unsubscribed')
