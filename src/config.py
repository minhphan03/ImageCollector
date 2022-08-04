import sys
from os import path
from tornado.options import define

settings = {
    'template_path': 'templates',
    'static_path': path.join(path.dirname(__file__), "../public/images"),
    'xsrf_cookies': False
}

define("port", default=8888, help='run on the given port', type=int)
PACKAGE_PATH = PACKAGE_PATH = path.realpath(path.join(path.dirname(__file__), '..'))
sys.path.append(PACKAGE_PATH)
