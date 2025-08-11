import argparse
from rag.rag import RAG
from rag.document_store import DocumentStore

def main():
    parser = argparse.ArgumentParser(description="RAG running lama3.2:1b")
    parser.add_argument("--question", help="Ask a single question")

    parser.add_argument("--language", default="en", help="Conversation language, either en or fr")
    parser.add_argument("--history", default="", help="Previous conversation history")
    parser.add_argument("--no-stream", action="store_true", help="Dont stream generated tokens")

    parser.add_argument("--add-doc", help="Add a document to the knowledge base")
    parser.add_argument("--add-dir", help="Add all pdf documents in the specified directory")
    parser.add_argument("--remove-doc", help="Add a document to the knowledge base")
    parser.add_argument("--list-docs", action='store_true', help="Removes document by its filename")
    
    args = parser.parse_args()

    if not(args.language == "en" or args.language == "fr"):
        print("The only available languages are 'en' or 'fr'")
        parser.print_help()
        return

    if args.question:
        rag = RAG(language=args.language)
        response = rag.ask(args.question, args.history, stream=not args.no_stream)
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