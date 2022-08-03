from tornado.web import Application
from tornado.options import define, options
import tornado.httpserver
from os import path
import base64
import asyncio, sys

from download import DownloadHandler
from upload import UploadHandler
from menu import MenuHandler

settings = {
    'template_path': 'templates',
    'static_path': 'public/css',
    'xsrf_cookies': False
}

define("port", default=8888, help='run on the given port', type=int)

PACKAGE_PATH = PACKAGE_PATH = path.realpath(path.join(path.dirname(__file__), '..'))
sys.path.append(PACKAGE_PATH)

settings = {
    'template_path': 'templates',
    'static_path': 'static',
    'xsrf_cookies': False
}
def make_app():
    return Application([
        (r"/", UploadHandler)
    ],
        debug=True, **settings)

async def main():
    options.parse_command_line()
    application = Application([
        (r"/", MenuHandler),
        (r"/upload", UploadHandler),
        (r"/download", DownloadHandler)
    ],
        debug=True, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())