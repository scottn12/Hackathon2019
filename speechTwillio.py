import azure.cognitiveservices.speech as speechsdk
from twilio.rest import Client

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "1fd982a510a04cd0bc548891b9323e35", "centralus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

account_sid = 'AC94fb14dfa4d409c2247a9ce90c6a2e4e'
auth_token = 'ea48a68853ff7c684c90c669a540f2e8'
client = Client(account_sid, auth_token)

# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print("Say something...")


# Starts speech recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed.  The task returns the recognition text as result. 
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query. 
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.

names = ['Steven', 'Jackson', 'Seve'];
phoneNumbers = ['+18623157785', '+15515023917', '+15512632881']

# Checks result.
while True:
	result = speech_recognizer.recognize_once()
	if result.reason == speechsdk.ResultReason.RecognizedSpeech:
		print("Recognized: {}".format(result.text))
		if(result.text.find("send a message") != -1):
			for i in range(len(names)):
				if(result.text.find(names[i]) != -1):
					message = client.messages.create(
                        body="Hello, its me",
                        to=phoneNumbers[i],
                        from_='+12565768383'
                    )
					
	elif result.reason == speechsdk.ResultReason.NoMatch:
		print("No speech could be recognized: {}".format(result.no_match_details))
	elif result.reason == speechsdk.ResultReason.Canceled:
		cancellation_details = result.cancellation_details
		print("Speech Recognition canceled: {}".format(cancellation_details.reason))
		if cancellation_details.reason == speechsdk.CancellationReason.Error:
			print("Error details: {}".format(cancellation_details.error_details))

