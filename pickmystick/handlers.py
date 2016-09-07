import tornado.web


class PackListHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, this is pack list")


class PackHandler(tornado.web.RequestHandler):
    def get(self, pack_id: str):
        self.write("I got: {0}".format(pack_id))


class StickerHandler(tornado.web.RequestHandler):
    def get(self, pack_id: str, sticker_id: str):
        self.write("I got: {0} {1}".format(pack_id, sticker_id))
