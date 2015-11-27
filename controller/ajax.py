# coding=utf-8
import tornado.web
from tornado import gen
from controller.base import BaseHandler
from database import *
from function import ajax_need_login, humantime


class AjaxHandler(BaseHandler):
    def post(self, *args, **kwargs):
        action = "_%s_action" % args[0]
        if hasattr(self, action):
            getattr(self, action)()
        else:
            self._json("fail", "no action!")

    def _json(self, status, info=""):
        status = str(status)
        if type(info) == str:
            info = info.decode("utf8")
        data = {
            "status": status,
            "info": info
        }
        self.write(data)
        raise tornado.web.Finish()

    @tornado.web.asynchronous
    @gen.coroutine
    def _login_action(self):
        username = self.get_body_argument("username", None)
        password = self.get_body_argument("password", None)
        user = User.select().where(User.username == username).first()
        if user and user.check_password(password):
            user.set_last(self.get_ipaddress())
            user.save()
            self.set_session(user)
            self._json(1)
        else:
            self._json(0, "账号或密码错误")

    @tornado.web.asynchronous
    @gen.coroutine
    def _logout_action(self):
        self.set_secure_cookie("_user", "")
        self._json(1)

    @tornado.web.asynchronous
    @gen.coroutine
    @ajax_need_login
    def _domains_action(self):
        domains_query = DomainLogs.select().where(DomainLogs.user_id == self.current_user).order_by(
            DomainLogs.created_time.desc())
        domains_list = []
        for item in domains_query:
            domains_list.append({
                "id": item.id,
                "domain": item.domain
            })
        self._json(1, domains_list)

    @tornado.web.asynchronous
    @gen.coroutine
    @ajax_need_login
    def _domaininfo_action(self):
        domain_id = self.get_body_argument("domain_id", None)
        if domain_id:
            dns_query = DNSLogs.select().where(
                (DNSLogs.user_id == self.current_user) & (DNSLogs.domain_id == domain_id)).order_by(
                DNSLogs.created_time.desc())
            url_query = UrlLogs.select().where(
                (UrlLogs.user_id == self.current_user) & (UrlLogs.domain_id == domain_id)).order_by(
                UrlLogs.created_time.desc())
            dns_list = []
            url_list = []
            for item in dns_query:
                dns_list.append({
                    "id": item.id,
                    "ip": item.ip,
                    "created_time": humantime(item.created_time)
                })
            for item in url_query:
                url_list.append({
                    "id": item.id,
                    "url": item.url,
                    "ip": item.ip,
                    "created_time": humantime(item.created_time)
                })
            result = {
                "dns_list": dns_list,
                "url_list": url_list
            }
            self._json(1, result)
        else:
            self._json(0, "参数错误")

    @tornado.web.asynchronous
    @gen.coroutine
    @ajax_need_login
    def _deldomain_action(self):
        domain_id = self.get_body_argument("domain_id", None)
        domain_query = DomainLogs.select().where(
            (DomainLogs.user_id == self.current_user) & (DomainLogs.id == domain_id)).first()
        if domain_query:
            dns_query = DNSLogs.delete().where(DNSLogs.domain_id == domain_id)
            dns_query.execute()
            url_query = UrlLogs.delete().where(UrlLogs.domain_id == domain_id)
            url_query.execute()
            domain_query.delete_instance()
            self._json(1)
        else:
            self._json(0, "access deny")

    @tornado.web.asynchronous
    @gen.coroutine
    @ajax_need_login
    def _httppacket_action(self):
        url_id = self.get_body_argument("url_id", None)
        url_query = UrlLogs.select().where(
            (UrlLogs.user_id == self.current_user) & (UrlLogs.id == url_id)).first()
        if url_query:
            self._json(1, url_query.packet)
        else:
            self._json(0, "access deny")

    @tornado.web.asynchronous
    @gen.coroutine
    @ajax_need_login
    def _delalldomain_action(self):
        dns_query = DNSLogs.delete().where(DNSLogs.user_id == self.current_user)
        dns_query.execute()
        url_query = UrlLogs.delete().where(UrlLogs.user_id == self.current_user)
        url_query.execute()
        domain_query = DomainLogs.delete().where(DomainLogs.user_id == self.current_user)
        domain_query.execute()
        self._json(1)

    @tornado.web.asynchronous
    @gen.coroutine
    @ajax_need_login
    def _changepwd_action(self):
        oldpassword = self.get_body_argument("oldpassword", None)
        password = self.get_body_argument("password", None)
        if oldpassword and oldpassword:
            user = User.get(User.id == self.current_user)
            if user.check_password(oldpassword):
                user.set_password(password)
                user.save()
                self._json(1)
            else:
                self._json(0, "旧密码错误")
        else:
            self._json(0, "参数错误")
