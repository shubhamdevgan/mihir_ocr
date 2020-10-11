from flask import Flask, request,Response
import os
from flask_api import status
import cv2
from time import sleep
import requests
import io
import json
import os
import random

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test():
    return "<h1 style='color:blue'>Hello There!</h1>"
    
@app.route('/api', methods=['POST'])
def resume():
    try:
        file = request.files.get('resume',None)
        if not file:
            content = {
            'message':'resume is required',
            'status': status.HTTP_400_BAD_REQUEST
            }
            return content,status.HTTP_400_BAD_REQUEST


        file.save(file.filename)
        resim = file.filename
        img = cv2.imread(resim)
        print("Picture is Detected")

        api = img

        # Ocr
        url_api = "https://api.ocr.space/parse/image"
        _, compressedimage = cv2.imencode(".jpg", api, [1, 90])
        file_bytes = io.BytesIO(compressedimage)

        result = requests.post(url_api,
            files={resim: file_bytes},
            data={"apikey": "ab1379a32d88957",
            "language": "eng"})

        result = result.content.decode()
        print(result)
        result = json.loads(result)

        parsed_results = result.get("ParsedResults")[0]
        text_detected = parsed_results.get("ParsedText")
        print("\n\n Data \n\n",text_detected)

        os.remove(file.filename)
        content = {
            'message':'success',
            'data' : text_detected,
            'status': status.HTTP_200_OK
            }
        return content,status.HTTP_200_OK
    except Exception as e:
        content = {
            'message':'unsuccessfull',
            'status': status.HTTP_400_BAD_REQUEST
            }
        return content,status.HTTP_400_BAD_REQUEST

if __name__ == '__main__':
    app.run()
     