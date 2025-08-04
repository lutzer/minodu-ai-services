# sudo apt-get install pip
# sudo apt-get install -y python3-pyaudio
# sudo pip3 install vosk

import os
import sys
import json
import contextlib
import pyaudio
import io
from vosk import Model, KaldiRecognizer
import argparse

def main():

    parser = argparse.ArgumentParser(description="Speech to Text Transcription")
    parser.add_argument("--language", default="en", help="Conversation language, either en or fr")
    args = parser.parse_args()

    if not(args.language == "en" or args.language == "fr"):
        print("The only available languages are 'en' or 'fr'")
        parser.print_help()
        return

    # Path to the Vosk model
    #model_path = "models/vosk-model-small-pl-0.22/"
    model_path = "models/vosk-model-small-en-us-0.15" if args.language == "en" else "models/vosk-model-small-fr-0.22"
    if not os.path.exists(model_path):
        print(f"Model '{model_path}' was not found. Please check the path.")
        exit(1)

    model = Model(model_path)

    # Settings for PyAudio
    sample_rate = 16000
    chunk_size = 8192
    format = pyaudio.paInt16
    channels = 1

    # Initialization of PyAudio and speech recognition
    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
    recognizer = KaldiRecognizer(model, sample_rate)

    os.system('clear')
    print("\nSpeak now...")

    while True:
        data = stream.read(chunk_size)
        if recognizer.AcceptWaveform(data):
            result_json = json.loads(recognizer.Result())
            text = result_json.get('text', '')
            if text:
                print("\r" + text, end='\n')
        else:
            partial_json = json.loads(recognizer.PartialResult())
            partial = partial_json.get('partial', '')
            sys.stdout.write('\r' + partial)
            sys.stdout.flush()

if __name__ == "__main__":
    main()