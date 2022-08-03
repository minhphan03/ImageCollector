from tornado.web import RequestHandler
import uuid
from os import path

class UploadHandler(RequestHandler):
    async def get(self):
        self.render("upload.html")
    
    async def post(self):
        file = self.request.files['img'][0]
        # check extension (later)
        try: 
            fextension =  path.splitext(file['filename'])[1]
            image_uuid = str(uuid.uuid4())
            with open('public/images/'+ image_uuid + fextension, 'wb') as f:
                f.write(file['body'])
        except Exception as e:
            print(e)
        self.render('uuid.html', uuid=image_uuid)
