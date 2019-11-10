import asyncio, io, glob, os, sys, time, uuid, requests, cv2
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
webcam = cv2.VideoCapture(0)

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


while True:
    check, frame = webcam.read()
    time.sleep(5)
    cv2.imwrite(filename='saved_img.jpg', img=frame)
    im1 = open("saved_img.jpg", "rb")
    im2 = open("saved_img.jpg", "rb")
	
	# Identify the person
    face_ids = []
    faces = face_client.face.detect_with_stream(im1)
    for face in faces:
        face_ids.append(face.face_id)
		
	# Identify faces
    results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
    names = []
    for result in results:
        candidates = sorted(result.candidates, key=lambda c: c.confidence, reverse=True)
        if len(candidates) > 0:
            top_candidate = candidates[0]
            person = face_client.person_group_person.get(PERSON_GROUP_ID, top_candidate.person_id)
            if top_candidate.confidence > .8:
                names.append(person.name)
            else:
                names.append(person.name)

    for name in names:
        print(name)
	

    detected_faces = face_client.face.detect_with_stream(
        image=im2, return_face_attributes=attri)
    url = 'https://smartmirroryoo.azurewebsites.net/updatePersonState?person='
    if not detected_faces:
        r = requests.get(url+'no')
        img = Image.open('saved_img.jpg')
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), 'Person on screen: no')
        img.show()
    else:
        r = requests.get(url+'yes')
        img = Image.open('saved_img.jpg')
        # For each face returned use the face rectangle and draw a red box.
        draw = ImageDraw.Draw(img)
        for face in detected_faces:
            draw.rectangle(getRectangle(face), outline='red')
            topLeft, botRight = getRectangle(face)
            tLeft, tTop = getTextLoc(face)
            draw.text((tLeft, tTop - 40),
                      f'Emotion: {best_emotion(face.face_attributes.emotion)}')
            draw.text((tLeft, tTop - 20), f'Age :{face.face_attributes.age}')
        img.show()
