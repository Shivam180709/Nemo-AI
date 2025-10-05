import google.generativeai as genai
import json

import keyboard
import threading
import google.generativeai as genai
import json
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
# Replace this with your API key
apikey = "Api key"
global model_response
model_response = ""
# Configure the API with the provided API key
genai.configure(api_key=apikey)

# Set up the configuration for text generation
generation_config = {
    "temperature": 1.2,  # Controls randomness in responses (higher = more random)
    "top_p": 0.95,       # Controls the diversity of the model's responses
    "top_k": 64,         # Limits the number of candidate tokens considered
    "max_output_tokens": 8192,  # Maximum number of tokens to generate in a response
    "response_mime_type": "text/plain",  # Specifies the response format
}

# Define safety settings for content moderation
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",  # No content is blocked for harassment
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",  # No content is blocked for hate speech
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",  # No content is blocked for explicit content
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",  # No content is blocked for dangerous content
    },
]

# Initialize the generative model with the configuration
model = genai.GenerativeModel(
model_name="gemini-1.5-flash",  # Model name
safety_settings=safety_settings,  # Apply the defined safety settings
generation_config=generation_config,  # Apply the generation configuration
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
load_json_to_history(r'datas/permanent_memory.json')


chat_session = model.start_chat(
        history=history
    )

def Temp():
    global model_response
    search = "temperature in mughalsaria"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text,"html.parser")
    temperature = data.find("div",class_ = "BNeawe").text
    model_response =  f"The Temperature Outside Is {temperature}"
def screenshot():
    global model_response
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
    sleep(2)
    notification.notify(title=title,message=f"ScrennShot Saved as C:\\Users\\micro\\OneDrive\\Pictures\\Screenshots with name {filenamedate} ",app_name=app_name ,app_icon=app_icon, timeout=10)       
    model_response = "Here Is Your ScreenShot"

def OpenExe(Query):
            global model_response
            Query = str(Query).lower()
            Nameoftheapp = Query.replace("open ","")
            pyautogui.press('win')
            sleep(1)
            keyboard.write(Nameoftheapp)
            sleep(1)
            keyboard.press_and_release('enter')
            sleep(0.5)
            model_response = f"Opening {Nameoftheapp}"

def AI_Response(user_input):
    global model_response
    response = chat_session.send_message(user_input)
    model_response = response.text

    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})
    
    # Append this new conversation to the 'datas\permanent_memory.json' file
    if "add in your memory"in user_input or "save in your memory"in user_input :
        user_data = {
        "role": "user",
        "parts": [f"{user_input}"]
        }
        model_data = {
        "role": "model",
        "parts": [f"{model_response}"]
        }
        append_to_json_file(r'datas\permanent_memory.json', user_data)  
        append_to_json_file(r'datas\permanent_memory.json', model_data)  

def play_on_yt(user_input):
    global model_response
    user_input = user_input.lower().replace("play","")
    pywhatkit.playonyt(user_input)
    sleep(1)
    title = r'Nemo: ▶️▶️Video Played ..▶️▶️ '
    app_name= r'😊Nemo😊'
    app_icon=r"Icon.ico"
    notification.notify(title=title,message=f"Video played on youtube on the topic or related {user_input}.",app_name=app_name ,app_icon=app_icon, timeout=10)
    model_response = "Playing sir...."

def tell_time():
    global model_response
        # %I for 12-hour format, %M for minutes, %p for AM/PM
    hour_minute = datetime.datetime.now().strftime("%I:%M %p")
    model_response =  f"Sir, the time is {hour_minute}"
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
    global model_response
    # Extract the time from the user input
    duration_seconds = extract_time(user_input)
    
    if duration_seconds is not None:
        # If valid time is found, set the timer
        set_timer(duration_seconds)
        mgs = f"Timer started for {duration_seconds} seconds."
        model_response = mgs
        
    else:
        # If no valid time is found in the input
        model_response=  ("Sorry, I couldn't understand the time duration.")
#Functions for alarm
def extract_alarm_time(user_input):
    global model_response
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
        model_response = a
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
    global model_response
    # Extract the alarm time from the user input
    alarm_time = extract_alarm_time(user_input)
    
    if alarm_time is not None:
        # If a valid alarm time is found, set the alarm
        set_alarm(alarm_time)
    else:
        model_response = "Sorry, I couldn't understand the alarm time."
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




def get_response(user_input):
    """
    The function sends the input to the generative model, receives the response, 
    and prints it. It also appends the user input and model's response to the chat history.
    """
    if not handle_automation(user_input):
        # If not an automation command, use AI response
        AI_Response(user_input)
    # Append the user input and model response to the chat session history
    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})
    return model_response



if __name__ == "__main__":
    user_input = input("User: ")  # Take input from the user
    get_response(user_input)  # Send input to the AI model and print the response


