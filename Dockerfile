FROM python:3.11-slim AS base

RUN apt-get update -y && apt upgrade -y && apt-get clean -y

RUN apt-get install ffmpeg -y

ENV APP_HOME=/app

WORKDIR $APP_HOME

COPY . ./

RUN pip install -r requirements.txt

RUN (cd models/stt_models && unzip vosk-model-small-fr-0.22.zip && unzip vosk-model-small-en-us-0.15.zip)

CMD python main.py