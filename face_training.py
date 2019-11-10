import asyncio, io, glob, os, sys, time, uuid, requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

KEY = os.environ['FACE_SUBSCRIPTION_KEY']
ENDPOINT = os.environ['FACE_ENDPOINT']

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

PERSON_GROUP_ID = 'myteamsfaces'
TARGET_PERSON_GROUP_ID = str(uuid.uuid4())

'''
Create the PersonGroup
'''
# Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
print('Person group:', PERSON_GROUP_ID)
face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

Steven = face_client.person_group_person.create(PERSON_GROUP_ID, "Steven")
Jackson = face_client.person_group_person.create(PERSON_GROUP_ID, "Jackson")
Severus = face_client.person_group_person.create(PERSON_GROUP_ID, "Severus")
Scott = face_client.person_group_person.create(PERSON_GROUP_ID, "Scott")

'''
Detect faces and register to correct person
'''
# Find all jpeg images of friends in working directory
steven_images = [file for file in glob.glob('*.jpg') if file.startswith("Steven")]
jackson_images = [file for file in glob.glob('*.jpg') if file.startswith("Jackson")]
severus_images = [file for file in glob.glob('*.jpg') if file.startswith("Severus")]
scott_images = [file for file in glob.glob('*.jpg') if file.startswith("Scott")]

for image in steven_images:
    w = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, Steven.person_id, w)

for image in jackson_images:
    m = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, Jackson.person_id, m)

for image in severus_images:
    ch = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, Severus.person_id, ch)

for image in scott_images:
    x = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, Scott.person_id, x)

'''
Train PersonGroup
'''
print()
print('Training the person group...')
# Train the person group
face_client.person_group.train(PERSON_GROUP_ID)

while (True):
    training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
    print("Training status: {}.".format(training_status.status))
    print()
    if (training_status.status is TrainingStatusType.succeeded):
        break
    elif (training_status.status is TrainingStatusType.failed):
        sys.exit('Training the person group has failed.')
    time.sleep(5)
