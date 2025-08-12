# MINODU BOT

## Setup

* install raspberry pi os

  ```
  sudo apt update
  sudo apt upgrade
  ```

* Install olama `curl -fsSL https://ollama.com/install.sh | sh`
* install node js `curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - &&\ sudo apt-get install -y  nodejs`
* install ffmpeg: `sudo apt-get install ffmpeg`
### Install Models

* install ollama models
  ```
  ollama pull llama3.2:1b
  ollama pull nomic-embed-text  # For embeddings
  ```
* unzip vosk models with `cd data/stt_models &&unzip *.zip`

### Setup Service API

* install pyenv
* run `pyenv install 3.11` and set global with `pyenv global 3.11`
* create venv with `python -m venv .venv`
* then `source .venv/bin/activate`to activate it
* `pip install -r requirements.txt`  to install dependencies

### Add Documents to chatbot

* add documents with `python src/rag.py --add-docs data/documents/fr/ --language=fr`
* add documents with `python src/rag.py --add-docs data/documents/en/ --language=en`




