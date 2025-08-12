import os
import sys
import json
import wave
import vosk
import json
from pydub import AudioSegment
import tempfile

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

    def mp3_to_wav_stream(mp3_file_path):
        # Load the MP3 file
        audio = AudioSegment.from_mp3(mp3_file_path)
        
        # Create a BytesIO buffer to hold the WAV data
        wav_buffer = io.BytesIO()
        
        # Export as WAV to the buffer
        audio.export(wav_buffer, format="wav")
        
        # Reset buffer position to beginning
        wav_buffer.seek(0)
        
        return wav_buffer

    def transcribe_file(self, file):
        # Check if the file is MP3 and convert it if necessary
        if file.lower().endswith('.mp3'):
            # Load MP3 file
            audio = AudioSegment.from_mp3(file)
            
            # Convert to mono, 16-bit PCM WAV
            audio = audio.set_channels(1)  # Convert to mono
            audio = audio.set_sample_width(2)  # 16-bit
            
            # Create a temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                temp_wav_path = temp_wav.name
                audio.export(temp_wav_path, format='wav')
            
            try:
                # Process the converted WAV file
                return self._process_wav_file(temp_wav_path)
            finally:
                # Clean up the temporary file
                os.unlink(temp_wav_path)
        
        elif file.lower().endswith('.wav'):

            audio = AudioSegment.from_wav(file)

            if (audio.channels != 1):
                # Convert to mono, 16-bit PCM WAV
                audio = audio.set_channels(1)  # Convert to mono
                audio = audio.set_sample_width(2)  # 16-bit
                
                # Create a temporary WAV file
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                    temp_wav_path = temp_wav.name
                    audio.export(temp_wav_path, format='wav')
                
                try:
                    # Process the converted WAV file
                    return self._process_wav_file(temp_wav_path)
                finally:
                    # Clean up the temporary file
                    os.unlink(temp_wav_path)
            else:
                # Process WAV file directly
                return self._process_wav_file(file)
        
        else:
            raise Exception("Audio file must be WAV or MP3 format.")

    def _process_wav_file(self, file):
        """Helper method to process WAV files with Vosk"""
        wf = wave.open(file, "rb")
        
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            wf.close()
            raise Exception("Audio file must be WAV format mono PCM.")
        
        recognizer = vosk.KaldiRecognizer(self.model, wf.getframerate())
        recognizer.SetWords(True)
        recognizer.SetPartialWords(True)
        
        try:
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                recognizer.AcceptWaveform(data)
            
            result = json.loads(recognizer.FinalResult())
            return result["text"]
        
        finally:
            wf.close()