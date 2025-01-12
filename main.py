import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()
    
# def processCommand(c):
#     pass


# if __name__ == "__main__":
#     speak("Initiallizing......")
#     while True:
#         # Listen for the wake word 
#         # Obtain audio from the microphone
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             print("Listening.....")
#             audio = r.listen(source, timeout=2 , phrase_time_limit=1)
            
#         print("Recognizing.....")   
        
#         try:
#             with sr.Microphone() as source:
#                 print("Listening.....")
#                 audio = r.listen(source, timeout=2 )
#             word = r.recognize_google(audio)
#             if word.lower()=="Jarvis":
#                 speak("Yes")
#                 # Listen for command
#                 with sr.Microphone() as source:
#                     print("Active...")
#                     audio = r.listen(source)
#                     command = r.recognize_google(audio)
#         except Exception as e:
#             print("Error;{0}".format(e))