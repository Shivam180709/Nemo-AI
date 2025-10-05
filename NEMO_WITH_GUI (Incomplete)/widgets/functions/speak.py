import pyttsx3


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1])
engine.setProperty('rate', 165)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
engine.setProperty('voice', voices[0].id)  


def speak(text):
    engine.say(text)
    engine.runAndWait()