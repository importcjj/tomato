# -*- coding:utf-8 -*-

import Queue
import uuid


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
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

import logging
logger = logging.getLogger(__name__)

define('port', default=8000, type=int)


##################################################################
#
# BUSINESS MODEL
#
##################################################################

class Hotel(object):

    def __init__(self, waiting_max=20, room_size=2):
        self.room_size = room_size
        self.waiting_max = waiting_max
        self.full_rooms = list()
        self.match_rooms = Queue.Queue(waiting_max)

    def check_in(self, person, size=2):
        try:
            room = self.match_rooms.get_nowait()
        except Queue.Empty:
            room = self._open_new_room(person)
            self.match_rooms.put(room)
        else:
            room.join(person)
            if room.p_number == self.room_size:
                self.full_rooms.append(room)
            else:
                self.match_rooms.put(room)
        finally:
            return room

    def checkout_out(self, person):
        person.left_room()

    def _open_new_room(self, opener):
        return Room.new(self, opener)


class Room(object):

    def __init__(self, hotel, opener):
        self._hotel = hotel
        self._room = list()
        self.message_stack = list()
        self.size = self._hotel.room_size

    def join(self, person):
        if self.p_number >= self.size:
            return
        if person in self._room:
            return
        self._room.append(person)
        person.room = self
        person.index = self.p_number - 1

    def broadcast(self, _from, message):
        self._msg_store(message)
        for person in self._room:
            logger.info(_from._talk_to(person, message))
            person.receive(message)

    def _msg_store(self, message):
        self.message_stack.append(message)

    @property
    def p_number(self):
        return len(self._room)

    @classmethod
    def new(cls, hotel, opener, size=2):
        new_room = cls(hotel, opener)
        new_room.join(opener)
        return new_room


class Person(object):

    def __init__(self, callback):
        self.token = uuid.uuid4().bytes
        self.handler = {self.token: callback}

    def on_message(self, message):
        if not getattr(self, 'room', None):
            return
        self.room.broadcast(self, message)

    def receive(self, message):
        self.handler[self.token](message)

    def left_room(self):
        if not self.room:
            return
        self.room._room.pop(self.index)
        delattr(self, 'room')

    def _talk_to(self, _to, message):
        return '{} => {} : {}'.format(self, _to, message)

    def __str__(self):
        return 'socket[token:{}]'.format(self.token)

test_hotel = Hotel()
##################################################################
#
# WEB SERVER
#
##################################################################


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/chatroom', ChatRoomHandler),
            (r'/chatserver', ChatServerHandler)
        ]
        settings = {
            'debug': True,
            'template_path': os.path.join(PROJECT_PATH, 'templates'),
            'static_path': os.path.join(PROJECT_PATH, 'static')
        }
        super(Application, self).__init__(handlers, **settings)


class ChatRoomHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('chatroom.html', page_title="let's chat")


class ChatServerHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        self.person = Person(self.callback)
        test_hotel.check_in(self.person)
        logger.info(self.person)

    def on_close(self):
        test_hotel.checkout_out(self.person)
        logger.warning('killing {}'.format(self.person))
        del self.person

    def on_message(self, message):
        self.person.on_message(message)

    def callback(self, message):
        self.write_message(message)

if __name__ == '__main__':

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
