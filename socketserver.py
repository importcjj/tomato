# -*- coding

import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop
import tornado.websocket

from tornado.options import (
    define,
    options
)

import os.path
SERVER_REALPATH = os.path.dirname(os.path.realpath(__file__))

import logging
logger = logging.getLogger("my")
# handler = logging.StreamHandler()
# handler.setLevel(logging.WARNING)
# formatter = logging.Formatter(
#     '%(asctime)s[%(procssName)s] [%(levelname)s]: %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

import uuid

define('port', default=8000, type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/chatroom', ChatRoomHandler),
            (r'/chatserver', ChatingHandler)
        ]
        settings = dict(
            template_path=os.path.join(SERVER_REALPATH, 'templates'),
            static_path=os.path.join(SERVER_REALPATH, 'static'),
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


class ChatRoomHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('chatroom.html', page_title='chatroom')


class ChatRoom(object):
    pool = dict()

    @classmethod
    def regiser(cls, session, callback):
        if session in cls.pool:
            return
        cls.pool[session] = callback
        cls._notify(session)

    @classmethod
    def unregister(cls, session):
        if session not in cls.pool:
            return
        cls.pool.pop(session)

    @classmethod
    def _notify(cls, uuid):
        for session in cls.pool:
            cls.pool.get(session)(
                'new session has joined {}'.format(uuid))


class ChatingHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        self.uuid = uuid.uuid4()
        logger.info('new {} socket connection.'.format(self.uuid))
        ChatRoom.regiser(self.uuid, self.callback)

    def on_close(self):
        logger.info('socket connection was closed.')
        ChatRoom.unregister(self.uuid)

    def on_message(self, message):
        logger.info(message)

    def callback(self, message):
        self.write_message(message)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
