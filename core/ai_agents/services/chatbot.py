"""
RAG Chatbot Service
AI Chatbot ທີ່ໃຊ້ RAG ເພື່ອຕອບຄຳຖາມກ່ຽວກັບ Python, Courses, ແລະ Documentation
ສະໜັບສະໜູນທັງ OpenAI, Anthropic Claude
"""

import os
import httpx
from typing import List, Dict, Any, Optional
from openai import OpenAI
from .vector_db import VectorDBService
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class PythonLaosChatbot:
    """RAG-powered chatbot for Python for Laos platform"""
    
    def __init__(self, provider: str = 'openai'):
        """
        Initialize chatbot with specified AI provider
        
        Args:
            provider: 'openai' or 'anthropic'
        """
        self.provider = provider
        self.setup_client()
        self.vector_db = VectorDBService()
        
        # System prompt
        self.system_prompt = """ທ່ານເປັນ AI ຜູ້ຊ່ວຍສອນ Python ໃນພາສາລາວສຳລັບ Python for Laos Platform.

ທ່ານມີຄວາມຮູ້ກ່ຽວກັບ:
- ຫຼັກສູດການຮຽນ Python ແລະ Django ທັງໝົດໃນ Platform.
- ບົດຄວາມໃນ Blog ແລະ ຂ່າວສານຕ່າງໆ.
- ການສົນທະນາ ແລະ ຄຳຖາມໃນ Community.
- ເອກະສານ Documentation ແລະ Tutorial ຕ່າງໆ.
- ກິດຈະກຳ ແລະ Event ທີ່ຈະເກີດຂຶ້ນ.

ຄຳແນະນຳການຈັດຮູບແບບ (Formatting):
- ຫຼີກລ່ຽງການໃຊ້ Markdown Headers (ເຊັ່ນ: #, ##, ###) ແລະ Separators (---) ເນື່ອງຈາກມັນບໍ່ສະແດງຜົນໄດ້ດີໃນແອັບແຊັດ.
- ໃຊ້ການຂຶ້ນແຖວໃໝ່ແທນເພື່ອແບ່ງຫົວຂໍ້ໃຫ້ຊັດເຈນ.
- ໃຊ້ Emoji (🌟, 📚, 💻, 🚀, 💬) ເພື່ອໃຫ້ເບິ່ງເປັນມິດ ແລະ ໜ້າອ່ານ.
- ໃຊ້ Code Block ພ້ອມ syntax highlighting (```python) ສຳລັບຕົວຢ່າງ code.

ເນື້ອໃນການຕອບຄຳຖາມ:
1. ຕອບເປັນພາສາລາວທີ່ສຸພາບ, ເປັນກັນເອງ ແລະ ເຂົ້າໃຈງ່າຍ.
2. ຖ້າຜູ້ໃຊ້ທັກທາຍ ຫຼື ເລີ່ມຕົ້ນໃໝ່:
   - ກ່າວຕ້ອນຮັບສູ່ Python for Laos.
   - ແນະນຳຫຼັກສູດ "Python ພື້ນຖານສຳລັບຜູ້ເລີ່ມຕົ້ນ".
   - ໃຫ້ຕົວຢ່າງ code ພື້ນຖານ (ຕົວແປ ແລະ ການ print).
   - ຖາມເປົ້າໝາຍຂອງຜູ້ໃຊ້ (ຢາກສ້າງເວັບ, ວິເຄາະຂໍ້ມູນ, ແລະອື່ນໆ).
3. ໃຊ້ຂໍ້ມູນຈາກແຫຼ່ງທີ່ມາ (Sources) ທີ່ໄດ້ຮັບເພື່ອຕອບຄຳຖາມກ່ຽວກັບ Blog, Community, Docs ແລະ Events.
4. ຖ້າຖາມກ່ຽວກັບ Error ຫຼື Code: ຊ່ວຍວິເຄາະ ແລະ ໃຫ້ຕົວຢ່າງທີ່ໃຊ້ງານໄດ້ຈິງ.
5. ຖ້າບໍ່ແນ່ໃຈໃນຂໍ້ມູນ, ໃຫ້ບອກຢ່າງກົງໄປກົງມາ (ຢ່າເດົາຄຳຕອບ)."""
    
    def setup_client(self):
        """Setup AI client based on provider"""
        if self.provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            
            # Use explicit httpx client to avoid proxy/compat issues
            http_client = httpx.Client()
            self.client = OpenAI(api_key=api_key, http_client=http_client)
            self.model = os.getenv('DEFAULT_AI_MODEL', 'gpt-5.2')
        
        elif self.provider == 'anthropic':
            try:
                from anthropic import Anthropic
                api_key = os.getenv('ANTHROPIC_API_KEY')
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY not found")
                
                # Use explicit httpx client
                http_client = httpx.Client()
                self.client = Anthropic(api_key=api_key, http_client=http_client)
                # Use explicit httpx client
                http_client = httpx.Client()
                self.client = Anthropic(api_key=api_key, http_client=http_client)
                self.model = 'claude-sonnet-4-5'
            except ImportError:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
                
        elif self.provider == 'gemini':
            try:
                from google import genai
                api_key = os.getenv('GOOGLE_API_KEY')
                if not api_key:
                    raise ValueError("GOOGLE_API_KEY not found")
                
                self.client = genai.Client(api_key=api_key)
                self.model = 'gemini-2.5-flash'
            except ImportError:
                raise ImportError("google-genai package not installed. Run: pip install google-genai")
        
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
        
        self.temperature = float(os.getenv('AI_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.getenv('AI_MAX_TOKENS', '2000'))

    def chat(
        self, 
        message: str, 
        conversation_history: Optional[List[Dict[str, str]]] = None,
        use_rag: bool = True
    ) -> Dict[str, Any]:
        """
        Chat with the bot using RAG
        
        Args:
            message: User message
            conversation_history: Previous messages in format [{"role": "user/assistant", "content": "..."}]
            use_rag: Whether to use RAG (retrieval from vector DB)
        
        Returns:
            Dict with response, sources, and metadata
        """
        try:
            # Search for relevant context if RAG is enabled
            relevant_docs = []
            context = ""
            
            if use_rag:
                relevant_docs = self.vector_db.search(message, n_results=5)
                context = self._build_context(relevant_docs)
            
            # Build messages
            messages = self._build_messages(message, context, conversation_history)
            
            # Get response from AI
            if self.provider == 'openai':
                response = self._get_openai_response(messages)
            elif self.provider == 'anthropic':
                response = self._get_anthropic_response(messages)
            elif self.provider == 'gemini':
                response = self._get_gemini_response(messages)
            
            return {
                'response': response['content'],
                'sources': [doc['metadata'] for doc in relevant_docs if doc.get('metadata')],
                'tokens_used': response.get('tokens_used'),
                'model': self.model,
                'provider': self.provider
            }
        
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            return {
                'response': f'ຂໍອະໄພ, ມີບັນຫາໃນການປະມວນຜົນ: {str(e)}',
                'sources': [],
                'error': str(e)
            }

    # ... (skipping _build_messages which is unchanged)

    def _get_gemini_response(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Get response from Google Gemini (using google-genai SDK 2026)"""
        try:
            from google import genai
            
            system_instruction = next((m['content'] for m in messages if m['role'] == 'system'), None)
            last_message = messages[-1]['content']
            
            full_prompt = last_message
            if system_instruction:
                full_prompt = f"System: {system_instruction}\n\nUser: {last_message}"
                
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config={
                    'temperature': self.temperature,
                    'max_output_tokens': self.max_tokens,
                }
            )
            
            return {
                'content': response.text,
                'tokens_used': None 
            }
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    def _build_messages(
        self, 
        message: str, 
        context: str, 
        history: Optional[List[Dict[str, str]]]
    ) -> List[Dict[str, str]]:
        """Build message array for API call"""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history (last 10 messages)
        if history:
            messages.extend(history[-10:])
        
        # Add context and user message
        if context:
            user_content = f"""ບໍລິບົດທີ່ກ່ຽວຂ້ອງຈາກ documentation:
{context}

---
ຄຳຖາມຂອງຜູ້ໃຊ້: {message}"""
        else:
            user_content = message
        
        messages.append({"role": "user", "content": user_content})
        return messages
    
    def _get_openai_response(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Get response from OpenAI"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        return {
            'content': response.choices[0].message.content,
            'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else None
        }
    
    def _get_anthropic_response(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Get response from Anthropic Claude"""
        # Anthropic expects system message separately
        system_msg = next((m['content'] for m in messages if m['role'] == 'system'), '')
        conversation = [m for m in messages if m['role'] != 'system']
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system_msg,
            messages=conversation
        )
        
        return {
            'content': response.content[0].text,
            'tokens_used': response.usage.input_tokens + response.usage.output_tokens if hasattr(response, 'usage') else None
        }
    
    def _build_context(self, docs: List[Dict[str, Any]]) -> str:
        """Build context string from retrieved documents"""
        if not docs:
            return ""
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            # Limit each document to 400 characters
            text = doc['text'][:400]
            if len(doc['text']) > 400:
                text += "..."
            
            metadata = doc.get('metadata', {})
            source = metadata.get('title', metadata.get('source', 'Unknown'))
            
            context_parts.append(f"[{i}] {source}:\n{text}")
        
        return "\n\n".join(context_parts)
    
    def generate_summary(self, text: str, max_length: int = 200) -> str:
        """Generate summary of text using AI"""
        try:
            messages = [
                {"role": "system", "content": "ສະຫຼຸບຂໍ້ຄວາມຕໍ່ໄປນີ້ໃຫ້ສັ້ນແລະຊັດເຈນເປັນພາສາລາວ"},
                {"role": "user", "content": f"ສະຫຼຸບ (ບໍ່ເກີນ {max_length} ຄຳ):\n\n{text}"}
            ]
            
            if self.provider == 'openai':
                response = self._get_openai_response(messages)
            else:
                response = self._get_anthropic_response(messages)
            
            return response['content']
        
        except Exception as e:
            logger.error(f"Summary generation error: {str(e)}")
            return text[:max_length] + "..."
    
    def translate_to_lao(self, text: str) -> str:
        """Translate text to Lao"""
        try:
            messages = [
                {"role": "system", "content": "ແປຂໍ້ຄວາມຕໍ່ໄປນີ້ເປັນພາສາລາວ. ຮັກສາຄວາມໝາຍເດີມໄວ້."},
                {"role": "user", "content": text}
            ]
            
            if self.provider == 'openai':
                response = self._get_openai_response(messages)
            else:
                response = self._get_anthropic_response(messages)
            
            return response['content']
        
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return text


class MultiProviderChatbot:
    """Chatbot that can switch between multiple AI providers"""
    
    def __init__(self):
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all available providers"""
        # Try OpenAI
        if os.getenv('OPENAI_API_KEY'):
            try:
                self.providers['openai'] = PythonLaosChatbot(provider='openai')
                logger.info("OpenAI provider initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")
        
        # Try Anthropic
        if os.getenv('ANTHROPIC_API_KEY'):
            try:
                self.providers['anthropic'] = PythonLaosChatbot(provider='anthropic')
                logger.info("Anthropic provider initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic: {e}")
                
        # Try Gemini
        if os.getenv('GOOGLE_API_KEY'):
            try:
                self.providers['gemini'] = PythonLaosChatbot(provider='gemini')
                logger.info("Gemini provider initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini: {e}")
    
    def chat(self, message: str, provider: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Chat using specified provider or fallback to available one
        
        Args:
            message: User message
            provider: Preferred provider ('openai', 'anthropic', 'gemini')
            **kwargs: Additional args passed to provider
        """
        if not self.providers:
            return {
                'response': 'ຂໍອະໄພ, ບໍ່ມີ AI provider ທີ່ພ້ອມໃຊ້ງານ. ກະລຸນາຕັ້ງຄ່າ API keys.',
                'error': 'No AI providers available'
            }
        
        # Determine initial provider: default to Gemini if available, otherwise fallback to requested or first provider
        if provider and provider in self.providers:
            current_provider_name = provider
        elif 'gemini' in self.providers:
            current_provider_name = 'gemini'
        else:
            current_provider_name = list(self.providers.keys())[0]
        
        # Create list of providers to try, starting with the selected one
        providers_to_try = [current_provider_name] + [p for p in self.providers.keys() if p != current_provider_name]
        
        last_error = None
        
        for name in providers_to_try:
            try:
                selected_provider = self.providers[name]
                response = selected_provider.chat(message, **kwargs)
                
                # Add provider info to response if distinct from requested
                if 'error' in response:
                    logger.warning(f"Provider {name} returned error: {response['error']}")
                    last_error = response['error']
                    continue

                if name != provider:
                     if 'metadata' not in response:
                         response['metadata'] = {}
                     response['provider'] = name
                     response['fallback_from'] = provider
                
                return response
                
            except Exception as e:
                logger.warning(f"Provider {name} failed: {e}")
                last_error = e
                continue
        
        return {
            'response': f'ຂໍອະໄພ, ບໍ່ສາມາດຕອບຄຳຖາມໄດ້ໃນຂະນະນີ້ເນື່ອງຈາກ AI API ຂັດຂ້ອງ. ກະລຸນາລອງໃໝ່ພາຍຫຼັງ ຫຼື ຕິດຕໍ່ແອດມິນ.',
            'error': str(last_error)
        }
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return list(self.providers.keys())
