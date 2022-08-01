from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import uuid, sys
from os import path
import base64

PACKAGE_PATH = PACKAGE_PATH = path.realpath(path.join(path.dirname(__file__), '..'))
sys.path.append(PACKAGE_PATH)

class UploadHandler(RequestHandler):
    def get(self):
        self.write({'message': '{}'.format(str(uuid.uuid4()))})
    
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
    pass

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

if __name__ == '__main__':
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()