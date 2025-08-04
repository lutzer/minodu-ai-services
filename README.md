# MINODU BOT

## Setup

* install raspberry pi os

  ```
  sudo apt update
  sudo apt upgrade
  ```

* Install olama `curl -fsSL https://ollama.com/install.sh | sh`
* install node js `curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - &&\ sudo apt-get install -y nodejs`

### Install Models

```
ollama pull llama3.2:1b
ollama pull nomic-embed-text  # For embeddings
```

### Setup Chatbot Python Script

* go into *rag* folder and run `python -m venv .venv`
* then `source .venv/bin/activate`to activate it
* `pip install -r requirements.txt`  to install dependencies
* add documents with `python src/rag.py --add-docs ../documents/fr/ --language=fr`

### Setup api

* check [rag-api/README.md](rag-api/README.md)

### setup Speech to text

* go into *tts* folder and run `python -m venv .venv`
* then `source .venv/bin/activate`to activate it
* `apt-get install portaudio`
* `pip install -r requirements.txt`

## Model Benchmark

| Model         | First token time    | Token time | 
| ----          | ----                | ----       | 
| llama3.2:1b   |                     |            |
| gemma2:2b     |                     |            |

## TODO

* try out 
  * Llama 3.2 3B: Often faster inference than Gemma2:2b despite being larger
  * Qwen2.5 1.5B: Excellent context handling, very efficient



