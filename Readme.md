# AI Email / Message Classifier

An AI-powered web application for classifying and analyzing business emails and messages.

The application accepts a business message and uses AI to determine its category, priority, sentiment, summary, and suggested next action.

## Features

- Create and store business messages
- Classify messages using AI
- Detect message category
- Assign message priority
- Detect sentiment
- Generate a short AI summary
- Suggest the next action
- Search message history
- Filter messages by category and priority
- Dashboard with message statistics
- Delete messages
- REST API using FastAPI
- SQLite database
- Next.js frontend
- Automated API tests
- Swagger/OpenAPI documentation

## Technology Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

### Database

- SQLite

### AI

- Gemini API
- Dedicated LLM service for AI analysis

### Testing

- Pytest
- FastAPI TestClient

---

# Architecture

The application follows a layered architecture:

```text
                 Next.js Frontend
                       │
                       │ HTTP / REST API
                       ▼
                FastAPI Router
                       │
                       ▼
                Message Service
                  /          \
                 /            \
                ▼              ▼
        Repository         LLM Service
             │                  │
             ▼                  ▼
          SQLite             Gemini