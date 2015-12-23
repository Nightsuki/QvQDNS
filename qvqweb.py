#!/usr/bin/python
import tornado.ioloop
import tornado.web
import tornado.options
import sys
from database import UrlLogs, DomainLogs, DNSLogs, User

tornado.options.define("port", default=8020, type=int)
tornado.options.parse_command_line()


class Record(tornado.web.RequestHandler):
    def prepare(self):
        domain_query = DomainLogs.select().where(DomainLogs.domain == self.request.host).first()
        if not domain_query:
            user = User.select().where(User.domain == self.request.host.split(".")[-3]).first()
            if not user:
                return
            domain_query = DomainLogs()
            domain_query.user_id = user.id
            domain_query.domain = self.request.host.split(".")[-3]
            domain_query.save()
            log = DNSLogs()
            log.ip = self.request.headers.get('X-Forwarded-For')
            log.user_id = user.id
            log.domain_id = domain_query.id
            log.save()
        if not self.request.uri == "/favicon.ico":
            log = UrlLogs()
            packet = "%s %s %s\n" % (self.request.method, self.request.uri, self.request.version)
            for header in self.request.headers:
                packet += "%s: %s\n" % (header, self.request.headers.get(header))
            packet += "\n%s" % self.request.body
            log.url = self.request.uri
            log.ip = self.request.headers.get("X-Forwarded-For")
            log.domain_id = domain_query.id
            log.user_id = domain_query.user_id
            log.packet = packet
            log.save()

    def get(self, *args, **kwargs):
        self.write("QvQ !")

    def post(self, *args, **kwargs):
        self.get(*args, **kwargs)

    def put(self, *args, **kwargs):
        self.get(*args, **kwargs)

    def options(self, *args, **kwargs):
        self.get(*args, **kwargs)

    def head(self, *args, **kwargs):
        self.get(*args, **kwargs)

application = tornado.web.Application([
    (r"^/(.*?)", Record),
], )

if __name__ == "__main__":
    try:
        application.listen(tornado.options.options.port)
        tornado.ioloop.IOLoop.instance().start()
    except:
        import traceback

        print(traceback.print_exc())
    finally:
        sys.exit(0)
