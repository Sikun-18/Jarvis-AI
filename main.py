import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Setting up the voice (female voice in this case)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 for female

# Setting up the speaking rate
rate = engine.getProperty('rate')
print(f"Current speaking rate: {rate}")
engine.setProperty('rate', 190)  # Set new speaking rate

newsapi = "f9c6260a90ad42c88a11b344c1e2bab4"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    elif "tell me the news" in c:
        r = requests.get(f"https://newsapi.org/v2/everything?q=apple&from=2024-08-20&to=2024-08-20&sortBy=popularity&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
        else:
            speak("Sorry, I couldn't fetch the news at the moment.")
    else:
        speak("I'm sorry, I didn't understand that command.")

if __name__ == "__main__":
    speak("Initializing Jarvis..")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=3)
            
            word = recognizer.recognize_google(audio).lower()
            if word == "jarvis":
                speak("Yes?")
                
                with sr.Microphone() as source:
                    print("Jarvis Active..")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
                    
        except sr.UnknownValueError:
            print("Sorry, I did not catch that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error: {e}")
