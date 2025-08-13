import wave
from piper import PiperVoice
import os
import io

class SpeechGenerator:
    def __init__(self, language="en"):

        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = "../../data/tts_models/en_GB-cori-medium.onnx" if language == "en" else "../../data/tts_models/fr_FR-upmc-medium.onnx"
        model_path = os.path.join(script_dir, model_path)
        self.voice = PiperVoice.load(model_path)

        print(self.voice)

    def samplerate(self) -> int:
        return self.voice.config.sample_rate
    
    def channels(self) -> int:
        return 1
        
    def synthesize(self, text: str):
        for chunk in self.voice.synthesize(text):
            yield chunk.audio_int16_bytes

    def generate_wav(audio_chunks, channels, samplerate, samplewidth=2) -> io.BytesIO:
        """Generate WAV file as BytesIO object"""
        buffer = io.BytesIO()

        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(samplewidth)
            wav_file.setframerate(samplerate)
            wav_file.setnframes(len(audio_chunks))

            for chunk in audio_chunks:
                wav_file.writeframes(chunk)

            wav_file.close()
        
        buffer.seek(0)  # Reset to beginning for reading
        return buffer