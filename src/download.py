from tornado.web import RequestHandler

class DownloadHandler(RequestHandler):
    def get(self):
        self.render("download.html")
    
    def post(self):
        self.render("finish.html")
