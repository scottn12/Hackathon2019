import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType


def best_emotion(emotion):
    emotions = {}
    emotions['anger'] = emotion.anger
    emotions['contempt'] = emotion.contempt
    emotions['disgust'] = emotion.disgust
    emotions['fear'] = emotion.fear
    emotions['happiness'] = emotion.happiness
    emotions['neutral'] = emotion.neutral
    emotions['sadness'] = emotion.sadness
    emotions['surprise'] = emotion.surprise
    return max(zip(emotions.values(), emotions.keys()))[1]


attri = ['emotion', 'age']

# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = '06bfe4c9841a4acfb7926f707c18bc91'

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = 'https://centralus.api.cognitive.microsoft.com'

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


# Detect a face in an image that contains a single face
single_face_image_url = 'https://www.biography.com/.image/t_share/MTQ1MzAyNzYzOTgxNTE0NTEz/john-f-kennedy---mini-biography.jpg'
single_image_name = os.path.basename(single_face_image_url)

im1 = open("smileMe.jpg", "rb")
detected_faces = face_client.face.detect_with_stream(
    image=im1,
    return_face_attributes=attri)
'''
detected_faces = face_client.face.detect_with_url(
    url=single_face_image_url, return_face_attributes=attri)
'''
if not detected_faces:
    raise Exception('No face detected from image {}'.format(single_image_name))

# Convert width height to a point in a rectangle


def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    bottom = left + rect.height
    right = top + rect.width
    return ((left, top), (bottom, right))


def getTextLoc(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    return left, top


img = Image.open('smileMe.jpg')
# For each face returned use the face rectangle and draw a red box.
draw = ImageDraw.Draw(img)
for face in detected_faces:
    draw.rectangle(getRectangle(face), outline='red')
    topLeft, botRight = getRectangle(face)
    tLeft, tTop = getTextLoc(face)
    draw.text((tLeft, tTop - 40),
              f'Emotion: {best_emotion(face.face_attributes.emotion)}')
    draw.text((tLeft, tTop - 20), f'Age :{face.face_attributes.age}')
# Display the image in the users default image browser.
img.show()
