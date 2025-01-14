import speech_recognition as sr
sr.Microphone.list_microphone_names()
import pyaudio

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(1)
numdevices = info.get('deviceCount')

for i in range(1, numdevices):
    if (p.get_device_info_by_host_api_device_index(1, i).get('maxInputChannels')) > 1:
        print('Input Device id ', i, ' - ', p.get_device_info_by_host_api_device_index(1, i).get('name'))
import pyttsx3
import pywhatkit
from datetime import datetime
import wikipedia
import pyjokes
import webbrowser

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def open(url):
    webrowser.open(url)
def search(query):
    wikipedia.set_lang('en')
    result=wikipedia.summary(query,sentences=2)
    print(result)    

def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(sr.Microphone().list_microphone_names())
        print('Listening...')
        audio = r.listen(source)

    try:
        print('Recognizing...')
        command = r.recognize_google(audio)
        print(f'You said: {command}')
        return command
    
    except sr.UnknownValueError:
        print('Sorry, I didnt understand that.')
        return ''

def run_keira():

    while True:
        command_1 = main()
        print(command_1)
        if 'stop' in command_1:
            speak('Goodbye!')
            break
        if 'play' in command_1:
            song = command_1.replace('play', '')
            speak('playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command_1:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak('Current time is ' + time)
            print('Current time is', time)
        elif 'date' in command_1:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            speak('Today is ' + date)
            print('Today is', date)
        elif 'where am I' in command_1:
            location = get_location()
            speak('Your current location is latitude ' + str(location[0]) + ' and longitude ' + str(location[1]))
            print('Your current location is latitude', location[0], 'and longitude', location[1])

        elif 'joke' in command_1:
            speak(pyjokes.get_joke())
        else:
            speak('sorry,no results found')
if __name__=='__main__':
    main()

while True:
    run_keira()

