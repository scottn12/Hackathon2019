import azure.cognitiveservices.speech as speechsdk
from twilio.rest import Client
import requests

import os
import time
from xml.etree import ElementTree
import simpleaudio as sa

try:
    input = raw_input
except NameError:
    pass

speech_key, service_region = "1fd982a510a04cd0bc548891b9323e35", "centralus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

account_sid = 'AC94fb14dfa4d409c2247a9ce90c6a2e4e'
auth_token = 'ea48a68853ff7c684c90c669a540f2e8'
client = Client(account_sid, auth_token)

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

names = ['Steven', 'Jackson', 'Seve']
phoneNumbers = ['+18623157785', '+15515023917', '+15512632881']

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

				  
def speak_out(str):
	app = TextToSpeech(speech_key, str)
	app.get_token()
	app.save_audio()
	wave_obj = sa.WaveObject.from_wave_file('sample.wav')
	play_obj = wave_obj.play()
	play_obj.wait_done()				  

while True:
	print("Say something...")
	t = ''
	result = speech_recognizer.recognize_once()
	if result.reason == speechsdk.ResultReason.RecognizedSpeech:
		print("Recognized: {}".format(result.text))
		if(result.text.find("Send a message") != -1):
			for i in range(len(names)):
				if(result.text.find(names[i]) != -1):
					print('Say the content')
					speak_out('What would you like to say')
					result = speech_recognizer.recognize_once()
					if result.reason == speechsdk.ResultReason.RecognizedSpeech:
						t = result.text
						r = requests.get('http://127.0.0.1:5000'+'/confirmMsg?msg='+t)
						print(f'Sending mesg: {t}, do you want to send it?')
						speak_out(f'Sending message: {t}, do you want to send it?')
						# Send result to frontend for comfirm
						result = speech_recognizer.recognize_once()
						if result.reason == speechsdk.ResultReason.RecognizedSpeech:
							if result.text.find('Yes') is not -1:
								message = client.messages.create(
									body=t,
									to=phoneNumbers[i],
									from_='+12565768383'
								)
								print('Sent!')
								speak_out('Sent')
							else:
								print('Canceled')
								speak_out('Canceled')
					else:
						t = 'Can\'t understand'
						continue

					
	elif result.reason == speechsdk.ResultReason.NoMatch:
		print("No speech could be recognized: {}".format(result.no_match_details))
	elif result.reason == speechsdk.ResultReason.Canceled:
		cancellation_details = result.cancellation_details
		print("Speech Recognition canceled: {}".format(cancellation_details.reason))
		if cancellation_details.reason == speechsdk.CancellationReason.Error:
			print("Error details: {}".format(cancellation_details.error_details))

