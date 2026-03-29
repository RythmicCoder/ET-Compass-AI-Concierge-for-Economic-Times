"""
ET Compass Backend - Flask + OpenAI
Intelligent content recommendation system with AI-powered chatbot
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Content Database (ET ecosystem)
CONTENT_DATABASE = {
    "et_prime": [
        {
            "id": "ep1",
            "title": "Index Funds: Building Wealth Systematically",
            "description": "A comprehensive guide to understanding and investing in index funds for long-term wealth creation.",
            "duration": "8 min read",
            "experience_level": ["beginner"],
            "goals": ["learn", "portfolio"],
            "risk_profiles": ["conservative", "moderate", "aggressive"],
            "url": "https://economictimes.indiatimes.com/etprime",
            "category": "ET Prime"
        },
        {
            "id": "ep2",
            "title": "Portfolio Diversification Strategies",
            "description": "Learn how to build a balanced portfolio that reduces risk while maximizing returns.",
            "duration": "12 min read",
            "experience_level": ["beginner", "intermediate"],
            "goals": ["portfolio", "learn"],
            "risk_profiles": ["moderate"],
            "url": "https://economictimes.indiatimes.com/etprime",
            "category": "ET Prime"
        },
        {
            "id": "ep3",
            "title": "Beginner's Guide to Stock Market Basics",
            "description": "Master essential stock market terminology and concepts every investor should know.",
            "duration": "15 min read",
            "experience_level": ["beginner"],
            "goals": ["learn"],
            "risk_profiles": ["conservative", "moderate"],
            "url": "https://economictimes.indiatimes.com/etprime",
            "category": "ET Prime"
        },
        {
            "id": "ep4",
            "title": "Advanced Trading Strategies for Active Investors",
            "description": "Technical analysis, momentum trading, and risk management for experienced traders.",
            "duration": "20 min read",
            "experience_level": ["advanced"],
            "goals": ["trading"],
            "risk_profiles": ["aggressive"],
            "url": "https://economictimes.indiatimes.com/etprime",
            "category": "ET Prime"
        }
    ],
    "et_markets": [
        {
            "id": "em1",
            "title": "Advanced Stock Screener",
            "description": "Filter stocks by multiple criteria including P/E ratio, market cap, and dividend yield.",
            "duration": "Tool",
            "experience_level": ["beginner", "intermediate", "advanced"],
            "goals": ["portfolio", "trading"],
            "risk_profiles": ["moderate", "aggressive"],
            "url": "https://economictimes.indiatimes.com/markets",
            "category": "ET Markets"
        },
        {
            "id": "em2",
            "title": "Portfolio Tracker",
            "description": "Real-time tracking of your holdings with detailed performance analytics and insights.",
            "duration": "Tool",
            "experience_level": ["beginner", "intermediate", "advanced"],
            "goals": ["portfolio"],
            "risk_profiles": ["conservative", "moderate", "aggressive"],
            "url": "https://economictimes.indiatimes.com/markets",
            "category": "ET Markets"
        },
        {
            "id": "em3",
            "title": "Market Data & Charts",
            "description": "Historical data, live quotes, and interactive charts for stocks and indices.",
            "duration": "Tool",
            "experience_level": ["beginner", "intermediate", "advanced"],
            "goals": ["trading", "learn"],
            "risk_profiles": ["moderate", "aggressive"],
            "url": "https://economictimes.indiatimes.com/markets",
            "category": "ET Markets"
        }
    ],
    "masterclasses": [
        {
            "id": "mc1",
            "title": "Investing Fundamentals: 5-Part Series",
            "description": "Complete masterclass covering the foundations of investment management and portfolio building.",
            "duration": "4 hours",
            "experience_level": ["beginner"],
            "goals": ["learn", "portfolio"],
            "risk_profiles": ["conservative", "moderate"],
            "url": "https://economictimes.indiatimes.com/masterclass",
            "category": "Masterclass"
        },
        {
            "id": "mc2",
            "title": "Risk Management for Beginners",
            "description": "Learn how to identify, assess, and manage investment risks effectively.",
            "duration": "3 hours",
            "experience_level": ["beginner", "intermediate"],
            "goals": ["learn", "portfolio"],
            "risk_profiles": ["conservative"],
            "url": "https://economictimes.indiatimes.com/masterclass",
            "category": "Masterclass"
        },
        {
            "id": "mc3",
            "title": "Reading Financial Statements",
            "description": "Master the ability to analyze company financial statements for investment decisions.",
            "duration": "5 hours",
            "experience_level": ["intermediate", "advanced"],
            "goals": ["learn", "trading"],
            "risk_profiles": ["moderate", "aggressive"],
            "url": "https://economictimes.indiatimes.com/masterclass",
            "category": "Masterclass"
        }
    ],
    "trending": [
        {
            "id": "tr1",
            "title": "Fed Interest Rate Decision Impact",
            "description": "Analysis of how the latest rate decision affects equity markets and investment strategies.",
            "duration": "5 min read",
            "experience_level": ["beginner", "intermediate", "advanced"],
            "goals": ["learn", "trading"],
            "risk_profiles": ["moderate", "aggressive"],
            "url": "https://economictimes.indiatimes.com/markets",
            "category": "Trending"
        },
        {
            "id": "tr2",
            "title": "Corporate Earnings Season Overview",
            "description": "Key takeaways from earnings reports and implications for stock valuations.",
            "duration": "7 min read",
            "experience_level": ["intermediate", "advanced"],
            "goals": ["trading"],
            "risk_profiles": ["aggressive"],
            "url": "https://economictimes.indiatimes.com/markets",
            "category": "Trending"
        }
    ]
}

# Chat History for context
chat_history = []


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "ET Compass Backend"})


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chatbot endpoint - processes user messages and returns AI responses
    Uses OpenAI GPT for intelligent conversation
    """
    try:
        data = request.json
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Add user message to history
        chat_history.append({
            "role": "user",
            "content": user_message
        })

        # System prompt for ET Compass chatbot
        system_prompt = """You are ET Compass, an intelligent financial guidance chatbot for Economic Times.
        Your role is to understand the user's financial profile and recommend relevant content from ET's ecosystem.
        
        You are conducting a 5-question onboarding to understand:
        1. What brings them to ET (interest)
        2. Their investing experience level
        3. Their primary financial goal
        4. How much time they can dedicate
        5. Their risk tolerance
        
        Be conversational, helpful, and professional. After gathering all information, provide a brief summary
        and ask if they want to see personalized recommendations.
        
        Keep responses concise and focused."""

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                *chat_history
            ],
            temperature=0.7,
            max_tokens=150
        )

        ai_response = response.choices[0].message['content']

        # Add AI response to history
        chat_history.append({
            "role": "assistant",
            "content": ai_response
        })

        return jsonify({
            "success": True,
            "response": ai_response,
            "message_count": len(chat_history)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """
    Get personalized content recommendations based on user profile
    Uses AI to score and filter content
    """
    try:
        profile = request.json
        
        if not profile:
            return jsonify({"error": "No profile provided"}), 400

        # Extract profile data
        experience = profile.get('experience', 'beginner').lower()
        goal = profile.get('goal', 'learn').lower()
        risk = profile.get('riskTolerance', 'moderate').lower()
        time = profile.get('timeCommitment', '1-3 hours').lower()

        # Score all content
        scored_content = []
        
        for category, items in CONTENT_DATABASE.items():
            for item in items:
                score = score_content(item, experience, goal, risk, time)
                item['score'] = score
                item['category_key'] = category
                scored_content.append(item)

        # Sort by score
        scored_content.sort(key=lambda x: x['score'], reverse=True)

        # Group by category
        recommendations = {
            "et_prime": [c for c in scored_content if c['category'] == 'ET Prime'][:3],
            "et_markets": [c for c in scored_content if c['category'] == 'ET Markets'][:3],
            "masterclasses": [c for c in scored_content if c['category'] == 'Masterclass'][:3],
            "trending": [c for c in scored_content if c['category'] == 'Trending'][:2]
        }

        return jsonify({
            "success": True,
            "recommendations": recommendations,
            "profile": {
                "experience": experience,
                "goal": goal,
                "risk": risk,
                "time": time
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/score', methods=['POST'])
def score_single():
    """Score a single recommendation for the user"""
    try:
        data = request.json
        recommendation = data.get('recommendation')
        profile = data.get('profile')

        if not recommendation or not profile:
            return jsonify({"error": "Missing data"}), 400

        score = score_content(
            recommendation,
            profile.get('experience', 'beginner'),
            profile.get('goal', 'learn'),
            profile.get('riskTolerance', 'moderate'),
            profile.get('timeCommitment', '1-3 hours')
        )

        return jsonify({
            "success": True,
            "score": score,
            "recommendation_id": recommendation.get('id')
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/explain', methods=['POST'])
def explain_recommendation():
    """
    Use OpenAI to generate AI explanation for why content is recommended
    """
    try:
        data = request.json
        recommendation = data.get('recommendation')
        profile = data.get('profile')

        if not recommendation or not profile:
            return jsonify({"error": "Missing data"}), 400

        prompt = f"""
        Explain in 3-4 sentences why this content is perfect for the user:
        
        Content: {recommendation.get('title')}
        Description: {recommendation.get('description')}
        
        User Profile:
        - Experience: {profile.get('experience')}
        - Goal: {profile.get('goal')}
        - Risk Tolerance: {profile.get('riskTolerance')}
        - Time Available: {profile.get('timeCommitment')}
        
        Be specific, professional, and encouraging."""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )

        explanation = response.choices[0].message['content']

        return jsonify({
            "success": True,
            "explanation": explanation,
            "recommendation_id": recommendation.get('id')
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset_chat():
    """Reset chat history for new user"""
    global chat_history
    chat_history = []
    return jsonify({"success": True, "message": "Chat history cleared"})


def score_content(item, experience, goal, risk, time):
    """
    Score content based on user profile match
    Returns score 0-100
    """
    score = 0

    # Experience match (30 points)
    if experience in item.get('experience_level', []):
        score += 30
    elif experience == 'intermediate' and 'beginner' in item.get('experience_level', []):
        score += 15
    elif experience == 'advanced' and any(e in item.get('experience_level', []) for e in ['intermediate', 'beginner']):
        score += 10

    # Goal match (30 points)
    if goal in item.get('goals', []):
        score += 30

    # Risk profile match (20 points)
    if risk in item.get('risk_profiles', []):
        score += 20

    # Time commitment match (20 points)
    if time == '<1 hour' and 'min' in item.get('duration', '').lower():
        score += 20
    elif time == '1-3 hours' and any(x in item.get('duration', '').lower() for x in ['read', 'min', 'hour']):
        score += 20
    elif time == '3+ hours' and any(x in item.get('duration', '').lower() for x in ['hour']):
        score += 20

    return score


if __name__ == '__main__':
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("WARNING: OPENAI_API_KEY not found in .env file")
        print("Please create .env file with: OPENAI_API_KEY=your_key_here")
    
    # Run Flask app
    app.run(debug=True, port=5000)
