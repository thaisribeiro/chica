
import os
import re
import pathlib
import urllib.request
import moviepy.editor as MP
import pywhatkit
from pytube import YouTube
from speech import play_sound

path = pathlib.Path(__file__).parent.resolve()

def search_video(search):
    if search.startswith("https://www.youtube.com"):
        res = urllib.request.urlopen(search)
        
        if res.getcode() == 200:
            return search
    
    search_url = f'https://www.youtube.com/results?search_query={search.replace(" ", "+")}'
    try:
        html = urllib.request.urlopen(search_url)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = ("https://www.youtube.com/watch?v=" + video_ids[0])
    except:
        url = search_url
    return url

def run_download(search):
    """
        Faz download da música e converte para mp3
    """
    url = search_video(search)
    YouTube(url).streams.filter(file_extension='mp4').first().download(f'{path}/downloads')
    convert_video_audio()
    
def run_youtube(search):
    """
        Abre o Youtube
    """
    url = search_video(search)
    pywhatkit.playonyt(url)
    
def convert_video_audio():
    for file in os.listdir(f'{path}/downloads'):
        if re.search('mp4', file):
            video_path = os.path.join(f'{path}/downloads', file)
            audio_path = os.path.join(f'{path}/downloads', os.path.splitext(file)[0] + "." + 'mp3')
            newfile = MP.AudioFileClip(video_path)
            newfile.write_audiofile(audio_path)
            os.remove(video_path)
            play_sound(f'{path}/downloads/{file[:-4]}.mp3')