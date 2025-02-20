from flask import Flask, request, jsonify, render_template
import datetime
import webbrowser
import os
import random
import platform
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

app = Flask(__name__)

# Reminders and To-Do List
reminders = []
todo_list = []

# Function to process commands
def process_command(command):
    response = "I didn't understand that. Please try again."

    if 'hello' in command or 'hi' in command:
        response = "Hello! How can I assist you today?"

    elif 'how are you' in command:
        response = "I'm doing great! How can I help you?"

    elif 'time' in command:
        response = datetime.datetime.now().strftime("%I:%M %p")

    elif 'date' in command:
        response = datetime.datetime.now().strftime("%B %d, %Y")

    elif 'open google' in command:
        webbrowser.open("https://www.google.com")
        response = "Opening Google."

    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube."

    elif 'search google' in command:
        query = command.replace("search google", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            response = f"Searching Google for {query}."
        else:
            response = "What should I search for?"

    elif 'increase volume' in command:
        set_volume("increase")
        response = "Increasing volume."

    elif 'decrease volume' in command:
        set_volume("decrease")
        response = "Decreasing volume."

    elif 'mute' in command:
        set_volume("mute")
        response = "Volume muted."

    elif 'unmute' in command:
        set_volume("unmute")
        response = "Volume unmuted."

    elif 'increase brightness' in command:
        set_brightness("increase")
        response = "Increasing brightness."

    elif 'decrease brightness' in command:
        set_brightness("decrease")
        response = "Decreasing brightness."

    elif 'open' in command:
        app_name = command.replace("open ", "").strip()
        open_application(app_name)
        response = f"Opening {app_name}."

    elif 'lock' in command:
        system_control("lock")
        response = "Locking the system."

    elif 'sleep' in command:
        system_control("sleep")
        response = "Putting the system to sleep."

    elif 'log off' in command:
        system_control("log off")
        response = "Logging off the system."

    elif 'exit' in command or 'bye' in command:
        response = "Goodbye! Have a great day!"

    # New Commands
    elif 'set reminder' in command:
        try:
            parts = command.split("for")
            reminder_text = parts[0].replace("set reminder", "").strip()
            time = parts[1].strip()
            reminders.append((reminder_text, time))
            response = f"Reminder set for {time}: {reminder_text}"
        except:
            response = "Please specify the reminder text and time. Example: 'Set reminder for 3 PM to take a break.'"

    elif 'tell me a joke' in command or 'joke' in command:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
        ]
        response = random.choice(jokes)

    elif 'play a game' in command or 'number game' in command:
        response = "I'm thinking of a number between 1 and 10. Can you guess it?"

    elif 'system info' in command or 'system information' in command:
        system = platform.system()
        node = platform.node()
        release = platform.release()
        response = f"System: {system}, Node: {node}, Release: {release}"

    elif 'add task' in command:
        task = command.replace("add task", "").strip()
        if task:
            todo_list.append(task)
            response = f"Task added: {task}"
        else:
            response = "Please specify a task to add."

    elif 'view tasks' in command:
        if todo_list:
            response = "Your to-do list: " + ", ".join(todo_list)
        else:
            response = "Your to-do list is empty."

    elif 'delete task' in command:
        task = command.replace("delete task", "").strip()
        if task in todo_list:
            todo_list.remove(task)
            response = f"Task deleted: {task}"
        else:
            response = f"Task '{task}' not found."

    elif 'flip a coin' in command:
        response = random.choice(["Heads", "Tails"])

    elif 'roll a dice' in command:
        response = f"You rolled a {random.randint(1, 6)}"

    elif 'calculate' in command:
        expression = command.replace("calculate", "").strip()
        try:
            result = eval(expression)
            response = f"The result is {result}"
        except:
            response = "Invalid expression. Example: 'calculate 2 + 2'"

    elif 'shutdown' in command:
        os.system("shutdown /s /t 1")
        response = "Shutting down the system."

    elif 'restart' in command:
        os.system("shutdown /r /t 1")
        response = "Restarting the system."

    elif 'tell me a fact' in command or 'fact' in command:
        facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!",
            "Octopuses have three hearts. Two pump blood to the gills, and one pumps it to the rest of the body.",
        ]
        response = random.choice(facts)

    return response

# Function to control system volume
def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        if level == "mute":
            volume.SetMute(1, None)
        elif level == "unmute":
            volume.SetMute(0, None)
        elif level == "increase":
            current_vol = volume.GetMasterVolumeLevelScalar()
            volume.SetMasterVolumeLevelScalar(min(current_vol + 0.1, 1.0), None)
        elif level == "decrease":
            current_vol = volume.GetMasterVolumeLevelScalar()
            volume.SetMasterVolumeLevelScalar(max(current_vol - 0.1, 0.0), None)
    except Exception as e:
        print(f"Volume control error: {e}")

# Function to control screen brightness
def set_brightness(level):
    try:
        if level == "increase":
            sbc.set_brightness(min(sbc.get_brightness()[0] + 10, 100))
        elif level == "decrease":
            sbc.set_brightness(max(sbc.get_brightness()[0] - 10, 0))
    except Exception as e:
        print(f"Brightness control error: {e}")

# Function to open applications
def open_application(app_name):
    apps = {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
    }
    if app_name in apps:
        os.startfile(apps[app_name])

# Function to lock, sleep, log off system
def system_control(action):
    if action == "lock":
        os.system("rundll32.exe user32.dll,LockWorkStation")
    elif action == "sleep":
        os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
    elif action == "log off":
        os.system("shutdown -l")

# Flask route for the home page
@app.route("/")
def home():
    return render_template("index.html")

# Flask route to handle commands
@app.route("/command", methods=["POST"])
def command():
    data = request.json
    command = data.get("command", "").lower()
    response = process_command(command)
    return jsonify({"response": response})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)