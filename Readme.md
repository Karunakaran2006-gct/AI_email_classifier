# AI Email / Message Classifier

An AI-powered web application for classifying and analyzing business emails and messages.

The application accepts a business message and uses AI to determine its category, priority, sentiment, summary, and suggested next action.

---

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

---

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

## Architecture

The application follows a layered architecture to separate API handling, business logic, database operations, and AI processing.

```text
                    ┌──────────────────┐
                    │   Next.js UI     │
                    │    Frontend      │
                    └────────┬─────────┘
                             │ HTTP / REST
                             ▼
                    ┌──────────────────┐
                    │   FastAPI Router │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Message Service │
                    │  Business Logic  │
                    └──────┬─────┬─────┘
                           │     │
                 ┌─────────┘     └─────────┐
                 ▼                         ▼
        ┌──────────────────┐      ┌──────────────────┐
        │    Repository    │      │   LLM Service    │
        │  Database Access │      │   AI Analysis    │
        └────────┬─────────┘      └────────┬─────────┘
                 │                         │
                 ▼                         ▼
        ┌──────────────────┐      ┌──────────────────┐
        │      SQLite      │      │      Gemini      │
        │     Database     │      │       API        │
        └──────────────────┘      └──────────────────┘

## Architecture Layers

Router → Handles HTTP requests and responses
Schema → Validates input and output data
Service → Contains application business logic
Repository → Handles database operations
LLM Service → Handles AI analysis

##project structure

Micro module API/
│
├── backend/
│   ├── app/
│   │   ├── llm/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   └── messages.db
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   └── layout.tsx
│   ├── package.json
│   └── ...
│
└── README.md

## API Documentation
API Documentation

Base URL:

http://127.0.0.1:8000
Method	Endpoint	                  Description
POST	/api/messages/	             Create a new message
GET	    /api/messages/	             Retrieve messages with optional filters
GET	    /api/messages/{id}	         Retrieve a message by ID
POST	/api/messages/{id}/analyze	 Analyze a message using AI
DELETE	/api/messages/{id}	         Delete a message
GET	    /api/messages/summary	     Get dashboard statistics
GET	    /api/health	                 Check API health

## Swagger Documentation

Interactive API documentation is available at:http://127.0.0.1:8000/docs

## DB design

The application uses SQLite for local data storage. SQLAlchemy is used as the ORM for database operations
| Column             | Type    | Description                     |
| ------------------ | ------- | ------------------------------- |
| `id`               | Integer | Primary key                     |
| `sender`           | String  | Sender's email or identifier    |
| `subject`          | String  | Message subject                 |
| `body`             | Text    | Full message content            |
| `category`         | String  | AI-generated category           |
| `priority`         | String  | AI-generated priority           |
| `sentiment`        | String  | AI-generated sentiment          |
| `summary`          | Text    | AI-generated message summary    |
| `suggested_action` | Text    | AI-generated recommended action |

## AI Classification Values

Category:

Incident, Request, Complaint, Inquiry, General

Priority:

Critical, High, Medium, Low

The message is initially stored with its basic details. When the AI analysis endpoint is called, the classification results are generated and stored in the same record.

Database file:

backend/messages.db

Example Input
Subject:
Unable to access my account

Message:
I have been unable to log in to my account since this morning.
Example AI Output
{
  "category": "Incident",
  "priority": "High",
  "sentiment": "Negative",
  "summary": "Customer is unable to access their account.",
  "suggested_action": "Investigate the login issue and assist the customer."
}

## Appliction FLow
User enters message
        ↓
Next.js Frontend
        ↓
POST /api/messages/
        ↓
FastAPI
        ↓
Message Service
        ↓
SQLite
        ↓
Message created
        ↓
POST /api/messages/{id}/analyze
        ↓
LLM Service
        ↓
Gemini API
        ↓
Structured AI result
        ↓
Validation
        ↓
SQLite
        ↓
Updated message displayed in frontend
