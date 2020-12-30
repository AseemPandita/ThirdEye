from camera import captureImage
import config
import requests

subscription_key = config.subscription_key
endpoint = config.endpoint
ocr_url = config.ocr_url

def getOcrData(image_path):
    print("Read Text intent launched")
    captureImage()
    image_data = open(image_path, "rb").read()
    
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type':'application/octet-stream'}
    params = {'language': 'unk', 'detectOrientation': 'true'}
    response = requests.post(ocr_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    analysis = response.json()

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

    return output
