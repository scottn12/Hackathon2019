from flask import Flask, jsonify, request, Response
import azure.cognitiveservices.speech as speechsdk
import fetchemail
import callendar
import datetime
import requests
import time
from xml.etree import ElementTree
import simpleaudio as sa

speech_key, service_region = "1fd982a510a04cd0bc548891b9323e35", "centralus"
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

app = Flask(__name__)

personState = False
personList = None
emailState = False
registerUser = ['jackson']
hasMsg = False
Msg = ''

timeStart = None


class TextToSpeech(object):
    def __init__(self, subscription_key, str):
        self.subscription_key = subscription_key
        self.tts = str
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    def get_string(self, str):
        self.strToSend = str

    def get_token(self):
        fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {'Ocp-Apim-Subscription-Key': self.subscription_key}
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self):
        base_url = 'https://westus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set(
            'name', 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)')
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open('sample.wav', 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) +
                      "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) +
                  "\nSomething went wrong. Check your subscription key and headers.\n")


@app.route('/checkForPerson')
def checkForPerson():
    global personState
    global personList
    resp = jsonify({'person': personState, 'data': personList})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp, 200


@app.route('/updatePersonState', methods=['POST'])
def updateState():
    global personState
    global personList
    json = request.json
    # {'person': [['Jackson', 'contempt']]}
    print(json)
    if len(json['person']) > 0:
        personState = True
        personList = json['person']
    else:
        personState = False
        personList = []
    return 'success'
# Rec
@app.route('/checkForEmail')
def checkForEmail():
    global emailState
    if emailState:
        resp = jsonify({'email': True})
        emailState = False
    else:
        resp = jsonify({'email': False})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp, 200


@app.route('/updateEmailState')
def updateEmailState():
    global emailState
    state = request.args.get('email')
    if state == 'yes':
        emailState = True
    else:
        emailState = False
    return 'success'


@app.route('/readEmail')
def readEmail():
    r = fetchemail.main()
    resp = jsonify({'email': r})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp, 200


@app.route('/getSchedule')
def schedule():
    global registerUser
    person = request.args.get('user')
    if person not in registerUser:
        resp = jsonify({'status': 'nRegistered'})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, 200
    else:
        s = callendar.getSchedule(person)
        return jsonify(s)


@app.route('/confirmMsg', methods=['GET'])
def addComfirm():
    global hasMsg
    global Msg
    msg = request.args.get('msg')
    hasMsg = True
    Msg = msg
    return 'success'


@app.route('/checkMsg', methods=['GET'])
def ckMsg():
    global hasMsg
    if hasMsg:
        t = hasMsg
        hasMsg = False
        resp = jsonify({'status': t})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, 200
    else:
        resp = jsonify({'status': hasMsg})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, 200


@app.route('/getMsg', methods=['GET'])
def getMst():
    global Msg
    resp = jsonify({'msg': Msg})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp, 200


def speak_out(str):
    app = TextToSpeech(speech_key, str)
    app.get_token()
    app.save_audio()
    wave_obj = sa.WaveObject.from_wave_file('sample.wav')
    play_obj = wave_obj.play()
    play_obj.wait_done()


@app.route('/readThis', methods=['GET'])
def read():
    global timeStart
    m = request.args.get('msg')
    speak_out(m)
    t = datetime.datetime.now()
    print(time)
    print(t)
    if timeStart is not None:
        if t > timeStart + datetime.timedelta(seconds=20):
            print('here')
            speak_out(m)
            timeStart = datetime.datetime.now()
    resp = jsonify({'status': 'yo'})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp, 200


if __name__ == '__main__':
    app.run()
