import os
import sys
import logging
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_chroma import Chroma
from typing import Iterator
import textwrap
from dataclasses import dataclass, asdict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class WeatherLLM:

    @dataclass
    class SensorData:
        temperature: float
        humidity: float

    def __init__(self, language="en"):

        self.language = 0 if language == "en" else 1

        ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434/")

        self.llm = OllamaLLM(base_url=ollama_host, model="llama3.2:1b", temperature=0.1, keep_alive=600 )
        
        # Simple chain
        if language == "en":
            self.template = textwrap.dedent("""
                You are a weather assistant, please create a text that summarizes the weather from the 
                following sensor values:

                Temperature: {temperature} degree Celsius
                Humidity: {humidity} %
            """)
        else:
            self.template = textwrap.dedent("""
                You are a weather assistant, please create a text that summarizes the weather from the 
                following sensor values:

                Temperature: {temperature} degree Celsius
                Humidity: {humidity} %             
            """)
        
        self.prompt = ChatPromptTemplate.from_template(self.template)
        
        # Create the chain
        self.chain = (
            RunnableParallel({
                "temperature": lambda x: x["temperature"], 
                "humidity": lambda x: x["humidity"]
            })
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def ask(self, sensorData : SensorData) -> str:
        return self.chain.invoke(asdict(sensorData))
    
    def ask_streaming(self, sensorData : SensorData) -> Iterator[str]:
        for chunk in self.chain.stream(asdict(sensorData)):
            yield chunk

