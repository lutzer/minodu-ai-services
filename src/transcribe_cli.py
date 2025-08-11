# sudo apt-get install pip
# sudo apt-get install -y python3-pyaudio
# sudo pip3 install vosk

import argparse
from stt.stt_transcriber import SttTranscriber

def main():
    parser = argparse.ArgumentParser(description="Speech to Text Transcription")
    parser.add_argument('file', nargs='?', default=None, help="Audio file to transcribe, if empty it records from the mic")
    parser.add_argument("--language", default="en", help="Conversation language, either en or fr")
    parser.add_argument('--file', help="Audio file to transcribe")
    args = parser.parse_args()

    if not(args.language == "en" or args.language == "fr"):
        print("The only available languages are 'en' or 'fr'")
        parser.print_help()
        return

    if args.file is None:
        transcriber = SttTranscriber(args.language)
        transcriber.transcribe_mic_stream()
    else:
        transcriber = SttTranscriber(args.language)
        result = transcriber.transcribe_file(args.file)
        print(result)

if __name__ == "__main__":
    main()