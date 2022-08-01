from urllib.request import Request
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

class CollectHandler(RequestHandler):
    def get(self):
        self.write({'message': 'upload successful'})

class ShowImage(RequestHandler):
    def post(self):
        self.write({'uuid': 'placeholder'})

def make_app():
    return Application([
        (r"/", CollectHandler)
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()


