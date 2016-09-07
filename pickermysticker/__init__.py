import tornado.ioloop

from pickermysticker.application import PickerMyStickerApplication


if __name__ == "__main__":
    app = PickerMyStickerApplication('')
    app.listen(3000, '127.0.0.1')
    tornado.ioloop.IOLoop.current().start()
