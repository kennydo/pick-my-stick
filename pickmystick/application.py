from tornado.web import (
    Application,
    url,
)

from pickmystick.handlers import (
    StickerHandler,
    PackHandler,
    PackListHandler,
)


class PickMyStickApplication:

    def __init__(self, config_path: str) -> None:
        handlers = [
            url('/packs', PackListHandler, name='pack_list'),
            url('/packs/(\d+)', PackHandler, name='pack'),
            url('/packs/(\d+)/stickers/(\d+\.(?:gif|png))', StickerHandler, name='sticker'),
        ]

        settings = {
            'debug': True,
        }

        self.tornado_app = Application(handlers)

    def listen(self, port: int) -> None:
        self.tornado_app.listen(port)
