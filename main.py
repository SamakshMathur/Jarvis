import speech_recognition as sr
import webbrowser
import pyttsx3
import time

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c): 
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com/")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com/")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://in.linkedin.com/") 
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    
if __name__ == "__main__":
    speak("Initializing jarvis...")

# Flag to control the response
jarvis_activated = False

while True:
    r = sr.Recognizer()      
    print("Recognizing...")
    try:             
        with sr.Microphone() as source:               
            print("Listening")                           
            audio = r.listen(source, timeout=2, phrase_time_limit=1)           
        word = r.recognize_google(audio) # type: ignore
        if word.lower() == "jarvis" and not jarvis_activated:
            speak("Ya")   
            jarvis_activated = True
            with sr.Microphone() as source:
                print("Jarvis active...")                           
                audio = r.listen(source)
                command = r.recognize_google(audio) # type: ignore
                processCommand(command) # type: ignore
                # Reset the flag after processing the command
                jarvis_activated = False
                      
    except Exception as e:
        print("Error; {0}".format(e))
        # Reset the flag in case of an error
        jarvis_activated = False