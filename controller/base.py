# coding=utf-8
import time
import tornado.web
from function import humantime, time_span
from database import User


class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.set_header("X-XSS-Protection", "1; mode=block")
        self.set_header("X-UA-Compatible", "IE=edge,chrome=1")
        self.set_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-eval'; "
                                                   "connect-src 'self'; img-src 'self' data:; "
                                                   "style-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                                                   "font-src 'self'; "
                                                   "frame-src 'self'; ")
        self.clear_header("Server")

    def check_login(self):
        try:
            user = self.get_secure_cookie("_user")
            assert user
        except AssertionError:
            self.write("请先登录")

    def set_session(self, user):
        try:
            self.set_secure_cookie("_user", str(user.id))
            return user
        except Exception, e:
            print(e)
            return None

    def get_current_user(self):
        try:
            user = self.get_secure_cookie("_user")
            assert user
        except Exception, e:
            print(e)
            user = None
        return user

    def render(self, template_name, **kwargs):
        kwargs["humantime"] = humantime
        kwargs["time_span"] = time_span
        template_name = str(template_name)
        return super(BaseHandler, self).render(template_name, **kwargs)

    def get_ipaddress(self):
        if self.request.headers.get('X-Forwarded-For'):
            return self.request.headers.get('X-Forwarded-For')
        else:
            return self.request.remote_ip


class NotFoundHandler(BaseHandler):
    def prepare(self):
        BaseHandler.prepare(self)

    def get(self, *args, **kwargs):
        self.set_status(404)
        self.render("404.html")

    def post(self, *args, **kwargs):
        self.get(*args, **kwargs)
