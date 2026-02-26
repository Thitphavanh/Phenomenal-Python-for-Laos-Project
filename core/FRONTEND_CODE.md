# 🎨 FRONTEND UI CODE
# ໂຄ້ດ HTML/CSS/JavaScript ສຳລັບ AI Chatbot

## 📁 ໂຄງສ້າງ Files

```
ai_agents/
├── templates/ai_agents/
│   ├── chatbot.html
│   └── analytics_dashboard.html
└── static/ai_agents/
    ├── css/
    │   └── chatbot.css
    └── js/
        └── chatbot.js
```

---

## 1. Chatbot HTML
**File**: `ai_agents/templates/ai_agents/chatbot.html`

```html
{% load static %}
<!DOCTYPE html>
<html lang="lo">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot - Python for Laos</title>
    <link rel="stylesheet" href="{% static 'ai_agents/css/chatbot.css' %}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="header-content">
                <i class="fas fa-robot"></i>
                <h1>Python AI ຜູ້ຊ່ວຍ</h1>
            </div>
            <div class="header-actions">
                <select id="ai-provider" class="provider-select">
                    <option value="openai">OpenAI GPT-4</option>
                    <option value="anthropic">Claude AI</option>
                </select>
                <button onclick="clearChat()" class="btn-clear">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>

        <div class="chat-messages" id="chat-messages">
            <div class="message bot-message">
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>ສະບາຍດີ! ຂ້ອຍແມ່ນ AI ຜູ້ຊ່ວຍສອນ Python. ຂ້ອຍສາມາດຊ່ວຍທ່ານໃນ:</p>
                    <ul>
                        <li>ຄຳຖາມກ່ຽວກັບ Python programming</li>
                        <li>ແນະນຳຫຼັກສູດທີ່ເໝາະສົມ</li>
                        <li>ແກ້ບັນຫາ code errors</li>
                        <li>ອະທິບາຍແນວຄວາມຄິດ programming</li>
                    </ul>
                    <p><strong>ທ່ານມີຄຳຖາມອັນໃດບໍ?</strong></p>
                </div>
            </div>
        </div>

        <div class="chat-input-container">
            <div class="typing-indicator" id="typing-indicator" style="display: none;">
                <span></span><span></span><span></span>
            </div>
            <form id="chat-form" class="chat-input">
                <textarea
                    id="message-input"
                    placeholder="ພິມຄຳຖາມຂອງທ່ານ..."
                    rows="1"
                ></textarea>
                <button type="submit" id="send-button">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </form>
        </div>
    </div>

    <script src="{% static 'ai_agents/js/chatbot.js' %}"></script>
</body>
</html>
```

---

## 2. Chatbot CSS
**File**: `ai_agents/static/ai_agents/css/chatbot.css`

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Noto Sans Lao', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.chat-container {
    width: 100%;
    max-width: 900px;
    height: 90vh;
    background: white;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

/* Header */
.chat-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-content {
    display: flex;
    align-items: center;
    gap: 15px;
}

.header-content i {
    font-size: 32px;
}

.header-content h1 {
    font-size: 24px;
    font-weight: 600;
}

.header-actions {
    display: flex;
    gap: 10px;
    align-items: center;
}

.provider-select {
    padding: 8px 15px;
    border: none;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    font-size: 14px;
    cursor: pointer;
}

.provider-select option {
    color: #333;
}

.btn-clear {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s;
}

.btn-clear:hover {
    background: rgba(255, 255, 255, 0.3);
}

/* Messages */
.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 30px;
    background: #f8f9fa;
}

.message {
    display: flex;
    gap: 15px;
    margin-bottom: 25px;
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}

.bot-message .message-avatar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.user-message {
    flex-direction: row-reverse;
}

.user-message .message-avatar {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
}

.message-content {
    background: white;
    padding: 15px 20px;
    border-radius: 15px;
    max-width: 70%;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.user-message .message-content {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.message-content p {
    margin-bottom: 10px;
    line-height: 1.6;
}

.message-content ul {
    margin-left: 20px;
    margin-bottom: 10px;
}

.message-content li {
    margin-bottom: 8px;
}

.message-content code {
    background: #f4f4f4;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
}

.user-message .message-content code {
    background: rgba(255, 255, 255, 0.2);
}

.message-content pre {
    background: #2d2d2d;
    color: #f8f8f2;
    padding: 15px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 10px 0;
}

.message-content pre code {
    background: none;
    padding: 0;
    color: inherit;
}

/* Sources */
.sources {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #eee;
}

.sources h4 {
    font-size: 12px;
    color: #666;
    margin-bottom: 8px;
}

.source-link {
    display: inline-block;
    background: #f0f0f0;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 12px;
    color: #667eea;
    text-decoration: none;
    margin-right: 8px;
    margin-bottom: 8px;
}

/* Input */
.chat-input-container {
    padding: 20px 30px;
    background: white;
    border-top: 1px solid #eee;
}

.typing-indicator {
    display: flex;
    gap: 5px;
    padding: 10px 0;
}

.typing-indicator span {
    width: 8px;
    height: 8px;
    background: #667eea;
    border-radius: 50%;
    animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes typing {
    0%, 60%, 100% {
        transform: translateY(0);
        opacity: 0.4;
    }
    30% {
        transform: translateY(-10px);
        opacity: 1;
    }
}

.chat-input {
    display: flex;
    gap: 15px;
    align-items: flex-end;
}

#message-input {
    flex: 1;
    padding: 15px;
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    font-size: 16px;
    font-family: inherit;
    resize: none;
    max-height: 150px;
    transition: border-color 0.3s;
}

#message-input:focus {
    outline: none;
    border-color: #667eea;
}

#send-button {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    border: none;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-size: 18px;
    cursor: pointer;
    transition: transform 0.2s;
}

