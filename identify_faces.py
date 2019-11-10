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
Identify a face against a defined PersonGroup
'''
# Reference image for testing against
group_photo = 'group1.jpg'
IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))

# Get test image
test_image_array = glob.glob(os.path.join(IMAGES_FOLDER, group_photo))
image = open(test_image_array[0], 'r+b')

# Detect faces
face_ids = []
faces = face_client.face.detect_with_stream(image)
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
			names.append('I see ' + person.name)
		else:
			names.append('I think I see ' + person.name)

for name in names:
	print(name)