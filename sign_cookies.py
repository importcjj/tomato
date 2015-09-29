# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop

from tornado.options import (
    define,
    options
)

# To generate a cookie_secret
# >> > import base64, uuid
# >> > base64.b64encode(uuid.uuid4().bytes, uuid, uuid4().bytes)


# 定义cli参数
define('port', default=8000, type=int)


# 定义app
class Application(tornado.web.Application):

    def __init__(self):
        # 路由处理
        handlers = [
            (r'/', IndexHandler),
        ]

        setting = dict(
            cookie_secret='wk/W701gQjeHPA8bsPNlg+odPMkJFkf2ii7L7nm36pM=',
            debug=True
        )
        super(Application, self).__init__(handlers, **setting)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        # 获取签名cookie
        cookie = self.get_secure_cookie('count')
        count = int(cookie) + 1 if cookie else 1

        count_string = '1 time' if count == 1 else '{} times'.format(count)

        # 返回新的签名cookie
        # Expected bytes, unicode, or None
        self.set_secure_cookie('count', str(count))
        self.write('<html><head><title>Cookie Counter</title></head>'
                   '<body><h1>You’ve viewed this page {} times.</h1>'
                   .format(count_string) +
                   '</body></html>')

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
