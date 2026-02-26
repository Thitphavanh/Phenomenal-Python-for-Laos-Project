# AI Agents Setup Guide
# ຄູ່ມືການຕິດຕັ້ງ AI Agents

## ✅ Files Created Successfully!

All AI Agent features have been implemented. Now let's set them up.

## 🚀 Installation Steps

### Step 1: Install Dependencies

```bash
cd /Users/hery/My-Project/Phenomenal-Python-for-Laos-Project/core
pip install -r requirements.txt
```

This will install:
- Django REST Framework
- Celery & Redis
- OpenAI, Anthropic, LangChain
- ChromaDB, Sentence Transformers
- Pandas, NumPy, scikit-learn
- Tesseract OCR, OpenCV
- And all other dependencies

### Step 2: Install System Dependencies

**Install Tesseract OCR:**

On macOS:
```bash
brew install tesseract
```

On Ubuntu/Debian:
```bash
sudo apt-get install tesseract-ocr
```

**Install Redis:**

On macOS:
```bash
brew install redis
brew services start redis
```

On Ubuntu/Debian:
```bash
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

### Step 3: Configure Environment Variables

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required: OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: Anthropic Claude API Key
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Redis/Celery
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=python_for_laos_docs

# OCR
TESSERACT_PATH=/usr/local/bin/tesseract
OCR_CONFIDENCE_THRESHOLD=0.7
```

### Step 4: Run Database Migrations

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

This creates tables for:
- ChatConversation, ChatMessage
- CourseAnalytics
- PaymentSlipAnalysis
- CourseRecommendation
- VectorDocument
- Celery Beat (periodic tasks)
- Celery Results

### Step 5: Create Superuser (if needed)

```bash
python3 manage.py createsuperuser
```

### Step 6: Populate Vector Database

```bash
python3 manage.py populate_vector_db
```

This will index all your courses, blog posts, and documentation for RAG chatbot.

### Step 7: Start Services

**Terminal 1 - Django Server:**
```bash
python3 manage.py runserver
```

**Terminal 2 - Celery Worker:**
```bash
celery -A core worker --loglevel=info
```

**Terminal 3 - Celery Beat (optional, for periodic tasks):**
```bash
celery -A core beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

---

## 🎯 Test the Implementation

### 1. Access Chatbot UI

Visit: http://localhost:8000/ai/chatbot/

Try asking:
- "What is Python?"
- "Tell me about Django"
- "How do I learn programming?"

### 2. Test API Endpoints

**Chat API:**
```bash
curl -X POST http://localhost:8000/ai/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Python?",
    "provider": "openai",
    "use_rag": true
  }'
```

**AI Status:**
```bash
curl http://localhost:8000/ai/api/status/
```

### 3. Access Django Admin

Visit: http://localhost:8000/admin/

You can manage:
- Chat conversations
- Course analytics
- Payment slip analyses
- Recommendations
- Periodic tasks (Celery Beat)

---

## 📊 Using the Features

### Chatbot
- Access at `/ai/chatbot/`
- Uses RAG with your content
- Supports OpenAI and Anthropic providers
- Maintains conversation history

### Course Analytics
```python
from ai_agents.tasks import generate_course_analytics_task

# Generate analytics for course ID 1
task = generate_course_analytics_task.delay(1)
result = task.get()
```

### Payment Slip Processing
Upload payment slip via API:
```bash
curl -X POST http://localhost:8000/ai/api/payment-slips/analyze/ \
  -F "image=@payment_slip.jpg"
```

### Course Recommendations
```python
from ai_agents.tasks import generate_user_recommendations_task

# Generate recommendations for user ID 1
task = generate_user_recommendations_task.delay(1, limit=5)
result = task.get()
```

---

## 🔧 Troubleshooting

### Error: ModuleNotFoundError

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Error: Redis connection refused

**Solution:** Start Redis
```bash
brew services start redis  # macOS
sudo systemctl start redis  # Linux
```

### Error: Tesseract not found

**Solution:** Install Tesseract OCR
```bash
brew install tesseract  # macOS
sudo apt-get install tesseract-ocr  # Linux
```

### Error: ImportError for courses.models

**Solution:** Make sure courses app is properly set up with:
- Course model with fields: title, description, short_description, status, duration_hours
- Enrollment model with fields: student, course, status, enrolled_at, completed_at, progress_percentage
- LessonProgress model (if used)

### Celery tasks not running

**Check:**
1. Is Redis running? `redis-cli ping`
2. Is Celery worker running? Check terminal output
3. Are tasks queued? `redis-cli LLEN celery`

---

## 📚 Documentation

Refer to these guides for more details:

1. **AI_AGENTS_IMPLEMENTATION_GUIDE.md** - Complete API documentation
2. **QUICK_START_AI_AGENTS.md** - Quick start guide
3. **CELERY_TASKS_GUIDE.md** - Celery tasks guide
4. **FRONTEND_CODE.md** - Frontend code documentation
5. **AI_AGENTS_COMPLETE_SUMMARY.md** - Complete feature summary

---

## ✅ Verification Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Redis running (`redis-cli ping` returns PONG)
- [ ] Tesseract installed (`tesseract --version` works)
- [ ] `.env` file created with API keys
- [ ] Migrations run (`python3 manage.py migrate`)
- [ ] Vector DB populated (`python3 manage.py populate_vector_db`)
- [ ] Django server running (port 8000)
- [ ] Celery worker running (separate terminal)
- [ ] Chatbot accessible at `/ai/chatbot/`
- [ ] Admin panel shows AI Agents models

---

## 🎉 Success!

Once all steps are complete, you'll have:
- ✅ AI-powered chatbot with RAG
- ✅ Course analytics and predictions
- ✅ Payment slip OCR processing
- ✅ Personalized course recommendations
- ✅ Asynchronous task processing
- ✅ RESTful API
- ✅ Modern web interface

**Your Python for Laos platform is now AI-powered!**

---

## 🆘 Need Help?

Check the documentation files or review the implementation guides for detailed information on each feature.

**Happy coding! / ມີຄວາມສຸກກັບການພັດທະນາ!** 🚀
