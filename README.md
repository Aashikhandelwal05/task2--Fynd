# Customer Feedback Dashboard

A production-style web application with User and Admin dashboards for customer feedback analysis using LLM-powered insights.

## Features

- **User Dashboard**: Submit feedback with ratings (1-5) and receive personalized responses
- **Admin Dashboard**: View all submissions with auto-generated summaries and recommended actions
- **LLM Integration**: OpenRouter API with Llama 3.1 for intelligent analysis
- **Persistent Storage**: SQLite database shared between both dashboards

## Tech Stack

**Backend**: Python, FastAPI, SQLAlchemy, OpenRouter API  
**Frontend**: HTML, CSS, JavaScript  
**Database**: SQLite

## Project Structure

```
task2_ai_feedback/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── database.py       # SQLite configuration
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── llm.py            # OpenRouter integration
│   └── requirements.txt
│
└── frontend/
    ├── user.html         # Customer feedback form
    ├── admin.html        # Admin dashboard
    ├── style.css
    └── script.js
```

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the `backend/` directory:

```
OPENROUTER_API_KEY=your_openrouter_api_key
```

Get your API key from [OpenRouter](https://openrouter.ai/keys).

### 3. Run the Server

```bash
uvicorn main:app --reload
```

### 4. Open Dashboards

- **User Dashboard**: Open `frontend/user.html` in browser
- **Admin Dashboard**: Open `frontend/admin.html` in browser

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/submit-review` | Submit a review with rating and text |
| GET | `/reviews` | Get all reviews with analysis |

### Request/Response Examples

**POST /submit-review**
```json
{
  "rating": 5,
  "review": "Great product!"
}
```

**Response**
```json
{
  "status": "success",
  "ai_response": "Thank you for your feedback..."
}
```

## Deployment

The app is deployment-ready for platforms like Render or Vercel:

- Environment variables for API keys
- No hardcoded secrets
- SQLite for simple persistence
