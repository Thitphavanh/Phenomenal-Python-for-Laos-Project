import os
import sys
import django

# Setup Django
sys.path.append('/Users/hery/My-Project/Phenomenal-Python-for-Laos-Project/core')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from ai_agents.services.vector_db import VectorDBService

def verify_rag():
    vdb = VectorDBService()
    queries = [
        "Python Programming",  # Should find blog post
        "Django Framework",    # Should find course or doc
        "Workshop",            # Should find event
        "Community",           # Should find community topic
    ]
    
    for query in queries:
        print(f"\n--- Searching for: '{query}' ---")
        results = vdb.search(query, n_results=2)
        if results:
            for i, res in enumerate(results):
                source = res['metadata'].get('source', 'unknown')
                title = res['metadata'].get('title', 'No Title')
                print(f"{i+1}. Source: {source} | Title: {title}")
        else:
            print("No results found.")

if __name__ == "__main__":
    verify_rag()
