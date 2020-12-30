from camera import captureImage
import config
import requests

subscription_key = config.subscription_key
endpoint = config.endpoint
analyze_url = config.analyze_url

def getVisionData(image_path):
    print("What do I see intent launched")
    captureImage()
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    analysis = response.json()

    image_caption = analysis["description"]["captions"][0]["text"].capitalize()

    return image_caption
