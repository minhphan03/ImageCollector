from tornado.web import Application, RequestHandler
from tornado.options import define, options
import tornado.httpserver
import uuid, sys
from os import path, environ
import base64
import asyncio
import motor.motor_tornado
from bson import ObjectId

PACKAGE_PATH = PACKAGE_PATH = path.realpath(path.join(path.dirname(__file__), '..'))
sys.path.append(PACKAGE_PATH)

# connect to the database
client = motor.motor_tornado.MotorClient(environ["MONGODB_URL"])
db = client.imageDatabase

define("port", default=8888, help='run on the given port', type=int)

# class PageHandler(RequestHandler):
#     def json_response(self, data, status_code=200):
#         self.set_status(status_code)
        
class UploadHandler(RequestHandler):
    async def get(self):
        self.write({'message': '{}'.format(str(uuid.uuid4()))})
    
    async def post(self):
        print("hello it's here")
        file = self.request.files['image'][0]
        self.write("it's here")
        print("it's in here?")
        # check extension (later)
        try: 
            fextension =  path.splitext(file['filename'])[1]
            image_uuid = str(uuid.uuid4())
            with open('public/images/'+ image_uuid + "." + fextension, 'wb') as f:
                f.write(file['body'])

            # connect to the images database
            objectID = str(ObjectId())
            new_image = await self.settings["db"]["images"].insert_one(
                {
                    "_id": objectID,
                    "uuid": image_uuid,
                    "path": "this is the path"
                }
            )
            created_image = await self.settings["db"]["images"].find_one(
                {
                    "_id": new_image.inserted_id
                }
            )
            self.set_status(201)
            return self.write(created_image)
        except Exception as e:
            print(e)

class ShowImageHandler(RequestHandler):
    def get(self, image_uuid=None):
        if image_uuid is not None:
            pass

settings = {
    'template_path': 'templates',
    'static_path': 'static',
    'xsrf_cookies': False
}

async def main():
    options.parse_command_line()
    application = Application([
        (r"/", UploadHandler),
        (r"/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", ShowImageHandler)
    ],
        debug=True, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
