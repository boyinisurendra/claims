# Healthcare Insurance Claim Review Assistant

An AI-powered system to automate the review of insurance claims using OCR, validation, and recommendation agents.

## Architecture

```
Claim Submission (PDF)
        ↓
    OCR Agent (Extract text & fields)
        ↓
    Validation Agent (Check against policies, detect missing fields)
        ↓
    Recommendation Agent (Approve/Deny/Flag with reasoning)
        ↓
    Human Review & Approval
        ↓
    Claim Processed
```

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: React 18+
- **Database**: SQLite (MVP) / PostgreSQL (production)
- **OCR**: Tesseract + pytesseract
- **AI/Agents**: LangChain + Claude API
- **RAG**: LangChain with FAISS vector store

## Project Structure

```
claim_review_assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app
│   │   ├── config.py               # Configuration
│   │   ├── database.py             # Database setup
│   │   ├── models.py               # Database models
│   │   ├── schemas.py              # Request/response schemas
│   │   ├── agents/                 # Agent workflows
│   │   │   ├── __init__.py
│   │   │   ├── ocr_agent.py        # OCR extraction
│   │   │   ├── validation_agent.py # Field validation
│   │   │   └── recommendation_agent.py  # Approval recommendation
│   │   ├── rag/                    # RAG setup
│   │   │   ├── __init__.py
│   │   │   ├── policy_loader.py    # Load insurance policies
│   │   │   └── retriever.py        # Vector store retrieval
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py           # API endpoints
│   │   └── utils/
│   │       └── pdf_handler.py      # PDF processing utilities
│   ├── tests/
│   │   ├── test_agents.py
│   │   └── test_api.py
│   ├── data/
│   │   ├── policies/               # Insurance policy guidelines
│   │   └── sample_claims/          # Sample PDFs for testing
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ClaimUpload.jsx
│   │   │   ├── ClaimReviewDashboard.jsx
│   │   │   ├── ClaimDetails.jsx
│   │   │   └── ApprovalForm.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── ClaimDetail.jsx
│   │   ├── services/
│   │   │   └── api.js             # API client
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
└── docker-compose.yml
```

## Setup Instructions

### Backend Setup

1. **Create virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys (Claude API key, etc.)
   ```

4. **Initialize database**:
   ```bash
   python -c "from app.database import init_db; init_db()"
   ```

5. **Run backend**:
   ```bash
   python run.py
   ```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start dev server**:
   ```bash
   npm run dev
   ```

Frontend will be available at `http://localhost:5173`

## API Endpoints

### POST `/api/claims/upload`
Upload a claim PDF for processing.

**Request**: Form data with file
**Response**: `{ claim_id, status, extracted_data }`

### GET `/api/claims/{claim_id}`
Retrieve claim details and review status.

### GET `/api/claims/pending`
Get all claims pending human review.

### POST `/api/claims/{claim_id}/approve`
Approve a claim with optional notes.

### POST `/api/claims/{claim_id}/deny`
Deny a claim with rejection reason.

## Features

- ✅ PDF upload and OCR processing
- ✅ Automatic field validation against policies
- ✅ AI-powered approval recommendations
- ✅ Missing field detection
- ✅ Human review workflow
- ✅ Audit logs (approval/denial history)
- ✅ Policy-aware RAG for context

## Environment Variables

```
CLAUDE_API_KEY=sk-...
DATABASE_URL=sqlite:///claims.db
TESSERACT_PATH=/usr/bin/tesseract  # or path on your system
LOG_LEVEL=INFO
```

## Testing

```bash
# Run backend tests
cd backend
pytest tests/

# Run frontend tests
cd frontend
npm test
```

## Next Steps for Full Implementation

1. Add more insurance policy templates
2. Implement audit logging system
3. Add user authentication
4. Build analytics dashboard
5. Deploy with Docker
6. Add support for multiple file formats
"# Insurance_claims" 
