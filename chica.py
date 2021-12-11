import os
import pathlib
import random
import pytz
import speech_recognition as sr
import wikipedia
import pyjokes
from datetime import datetime, timezone
from speech import to_speak
from nlp.extract import get_response, class_prediction
from pydub import AudioSegment
from pydub.playback import play
from youtube import run_youtube

wikipedia.set_lang("pt")
path = pathlib.Path(__file__).parent.resolve()
IST = pytz.timezone('America/Sao_Paulo')

listener = sr.Recognizer()


def listening():
    with sr.Microphone() as src:
        print('listening...')
        listener.adjust_for_ambient_noise(src)
        voice = listener.listen(src)
        try:
            event = listener.recognize_google(voice, language='pt-BR')
            event = event.lower()
        except:
            event = 'anything_else'

    return event


def voice_chica(tag):
    song = AudioSegment.from_mp3(f'{path}/audios/{tag}.mp3')
    play(song)

def run():
    """
        Método que irá iniciar nossa assistente virtual e o reconhecimento de voz
        nesse momento a voz da chica será o default.
        Quem enjoar da minha voz, pode usar o
        to_speak passando o random.choices(response) no lugar de voice_chica

    """
    event = listening()
    print(f'evento: {event}')

    intents = class_prediction(event)
    response, context, tag = get_response(intents)

    if tag == 'song':
        voice_chica(tag)
        run_youtube(event)
    elif tag == 'hours':
        voice_chica(tag)
        hours_speak = f'{datetime.now(IST).hour} horas e {datetime.now(IST).minute} minutos'
        to_speak(hours_speak)
        voice_chica(f'{tag}2')
    elif tag == 'days':
        voice_chica(tag)
        days_speak = f'{datetime.now(IST).day}'
        to_speak(days_speak)
    elif tag == 'search':
        voice_chica(tag)
        voice_chica(f'{tag}2')
        info = wikipedia.summary(event, 1)
        to_speak(info)
    else:
        voice_chica(tag)

while True:
    run()
