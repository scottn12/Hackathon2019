import time
import speech_recognition as sr
import requests

def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

if __name__ == "__main__":
    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = ["news", "calendar", "weather", "email"]

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    print('Getting starting...')
    time.sleep(2)
    while True:
        url = 'http://127.0.0.1:5000/updateEmailState?email='

        print('What do you want to know?\n')
        guess = recognize_speech_from_mic(recognizer, microphone)
        abc=guess["transcription"]
        news='email'
        stop='stop'
        if guess["transcription"] or not guess["success"]:
            if stop in abc and abc is not None:
                break
            print("You said: {}\n".format(guess["transcription"]))
            
            if news in abc and abc is not None: 
                print('got it!\n\n')
                r = requests.get(url+'yes')
            else:
                print('Want some news?\n\n')
                r = requests.get(url+'no')
            continue

        print("I didn't catch that. What did you say?\n")

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            continue
          
