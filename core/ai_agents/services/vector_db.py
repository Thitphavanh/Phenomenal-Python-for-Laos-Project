"""
Vector Database Service using ChromaDB
ບໍລິການ Vector Database ໃຊ້ສຳລັບ RAG (Retrieval-Augmented Generation)
"""

import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from django.conf import settings


class VectorDBService:
    """Manage ChromaDB operations for RAG system"""
    
    def __init__(self):
        self.persist_directory = str(getattr(
            settings, 'CHROMA_PERSIST_DIRECTORY', './chroma_db'
        ))
        self.collection_name = getattr(
            settings, 'CHROMA_COLLECTION_NAME', 'python_for_laos_docs'
        )
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Embedding model (lazy loaded)
        self._embedding_model = None
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Python for Laos documentation and course content"}
        )
    
    @property
    def embedding_model(self):
        """Lazy load embedding model"""
        if self._embedding_model is None:
            print("Loading embedding model (this may take a while)...")
            self._embedding_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        return self._embedding_model
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Add documents to vector database"""
        try:
            ids = [doc['id'] for doc in documents]
            texts = [doc['text'] for doc in documents]
            metadatas = [doc.get('metadata', {}) for doc in documents]
            
            embeddings = self.embedding_model.encode(texts).tolist()
            
            self.collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas
            )
            
            return True
        except Exception as e:
            print(f"Error adding documents: {e}")
            return False
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            query_embedding = self.embedding_model.encode([query]).tolist()
            
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            
            formatted_results = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        'text': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else None
                    })
            
            return formatted_results
        except Exception as e:
            print(f"Error searching: {e}")
            return []
    
    def delete_collection(self):
        """Delete the entire collection"""
        try:
            self.client.delete_collection(name=self.collection_name)
            return True
        except Exception as e:
            print(f"Error deleting collection: {e}")
            return False
    
    def get_collection_count(self) -> int:
        """Get number of documents in collection"""
        return self.collection.count()
