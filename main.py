import string

import pyttsx3  # converts text to speech
import datetime  # required to resolve any query regarding date and time
import speech_recognition as sr  # required to return a string output by taking microphone input from the user
import wikipedia  # required to resolve any query regarding wikipedia
import webbrowser  # required to open the prompted application in web browser
import os.path  # required to fetch the contents from the specified folder/directory
import smtplib  # required to work with queries regarding e-mail
from search_engines import Google, Bing, Duckduckgo
from utils.sigmoid import stable_sigmoid as sig

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

bot_name = "Cortana"


# TODO: 1. integrate deepvoice so we can create voice 'profiles' with testing data provided from audio files to
#          customize the voice.
#       2. update the learn_something_new to scrape the TOP 3 search results from the engines.
#       3. compare the 9 results to find similarities. Returns an 'answer'.
#       4. function will create the new if/elif statement with exception handler in a 'self-made' file.
#       5. connect 3rd party API for q/a -> alexa, cortana, etc.


def speak(audio):  # function for assistant to speak
    engine.say(audio)
    engine.runAndWait()  # without this command, the assistant won't be audible to us


def wish_me():  # function to wish the user according to the daytime
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak('Good Morning')

    elif 12 < hour < 18:
        speak('Good Afternoon')

    else:
        speak('Good Evening')

    speak("Hello, I am " + bot_name + ", What can I do for you?")


def take_command():  # function to take an audio input from the user
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 2
        audio = r.listen(source)

    try:  # error handling
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-US')  # using google for voice recognition
        print(f'User said: {query}\n')
    except ValueError as v:
        print('Hmm, I will have to learn that...')
        return 'None'

    return query


def send_email(to, content):  # function to send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('senders_eamil@gmail.com', 'senders_password')
    server.sendmail('senders_email@gmail.com', to, content)
    server.close()


def get_sigmoid(number):  # function to send email
    answer = "I am not sure, I will need to ponder this"
    try:
        answer = sig(number)
    except ValueError as v:
        print(v)
        speak(answer)

    speak(answer)


def learn_something_new(question):
    search_browser1 = Google()
    search_browser2 = Bing()
    search_browser3 = Duckduckgo()
    result_of_search_1 = search_browser1.search(question).links().index(0)
    result_of_search_2 = search_browser2.search(question)
    result_of_search_3 = search_browser3.search(question)
    links1 = result_of_search_1.links()
    links2 = result_of_search_2.links()
    links3 = result_of_search_3.links()
    print(links1)
    print(links2)
    print(links3)


if __name__ == '__main__':  # execution control
    wish_me()
    while True:
        query = take_command().lower()  # converts user asked query into lower case

        # The whole logic for execution of tasks based on user asked query

        if 'open youtube' in query:
            webbrowser.open('youtube.com')

        if 'what is your name' in query:
            speak("My name is " + bot_name)

        elif 'wikipedia' in query:
            try:
                speak('Searching Wikipedia....')
                query = query.replace('wikipedia', '')
                results = wikipedia.summary(query, sentences=5)
                print(results)
                speak(results)
            except Exception as e:
                print(e)
                speak('Sorry, something seems to be wrong with my HTML parser')

        elif 'open google' in query:
            webbrowser.open('google.com')

        elif 'very good' in query:
            speak('Thank you')

        elif 'get sigmoid' in query:
            try:
                query = query.find(string.digits)
                results = sig(query)
                print(results)
                speak(results)
            except Exception as e:
                print(e)
                speak('Sorry, I am not sure, I will need to look into this')

        elif 'play music' in query:
            speak('okay boss')
            music_dir = 'music_dir_of_the_user'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'time' in query:
            start_time = datetime.datetime.now().strftime('%H:%M')
            speak(f'Sir the time is {start_time}')

        elif 'pycharm' in query:
            code_path = 'pycharm_directory_of_your_computer'
            os.startfile(code_path)

        elif 'email' in query:
            try:
                speak('what should i write in the email?')
                content = take_command()
                to = 'reciever_email@gmail.com'
                send_email(to, content)
                speak('email has been sent')
            except Exception as e:
                print(e)
                speak('Sorry, I am not able to send this email')

        elif 'exit' in query:
            speak('okay boss, please call me when you need me')
            quit()

        else:
            learn_something_new(query)
