import os
import time
from gtts import gTTS
from pydub import AudioSegment
from pygame import mixer

def to_speak(message):
    file = 'audio_temp.mp3'
    audio = gTTS(message,  lang='pt-br', slow=False)
    audio.save(file)
    play_sound(file)

def play_sound(file):
    if os.name == 'posix':
        sound = AudioSegment.from_mp3(file)
        old = file
        file = f'{file.split(".")[0]}.ogg'
        sound.export(file, format='ogg')
        os.remove(old)

    mixer.init()
    mixer.music.load(file)
    mixer.music.play()

    seconds = 0
    while mixer.music.get_busy() == 1:
        time.sleep(0.5)
        seconds += 0.5

    mixer.quit()
    os.remove(file)
