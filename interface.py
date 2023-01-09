import PySimpleGUI as sg
from idenficador import *

sg.theme('Reddit')
layout = [
    [sg.Text('Musica: ',font='arial 12 bold'), sg.Text('',font='arial 12 bold',key='musicaatual')],
    [sg.Text('Artista: ',font='arial 12 bold'), sg.Text('',font='arial 12 bold',key='artistaatual')],
    [sg.Text('Digite a letra de uma musica: ',size=(45,1)), sg.Button('Parar')],
    [sg.InputText('',key='texto', size=(50,1)), sg.Button('Tocar',font='arial 12 bold',bind_return_key=True)],
]

janela = sg.Window('DescobreMusicas', layout=layout, finalize=True, size=(450,150),icon='music.ico')
musicatemp = None
limpar_mp3()
trecho = None
while True:
    janela.refresh()
    event, value = janela.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'Tocar':
        if len(value['texto']) <2:
            sg.popup('Busca inválida.',icon='music.ico')
            continue
        mx.stop()
        if value['texto'] == trecho:
            mx.init()
            tocar_mp3()
            continue
        trecho = value['texto']
        janela.refresh()
        sg.popup_quick_message('Identificando letra...', auto_close_duration=5, relative_location=(135, 0))
        musica = encontrar_musica(trecho)
        janela.refresh()
        if musica == musicatemp:
            mx.init()
            tocar_mp3()
            continue
        else:
            limpar_mp3()
            musicatemp = musica
            janela['musicaatual'].update(musica[0])
            janela.refresh()
            janela['artistaatual'].update(musica[1])
            janela.refresh()
            sg.popup_quick_message('Carregando música...',auto_close_duration=5,relative_location=(135,0))
            pegar_musica(musica)
            mx.init()
            tocar_mp3()
            janela.refresh()


    if event == 'Parar':
        mx.stop()
limpar_mp3()
janela.close()