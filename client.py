import speech_recognition as sr
import pyttsx3
import webbrowser
import musicLibrary
import requests
import tkinter as tk
from tkinter import scrolledtext

# Initialize dependencies
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "cc4ae022a50b4c9badcf9675c34d6da3"

# Context storage
context = {"last_command": None}

# Text-to-Speech function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Fetch News
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
                output_to_gui(f"{idx}. {title} - {source}")
                speak(f"{idx}. {title} from {source}.")
    except requests.exceptions.RequestException as e:
        output_to_gui(f"Error fetching news: {e}")
        speak("Sorry, I couldn't fetch the news right now.")

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

# Command processing
def processCommand(command):
    output_to_gui(f"Processing command: {command}")
    
    if "open google" in command.lower():
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "news" in command.lower():
        fetchNews()
    elif "play" in command.lower():
        song = command.lower().split(" ")[1]
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            speak(f"Playing the song: {song}")
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song." )
    elif "stop" in command.lower() :
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I didn't understand the command.")

# Listening function
def listen():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            output_to_gui("Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

        output_to_gui("Recognizing...")
        command = recognizer.recognize_google(audio)
        analyze_context(command)  # Pass command through context analyzer
    except sr.UnknownValueError:
        output_to_gui("Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        output_to_gui(f"Request error: {e}")
        speak("Sorry, there was a problem with the speech service.")
    except Exception as e:
        output_to_gui(f"Error: {e}")

# Output to GUI
def output_to_gui(message):
    output_box.insert(tk.END, message + "\n")
    output_box.see(tk.END)

# GUI setup
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("500x400")

# Output Box
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), height=20, width=50)
output_box.pack(pady=10)

# Speak Button
speak_button = tk.Button(root, text="Speak", font=("Arial", 14), command=listen)
speak_button.pack(pady=10)

# Start GUI
speak("Voice Assistant Initialized with Context Awareness. Click Speak to give a command.")
output_to_gui("Voice Assistant Initialized. Click Speak to give a command.")
root.mainloop()








# def initializeGUI():
#     root = tk.Tk()
#     root.title("Voice Assistant")
#     root.geometry("400x300")

#     title = tk.Label(root, text="Voice Assistant", font=("Helvetica", 16))
#     title.pack(pady=20)

#     status_label = tk.Label(root, text="Listening...", font=("Helvetica", 12))
#     status_label.pack(pady=10)

#     def startListening():
#         threading.Thread(target=continuousListening, daemon=True).start()

#     start_button = tk.Button(root, text="Start Listening", command=startListening, font=("Helvetica", 14))
#     start_button.pack(pady=10)

#     # Exit button
#     exit_button = tk.Button(root, text="Exit", command=root.destroy, font=("Helvetica", 14))
#     exit_button.pack(pady=10)

#     root.mainloop()

# if __name__ == "__main__":
#     initializeGUI()