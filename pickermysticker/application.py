from tornado.web import (
    Application,
    url,
)

from pickermysticker.handlers import (
    SendStickerHandler,
    SlashCommandHandler,
    StickerHandler,
    PackHandler,
    PackListHandler,
)
from pickermysticker.sticker_store import StickerStore


class PickerMyStickerApplication:

    def __init__(self, config_path: str) -> None:
        handlers = [
            url('/slash-command', SlashCommandHandler, name='slash_command'),
            url('/packs', PackListHandler, name='pack_list'),
            url('/packs/(\d+)', PackHandler, name='pack'),
            url('/packs/(\d+)/stickers/(\d+\.(?:gif|png))', StickerHandler, name='sticker'),
            url('/packs/(\d+)/stickers/(\d+\.(?:gif|png))/send', SendStickerHandler, name='send_sticker'),
        ]

        settings = {
            'debug': True,
            'xheaders': True,
        }

        sticker_store = StickerStore('/home/kedo/Workspace/picker-my-sticker/data')
        slack_token = 'CONFIG'

        self.tornado_app = Application(handlers, **settings)
        self.tornado_app.sticker_store = sticker_store

    def listen(self, port: int, address: str) -> None:
        self.tornado_app.listen(port, address)
