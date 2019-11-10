import cv2
import time
import asyncio
import glob
import io
import os
import sys
import time
import uuid
from io import BytesIO
from urllib.parse import urlparse

import requests
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import (OperationStatusType,
                                                        Person,
                                                        SnapshotObjectType,
                                                        TrainingStatusType)
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageDraw

# Configs
attri = ['emotion', 'age']
KEY = '06bfe4c9841a4acfb7926f707c18bc91'
ENDPOINT = 'https://centralus.api.cognitive.microsoft.com'
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

webcam = cv2.VideoCapture(0)

while True:
    check, frame = webcam.read()
    time.sleep(5)
    cv2.imwrite(filename='saved_img.jpg', img=frame)
    im1 = open("saved_img.jpg", "rb")
    detected_faces = face_client.face.detect_with_stream(
        image=im1, return_face_attributes=attri)
    url = 'https://smartmirroryoo.azurewebsites.net/updatePersonState?person='
    if len(detected_faces) is not 0:
        r = requests.get(url+'yes')
    else:
        r = requests.get(url+'no')
