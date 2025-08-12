import os
import json
import wave
import vosk
import json
from pydub import AudioSegment
import tempfile
import io

class SttTranscriber:
    def __init__(self, language="en"):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        model_path = "../../data/stt_models/vosk-model-small-en-us-0.15" if language == "en" else "../../data/stt_models/vosk-model-small-fr-0.22"
        model_path = os.path.join(script_dir, model_path)
        if not os.path.exists(model_path):
            print(f"Model '{model_path}' was not found. Please check the path.")
            exit(1)

        vosk.SetLogLevel(-1)

        self.model = vosk.Model(model_path)


    def transcribe_stream(self):
        print("Not implemented")
        # # Settings for PyAudio
        # sample_rate = 16000
        # chunk_size = 8192
        # format = pyaudio.paInt16
        # channels = 1

        # # Initialization of PyAudio and speech recognition
        # p = pyaudio.PyAudio()
        # stream = p.open(format=format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
        # recognizer = vosk.KaldiRecognizer(self.model, sample_rate)

        # os.system('clear')
        # print("\nSpeak now...")

        # while True:
        #     data = stream.read(chunk_size)
        #     if recognizer.AcceptWaveform(data):
        #         result_json = json.loads(recognizer.Result())
        #         text = result_json.get('text', '')
        #         if text:
        #             print("\r" + text, end='\n')
        #     else:
        #         partial_json = json.loads(recognizer.PartialResult())
        #         partial = partial_json.get('partial', '')
        #         sys.stdout.write('\r' + partial)
        #         sys.stdout.flush()

    def transcribe_raw(self, wav_buffer: io.BytesIO):
        """method to process raw wav data with Vosk"""
        wav_buffer.seek(0)

        with wave.open(wav_buffer, "rb") as wf:
            framerate = wf.getframerate()
        
            recognizer = vosk.KaldiRecognizer(self.model, framerate)
            recognizer.SetWords(True)
            recognizer.SetPartialWords(True)
        
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                recognizer.AcceptWaveform(data)
            
            result = json.loads(recognizer.FinalResult())
            return result["text"]
        

    def transcribe_file(self, file):
        if file.name.lower().endswith(".mp3"):
            audio = AudioSegment.from_mp3(file)
            audio = audio.set_channels(1).set_sample_width(2)

            wav_io = io.BytesIO()
            audio.export(wav_io, format="wav")
            return self.transcribe_raw(wav_io)

        elif file.name.lower().endswith(".wav"):
            audio = AudioSegment.from_wav(file)

            if audio.channels != 1:
                audio = audio.set_channels(1).set_sample_width(2)
                wav_io = io.BytesIO()
                audio.export(wav_io, format="wav")
                return self.transcribe_raw(wav_io)
            else:
                # Already mono — just ensure buffer position is at start
                file.seek(0)
                return self.transcribe_raw(file)

        else:
            raise Exception("Audio file must be WAV or MP3 format.")