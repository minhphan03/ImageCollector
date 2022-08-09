
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options
import tornado.httpserver
from os import path
import asyncio
from tornado.web import RequestHandler
from datetime import datetime
from bson import ObjectId
from motor import motor_asyncio
import uuid
from config import *

# connect to the database
try:
    client = motor_asyncio.AsyncIOMotorClient('image_database', 27017)
    db = client['database']
    coll = db['images']
except Exception as e:
    print(e)
    print("error is here!")


class MenuHandler(RequestHandler):
    def get(self):
        return self.render("menu.html")


class UploadHandler(RequestHandler):
    async def get(self):
        self.render("upload.html")
    
    async def post(self):
        file = self.request.files['img'][0]
        # check extension (later)
        try: 
            fextension =  path.splitext(file['filename'])[1]
            image_uuid = str(uuid.uuid4())
            image_path = 'public/images/'+ image_uuid + fextension
            with open(image_path, 'wb') as f:
                f.write(file['body'])

            dict_ = {
                        "uuid": image_uuid,
                        "extension": fextension,
                        "path": image_path,
                        "time_created": str(datetime.now())
                    }
            dict_["_id"] = str(ObjectId())

            new_image = await self.settings["db"]["images"].insert_one(dict_)
            print("it's here in line 50")

            # confirm image has been added to database
            created_image = await self.settings["db"]["images"].find_one(      
                {
                    "_id": new_image.inserted_id
                }
            )
            self.write(created_image["uuid"])
            self.set_status(201)
            self.render('uuid.html', uuid=image_uuid)
        except Exception as e:
            print(e)
            self.render("error.html")
            

class DownloadHandler(RequestHandler):
    async def get(self):
        self.render("download.html")
    
    async def post(self):
        try:
            image_uuid = self.get_body_argument("image_uuid", default=None, strip=True)
            if uuid is not None:
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
                    self.render("error.html")
                    raise tornado.web.HTTPError(404)
            else:
                print("invalid input")
                self.render("error.html")
                raise tornado.web.HTTPError(404)
            
            # self.render("finish.html")
        except Exception as e:
            print(e)
            self.render("error.html")

class APIHandler(RequestHandler):
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

async def main():
    options.parse_command_line()
    application = Application([
        # ui
        (r"/", MenuHandler),
        (r"/upload", UploadHandler),
        (r"/download", DownloadHandler),

        # api
        (r"/api", APIHandler),
        (r"/api/(?P<image_uuid>[̉̉̉a-zA-Z0-9_.-]+)", APIHandler),

        # static handler
        (r"/images/(.*)", StaticFileHandler, dict(path=settings["static_path"]))
    ],
        db=db,
        debug=True, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(main())