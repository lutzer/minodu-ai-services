import os
import logging
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_chroma import Chroma
import chromadb
from chromadb.config import Settings

# Suppress ChromaDB warnings and telemetry errors
logging.getLogger("chromadb").setLevel(logging.ERROR)
logging.getLogger("chromadb.telemetry").setLevel(logging.CRITICAL)

# Completely suppress ChromaDB logs

class SimpleLangChainRAG:
    def __init__(self):

        self.llm = OllamaLLM(model="llama3.2:1b", temperature=0.1)
        
        # Vector store setup (same as above)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

        dirname = os.path.dirname(__file__)
        self.chroma_client = chromadb.PersistentClient(
            path=os.path.join(dirname, 'database'),
            settings=Settings(anonymized_telemetry=False)
        )
        #self.collection = self.chroma_client.get_or_create_collection(name="documents")

        self.vectorstore = Chroma(
            client=self.chroma_client,
            collection_name="documents",
            embedding_function=self.embeddings
        )
        
        # Simple chain
        self.template = """Answer based only on this context:

{context}

Question: {question}
Answer:"""
        
        self.prompt = ChatPromptTemplate.from_template(self.template)
        
        # Create the chain
        self.chain = (
            {"context": self.vectorstore.as_retriever(), "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def ask(self, question: str, stream: bool = False) -> str:
        if not stream:
            print(self.chain.invoke(question))
        else:
            for chunk in self.chain.stream(question):
                print(chunk, end='', flush=True)
            print()


def main():
    simple_rag = SimpleLangChainRAG()
    simple_rag.ask("What is Python?", stream = True)

if __name__ == "__main__":
    main()
