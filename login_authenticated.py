# -*- coding:utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop

from tornado.options import (
    define,
    options
)

define('port', default=8000, type=int)

import os.path
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler)
        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(PROJECT_PATH, 'templates'),
            xsrf_cookies=True,
            login_url='/login',
            cookie_secret='wk/W701gQjeHPA8bsPNlg+odPMkJFkf2ii7L7nm36pM='
        )

        super(Application, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie('username')


class IndexHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.write('Welcome。。{}'.format(self.current_user))


class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username', '')
        if not username:
            self.redirect('/login')
        self.set_secure_cookie('username', username)
        self.redirect('/')


class LogoutHandler(BaseHandler):

    def get(self):
        if self.get_argument('logout', ''):
            self.clear_cookie('username')
            self.redirect('/login')
        self.redirect('/')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
