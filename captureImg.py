import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
import cv2
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
from msrest.authentication import CognitiveServicesCredentials

# Configs
attri = ['emotion', 'age']
# KEY = '06bfe4c9841a4acfb7926f707c18bc91'
# ENDPOINT = 'https://centralus.api.cognitive.microsoft.com'
KEY = '19844e61112344d597448b416a259cc4'
ENDPOINT = 'https://centralus.api.cognitive.microsoft.com/'

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
webcam = cv2.VideoCapture(1)

PERSON_GROUP_ID = 'myteamsfaces'
TARGET_PERSON_GROUP_ID = str(uuid.uuid4())
# Debug helpers


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


url = 'https://smartmirroryoo.azurewebsites.net/updatePersonState?person='
url = 'http://127.0.0.1:5000/updatePersonState'
while True:
    check, frame = webcam.read()
    time.sleep(.5)
    cv2.imwrite(filename='saved_img.jpg', img=frame)
    im1 = open("saved_img.jpg", "rb")

    # Identify the person
    face_ids = []
    faces = face_client.face.detect_with_stream(
        im1, return_face_attributes=attri)
    for face in faces:
        face_ids.append(face.face_id)

        # Identify faces
    if len(face_ids) is not 0:
        print('Person detected!')
        results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
        names = []
        for result in results:
            candidates = sorted(result.candidates,
                                key=lambda c: c.confidence, reverse=True)
            if len(candidates) > 0:
                top_candidate = candidates[0]
                person = face_client.person_group_person.get(
                    PERSON_GROUP_ID, top_candidate.person_id)
                if top_candidate.confidence > .8:
                    names.append(person.name)
                else:
                    names.append(person.name)
        post = {'person':[]}
        for name,face in zip(names, faces):
            emo = best_emotion(face.face_attributes.emotion)
            post['person'].append([name,emo])
            print(f'Name: {name}, Emo: {emo}')
        r = requests.post(url, json=post)
        '''
        img = Image.open('saved_img.jpg')
        # For each face returned use the face rectangle and draw a red box.
        draw = ImageDraw.Draw(img)
        for face in faces:
            draw.rectangle(getRectangle(face), outline='red')
            topLeft, botRight = getRectangle(face)
            tLeft, tTop = getTextLoc(face)
            draw.text((tLeft, tTop - 40),
                      f'Emotion: {best_emotion(face.face_attributes.emotion)}')
            draw.text((tLeft, tTop - 20), f'Age :{face.face_attributes.age}')
        img.show()
        '''
    else:
        print('No person detected!')
        post = {'person': []}
        r = requests.post(url, json=post)
        '''
        img = Image.open('saved_img.jpg')
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), 'Person on screen: no')
        img.show()
        '''
