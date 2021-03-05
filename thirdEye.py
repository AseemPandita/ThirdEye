import logging
import os
import sys
from flask import Flask
from flask_ask import Ask, request, session, question, statement
from io import BytesIO
from ocrHelper import getOcrData
from visionHelper import getVisionData


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

IMAGE_PATH = "data/image.jpg"


@ask.launch
def launch():
    print("Application launched")
    speech_text = 'Third Eye Activated! Point your camera and ask me for a description'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('WhatDoISee')
def whatDoISee():
    image_caption = getVisionData(IMAGE_PATH)
    if image_caption == "":
        image_caption = "I couldn't see it clearly. Please retry."
    speech_text = image_caption
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('ReadText')
def readIntent():
    output = getOcrData(IMAGE_PATH)
    if output == "":
        output = "Could not recognize the text."
    speech_text = output
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('DeleteData')
def readIntent():
    output = getOcrData(IMAGE_PATH)
    if output == "":
        output = "Could not recognize the text."
    speech_text = output
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

# Other amazon intents ------------------------------

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
