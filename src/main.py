from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.options import define, options
import tornado.httpserver
import uuid, sys
from os import path
import base64
import asyncio

settings = {
    'template_path': 'src/templates',
    'static_path': 'static',
    'xsrf_cookies': False
}

define("port", default=8888, help='run on the given port', type=int)

PACKAGE_PATH = PACKAGE_PATH = path.realpath(path.join(path.dirname(__file__), '..'))
sys.path.append(PACKAGE_PATH)

class UploadHandler(RequestHandler):
    def get(self):
        self.render("upload.html")
    
    def post(self):
        print("hello it's here")
        file = self.request.files['image'][0]
        self.write("it's here")
        print("it's in here?")
        # check extension (later)
        try: 
            # fname =  path.splitext(file['filename'])
            with open('public/images/'+ file['filename'], 'wb') as f:
                f.write(file['body'])
            self.finish('file is uploaded')
            print("hello it's overrrrrrr hear!")
        except Exception as e:
            print(e)

class ShowImage(RequestHandler):
    def get(self):
        return self.render("download.html")

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
        (r"/", UploadHandler)
    ],
        debug=True, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())