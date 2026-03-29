# ET Compass - Complete Setup Guide

## Overview
ET Compass is an AI-powered financial concierge for Economic Times with:
- Smart chatbot using OpenAI GPT
- Personalized content filtering based on user profile
- Direct links to ET Prime, Markets, and Masterclasses
- Flask backend API
- HTML/CSS frontend

---

## Prerequisites

### 1. Get OpenAI API Key
1. Go to https://platform.openai.com/account/api-keys
2. Sign up or log in
3. Create new API key
4. Copy the key (starts with `sk-`)

### 2. Install Python
- Download Python 3.8+ from https://www.python.org/downloads/
- Verify installation: `python --version`

---

## Setup Instructions

### Step 1: Create Project Folder
```bash
mkdir et-compass
cd et-compass
```

### Step 2: Copy Files
Copy these files to the `et-compass` folder:
- `app.py` (Python backend)
- `requirements.txt` (Python dependencies)
- `.env.example` (environment template)
- `ET-Compass-With-Backend.html` (frontend)

### Step 3: Create Virtual Environment (Optional but Recommended)
```bash
# Mac/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment
1. Copy `.env.example` to `.env`
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Step 6: Run Backend
```bash
python app.py
```

You should see:
```
Running on http://127.0.0.1:5000/
```

### Step 7: Open Frontend
1. Open `ET-Compass-With-Backend.html` in your browser
2. Or run a local server:
```bash
# Python 3
python -m http.server 8000

# Then open: http://localhost:8000/ET-Compass-With-Backend.html
```

---

## How It Works

### Frontend (HTML/CSS/JavaScript)
- Single page application with 5 screens
- Sends requests to Python backend via API calls
- Displays personalized recommendations

### Backend (Flask + Python)
- `POST /api/chat` - Process chatbot messages with OpenAI
- `POST /api/recommendations` - Get filtered content based on profile
- `POST /api/explain` - Generate AI explanation for recommendations
- `POST /api/score` - Score content relevance

### Content Filtering
User profile is collected via 5 questions:
1. Interest (Learn/Portfolio/Trading/Masterclasses)
2. Experience (Beginner/Intermediate/Advanced)
3. Goal (Learn/Portfolio/Trading/Wealth)
4. Time (< 1hr / 1-3hrs / 3+ hrs)
5. Risk (Conservative/Moderate/Aggressive)

Each content item is scored on how well it matches the user's profile.

---

## API Endpoints

### Health Check
```
GET /api/health
Response: { "status": "healthy" }
```

### Chatbot
```
POST /api/chat
Request: { "message": "user message" }
Response: { "response": "AI response", "message_count": 5 }
```

### Get Recommendations
```
POST /api/recommendations
Request: {
  "experience": "beginner",
  "goal": "portfolio",
  "riskTolerance": "moderate",
  "timeCommitment": "1-3 hours"
}
Response: {
  "recommendations": {
    "et_prime": [...],
    "et_markets": [...],
    "masterclasses": [...],
    "trending": [...]
  }
}
```

### Explain Recommendation
```
POST /api/explain
Request: {
  "recommendation": {...},
  "profile": {...}
}
Response: { "explanation": "Why this is recommended for you..." }
```

---

## Customization

### Add More Content
Edit `CONTENT_DATABASE` in `app.py`:
```python
CONTENT_DATABASE = {
    "et_prime": [
        {
            "id": "ep5",
            "title": "Your Article Title",
            "description": "...",
            "duration": "10 min read",
            "experience_level": ["beginner", "intermediate"],
            "goals": ["learn", "portfolio"],
            "risk_profiles": ["conservative", "moderate"],
            "url": "https://economictimes.indiatimes.com/etprime",
            "category": "ET Prime"
        }
    ]
}
```

### Modify Questions
Edit `questionDatabase` in the HTML file:
```javascript
const questionDatabase = [
    {
        text: "Your question here?",
        options: ["Option 1", "Option 2", "Option 3"],
        key: "profileKey"
    }
]
```

### Change Scoring Algorithm
Edit `score_content()` function in `app.py` to weight factors differently.

---

## Troubleshooting

### "Connection Refused" Error
- Make sure backend is running: `python app.py`
- Check if port 5000 is available
- Change port in `app.py`: `app.run(debug=True, port=5001)`

### "OpenAI API Key Error"
- Check `.env` file has correct key
- API key should start with `sk-`
- Make sure you have API credits in OpenAI account

### CORS Issues
- Ensure `flask-cors` is installed: `pip install flask-cors`
- Frontend and backend can be on different ports

### Content Not Loading
- Check browser console for errors (F12)
- Verify API response in Network tab
- Check backend logs for errors

---

## Deployment

### Deploy Backend to Heroku
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create et-compass

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-your-key

# Deploy
git push heroku main
```

### Deploy Frontend to Netlify
1. Update `API_BASE` in HTML to your Heroku URL
2. Drag and drop folder to Netlify
3. Or use Netlify CLI

### Docker Deployment
Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

Run:
```bash
docker build -t et-compass .
docker run -e OPENAI_API_KEY=sk-your-key -p 5000:5000 et-compass
```

---

## File Structure
```
et-compass/
├── app.py                          # Flask backend
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (create from .env.example)
├── .env.example                    # Template for .env
└── ET-Compass-With-Backend.html    # Frontend
```

---

## Support & Next Steps

### To Add More Features
1. **User Authentication** - Add login system
2. **Database** - Store user profiles and recommendations
3. **Analytics** - Track user engagement
4. **Streaming Chat** - Use OpenAI streaming for live responses
5. **Voice** - Add voice-based chatbot

### To Improve Filtering
1. Add more content attributes
2. Use machine learning to improve scoring
3. Track user feedback and refine recommendations

### To Scale
1. Add caching for recommendations
2. Use Celery for background tasks
3. Add database for content and profiles
4. Implement user authentication

---

## License & Credits
Built for Economic Times hackathon.
Uses OpenAI GPT-3.5-turbo for AI capabilities.

---

## Contact & Support
For issues or questions, check the backend logs or browser console.
