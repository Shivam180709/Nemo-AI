

import keyboard
import threading
import speech_recognition as sr
import multiprocessing
import google.generativeai as genai
import json
import pyttsx3
from time import sleep
import datetime
import requests

import pyautogui
import os
from bs4 import BeautifulSoup
import pywhatkit
import re
from plyer import notification
import pygame



def LISTEN(stop_listening, shared_dict,stop_flag):
   
    """ This is the ultimate Listen Function which listens in background."""
    # Create a recognizer object
    recognizer = sr.Recognizer()
    def listen(stop_listening, shared_dict):
        """Function to continuously listen for user speech.""" 
        while True:
            with sr.Microphone() as source:
                #print("Listening...")
                audio = recognizer.listen(source)
                
                # Send audio for processing
                threading.Thread(target=process_audio, args=(audio, stop_listening, shared_dict)).start()

    def process_audio(audio, stop_listening, shared_dict):
        """Function to process the audio and convert it to text."""
        try:
            #print("Processing audio...")
            # Recognize speech using Google Web Speech API
            recognized_text = recognizer.recognize_google(audio, language='en-IN')
            #print(f"Recognized: {recognized_text}")
            if "hold" in recognized_text.lower() or "wait" in recognized_text.lower() or "stop" in recognized_text.lower() :
                stop_flag.value = True  # Set the stop flag to True
                print("Stopping speech...")
            if "nemo" in recognized_text.lower() or "imo" in recognized_text.lower() or "memo" in recognized_text.lower() or"nemo" in recognized_text.lower() :
                #print("ACTIVATING SIR>>>>..........")
                try:
                    recognized_text =re.sub(r"\bnemo\b", "", recognized_text, flags=re.IGNORECASE).strip()
                    recognized_text =re.sub(r"\bmemo\b", "", recognized_text, flags=re.IGNORECASE).strip()
                    recognized_text =re.sub(r"\bimo\b", "", recognized_text, flags=re.IGNORECASE).strip()
                except Exception as e:
                    print("Unable to Convert the text error: ",e)
                 # Update the shared dictionary
                shared_dict['text'] = recognized_text
                stop_listening.value = True  # Stop listening after activation
            else:
                print("You are not taking to Nemo.")
            
        except sr.UnknownValueError:
            pass
           #print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Request error from Google Speech Recognition service: {e}")

    listening_thread = threading.Thread(target=listen, args=(stop_listening, shared_dict))
    listening_thread.start()

    # Wait for the listening thread to finish
    listening_thread.join()
    print("Listening has stopped.")


if __name__ == '__main__':
    
    # Variable for Text to specch
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    #print(voices[1])

    engine.setProperty('rate', 165)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
    engine.setProperty('voice', voices[2].id)  

    # speak Function

    def speak(text):
            """Speak text in smaller chunks and check stop flag after each chunk."""
        
            stop_flag.value = False
            # Split the text into sentences based on punctuation (you can adjust the regex if needed)
            sentences = re.split(r'(?<=[.!?]) +', text)
            
            engine.startLoop(False)  # Start the event loop in non-blocking mode

            for sentence in sentences:
                if stop_flag.value:  # If the stop flag is set to True, stop speaking
                    engine.say("Ok Sir.")
                    engine.stop()

                    print("Speech stopped.")
                    break

                engine.say(sentence)
                
                # Process the speech asynchronously and wait for it to finish the sentence
                while engine.isBusy():
                    engine.iterate()  # Process the speech event loop

            engine.endLoop()  # End the loop when speech is finished


    # Creating  the model
    # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel for more.
    genai.configure(api_key="AIzaSyC3jexRtiTwxK7ITZmt4JiS-J0DR3OB7Ak")
    generation_config = {
    "temperature": 1.2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
    ]
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="Your Name is \"Nemo\" you are desktop virtual asistance. Give Responses as short as possible means about or less one or two sentenses depending on the question asked.Alway remember you have to give short responses.",
    )

    # Method for Add new data to Json File
    def append_to_json_file(file_path, new_data):
        try:
            # Step 1: Open and read the existing data from the JSON file
            with open(file_path, 'r') as file:
                try:
                    # Load the current content of the file into a list
                    data = json.load(file)
                    if not isinstance(data, list):
                        raise ValueError("The JSON file must contain a list at the top level.")
                except json.JSONDecodeError:
                    # If the file is empty or the content is not a valid JSON, we start with an empty list
                    data = []

            # Step 2: Append the new data to the list
            if isinstance(new_data, list):
                data.extend(new_data)  # Append if new_data is a list
            else:
                data.append(new_data)  # Append if new_data is a single object

            # Step 3: Write the updated data back to the JSON file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2)

            print(f"Data successfully appended to {file_path}.")

        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # List  passed the Model as the memory.
    history = []

    # Function to load JSON data from a file and assign it to the history variable
    def load_json_to_history(file_path):
        global history  # To modify the global variable history
        try:
            # Open the JSON file and load its content
            with open(file_path, 'r') as file:
                history = json.load(file)  # Assign the loaded data to the history variable
                print(f"Data successfully loaded into history from {file_path}.")
        
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: The file '{file_path}' contains invalid JSON.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Load the content of the JSON file into the history variable
    load_json_to_history(r'conversations.json')


    chat_session = model.start_chat(
        history=history
    )
    
    # Using MultiProcessing for using LISTEN function
    stop_flag = multiprocessing.Value('b', False)
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()
    shared_dict['text'] = "none"
    stop_listening = multiprocessing.Value("b", False)
    m1 = multiprocessing.Process(target=LISTEN, args=(stop_listening, shared_dict,stop_flag))
    m1.start()

