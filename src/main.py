from urllib.error import HTTPError
from tornado.web import Application, RequestHandler
from tornado.options import define, options
import tornado.httpserver
import uuid, sys
from os import path, environ
from datetime import datetime
import asyncio
import motor.motor_asyncio
from bson import ObjectId

PACKAGE_PATH = PACKAGE_PATH = path.realpath(path.join(path.dirname(__file__), '..'))
sys.path.append(PACKAGE_PATH)

# connect to the database
try:
    client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    db = client['database']
    coll = db['images']
except Exception as e:
    print(e)
    print("error is here!")

define("port", default=8888, help='run on the given port', type=int)

# class PageHandler(RequestHandler):
#     def json_response(self, data, status_code=200):
#         self.set_status(status_code)
        
class UploadHandler(RequestHandler):
    async def get(self, image_uuid=None):
        if image_uuid is not None:
            if (
                image:= await self.settings["db"]["images"].find_one(
                    {"uuid": image_uuid}
                )
            ) is not None:
                with open(image["path"], "rb") as f:
                    data = f.read()
                    self.write(data)
                    self.set_header("Content-type", "image/png")
            else:
                print("we don't have the photo you need")
                raise tornado.web.HTTPError(404)
        else:
            print("invalid input")
            raise tornado.web.HTTPError(404)
            
        # self.write({'message': '{}'.format(str(uuid.uuid4()))})

    async def post(self):
        file = self.request.files['image'][0]
        # check extension (later)
        try: 
            fextension =  path.splitext(file['filename'])[1]
            image_uuid = str(uuid.uuid4())
            image_path = 'public/images/'+ image_uuid + fextension
            with open(image_path, 'wb') as f:
                f.write(file['body'])

            # connect to the images database
            dict_ = {
                        "uuid": image_uuid,
                        "path": image_path,
                        "time_created": str(datetime.now())
                    }
            dict_["_id"] = str(ObjectId())
            new_image = await self.settings["db"]["images"].insert_one(dict_)
            print("it's here in line 50")
            created_image = await self.settings["db"]["images"].find_one(      
                {
                    "_id": new_image.inserted_id
                }
            )
            self.set_status(201)
            print("hello")
            return self.write(created_image["uuid"])
        except Exception as e:
            print(e)

settings = {
    'template_path': 'templates',
    'static_path': 'static',
    'xsrf_cookies': False
}

async def main():
    options.parse_command_line()
    application = Application([
        (r"/", UploadHandler),
        (r"/(?P<image_uuid>[̉̉̉a-zA-Z0-9_.-]+)", UploadHandler)
    ],
        db=db,
        debug=True, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
