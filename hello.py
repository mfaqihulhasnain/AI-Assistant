import speech_recognition as sr
import pyttsx3
import webbrowser
import musicLibrary
import requests
import os
from datetime import datetime, timedelta
import threading
import time


recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = os.getenv("cc4ae022a50b4c9badcf9675c34d6da3")
openai = " "

def speak(text):
    engine.say(text)
    engine.runAndWait()


# Context Analyzer
def analyze_context(command):
    global context

    # Use previous context to handle follow-ups
    if "what" in command.lower() and "news" in context["last_command"]:
        speak("Would you like me to fetch more news headlines?")
        context["last_command"] = "fetch_more_news"
    elif "yes" in command.lower() and context["last_command"] == "fetch_more_news":
        fetchNews()  # Call fetch news again
        context["last_command"] = "news"
    else:
        # Process the command as usual
        processCommand(command)
        context["last_command"] = command


def tell_joke():
    url = "https://v2.jokeapi.dev/joke/Programming?type=single"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        joke = data.get("joke", "Sorry, I couldn't fetch a joke.")
        speak(joke)
        print(joke)
    except Exception as e:
        print(f"Error fetching joke: {e}")
        speak("Sorry, I couldn't fetch a joke.")
        
def set_alarm_duration(duration):
    """Set an alarm after a specific duration (e.g., 10 minutes, 2 hours)."""
    try:
        duration = duration.lower()
        # Extract duration in minutes or hours
        if "minute" in duration:
            minutes = int(duration.split()[0])
            alarm_time = datetime.now() + timedelta(minutes=minutes)
        elif "hour" in duration:
            hours = int(duration.split()[0])
            alarm_time = datetime.now() + timedelta(hours=hours)
        else:
            speak("Sorry, I couldn't understand the duration.")
            return

        speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}, which is {duration} from now.")
        print(f"Alarm set for {alarm_time}.")

        # Continuously check the current time until the alarm time
        while datetime.now() < alarm_time:
            pass  # Continue to check until it's time for the alarm

        # Alarm Trigger
        speak("Wake up! Your alarm is ringing.")
        print("Alarm ringing!")
    except Exception as e:
        print(f"Error setting alarm: {e}")
        speak("Sorry, I couldn't set the alarm. Please try again.")

        

def set_reminder_duration(reminder_message, duration):
    """Set a reminder after a specific duration (e.g., 10 minutes, 2 hours)."""
    try:
        duration = duration.lower()
        # Extract duration in minutes or hours
        if "minute" in duration:
            minutes = int(duration.split()[0])
            reminder_time = datetime.now() + timedelta(minutes=minutes)
        elif "hour" in duration:
            hours = int(duration.split()[0])
            reminder_time = datetime.now() + timedelta(hours=hours)
        else:
            speak("Sorry, I couldn't understand the duration.")
            return

        speak(f"Reminder set for {duration} from now.")
        print(f"Reminder set for {reminder_time} with message: {reminder_message}.")

        # Continuously check the current time until the reminder time
        while datetime.now() < reminder_time:
            pass  # Continue to check until it's time for the reminder

        # Reminder Trigger
        speak(f"Reminder: {reminder_message}")
        print(f"Reminder: {reminder_message}")
    except Exception as e:
        print(f"Error setting reminder: {e}")
        speak("Sorry, I couldn't set the reminder. Please try again.")



def fetchNews():
    url = "https://newsapi.org/v2/top-headlines"
    params = {"sources": "techcrunch", "apiKey": newsapi}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            speak("Sorry, no news articles found.")
        else:
            speak("Here are the top headlines from TechCrunch.")
            for idx, article in enumerate(articles[:5], start=1):
                title = article.get("title", "No title")
                source = article.get("source", {}).get("name", "Unknown source")
                print(f"{idx}. {title} - {source}")
                speak(f"{idx}. {title} from {source}.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        speak("Sorry, I couldn't fetch the news right now.")

def processCommand(command):
    print(f"Processing command: {command}")
    
    if "open google" in command.lower():
        speak("Opening the google.")
        webbrowser.open("https://www.google.com")
        
    elif "open facebook" in command.lower():
        speak("Opening the facebook.")
        webbrowser.open("https://www.facebook.com")
        
    elif "open linkedin" in command.lower():
        speak("Opening the linkedin.")
        webbrowser.open("https://www.linkedin.com/feed/")
        
    elif "open youtube" in command.lower():
        speak("Opening the youtube.")
        webbrowser.open("https://www.youtube.com/")
        
    elif "open instagram" in command.lower():
        speak("Opening the youtube.")
        webbrowser.open("https://www.instagram.com/")
    
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            speak(f"Playing the song: {song}")
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    
    elif "set alarm" in command.lower():
        speak("How long from now should I set the alarm? Please specify in minutes or hours.")
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        duration = recognizer.recognize_google(audio)
        threading.Thread(target=set_alarm_duration, args=(duration,)).start()
        
    elif "set reminder" in command.lower():
        speak("What is the reminder message?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        reminder_message = recognizer.recognize_google(audio)

        speak("How long from now should I remind you? Please specify in minutes or hours.")
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        duration = recognizer.recognize_google(audio)

        threading.Thread(target=set_reminder_duration, args=(reminder_message, duration)).start()

    
    elif "news" in command.lower():
        fetchNews()
        
    elif "joke" in command.lower():
       tell_joke()
        
    elif "stop" in command.lower():
        speak("Goodbye!")
        exit()
        
    else:
        speak("Sorry, I didn't understand the command.")
  

if __name__ == "__main__":
    speak("Initializing...")
    while True:
        try:
            # Obtain audio from the microphone
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for noise
                print("Listening...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

            print("Recognizing...")
            word = recognizer.recognize_google(audio)
            if word.lower() == "hello":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Active... Listening for command.")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = recognizer.recognize_google(audio)
                
                if command.lower() not in ["", "stop"]:
                    processCommand(command)  # Process the user's command/question
                else:
                    speak("Sorry, I couldn't understand.")
                    
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            # speak("Sorry, I couldn't understand.")
        except sr.RequestError as e:
            print(f"Request error: {e}")
            speak("Sorry, there was a problem with the speech service.")
        except Exception as e:
            print(f"Error: {e}")