# Function Related to Features

    def Temp():
        search = "temperature in mughalsaria"
        url = f"https://www.google.com/search?q={search}"
        r = requests.get(url)
        data = BeautifulSoup(r.text,"html.parser")
        temperature = data.find("div",class_ = "BNeawe").text
        speak(f"The Temperature Outside Is {temperature}")

    def screenshot():
        current_datetime = datetime.datetime.now()
        formatted_time = current_datetime.strftime("%H%M%S")
        filenamedate = str(formatted_time) + str(".png")
        path1 = f"{filenamedate}"
        kk = pyautogui.screenshot()
        kk.save(path1)
        os.startfile(f"{filenamedate}")
        title = r'Nemo: 📸📷Screnshot Taken..📸📷'
        app_name= r'😊Nemo😊'
        app_icon=r"Icon.ico"
        print("Nemo: Scrennshot save at C:\\Users\\micro\\OneDrive\\Pictures\\Screenshots with name ",filenamedate,".\n")
        speak("Here Is Your ScreenShot")
        sleep(2)
        notification.notify(title=title,message=f"ScrennShot Saved as C:\\Users\\micro\\OneDrive\\Pictures\\Screenshots with name {filenamedate} ",app_name=app_name ,app_icon=app_icon, timeout=10)       
 
    def OpenExe(Query):
                Query = str(Query).lower()
                Nameoftheapp = Query.replace("open ","")
                speak(f"Opening {Nameoftheapp}") 
                pyautogui.press('win')
                sleep(1)
                keyboard.write(Nameoftheapp)
                sleep(1)
                keyboard.press_and_release('enter')
                sleep(0.5)
 
    def AI_Response(user_input):
        response = chat_session.send_message(user_input)
        model_response = response.text
        print(f'Nemo: {model_response}')
        speak(model_response)
        chat_session.history.append({"role": "user", "parts": [user_input]})
        chat_session.history.append({"role": "model", "parts": [model_response]})
        # Append this new conversation to the 'conversations.json' file
        if "add in your memory"in user_input or "save in your memory"in user_input :
            user_data = {
            "role": "user",
            "parts": [f"{user_input}"]
            }
            model_data = {
            "role": "model",
            "parts": [f"{model_response}"]
            }
            append_to_json_file(r'conversations.json', user_data)  
            append_to_json_file(r'conversations.json', model_data)  
  
    def play_on_yt(user_input):
        user_input = user_input.lower().replace("play","")
        pywhatkit.playonyt(user_input)
        speak("Playing sir....")
        sleep(1)
        title = r'Nemo: ▶️▶️Video Played ..▶️▶️ '
        app_name= r'😊Nemo😊'
        app_icon=r"Icon.ico"
        notification.notify(title=title,message=f"Video played on youtube on the topic or related {user_input}.",app_name=app_name ,app_icon=app_icon, timeout=10)
  
    def tell_time():
            # %I for 12-hour format, %M for minutes, %p for AM/PM
        hour_minute = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Sir, the time is {hour_minute}")

    # Function for Timmer 
    def extract_time(user_input):
    # Regex to find the number and unit (minutes, seconds, hours)
        match = re.search(r"(\d+)\s*(seconds?|minutes?|hours?)", user_input.lower())    
        if match:
            time_value = int(match.group(1))  # Extract the number (e.g., 5)
            time_unit = match.group(2)        # Extract the time unit (e.g., minutes)   
            # Convert everything to seconds for simplicity
            if "second" in time_unit:
                return time_value
            elif "minute" in time_unit:
                return time_value * 60
            elif "hour" in time_unit:
                return time_value * 3600
        return None  # Return None if no valid time is found        
    def set_timer(duration_seconds):
        def countdown():
            
            engine.stop()
            sleep(duration_seconds)  # Wait for the specified time
            title = r'Nemo: ⌛⌛Time Up...⌛⌛ '
            app_name= r'😊Nemo😊'
            app_icon=r"Icon.ico"
            notification.notify(title=title,message=f"Timer Setted of {duration_seconds} seconds is over.",app_name=app_name ,app_icon=app_icon, timeout=10)
            pygame.mixer.init()
            pygame.mixer.music.load("Alarm_timer_sound.wav")
            sleep(2)
            for i in range(4):
                pygame.mixer.music.play()
                sleep(2)
        
        # Start a new thread to run the countdown timer
        timer_thread = threading.Thread(target=countdown)
        timer_thread.start()
    def handle_timer_command(user_input):
        # Extract the time from the user input
        duration_seconds = extract_time(user_input)
        
        if duration_seconds is not None:
            # If valid time is found, set the timer
            set_timer(duration_seconds)
            mgs = f"Timer started for {duration_seconds} seconds."
            print("Nemo: ",mgs)
            speak(mgs)
        else:
            # If no valid time is found in the input
            print("Sorry, I couldn't understand the time duration.")

    #Functions for alarm
    def extract_alarm_time(user_input):
        # Regex to extract the hour, minute, and AM/PM or a.m./p.m.
        match = re.search(r"(\d{1,2}):(\d{2})\s*(AM|PM|a\.m\.|p\.m\.)", user_input, re.IGNORECASE)
        
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            period = match.group(3).lower()  # Lowercase the period for consistent comparison

            # Convert the period to "am" or "pm" for easier handling
            if period in ['a.m.', 'am']:
                period = "AM"
            elif period in ['p.m.', 'pm']:
                period = "PM"

            # Convert to 24-hour format
            if period == "PM" and hour != 12:
                hour += 12
            elif period == "AM" and hour == 12:
                hour = 0

            # Return a datetime object representing today at the given time
            now = datetime.datetime.now()
            alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            # If the alarm time has already passed today, set it for tomorrow
            if alarm_time < now:
                alarm_time = alarm_time.replace(day=now.day + 1)
            a = f"Alarm set for {alarm_time.strftime('%I:%M %p')}"
            print("Nemo: ",a)
            speak(a)
            return alarm_time
        return None
    def set_alarm(alarm_time):
        def monitor_alarm():
            

            # Continuously check if the alarm time has been reached
            while True:
                current_time = datetime.datetime.now()
                if current_time >= alarm_time:
                    #print("ALARM! Time's up!")
                    title = f'🤖Nemo: ⏰⏰It\'s {alarm_time.strftime('%I:%M %p')} ...⏰⏰ '
                    app_name= r'😊NEMO😊'
                    app_icon=r"Icon.ico"
                    notification.notify(title=title,message=f"Alarm Setted of {alarm_time.strftime('%I:%M %p')} is over.",app_name=app_name ,app_icon=app_icon, timeout=10)
                    pygame.mixer.init()
                    pygame.mixer.music.load("Alarm_timer_sound.wav")
                    sleep(2)
                    for i in range(4):
                        pygame.mixer.music.play()
                        sleep(2)
                    # You could add sound, a notification, or other alarm actions here
                    break
                # Sleep for a minute before checking again to avoid high CPU usage
                sleep(30)

        # Start the monitoring in a separate thread
        alarm_thread = threading.Thread(target=monitor_alarm)
        alarm_thread.start()
    def handle_alarm_command(user_input):
        # Extract the alarm time from the user input
        alarm_time = extract_alarm_time(user_input)
        
        if alarm_time is not None:
            # If a valid alarm time is found, set the alarm
            set_alarm(alarm_time)
        else:
            print("Sorry, I couldn't understand the alarm time.")

    # Function to handle automation commands
    commands = {
    r"(temperature)": lambda _: Temp(),
    r"(open)": OpenExe,  # This function needs user_input
    r"(timer)": handle_timer_command,
    r"(alarm)": handle_alarm_command,
    r"(play)": play_on_yt,  # This function also needs user_input
    r"(snap the screen|take screenshot|capture the screen)": lambda _: screenshot(),
    r"(the time)": lambda _: tell_time(),
}

     # Storing Keywords for Automation or specific functions.

    def handle_automation(user_input):
        for pattern, func in commands.items():
            if re.search(pattern, user_input.lower()):
                if callable(func):
                    func(user_input)  # Pass user_input only if necessary
                else:
                    func()  # Functions that don't require input can be called directly
                return True  # Indicates that a command was found and executed
        return False  # No automation command matched
   
    # Main Function runing the loop.
    def chatbot():
        while True:
            if stop_listening.value:
                print("User Said: ", shared_dict['text'])
                user_input = shared_dict['text']

                if user_input.lower() == "quit":
                    break

                # First check if the input is an automation command
                if not handle_automation(user_input):
                    # If not an automation command, use AI response
                    AI_Response(user_input)
                stop_listening.value = False
    
    # Calling the Main Function running all
    chatbot()
    