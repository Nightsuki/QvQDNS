# coding=utf-8
import tornado.web
from controller.base import BaseHandler
from tornado import gen
from function import *
from database import DNSLogs, UrlLogs, DomainLogs, User


class ListHandler(BaseHandler):
    def initialize(self):
        BaseHandler.initialize(self)

    @tornado.web.asynchronous
    @gen.coroutine
    @need_login
    def get(self, *args, **kwargs):
        domains_list = DomainLogs.select().where(DomainLogs.user_id == self.current_user).order_by(
            DomainLogs.created_time.desc())
        user = User.get(User.id == self.current_user)
        self.render("list.html", domains_list=domains_list, user=user)
