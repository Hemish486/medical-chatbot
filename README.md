# 🩺 Medical Chatbot – AI-Powered Virtual Medical Assistant

This is a Django-based chatbot application for general medical guidance. It supports API-based responses, user authentication, email verification, login rate limiting, chat history storage, and optional Firebase persistence.

---

## 🧠 Project Features

- Interactive chatbot embedded in a web interface
- Filters out irrelevant or non-medical queries
- Provides structured responses to general health-related questions
- User signup/login/logout and password reset
- Email verification before chatbot usage
- Login rate limiting via `django-axes`
- Session-bound chat history per user
- Optional Firebase Firestore chat persistence
- API key management via `.env`
- Live chatbox interface with real-time conversation

---

## 🔧 Technologies & Libraries Used

- **Backend:** Python, Django, OpenAI API, Requests, python-dotenv, django-axes, firebase-admin
- **Frontend:** HTML, CSS, JavaScript

---

## 💬 Example Interaction

**User**: "How to deal with frequent vomiting?"

**Bot**: (Provides a detailed answer based on general medical knowledge)

**User**: "When did World War II start?"

**Bot**: "I'm a medical chatbot and can only answer questions related to healthcare."

## 🚀 Installation & Usage

1. Open the project folder in your local environment
2. Create a `.env` file with the following content:

```env
OPENAI_API_KEY='your_openai_api_key_here'
OPENAI_MODEL='gpt-4o-mini'
API_ONLY_MODE='true'

# Optional: PAT-based model access
# GITHUB_TOKEN='github_pat_...'
# GITHUB_MODEL='openai/gpt-4o-mini'
# GITHUB_MODELS_BASE_URL='https://models.github.ai/inference'

# Auth/security
DEFAULT_FROM_EMAIL='noreply@example.com'
AXES_FAILURE_LIMIT='5'
AXES_COOLOFF_TIME='1'

# Optional Firebase (choose one)
# FIREBASE_CREDENTIALS_PATH='C:/path/to/service-account.json'
# FIREBASE_CREDENTIALS_JSON='{"type":"service_account", ...}'
```

3. Run migrations:

```
python manage.py makemigrations
python manage.py migrate
```

4. Start the Django development server:

```
python manage.py runserver
```

5. Open your browser and go to: http://localhost:8000

6. Create an account at `/signup/`, verify email from console mail output (dev), then use the chatbot.

7. You should see a chat interface titled “VIRTUAL MEDICAL HELP ONLINE 24/7”. In the bottom-right corner, click the chat icon to start asking questions.
   ![Chat preview](assets/chatbot.png)

This project is for educational purposes only. It should not be used to diagnose or treat real medical conditions. Always consult a healthcare professional.
