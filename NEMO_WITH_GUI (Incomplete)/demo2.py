import pyttsx3
while True:
    engine = pyttsx3.init()
    engine.say("This is a sample text to speech")
    engine.runAndWait()