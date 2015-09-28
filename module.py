# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop

from tornado.options import (
    define,
    options
)

import os.path

define('port', default=8000, type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/person', PersonInfoHandler),
            (r'/recommended', RecommendedHandler),
        ]

        settings = dict(
            template_path=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'templates'),
            static_path=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'static'),
            debug=True,
            ui_modules={
                'hello': HelloModule,
                'Book': BookModule
            },
        )
        super(Application, self).__init__(handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('This is the index<script>alert("hello world")</script>')


class PersonInfoHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('Person.html')


class RecommendedHandler(tornado.web.RequestHandler):

    def get(self):
        self.render(
            "recommended.html",
            page_title="Burt's Books | Recommended Reading",
            header_text="Recommended Reading",
            books=[
                {
                    "title": "Programming Collective Intelligence",
                    "subtitle": "Building Smart Web 2.0 Applications",
                    "image": "/static/images/collective_intelligence.gif",
                    "author": "Toby Segaran",
                    "date_added": 1310248056,
                    "date_released": "August 2007",
                    "isbn": "978-0-596-52932-1",
                    "description": "<p>This fascinating book demonstrates how you "
                        "can build web applications to mine the enormous amount of data created by people "
                        "on the Internet. With the sophisticated algorithms in this book, you can write "
                        "smart programs to access interesting datasets from other web sites, collect data "
                        "from users of your own applications, and analyze and understand the data once "
                        "you've found it.</p>"
                },
            ]
        )


class HelloModule(tornado.web.UIModule):

    def render(self, name):
        return '<h1>Hello, {username}</h1>'.format(username=name)


class BookModule(tornado.web.UIModule):

    def render(self, book):
        return self.render_string('modules/book.html', book=book)

    def embedded_javascript(self):
        return "document.write(\"hi!\")"

    def embedded_css(self):
        return ".book {background-color:#F5F5F5}"

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
