# Image Collector

An simple local image collector host using a local-backed MongoDB instance and implemented asynchronously using Python Tornado. This version is developed with additional html code to be more client-friendly. You can also test this collector using an API Platform, such as Postman. This is the backbone of the tool, which is more user-friendly with the UI version. 

### General Instruction for both versions

1. Download the Docker Image from Docker Hub using the command line (Command Prompt/Terminal) `docker image pull minhphan0612/imagecollector:1.0` with 1.0 as the lastest version

### Instructions for Using the API Version with Postman/Insomnia

2. Download the API testing app to your choosing
3. To test uploading images:
    - In the target URL bar: type "http://localhost:8888/upload"
    - choose POST as the API type
    -  
