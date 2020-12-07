import logging
import os
import sys
import requests
from flask import Flask
from flask_ask import Ask, request, session, question, statement
#import RPi.GPIO as GPIO
from PIL import Image
from io import BytesIO
import cv2
import config


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)



subscription_key = config.subscription_key
endpoint = config.endpoint
analyze_url = config.analyze_url
ocr_url = config.ocr_url
#face_api_url = config.face_api_url



image_path = "/home/pi/Desktop/image.jpg"

def captureImage():
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('image'+'.jpg', image)
    del(camera)

@ask.launch
def launch():
    print("App launched")
    speech_text = 'Third Eye Activated! Point your camera and ask me for a description'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('WhatDoISee')
def whatDoISee():
    print("whatdoisee intent is active")
    captureImage()
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    analysis = response.json()

    image_caption = analysis["description"]["captions"][0]["text"].capitalize()

    speech_text = image_caption
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('ReadText')
def readIntent():
    captureImage()
    image_data = open(image_path, "rb").read()

    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type':'application/octet-stream'}
    params = {'language': 'unk', 'detectOrientation': 'true'}
    #data = {'url': image_url}
    response = requests.post(ocr_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    analysis = response.json()

    # Extract the word bounding boxes and text.
    line_infos = [region["lines"] for region in analysis["regions"]]
    word_infos = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                word_infos.append(word_info)
    word_infos
    output = ""
    for word in word_infos:
        output += word["text"] + " "

    print(output)
    speech_text = output
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)





@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'Just ask what is in front of me?'
    return question(speech_text).reprompt(speech_text).simple_card('I can help you see', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
