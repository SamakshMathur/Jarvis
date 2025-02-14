import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import musicLibrary  # Ensure this module exists and has the 'songs' dictionary

# Initialize speech engine
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300  # Adjust based on noise level
engine = pyttsx3.init()

# API Key for NewsAPI
API_KEY = "5afedd6441a64a2599fa39d045617773"

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def processCommand(c): 
    """Processes the user's voice command."""
    c = c.lower()

    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://www.google.com/")
    elif "open facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com/")
    elif "open instagram" in c:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com/")
    elif "open linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com/feed/") 
    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com/")
    elif c.startswith("play"):
        words = c.split(" ")
        if len(words) > 1:
            song = words[1]
            if song in musicLibrary.songs:
                speak(f"Playing {song}")
                webbrowser.open(musicLibrary.songs[song])
            else:
                speak("Sorry, I couldn't find that song.")
        else:
            speak("Please specify a song to play.")
    elif "news" in c:
        speak("Fetching the latest news...")
        fetch_news()
        speak("Do you need anything else?")
    else:
        speak("I didn't understand that. Please try again.")

def fetch_news():
    """Fetches and reads top news headlines from NewsAPI."""
    URL = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us",  # Change to "in" for India
        "apiKey": API_KEY
    }

    try:
        response = requests.get(URL, params=params)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])

            if articles:
                speak("Here are the top news headlines.")
                for article in articles[:5]:  # Read only top 5 news
                    title = article.get("title", "No title available")
                    if title:  # Only read if there's a valid title
                        speak(title)
            else:
                speak("Sorry, I couldn't find any news articles.")
        else:
            speak(f"Failed to fetch news. API responded with status code {response.status_code}.")
    except Exception as e:
        speak("Error fetching news. Please check your internet connection.")
        print(f"Error: {e}")

def listen_for_command(retries=1):
    """Listens for a command and returns the recognized text."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # type: ignore # Adapts to background noise
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            command = recognizer.recognize_google(audio).lower() # type: ignore
            return command
        except sr.UnknownValueError:
            if retries > 0:
                speak("I didn't catch that, please repeat.")
                return listen_for_command(retries - 1)
            else:
                return None
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

if __name__ == "__main__":
    speak("Jarvis is now online.")

    while True:
        print("Say 'Jarvis' to activate...")
        
        wake_word = listen_for_command()
        if wake_word and "jarvis" in wake_word:
            speak("Yes boss, I'm listening.")

            while True:  # Keep listening after completing a task
                command = listen_for_command()
                
                if command:
                    processCommand(command)
                else:
                    speak("I didn't catch that. Please repeat.")
