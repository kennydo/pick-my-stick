import tornado.ioloop

from pickmystick.application import PickMyStickApplication


if __name__ == "__main__":
    app = PickMyStickApplication('')
    app.listen(3000)
    tornado.ioloop.IOLoop.current().start()
