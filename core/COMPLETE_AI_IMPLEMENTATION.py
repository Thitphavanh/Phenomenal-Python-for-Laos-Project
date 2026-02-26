"""
🤖 COMPLETE AI AGENTS IMPLEMENTATION
ການ Implement AI Agents ສຳລັບ Python for Laos Platform

ຟາຍນີ້ປະກອບດ້ວຍໂຄ້ດທີ່ສາມາດ copy ໄປໃຊ້ໄດ້ທັນທີ
Copy ແຕ່ລະ section ໄປໃສ່ໃນຟາຍທີ່ກຳນົດໄວ້

Author: Claude AI
Date: January 2026
"""

# ===============================================
# 1. VECTOR DATABASE SERVICE
# File: ai_agents/services/vector_db.py
# ===============================================

vector_db_code = '''
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
        self.persist_directory = getattr(
            settings, 'CHROMA_PERSIST_DIRECTORY', './chroma_db'
        )
        self.collection_name = getattr(
            settings, 'CHROMA_COLLECTION_NAME', 'python_for_laos_docs'
        )
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Python for Laos documentation and course content"}
        )
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """
        Add documents to vector database
        
        Args:
            documents: List of dicts with keys: id, text, metadata
        
        Returns:
            bool: Success status
        """
        try:
            ids = [doc['id'] for doc in documents]
            texts = [doc['text'] for doc in documents]
            metadatas = [doc.get('metadata', {}) for doc in documents]
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(texts).tolist()
            
            # Add to collection
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
        """
        Search for similar documents
        
        Args:
            query: Search query
            n_results: Number of results to return
        
        Returns:
            List of relevant documents with metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query]).tolist()
            
            # Search
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            
            # Format results
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
'''

# ===============================================
# 2. RAG CHATBOT SERVICE
# File: ai_agents/services/chatbot.py
# ===============================================

chatbot_code = '''
"""
RAG Chatbot Service
AI Chatbot ທີ່ໃຊ້ RAG ເພື່ອຕອບຄຳຖາມກ່ຽວກັບ Python ແລະຫຼັກສູດຕ່າງໆ
"""

import os
from typing import List, Dict, Any
from openai import OpenAI
from .vector_db import VectorDBService
from django.conf import settings


class PythonLaosChatbot:
    """RAG-powered chatbot for Python for Laos platform"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('DEFAULT_AI_MODEL', 'gpt-4-turbo-preview')
        self.temperature = float(os.getenv('AI_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.getenv('AI_MAX_TOKENS', '2000'))
        
        # Initialize vector DB
        self.vector_db = VectorDBService()
        
        # System prompt
        self.system_prompt = """ທ່ານເປັນ AI ຜູ້ຊ່ວຍສອນ Python ໃນພາສາລາວ.
        ທ່ານມີຄວາມຮູ້ກ່ຽວກັບ:
        - Python programming language
        - ຫຼັກສູດ Python for Laos
        - Web development ດ້ວຍ Django
        - Machine Learning ພື້ນຖານ
        
        ກະລຸນາຕອບຄຳຖາມເປັນພາສາລາວໃຫ້ງ່າຍຕໍ່ການເຂົ້າໃຈ.
        ຖ້າບໍ່ແນ່ໃຈກ່ຽວກັບຂໍ້ມູນ, ໃຫ້ບອກວ່າບໍ່ແນ່ໃຈແທນທີ່ຈະໃຫ້ຂໍ້ມູນຜິດ."""
    
    def chat(
        self, 
        message: str, 
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Chat with the bot using RAG
        
        Args:
            message: User message
            conversation_history: Previous messages
        
        Returns:
            Dict with response and sources
        """
        # Search for relevant context
        relevant_docs = self.vector_db.search(message, n_results=3)
        
        # Build context from retrieved documents
        context = self._build_context(relevant_docs)
        
        # Build messages
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history[-10:])  # Last 10 messages
        
        # Add context and user message
        user_message_with_context = f"""ບໍລິບົດທີ່ກ່ຽວຂ້ອງ:
{context}

ຄຳຖາມຂອງຜູ້ໃຊ້: {message}"""
        
        messages.append({"role": "user", "content": user_message_with_context})
        
        # Get response from OpenAI
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            answer = response.choices[0].message.content
            
            return {
                'response': answer,
                'sources': [doc['metadata'] for doc in relevant_docs if doc.get('metadata')],
                'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else None
            }
        except Exception as e:
            return {
                'response': f'ຂໍອະໄພ, ມີບັນຫາໃນການປະມວນຜົນ: {str(e)}',
                'sources': [],
                'error': str(e)
            }
    
    def _build_context(self, docs: List[Dict[str, Any]]) -> str:
        """Build context string from retrieved documents"""
        if not docs:
            return "ບໍ່ມີຂໍ້ມູນທີ່ກ່ຽວຂ້ອງ"
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            context_parts.append(f"{i}. {doc['text'][:500]}...")  # Limit to 500 chars
        
        return "\n\n".join(context_parts)
'''

# Print instructions
print("=" * 60)
print("✅ AI AGENTS IMPLEMENTATION CODE GENERATED")
print("=" * 60)
print("\n📝 ຂັ້ນຕອນການ Setup:\n")
print("1. Copy code ຈາກຕົວແປ vector_db_code ໄປໃສ່:")
print("   → ai_agents/services/vector_db.py")
print("\n2. Copy code ຈາກຕົວແປ chatbot_code ໄປໃສ່:")
print("   → ai_agents/services/chatbot.py")
print("\n3. Run: python3 manage.py makemigrations ai_agents")
print("4. Run: python3 manage.py migrate")
print("5. Setup .env file ດ້ວຍ OPENAI_API_KEY")
print("\n" + "=" * 60)

