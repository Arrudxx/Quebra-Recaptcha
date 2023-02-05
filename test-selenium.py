from selenium.webdriver.chrome.service import Service
from selenium import webdriver

import speech_recognition as sr
import av
import os


def To_Way(in_path: str, out_path: str = None, sample_rate: int = 16000) -> str:

    # convert audio to .wav
    # Faz a conversão do audio para .wav
    if out_path is None:
        out_path = os.path.splitext(in_path)[0] + '.wav'

    with av.open(in_path) as in_container:
        in_stream = in_container.streams.audio[0]
        with av.open(out_path, 'w', 'wav') as out_container:
            out_stream = out_container.add_stream(
                'pcm_s16le',
                rate=sample_rate,
                layout='mono'
            )
            for frame in in_container.decode(in_stream):
                for packet in out_stream.encode(frame):
                    out_container.mux(packet)

    return out_path


def speak_mic():

    # if the file exists delete it
    # se o arquivo exisir o apague
    if os.path.exists("audio.mp3"):
        os.remove("audio.mp3")

    mic = sr.Recognizer()

    with sr.AudioFile("audio.wav") as source:
        # Call noise reduction algorithm
        # Chama o agoritmo de reduçã de ruido
        mic.adjust_for_ambient_noise(source)
        # Save what was said in a variable
        # Guavar o que foi dito numa variavel
        audio = mic.listen(source)

    try:
        # pass the variable to the pattern recognition algorithm
        # passa a variavel para o algoritmo reconhecedor de padrões

        # language parameter can be changed
        # o paramentro da linguagem pode ser mudado
        phrase = mic.recognize_google(audio, language='en-US')

        # return phrase
        # retorna frase

        print("Audio: " + phrase)

        return phrase

    except sr.UnknownValueError:
        print("Audio not recognized")


def Resolve_Recaptcha():

    # Pass the MP3 audio path as the first parameter and the audio.wav that will be created as the second parameter
    # Passar o caminho do áudio MP3 como primeiro parâmetro e o audio.wav que será criado como segundo parâmetro
    To_Way(rf"audio.mp3", rf"audio.wav")
    speak_mic()


def Start_Selenium():
    service = Service(executable_path="geckodriver.exe")
    driver = webdriver.Firefox(service=service)

    driver.get("https://patrickhlauke.github.io/recaptcha/")

    input()


Start_Selenium()
