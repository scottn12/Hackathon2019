import azure.cognitiveservices.speech as speechsdk
from twilio.rest import Client
import requests

speech_key, service_region = "1fd982a510a04cd0bc548891b9323e35", "centralus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

account_sid = 'AC94fb14dfa4d409c2247a9ce90c6a2e4e'
auth_token = 'ea48a68853ff7c684c90c669a540f2e8'
client = Client(account_sid, auth_token)

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

names = ['Steven', 'Jackson', 'Seve']
phoneNumbers = ['+18623157785', '+15515023917', '+15512632881']

while True:
	print("Say something...")
	t = ''
	result = speech_recognizer.recognize_once()
	if result.reason == speechsdk.ResultReason.RecognizedSpeech:
		print("Recognized: {}".format(result.text))
		if(result.text.find("Send a message") != -1):
			print('here')
			for i in range(len(names)):
				if(result.text.find(names[i]) != -1):
					print('Say the content')
					result = speech_recognizer.recognize_once()
					if result.reason == speechsdk.ResultReason.RecognizedSpeech:
						t = result.text
						print(f'Sending mesg: {t}, confirm?')
						r = requests.get('http://127.0.0.1:5000'+'/confirmMsg?msg='+t)
						# Send result to frontend for comfirm
					else:
						t = 'Can\'t understand'
						continue
					result = speech_recognizer.recognize_once()
					if result.reason == speechsdk.ResultReason.RecognizedSpeech:
						if result.text.find('Yes') is not -1:
							message = client.messages.create(
								body=t,
								to=phoneNumbers[i],
								from_='+12565768383'
							)
							print('Sent!')
						else:
							print('Canceled')
					
	elif result.reason == speechsdk.ResultReason.NoMatch:
		print("No speech could be recognized: {}".format(result.no_match_details))
	elif result.reason == speechsdk.ResultReason.Canceled:
		cancellation_details = result.cancellation_details
		print("Speech Recognition canceled: {}".format(cancellation_details.reason))
		if cancellation_details.reason == speechsdk.CancellationReason.Error:
			print("Error details: {}".format(cancellation_details.error_details))

