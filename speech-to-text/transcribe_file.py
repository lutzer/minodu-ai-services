from vosk import Model, KaldiRecognizer
import argparse
import os
import wave

def main():

    parser = argparse.ArgumentParser(description="Speech to Text Transcription")
    parser.add_argument('file', help="Audio file to transcribe")
    parser.add_argument("--language", default="en", help="Conversation language, either en or fr")
    args = parser.parse_args()

    if not(args.language == "en" or args.language == "fr"):
        print("The only available languages are 'en' or 'fr'")
        parser.print_help()
        return

    wf = wave.open(args.file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)

    # Path to the Vosk model
    #model_path = "models/vosk-model-small-pl-0.22/"
    model_path = "models/vosk-model-small-en-us-0.15" if args.language == "en" else "models/vosk-model-small-fr-0.22"
    if not os.path.exists(model_path):
        print(f"Model '{model_path}' was not found. Please check the path.")
        exit(1)

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, wf.getframerate())
    recognizer.SetWords(True)
    recognizer.SetPartialWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        recognizer.AcceptWaveform(data)

    print(recognizer.FinalResult())

if __name__ == "__main__":
    main()