import os
import sys
import json
import contextlib
import io
import wave
import vosk
import json
import pyaudio

class SttTranscriber:
    def __init__(self, language="en"):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        model_path = "models/vosk-model-small-en-us-0.15" if language == "en" else "models/vosk-model-small-fr-0.22"
        model_path = os.path.join(script_dir, model_path)
        if not os.path.exists(model_path):
            print(f"Model '{model_path}' was not found. Please check the path.")
            exit(1)

        vosk.SetLogLevel(-1)

        self.model = vosk.Model(model_path)


    def transcribe_mic_stream(self):
        # Settings for PyAudio
        sample_rate = 16000
        chunk_size = 8192
        format = pyaudio.paInt16
        channels = 1

        # Initialization of PyAudio and speech recognition
        p = pyaudio.PyAudio()
        stream = p.open(format=format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
        recognizer = vosk.KaldiRecognizer(self.model, sample_rate)

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

    def transcribe_file(self, file):
        wf = wave.open(file, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM.")
            sys.exit(1)

        recognizer = vosk.KaldiRecognizer(self.model, wf.getframerate())
        recognizer.SetWords(True)
        recognizer.SetPartialWords(True)

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            recognizer.AcceptWaveform(data)


        result = json.loads(recognizer.FinalResult())
        return result["text"]