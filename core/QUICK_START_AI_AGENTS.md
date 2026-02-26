# 🚀 QUICK START: AI Agents Implementation
# ເລີ່ມຕົ້ນໄວສຳລັບ AI Agents

## ສິ່ງທີ່ໄດ້ສ້າງແລ້ວ ✅

ຂ້ອຍໄດ້ສ້າງສ່ວນປະກອບຕໍ່ໄປນີ້ໃຫ້ທ່ານແລ້ວ:

### 1. ໂຄງສ້າງພື້ນຖານ
- ✅ Django app `ai_agents` ສ້າງແລ້ວ
- ✅ Database models (models.py) - 6 models
- ✅ Requirements.txt updated ດ້ວຍ AI dependencies
- ✅ .env.example updated ດ້ວຍ AI configuration
- ✅ Vector Database Service (vector_db.py) ສຳເລັດ

### 2. Models ທີ່ສ້າງແລ້ວ (ai_agents/models.py)
1. **ChatConversation** - ບັນທຶກການສົນທະນາກັບ AI
2. **ChatMessage** - ຂໍ້ຄວາມແຕ່ລະຂໍ້ຄວາມ
3. **CourseAnalytics** - Analytics ຈາກ AI
4. **PaymentSlipAnalysis** - ວິເຄາະຮູບ Payment
5. **CourseRecommendation** - ແນະນຳຫຼັກສູດ
6. **VectorDocument** - ຕິດຕາມເອກະສານໃນ Vector DB

### 3. Services ທີ່ສ້າງແລ້ວ
- ✅ **VectorDBService** (vector_db.py) - ສຳເລັດ 100%

---

## ຂັ້ນຕອນການ Setup (5-10 ນາທີ)

### Step 1: ຕິດຕັ້ງ Dependencies

```bash
cd /Users/hery/My-Project/Phenomenal-Python-for-Laos-Project/core

# Option 1: ຕິດຕັ້ງທັງໝົດພ້ອມກັນ
pip3 install -r requirements.txt

# Option 2: ຕິດຕັ້ງເລືອກສິ່ງທີ່ຈຳເປັນ
pip3 install langchain==0.1.0 langchain-openai==0.0.2 chromadb==0.4.22
pip3 install sentence-transformers==2.3.1 openai==1.7.2
pip3 install djangorestframework pandas scikit-learn
pip3 install python-dotenv celery redis
```

###Step 2: ຕັ້ງຄ່າ Environment Variables

```bash
# ສ້າງ .env file
cp .env.example .env

# ແກ້ໄຂ .env ແລະໃສ່ OpenAI API key
nano .env
```

ເພີ່ມໃນ .env:
```env
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
DEFAULT_AI_MODEL=gpt-4-turbo-preview
AI_TEMPERATURE=0.7
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

### Step 3: ອັບເດດ Settings

ແກ້ໄຂ `core/settings/base.py`:

```python
INSTALLED_APPS = [
    # ... existing apps ...
    "rest_framework",  # ເພີ່ມ
    "ai_agents",       # ເພີ່ມ
]

# ເພີ່ມ settings ໃໝ່ດ້ານລຸ່ມ
import os
from dotenv import load_dotenv
load_dotenv()

# AI Configuration
CHROMA_PERSIST_DIRECTORY = os.getenv('CHROMA_PERSIST_DIRECTORY', './chroma_db')
CHROMA_COLLECTION_NAME = 'python_for_laos_docs'
```

### Step 4: Run Migrations

```bash
python3 manage.py makemigrations ai_agents
python3 manage.py migrate
```

---

## ສ້າງ Services ທີ່ເຫຼືອ

### Create Chatbot Service

ສ້າງ `ai_agents/services/chatbot.py`:

```python
"""RAG Chatbot Service"""
import os
from typing import List, Dict, Any
from openai import OpenAI
from .vector_db import VectorDBService

class PythonLaosChatbot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('DEFAULT_AI_MODEL', 'gpt-4-turbo-preview')
        self.vector_db = VectorDBService()

        self.system_prompt = """ທ່ານເປັນ AI ຜູ້ຊ່ວຍສອນ Python ໃນພາສາລາວ.
        ຕອບຄຳຖາມເປັນພາສາລາວໃຫ້ງ່າຍຕໍ່ການເຂົ້າໃຈ."""

    def chat(self, message: str, history: List = None) -> Dict:
        # Search relevant docs
        docs = self.vector_db.search(message, n_results=3)

        # Build context
        context = "\n\n".join([doc['text'][:500] for doc in docs])

        # Prepare messages
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"ບໍລິບົດ:\n{context}\n\nຄຳຖາມ: {message}"}
        ]

        # Get AI response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )

        return {
            'response': response.choices[0].message.content,
            'sources': [d['metadata'] for d in docs]
        }
```

### Create Simple View

ສ້າງ `ai_agents/views.py`:

```python
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services.chatbot import PythonLaosChatbot

chatbot = PythonLaosChatbot()

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')

        result = chatbot.chat(message)

        return JsonResponse(result)

    return JsonResponse({'error': 'POST only'}, status=405)

def chatbot_page(request):
    return render(request, 'ai_agents/chatbot.html')
