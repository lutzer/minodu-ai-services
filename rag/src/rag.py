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
import argparse

from document_store import DocumentStore

# Suppress ChromaDB warnings and telemetry errors
logging.getLogger("chromadb").setLevel(logging.ERROR)
logging.getLogger("chromadb.telemetry").setLevel(logging.CRITICAL)

class RAG:
    def __init__(self, language="en"):

        self.language = 0 if language == "en" else 1

        self.llm = OllamaLLM(model="llama3.2:1b", temperature=0.1)
        
        # Vector store setup (same as above)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

        dirname = os.path.dirname(__file__)
        self.chroma_client = chromadb.PersistentClient(
            path=os.path.join(dirname, '../database'),
            settings=Settings(anonymized_telemetry=False)
        )

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
        result = ""
        if not stream:
            result = self.chain.invoke(question)
        else:
            for chunk in self.chain.stream(question):
                result += chunk
                print(chunk, end='', flush=True)
            print()
        return result


def main():
    parser = argparse.ArgumentParser(description="RAG running lama3.2:1b")
    parser.add_argument("--language", default="en", help="Conversation language, either en or fr")
    parser.add_argument("--question", help="Ask a single question")
    parser.add_argument("--conversation", default="", help="Previous conversation")

    parser.add_argument("--add-doc", help="Add a document to the knowledge base")
    parser.add_argument("--add-dir", help="Add all pdf documents in the specified directory")
    parser.add_argument("--remove-doc", help="Add a document to the knowledge base")
    parser.add_argument("--list-docs", action='store_true', help="Removes document by its filename")
    
    parser.add_argument("--no-stream", action="store_true", help="Dont stream generated tokens")

    args = parser.parse_args()

    if not(args.language == "en" or args.language == "fr"):
        print("The only available languages are 'en' or 'fr'")
        parser.print_help()
        return

    if args.question:
        rag = RAG(language=args.language)
        response = rag.ask(args.question, stream=not args.no_stream)
        if args.no_stream and response is not None:
            print(f"{response}")
    elif args.add_doc:
        rag = RAG(language=args.language)
        store = DocumentStore(rag.vectorstore, rag.chroma_client)
        store.add_file(args.add_doc)
    elif args.add_dir:
        rag = RAG(language=args.language)
        store = DocumentStore(rag.vectorstore, rag.chroma_client)
        store.add_directory(args.add_dir)
    elif args.list_docs:
        rag = RAG(language=args.language)
        store = DocumentStore(rag.vectorstore, rag.chroma_client)
        documents = store.list_documents()
        print("LIST OF DOCUMENTS:")
        print("--- id, file, page:chunk ---")
        for doc in documents:
            print(doc['id'] + "\t" + doc["metadata"]["source"] + "\t" + str(doc["metadata"]["page"]) + ":" + str(doc["metadata"]["chunk_id"]) )
    elif args.remove_doc:
        rag = RAG(language=args.language)
        store = DocumentStore(rag.vectorstore, rag.chroma_client)
        store.delete_document(args.remove_doc)


    else:
        parser.print_help()
    

if __name__ == "__main__":
    main()
