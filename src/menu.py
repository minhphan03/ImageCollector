from tornado.web import RequestHandler

class MenuHandler(RequestHandler):
    def get(self):
        return self.render("menu.html")