```

### Create URLs

ສ້າງ `ai_agents/urls.py`:

```python
from django.urls import path
from . import views

app_name = 'ai_agents'

urlpatterns = [
    path('chat/', views.chatbot_page, name='chatbot'),
    path('api/chat/', views.chat_api, name='chat_api'),
]
```

ເພີ່ມໃນ `core/urls.py`:

```python
urlpatterns = [
    # ... existing patterns ...
    path('ai/', include('ai_agents.urls')),
]
```

---

## ທົດສອບລະບົບ

### 1. ທົດສອບ Vector DB

```python
# Python shell
python3 manage.py shell

from ai_agents.services.vector_db import VectorDBService

db = VectorDBService()

# Add test documents
docs = [
    {
        'id': 'test_1',
        'text': 'Python ແມ່ນພາສາ programming ທີ່ງ່າຍຕໍ່ການຮຽນຮູ້',
        'metadata': {'type': 'intro', 'topic': 'python'}
    }
]

db.add_documents(docs)

# Search
results = db.search('Python ແມ່ນຫຍັງ?')
print(results)
```

### 2. ທົດສອບ Chatbot

```python
from ai_agents.services.chatbot import PythonLaosChatbot

bot = PythonLaosChatbot()
response = bot.chat("Python ແມ່ນຫຍັງ?")
print(response['response'])
```

### 3. ເລີ່ມ Server

```bash
python3 manage.py runserver
```

ເປີດ: `http://localhost:8000/ai/chat/`

---

## ສ່ວນທີ່ຕ້ອງສ້າງຕໍ່ (Optional)

### 1. Payment Slip Processor

```python
# ai_agents/services/payment_slip_processor.py
import cv2
import pytesseract
from PIL import Image

class PaymentSlipProcessor:
    def process(self, image_path):
        # OCR to extract text
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='eng')

        # Extract amount, transaction ID, etc.
        # Use regex or AI to parse

        return {'extracted_text': text}
```

### 2. Course Analytics

```python
# ai_agents/services/analytics.py
import pandas as pd
from courses.models import Course, Enrollment

class CourseAnalyticsAgent:
    def analyze_course(self, course_id):
        course = Course.objects.get(id=course_id)
        enrollments = Enrollment.objects.filter(course=course)

        # Calculate metrics
        total_students = enrollments.count()
        completion_rate = enrollments.filter(status='completed').count() / total_students if total_students > 0 else 0

        return {
            'total_students': total_students,
            'completion_rate': completion_rate,
            'recommendations': self._generate_recommendations(course, completion_rate)
        }

    def _generate_recommendations(self, course, completion_rate):
        if completion_rate < 0.5:
            return "Consider adding more interactive content and exercises"
        return "Course is performing well"
```

### 3. Recommendation Engine

```python
# ai_agents/services/recommendation.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from courses.models import Course

class RecommendationEngine:
    def recommend_courses(self, user):
        # Get user's completed courses
        completed = user.enrollments.filter(status='completed').values_list('course__title', flat=True)

        # Get all courses
        all_courses = Course.objects.filter(status='published')

        # Simple content-based filtering
        # In production, use more sophisticated ML

        recommendations = []
        for course in all_courses:
            if course.title not in completed:
                recommendations.append({
                    'course': course,
                    'score': 0.8  # Placeholder
                })

        return recommendations[:5]
```

---

## ສະຫຼຸບ Files ທີ່ສ້າງແລ້ວ

```
✅ ai_agents/
   ✅ models.py (6 models)
   ✅ services/
      ✅ __init__.py
      ✅ vector_db.py (ສຳເລັດ)
      🔄 chatbot.py (ຕ້ອງສ້າງ)
      🔄 analytics.py (Optional)
      🔄 payment_slip_processor.py (Optional)
      🔄 recommendation.py (Optional)
   🔄 views.py (ຕ້ອງສ້າງ)
   🔄 urls.py (ຕ້ອງສ້າງ)

✅ requirements.txt (Updated)
✅ .env.example (Updated)
✅ AI_AGENTS_IMPLEMENTATION_GUIDE.md
✅ QUICK_START_AI_AGENTS.md (ເອກະສານນີ້)
```

---

## ຊັບພະຍາກອນເພີ່ມເຕິມ

- 📖 [AI Implementation Guide](./AI_AGENTS_IMPLEMENTATION_GUIDE.md)
- 📖 [LangChain Docs](https://python.langchain.com/)
- 📖 [OpenAI API Reference](https://platform.openai.com/docs)
- 📖 [ChromaDB Documentation](https://docs.trychroma.com/)

---

## 🐛 Troubleshooting

**ບັນຫາ**: `ModuleNotFoundError: No module named 'openai'`
**ແກ້ໄຂ**: `pip3 install openai==1.7.2`

**ບັນຫາ**: ChromaDB error
**ແກ້ໄຂ**: `rm -rf ./chroma_db` ແລ້ວສ້າງໃໝ່

**ບັນຫາ**: API key not found
**ແກ້ໄຂ**: ກວດສອບ `.env` file ແລະ restart server

---

**ສ້າງໂດຍ**: Claude Code AI
**ວັນທີ**: January 2026
**Version**: 1.0

🎉 ຂໍໃຫ້ສຳເລັດຜົນກັບ AI Agents!
