# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


from tornado.options import (
    define,
    options
)

import os.path
import textwrap

define("port", default=8000, help="run on given port", type=int)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        username = self.get_argument('name', 'User')
        self.write('hello, {username}'.format(username=username))


class ReverseHandler(tornado.web.RequestHandler):

    def get(self, input):
        self.write(input[::-1])


class WrapHandler(tornado.web.RequestHandler):

    def post(self):
        paragraph = self.get_argument('p', '')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(paragraph, int(width)))

    def write_error(self, status_code, **kwargs):
        print kwargs
        self.write('{}'.format(status_code))

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r'/', IndexHandler),
        (r'/reverse/(\w+)', ReverseHandler),
        (r'/wrap', WrapHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print __file__, os.path.dirname(os.path.realpath(__file__)), __name__
    tornado.ioloop.IOLoop.instance().start()
