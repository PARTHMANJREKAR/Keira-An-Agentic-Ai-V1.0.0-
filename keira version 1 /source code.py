import speech_recognition as sr
import pyttsx3
import pywhatkit
from datetime import datetime
import wikipedia
import pyjokes
import requests
from geopy.geocoders import Nominatim
from nltk.tokenize import word_tokenize
import nltk
import subprocess
import platform

nltk.download('punkt')

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)

WAKE_WORDS = ['hi','hey ','hello','keira','what','when','who']  # You can change or add more wake words here

def speak(text):
    """Convert text to speech and print it."""
    print("Bot:", text)
    engine.say(text)
    engine.runAndWait()

def google_search(query):
    """Open a Google search for the given query using the default web browser."""
    search_url = f"https://www.google.com/search?q={query}"
    try:
        if platform.system() == "Windows":
            subprocess.run(["start", "", search_url], shell=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", search_url])
        else:  # Linux and other Unix-like systems
            subprocess.run(["xdg-open", search_url])
    except Exception as e:
        print(f"Failed to open browser: {e}")

def search_wikipedia(query):
    """Search Wikipedia and return a summary."""
    wikipedia.set_lang('en')
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except Exception as e:
        speak("No results found on Wikipedia.")
        print("Error:", e)


def get_weather(lat, lon):
    """Fetch current weather data for the given coordinates."""
    api_key = '46adbc812440fd50918bfccfd35a42ea'  # Replace with your actual API key
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            city = data['name']
            return f"The current weather in {city} is {weather} with a temperature of {temp}°C."
        else:
            return "Sorry, I couldn't retrieve the weather information."
    except Exception as e:
        print("Weather API error:", e)
        return "An error occurred while fetching the weather data."


def get_location():
    """Get the user's approximate location based on IP address."""
    try:
        response = requests.get("https://ipinfo.io").json()
        latitude, longitude = response['loc'].split(',')
        geolocator = Nominatim(user_agent="bot_geolocator")
        location = geolocator.reverse(f"{latitude}, {longitude}", language='en')
        address = location.raw['address']
        return address.get('city', ''), address.get('state', ''), address.get('country', '')
    except Exception as e:
        print("Location error:", e)
        return None


def recognize_speech():
    """Listen and return the command if a wake word is detected."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

        command = recognizer.recognize_google(audio).lower()
        print("Heard:", command)

        for wake_word in WAKE_WORDS:
            if wake_word in command:
                # Remove only the first occurrence of the wake word
                cleaned_command = command.replace(wake_word, '', 1).strip()
                print("Wake word detected:", wake_word)
                return cleaned_command
        print("Wake word not detected.")
        return ""

    except sr.UnknownValueError:
        print("Speech not understood.")
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return ""
    except sr.WaitTimeoutError:
        print("Listening timed out.")
        return ""
    except OSError as e:
        print(f"Microphone error: {e}")
        return ""


def process_command(command):
    """Process and execute the user's command."""
    command = command.lower()

    if 'stop' in command:
        speak("Goodbye! Have a nice day!")
        return False
    elif 'play' in command:
        song = command.replace('play', '').strip()
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)
    elif 'who are you' in command or 'what is your name' in command:
        speak("Hello! I'm keira, your very own voice assistant. I'm designed to assist you with a variety of tasks, including playing your favorite songs, providing weather updates, telling jokes, and answering your questions. With a friendly voice and a wealth of knowledge, I'm here to make your day easier and more enjoyable. Whether you need information, entertainment, or just a quick chat, I'm always here to help!")
    elif 'time' in command:
        time_now = datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {time_now}")
    elif 'date' in command:
        today = datetime.now().strftime('%A, %B %d, %Y')
        speak(f"Today is {today}")
    elif 'location' in command or 'where am i' in command:
        loc = get_location()
        if loc:
            speak(f"You are in {loc[0]}, {loc[1]}, {loc[2]}")
        else:
            speak("Sorry, I couldn't determine your location.")
    elif 'joke' in command:
        speak(pyjokes.get_joke())
    elif 'search' in command:
        query = command.replace('search', '').strip()
        speak(f"Searching for {query}")
        google_search(query)
    elif 'wikipedia' in command:
        query = command.replace('wikipedia', '').strip()
        search_wikipedia(query)
    elif 'weather' in command:
        loc = get_location()
        if loc:
            city, state, country = loc
            geolocator = Nominatim(user_agent="bot_geolocator")
            location = geolocator.geocode(f"{city}, {state}, {country}")
            if location:
                weather_info = get_weather(location.latitude, location.longitude)
                speak(weather_info)
            else:
                speak("Sorry, I couldn't determine your exact location for weather information.")
        else:
            speak("Sorry, I couldn't determine your location.")
    else:
        speak("Sorry, I didn't understand that.")
    return True


def run_keira():
    speak("Hello, I'm Keira. How may I Help you Today?")
    while True:
        command = recognize_speech()
        print("Recognized command (after wake word):", command)  # debug
        if command:
            if not process_command(command):
                break


# Start the assistant
if __name__ == '__main__':
    run_keira()

