from typing import Dict, List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader
from pathlib import Path
import glob

class DocumentStore:
    def __init__(self, vectorstore, chroma_client):
        self.vectorstore = vectorstore
        self.chroma_client = chroma_client
        self.collection_name = vectorstore._collection_name
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def add_text_documents(self, texts, metadatas=None):
        """Add raw text documents"""
        if isinstance(texts, str):
            texts = [texts]
        
        # Split documents into chunks
        chunks = []
        chunk_metadatas = []
        
        for i, text in enumerate(texts):
            text_chunks = self.text_splitter.split_text(text)
            chunks.extend(text_chunks)
            
            # Create metadata for each chunk
            base_metadata = metadatas[i] if metadatas else {"source": f"doc_{i}"}
            for j, chunk in enumerate(text_chunks):
                chunk_metadata = base_metadata.copy()
                chunk_metadata["chunk_id"] = j
                chunk_metadatas.append(chunk_metadata)
        
        self.vectorstore.add_texts(texts=chunks, metadatas=chunk_metadatas)
        print(f"Added {len(chunks)} chunks from {len(texts)} documents")
    
    def add_file(self, file_path):
        """Add a single file"""
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)
        else:
            raise ValueError("Unsupported file type")
        
        documents = loader.load()
        texts = [doc.page_content for doc in documents]
        metadatas = [{"source": file_path, "page": i} for i in range(len(texts))]
        
        self.add_text_documents(texts, metadatas)
    
    def add_directory(self, directory_path, extension="pdf"):
        """Add all files from a directory"""
        files = glob.glob(f"{directory_path}/*.{extension}")
        for file in files:
            print("Adding file: " + file)
            self.add_file(file)

    def list_documents(self, limit: int = None) -> List[Dict]:
        """List all documents in the vector store with their metadata"""
        collection = self.chroma_client.get_collection(self.collection_name)
        
        # Get all documents
        results = collection.get(
            include=["metadatas", "documents"],
            limit=limit
        )
        
        documents = []
        for i, (doc_id, metadata, content) in enumerate(zip(results['ids'], results['metadatas'], results['documents'])):
            doc_info = {
                'id': doc_id,
                'metadata': metadata,
                'content_preview': content[:200] + "..." if len(content) > 200 else content,
                'content_length': len(content)
            }
            documents.append(doc_info)
        
        return documents
    
    def delete_chunk(self, doc_id: str):
        """Delete a document by its ID"""
        try:
            collection = self.chroma_client.get_collection(self.collection_name)
            collection.delete(ids=[doc_id])
            print(f"Deleted document with ID: {doc_id}")
        except Exception as e:
            print(f"Error deleting document {doc_id}: {e}")
    
    def delete_document(self, document_name: str):
        """Delete all documents from a specific source"""
        try:
            collection = self.chroma_client.get_collection(self.collection_name)
            
            # First, get all documents with this source
            results = collection.get(
                where={"source": document_name},
                include=["metadatas"]
            )
            
            if not results['ids']:
                print(f"No documents found with source: {document_name}")
                return 0
            
            # Delete all documents with this source
            collection.delete(where={"source": document_name})
            
            deleted_count = len(results['ids'])
            print(f"Deleted {deleted_count} documents from source: {document_name}")
            return deleted_count
            
        except Exception as e:
            print(f"Error deleting documents from source {document_name}: {e}")
            return 0
