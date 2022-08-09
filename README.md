# Image Collector

An simple local image collector host using a local-backed MongoDB instance and implemented asynchronously using Python Tornado. This version is developed with additional html code to be more client-friendly. You can also test this collector using an API Platform, such as Postman. This is the backbone of the tool, which is more user-friendly with the UI version. 

### General Instruction for both versions

1. Download the Docker Image from Docker Hub using the command line (Command Prompt/Terminal) `docker image pull minhphan0612/imagecollector:1.0` with 1.0 as the lastest version

### Instructions for using the API version with Postman/Insomnia
*Disclaimer: the instructions may vary based on the app you use. I use Postman to test the API, so variations may happen if you use another app*
2. Download the API testing app to your choosing
3. To test uploading images:
    - In the target URL bar: type "http://localhost:8888/api" (no slash / at the end)
    - Choose POST as the API request type
    - In the request body, choose form-data type. Put "image" (no double quotes) as key (don't forget to switch the upload type to file) and upload the image into the value box
    - If successful, the request will return a UUID. Refer to this UUID to retrieve your image.
4. To test downloading images using the UUID:
    - In the target URL bar: type "http://localhost:8888/api/{UUID}" where UUID is the UUID of the photo (discard the curly brackets when you use the link)
    - Choose GET as the API request type
    - Make sure the request body is set as "none"
    - Click send to send the request. If successful, the result image will be display in the result box.

### Instructions for using the UI version with web browser
2. Navigate to "http://localhost:8888/"
3. Follow the instructions on the menu to upload and download images. 
