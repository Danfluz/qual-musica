import os.path
import pathlib
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import yt_dlp
from youtube_search import YoutubeSearch
from pydub import AudioSegment
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer as mx
mx.init()



# trecho = 'get on your knees and bow or learn a lesson in violence'
def encontrar_musica(trecho, printi=False):
    resultado = search(trecho, lang='br')
    letras = False
    ouvir = False

    link = 'i'
    for i in resultado:
        if 'letras.mus' in i or 'vagalume.c' in i or 'letras.com' in i:
            link = i
            letras = True
            break
        elif 'ouvirmusica.c' in i or 'azlyrics' in i:
            link = i
            ouvir = True
            break
        else:
            pass
    if link == 'i':
        resultado = search(trecho+" lyrics", lang='br')
        letras = False
        ouvir = False

        link = 'x'
        for i in resultado:
            if 'letras.mus' in i:
                link = i
                letras = True
                break
            elif 'ouvirmusica.c' in i:
                link = i
                ouvir = True
                break
            elif 'vagalume.c' in i:
                link = i
                ouvir = True
                break
            elif 'letras.com' in i:
                link = i
                ouvir = True
                break
            elif 'azlyrics' in i:
                link = i
                ouvir = True
                break
            else:
                pass
    if link == 'x':
        if printi == True:
            print('Não foi possível encontrar a música.')
        return None
    else:
        content = requests.get(link).content
        site = BeautifulSoup(content, 'html.parser')
        titulo = site.find('title').text.split('-')
        if letras == True:
            artista = titulo[1].strip(' ')
            musica = titulo[0].strip(' ')
            musica = musica.title()
        elif ouvir == True:
            artista = titulo[0].strip(' ')
            musica = titulo[1].strip(' ')
            musica = musica.title()

        if '(Tradução)' in musica:
            musica = musica.replace('(Tradução)', '').strip(' ')

        if printi == True:
            print(f'Essa letra faz parte da música {musica}, tocada por {artista}.')

        return (musica, artista)






def pegar_musica(tupla_musica_artista):
    musica = tupla_musica_artista[0]
    artista = tupla_musica_artista[1]
    results = YoutubeSearch(f'{musica} {artista}', max_results=10).to_dict()
    youtubesong = [f"http://www.youtube.com{results[0]['url_suffix']}"]
    duracao_original = results[0]['duration'].replace(':', '.')
    tempoinicio = str(float(duracao_original) / 3.1)
    minutoinicio = int(tempoinicio[0])
    try:
        segundosinicio = int(tempoinicio[2:4])
    except ValueError:
        segundosinicio = int(tempoinicio[3:5])
    segundosfinal = segundosinicio + 30
    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        'quiet':True,
        'no_warnings':True,
        "external_downloader_args": ['-loglevel', 'panic'],
        # i️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        getmus = ydl.download(youtubesong)


    for arquivo in os.listdir(os.getcwd()):
        if arquivo.endswith('.mp3'):
            sound = AudioSegment.from_mp3(arquivo)
            startm = minutoinicio
            endm = minutoinicio
            start_s = segundosinicio
            end_s = segundosfinal

            StrtTime = startm * 60 * 1000 + start_s * 1000
            EndTime = endm * 60 * 1000 + end_s * 1000
            extract = sound[StrtTime:EndTime]
            extract.export('file.mp3', format='mp3')

def tocar_mp3():
    mx.Sound('file.mp3').play(loops=4, fade_ms=2000)

def limpar_mp3():
    for arquivo in os.listdir(os.getcwd()):
        if arquivo.endswith('.mp3') or arquivo.endswith('.webm') or arquivo.endswith('.part'):
            pathlib.Path(arquivo).unlink()


def baixar_img(termos):
    pass

# baixar_img('slayer live undead')
# musica = encontrar_musica(trecho)
mx.stop()