#!/usr/bin/python
import tornado.ioloop
import tornado.web
import tornado.options
import sys
import os
import controller.base

tornado.options.define("port", default=8021, type=int)
tornado.options.parse_command_line()

setting = {
    "template_path": os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates"),
    "cookie_secret": "69c4f5c32c7470fbe938689b4d676ae7",
    "compress_response": True,
    "default_handler_class": controller.base.NotFoundHandler,
    "xsrf_cookies": False,
    "static_path": os.path.join(os.path.abspath(os.path.dirname(__file__)), "static")
}


application = tornado.web.Application([
    (r"^/", "controller.user.UserHandler"),
    (r"^/ajax/([a-z_]+)", "controller.ajax.AjaxHandler"),
    (r"^/list", "controller.list.ListHandler"),
], **setting)

if __name__ == "__main__":
    try:
        application.listen(tornado.options.options.port)
        tornado.ioloop.IOLoop.instance().start()
    except:
        import traceback
        print traceback.print_exc()
    finally:
        sys.exit(0)

