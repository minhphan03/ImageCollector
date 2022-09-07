from ast import parse
import json
from tornado.web import Application, StaticFileHandler, RequestHandler
from tornado.options import define, options, parse_command_line
import logging
import tornado.httpserver
from os import path
import asyncio
from datetime import datetime
from bson import ObjectId
from motor import motor_asyncio
import uuid
from config import *
from check_type import guess_image_mime_type

# connect to the database
try:
    logging.info('Connecting to the database...')
    client = motor_asyncio.AsyncIOMotorClient('image_database', 27017)
    db = client['database']
    coll = db['images']
except Exception as e:
    print(e)


class MenuHandler(RequestHandler):
    def get(self):
        return self.render("menu.html")


class UploadHandler(RequestHandler):
    async def get(self):
        self.render("upload.html")
    
    async def post(self):
        file = self.request.files['img'][0]

        # check file type
        file_type = guess_image_mime_type(file['body'])
        if file_type == 'image/unknown-type':
            self.render("error.html")
            raise tornado.web.HTTPError(400)
        
        try: 
            # collect data to put into the database
            fextension =  path.splitext(file['filename'])[1]
            image_uuid = str(uuid.uuid4())
            image_path = 'public/images/'+ image_uuid + fextension
            with open(image_path, 'wb') as f:
                f.write(file['body'])

            dict_ = {
                        "uuid": image_uuid,
                        "extension": fextension,
                        "file_type": file_type,
                        "path": image_path,
                        "time_created": str(datetime.now())
                    }
            dict_["_id"] = str(ObjectId())

            new_image = await self.settings["db"]["images"].insert_one(dict_)

            # confirm image has been added to database
            created_image = await self.settings["db"]["images"].find_one(      
                {
                    "_id": new_image.inserted_id
                }
            )
            self.set_status(201)
            self.render('uuid.html', uuid=image_uuid)
        except Exception as e:
            print(e)
            self.render("error.html")
            raise tornado.web.HTTPError(500)
            

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
                        self.set_header("Content-type", image["file_type"])
                else:
                    self.render("error.html")
                    raise tornado.web.HTTPError(404)
            else:
                self.render("error.html")
                raise tornado.web.HTTPError(400)
            
            # self.render("finish.html")
        except Exception as e:
            print(e)
            self.render("error.html")
            raise tornado.web.HTTPError(500)

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
                    self.set_header("Content-type", image["file_type"])
            else:
                raise tornado.web.HTTPError(404)
        else:
            raise tornado.web.HTTPError(400)

    async def post(self):
        file = self.request.files['image'][0]
        file_type = guess_image_mime_type(file['body'])
        
        if file_type == 'image/unknown-type':
            return self.write(
                json.dumps(
                    {
                        'status': 'failed',
                        'message': 'wrong image format'
                    }
                )
            )
        
        try: 
            fextension =  path.splitext(file['filename'])[1]
            image_uuid = str(uuid.uuid4())
            image_path = 'public/images/'+ image_uuid + fextension
            with open(image_path, 'wb') as f:
                f.write(file['body'])

            # connect to the images database
            dict_ = {
                        "uuid": image_uuid,
                        "extension": fextension,
                        "file_type": file_type,
                        "path": image_path,
                        "time_created": str(datetime.now())
                    }
            dict_["_id"] = str(ObjectId())
            new_image = await self.settings["db"]["images"].insert_one(dict_)

            # check database that info is successfully written
            created_image = await self.settings["db"]["images"].find_one(      
                {
                    "_id": new_image.inserted_id
                }
            )
            self.set_status(201)
            return self.write(
                json.dumps(
                    {
                        'status': 'success',
                        'uuid': created_image['uuid']
                    }
                )
            )
        except Exception as e:
            raise tornado.web.HTTPError(500)

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