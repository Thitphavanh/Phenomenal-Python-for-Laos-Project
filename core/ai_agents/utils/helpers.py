"""
Helper functions for AI Agents
"""

import tiktoken
import logging
from typing import List, Dict, Any
from textwrap import shorten

logger = logging.getLogger(__name__)

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Count the number of tokens in a string for a specific model.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base used by gpt-4, gpt-3.5-turbo, text-embedding-ada-002
        encoding = tiktoken.get_encoding("cl100k_base")
        
    return len(encoding.encode(text))

def truncate_text(text: str, max_tokens: int, model: str = "gpt-3.5-turbo") -> str:
    """
    Truncate text to a maximum number of tokens.
    """
    if not text:
        return ""
        
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
        
    tokens = encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text
        
    return encoding.decode(tokens[:max_tokens])

def format_docs_for_context(docs: List[Dict[str, Any]]) -> str:
    """
    Format retrieved documents into a context string for the LLM.
    """
    context_parts = []
    
    for i, doc in enumerate(docs, 1):
        content = doc.get('content', '')
        source = doc.get('metadata', {}).get('source', 'Unknown')
        title = doc.get('metadata', {}).get('title', 'Untitled')
        
        context_parts.append(f"Source {i} ({title}):\n{content}\n")
        
    return "\n---\n".join(context_parts)

def clean_ocr_text(text: str) -> str:
    """
    Clean text extracted from OCR.
    """
    if not text:
        return ""
        
    # Remove excessive newlines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

def safe_float(value: Any) -> float:
    """
    Safely convert value to float.
    """
    try:
        if isinstance(value, str):
            # Remove currency symbols and commas
            clean_val = value.replace(',', '').replace('$', '').replace('LAK', '').strip()
            return float(clean_val)
        return float(value)
    except (ValueError, TypeError):
        return 0.0
