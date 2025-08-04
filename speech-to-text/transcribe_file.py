from vosk import Model, KaldiRecognizer
import argparse
import os

def main():

    parser = argparse.ArgumentParser(description="Speech to Text Transcription")
    parser.add_argument('file', help="Audio file to transcribe")
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
    recognizer = KaldiRecognizer(model, 16000)

    with open(args.file, "rb") as audio:
        while True:
            # Read a chunk of the audio file
            data = audio.read(4000)
            if len(data) == 0:
                break
            # Recognize the speech in the chunk
            recognizer.AcceptWaveform(data)

        # Get the final recognized result
        result = recognizer.FinalResult()
        print(result)

if __name__ == "__main__":
    main()