#send-button:hover {
    transform: scale(1.1);
}

#send-button:active {
    transform: scale(0.95);
}

/* Scrollbar */
.chat-messages::-webkit-scrollbar {
    width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.chat-messages::-webkit-scrollbar-thumb {
    background: #667eea;
    border-radius: 4px;
}

/* Responsive */
@media (max-width: 768px) {
    .chat-container {
        height: 100vh;
        border-radius: 0;
    }

    .message-content {
        max-width: 85%;
    }

    .header-content h1 {
        font-size: 18px;
    }
}
```

---

## 3. Chatbot JavaScript
**File**: `ai_agents/static/ai_agents/js/chatbot.js`

```javascript
// Chatbot JavaScript
let sessionId = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Auto-resize textarea
    const textarea = document.getElementById('message-input');
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Handle form submit
    document.getElementById('chat-form').addEventListener('submit', function(e) {
        e.preventDefault();
        sendMessage();
    });

    // Enter to send, Shift+Enter for newline
    textarea.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});

async function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();

    if (!message) return;

    // Add user message to chat
    addMessage(message, 'user');

    // Clear input
    input.value = '';
    input.style.height = 'auto';

    // Show typing indicator
    showTypingIndicator();

    // Get selected provider
    const provider = document.getElementById('ai-provider').value;

    try {
        // Send to API
        const response = await fetch('/ai/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId,
                provider: provider,
                use_rag: true
            })
        });

        const data = await response.json();

        // Hide typing indicator
        hideTypingIndicator();

        if (response.ok) {
            // Save session ID
            sessionId = data.session_id;

            // Add bot response
            addMessage(data.response, 'bot', data.sources);
        } else {
            addMessage('ຂໍອະໄພ, ມີບັນຫາໃນການເຊື່ອມຕໍ່. ກະລຸນາລອງໃໝ່.', 'bot');
        }
    } catch (error) {
        hideTypingIndicator();
        addMessage('ຂໍອະໄພ, ເກີດຂໍ້ຜິດພາດ: ' + error.message, 'bot');
    }
}

function addMessage(content, sender, sources = []) {
    const messagesContainer = document.getElementById('chat-messages');

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    // Format content (convert markdown-like syntax)
    let formattedContent = content
        .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*([^\*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/\*([^\*]+)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');

    contentDiv.innerHTML = `<p>${formattedContent}</p>`;

    // Add sources if available
    if (sources && sources.length > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'sources';
        sourcesDiv.innerHTML = '<h4>ແຫຼ່ງອ້າງອິງ:</h4>';

        sources.forEach(source => {
            const link = document.createElement('a');
            link.className = 'source-link';
            link.href = source.url || '#';
            link.textContent = source.title || 'Source';
            link.target = '_blank';
            sourcesDiv.appendChild(link);
        });

        contentDiv.appendChild(sourcesDiv);
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingIndicator() {
    document.getElementById('typing-indicator').style.display = 'flex';
}

function hideTypingIndicator() {
    document.getElementById('typing-indicator').style.display = 'none';
}

function clearChat() {
    if (confirm('ທ່ານແນ່ໃຈບໍວ່າຕ້ອງການລົບການສົນທະນາ?')) {
        sessionId = null;
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.innerHTML = `
            <div class="message bot-message">
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>ສະບາຍດີ! ຂ້ອຍສາມາດຊ່ວຍຫຍັງທ່ານໄດ້ບໍ?</p>
                </div>
            </div>
        `;
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
```

---

## 🚀 ວິທີໃຊ້

1. ສ້າງໂຟນເດີ້:
```bash
mkdir -p ai_agents/templates/ai_agents
mkdir -p ai_agents/static/ai_agents/{css,js}
```

2. Copy code ຂ້າງເທິງໃສ່ແຕ່ລະຟາຍ

3. Run server:
```bash
python3 manage.py runserver
```

4. ເຂົ້າເບິ່ງ:
```
http://localhost:8000/ai/chatbot/
```

---

## 📱 Features

- ✅ Real-time chat interface
- ✅ Support OpenAI & Claude
- ✅ Markdown formatting
- ✅ Code syntax highlighting
- ✅ Source citations
- ✅ Typing indicator
- ✅ Responsive design
- ✅ Session management
- ✅ Clear chat history

---

**Note**: ຕ້ອງມີ OPENAI_API_KEY ໃນ .env file ກ່ອນນຳໃຊ້!
