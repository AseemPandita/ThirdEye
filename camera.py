import cv2
import os

def captureImage():
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    if not os.path.exists('data'):
        os.makedirs('data')
    cv2.imwrite(os.path.join('data/' , 'image.jpg'), image)
    
    del(camera)
