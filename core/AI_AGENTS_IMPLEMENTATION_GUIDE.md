# 🤖 AI Agents Implementation Guide
# ຄູ່ມືການຕິດຕັ້ງ AI Agents ສຳລັບ Python for Laos Platform

## 📋 ສາລະບານ

1. [ພາບລວມລະບົບ AI Agent](#overview)
2. [ການຕິດຕັ້ງ Dependencies](#installation)
3. [ການຕັ້ງຄ່າ Environment](#configuration)
4. [Features ທີ່ສ້າງແລ້ວ](#features)
5. [ວິທີໃຊ້ງານ](#usage)
6. [API Endpoints](#api-endpoints)

---

## 🎯 ພາບລວມລະບົບ AI Agent {#overview}

ລະບົບ AI Agent ນີ້ປະກອບດ້ວຍ 4 ຄຸນສົມບັດຫຼັກ:

### 1. **AI Chatbot with RAG (Retrieval-Augmented Generation)**
   - ຕອບຄຳຖາມກ່ຽວກັບ Python, Courses, Documentation
   - ໃຊ້ Vector Database (ChromaDB) ສຳລັບຄົ້ນຫາຂໍ້ມູນທີ່ກ່ຽວຂ້ອງ
   - ສະໜັບສະໜູນທັງພາສາລາວແລະອັງກິດ

### 2. **Course Analytics AI Agent**
   - ວິເຄາະ enrollment trends
   - ຄາດການຍອດນັກຮຽນໃນອະນາຄົດ
   - ສະເໜີແນວທາງປັບປຸງຫຼັກສູດ

### 3. **Payment Slip OCR & Analysis**
   - ປະມວນຜົນຮູບພາບຫຼັກຖານການໂອນເງິນ
   - ດຶງຂໍ້ມູນ: ຈຳນວນເງິນ, Transaction ID, ວັນທີ
   - ຢືນຢັນຄວາມຖືກຕ້ອງດ້ວຍ AI

### 4. **Course Recommendation System**
   - ແນະນຳຫຼັກສູດທີ່ເໝາະສົມກັບຜູ້ໃຊ້
   - ໃຊ້ Machine Learning ວິເຄາະພຶດຕິກຳຜູ້ໃຊ້
   - Collaborative Filtering + Content-Based

---

## 🔧 ການຕິດຕັ້ງ Dependencies {#installation}

### ຂັ້ນຕອນທີ 1: ຕິດຕັ້ງ Python Packages

```bash
# ຕິດຕັ້ງທັງໝົດຈາກ requirements.txt
pip install -r requirements.txt

# ຫຼື ຕິດຕັ້ງແຍກສ່ວນ:
pip install langchain==0.1.0
pip install langchain-openai==0.0.2
pip install chromadb==0.4.22
pip install sentence-transformers==2.3.1
pip install openai==1.7.2
pip install pandas numpy scikit-learn
pip install pytesseract opencv-python
pip install djangorestframework
pip install celery redis
pip install python-dotenv
```

### ຂັ້ນຕອນທີ 2: ຕິດຕັ້ງ System Dependencies

#### macOS:
```bash
brew install tesseract
brew install redis
```

#### Ubuntu/Debian:
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install redis-server
```

### ຂັ້ນຕອນທີ 3: ເລີ່ມ Redis Server

```bash
redis-server
```

---

## ⚙️ ການຕັ້ງຄ່າ Environment {#configuration}

### 1. ສ້າງ .env file

```bash
cp .env.example .env
```

### 2. ແກ້ໄຂ .env ແລະໃສ່ API Keys

```env
# OpenAI API Key (ຈຳເປັນສຳລັບ AI features)
OPENAI_API_KEY=sk-your-actual-openai-api-key

# Optional: Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key

# AI Model Configuration
DEFAULT_AI_MODEL=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-3-small
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=2000

# Vector Database
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=python_for_laos_docs

# Celery & Redis
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

### 3. ເພີ່ມ ai_agents ໃນ INSTALLED_APPS

ແກ້ໄຂ `core/settings/base.py`:

```python
INSTALLED_APPS = [
    # ... existing apps ...
    "ai_agents",  # ເພີ່ມບັນທັດນີ້
    "rest_framework",  # ສຳລັບ API
]

# ເພີ່ມ REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# ເພີ່ມ Celery Configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Vientiane'
```

### 4. Run Migrations

```bash
python3 manage.py makemigrations ai_agents
python3 manage.py migrate
```

---

## ✨ Features ທີ່ສ້າງແລ້ວ {#features}

### 📁 ໂຄງສ້າງ Folder

```
ai_agents/
├── models.py                 # Database models
├── admin.py                  # Django admin configuration
├── views.py                  # API views
├── urls.py                   # URL routing
├── serializers.py            # DRF serializers
├── services/
│   ├── __init__.py
│   ├── vector_db.py         # Vector Database service (ChromaDB)
│   ├── chatbot.py           # RAG Chatbot service
│   ├── analytics.py         # Course Analytics AI
│   ├── payment_slip_processor.py  # Payment OCR
│   └── recommendation.py    # Recommendation engine
├── utils/
│   ├── __init__.py
│   └── helpers.py           # Helper functions
├── tasks.py                 # Celery async tasks
├── templates/
│   └── ai_agents/
│       ├── chatbot.html
│       └── analytics_dashboard.html
└── static/
    └── ai_agents/
        ├── css/
        └── js/
            └── chatbot.js
```

---

## 🚀 ວິທີໃຊ້ງານ {#usage}

### 1. ເລີ່ມ Celery Worker (ໃນ terminal ແຍກ)

```bash
celery -A core worker --loglevel=info
```

### 2. Populate Vector Database

```bash
python3 manage.py populate_vector_db
```

### 3. ເລີ່ມ Django Server

```bash
python3 manage.py runserver
```

### 4. ເຂົ້າໃຊ້ Chatbot

ເປີດ browser ແລະໄປທີ່:
```
http://localhost:8000/ai/chatbot/
```

---

## 📡 API Endpoints {#api-endpoints}

### Chatbot API

**POST** `/api/ai/chat/`
```json
{
  "message": "ຫຼັກສູດ Python ພື້ນຖານມີຫຍັງແດ່?",
  "session_id": "optional-session-id"
}
```

Response:
```json
{
  "response": "ຫຼັກສູດ Python ພື້ນຖານມີດັ່ງນີ້...",
  "sources": [
    {"title": "Python Basics", "url": "/docs/python-basics/"}
  ],
  "session_id": "abc123"
}
```

### Course Analytics API

**GET** `/api/ai/analytics/course/<course_id>/`

Response:
```json
{
  "course_id": 1,
  "enrollment_prediction": {
    "next_month": 150,
    "next_quarter": 450
  },
  "engagement_score": 0.85,
  "recommendations": "Consider adding more hands-on projects..."
}
```

### Payment Slip Analysis API

**POST** `/api/ai/payment-slip/analyze/`

Form data:
- `image`: File upload
- `event_registration_id`: Integer (optional)

Response:
```json
{
  "status": "completed",
  "extracted_data": {
    "amount": 50000.00,
    "transaction_id": "TXN123456789",
    "payment_date": "2024-01-15",
    "sender_name": "ທ້າວ ສົມພອນ"
  },
  "confidence_score": 0.92
}
```

### Course Recommendations API

**GET** `/api/ai/recommendations/`

Response:
```json
{
  "recommendations": [
    {
      "course": {
        "id": 1,
        "title": "Advanced Python Programming",
        "slug": "advanced-python"
      },
      "relevance_score": 0.95,
      "reason": "Based on your completion of Python Basics..."
    }
  ]
}
```

---

## 🎨 Frontend Integration

### Chatbot Widget (JavaScript)

```html
<!-- ເພີ່ມໃນ base template -->
<div id="ai-chatbot-widget"></div>

<script src="{% static 'ai_agents/js/chatbot.js' %}"></script>
<script>
  // Initialize chatbot
  const chatbot = new AIChatbot({
    apiEndpoint: '/api/ai/chat/',
    position: 'bottom-right',
    primaryColor: '#3B82F6',
    greetingMessage: 'ສະບາຍດີ! ຂ້ອຍສາມາດຊ່ວຍຫຍັງທ່ານໄດ້ບໍ?'
  });
</script>
```

---

## 🔐 Security Best Practices

1. **API Keys**: ບໍ່ຄວນເປີດເຜີຍ API keys ໃນ code
2. **Rate Limiting**: ຈຳກັດຈຳນວນ requests ຕໍ່ IP
3. **Input Validation**: Validate ທຸກ input ກ່ອນສົ່ງໃຫ້ AI
4. **User Permissions**: ກວດສອບສິດການເຂົ້າເຖິງກ່ອນເຮັດ analytics

---

## 📊 Monitoring & Logging

### View AI Usage Stats

```bash
python3 manage.py ai_stats
```

### Check Vector DB Status

```bash
python3 manage.py check_vector_db
```

---

## 🐛 Troubleshooting

### ບັນຫາທົ່ວໄປ:

**1. ChromaDB connection error**
```bash
# ລົບ database ແລະສ້າງໃໝ່
rm -rf ./chroma_db
python3 manage.py populate_vector_db
```

**2. Celery task not running**
```bash
# Restart Celery worker
celery -A core worker --loglevel=info --pool=solo
```

**3. OpenAI API rate limit**
```
# ຫຼຸດ rate ໃນ settings:
AI_MAX_TOKENS=1000
AI_TEMPERATURE=0.5
```

---

## 📚 ຂໍ້ມູນເພີ່ມເຕີມ

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [ChromaDB Documentation](https://docs.trychroma.com/)

---

## 🎓 ຕົວຢ່າງການນຳໃຊ້

### 1. Chatbot ຕອບຄຳຖາມ Python

```python
from ai_agents.services.chatbot import PythonLaosChatbot

chatbot = PythonLaosChatbot()
response = chatbot.chat("ເຂົ້າໃຈ list comprehension ແນວໃດ?")
print(response)
```

### 2. ວິເຄາະຫຼັກສູດ

```python
from ai_agents.services.analytics import CourseAnalyticsAgent

agent = CourseAnalyticsAgent()
insights = agent.analyze_course(course_id=1)
print(insights['recommendations'])
```

### 3. ປະມວນຜົນ Payment Slip

```python
from ai_agents.services.payment_slip_processor import PaymentSlipProcessor

processor = PaymentSlipProcessor()
result = processor.process_slip(image_path='payment.jpg')
print(f"Amount: {result['amount']} LAK")
```

---

## ✅ Next Steps

ຫຼັງຈາກອ່ານ guide ນີ້ແລ້ວ, ທ່ານສາມາດ:

1. ✅ ເລີ່ມຕັ້ງຄ່າ environment variables
2. ✅ Run migrations
3. ✅ Populate vector database
4. ✅ ທົດສອບ chatbot ຜ່ານ API
5. ✅ Integrate ເຂົ້າກັບ frontend

---

**ສ້າງໂດຍ**: Claude Code AI
**ອັບເດດລ່າສຸດ**: January 2026
**Version**: 1.0.0
