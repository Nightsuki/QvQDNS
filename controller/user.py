# coding=utf-8
import tornado.web
from controller.base import BaseHandler
from tornado import gen
from function import *


class UserHandler(BaseHandler):
    def initialize(self):
        BaseHandler.initialize(self)

    def get(self, *args, **kwargs):
        action = args[0] if len(args) > 0 else "index"
        method = "_view_%s" % action
        if hasattr(self, method):
            getattr(self, method)()
        else:
            self._view_index()

    @tornado.web.asynchronous
    @gen.coroutine
    def _view_index(self, *args, **kwargs):
        self.render("login.html")
