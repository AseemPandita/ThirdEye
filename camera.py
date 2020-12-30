import cv2
import os

def captureImage():
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite(os.path.join('data/' , 'image.jpg'), image)
    del(camera)
