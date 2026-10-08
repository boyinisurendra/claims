# Setup Guide - Healthcare Insurance Claim Review Assistant

## Quick Start (5 minutes)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Tesseract OCR (for PDF text extraction)
- Claude API Key

### Step 1: Install Tesseract OCR

**Windows:**
```bash
# Using chocolatey
choco install tesseract

# Or download from: https://github.com/UB-Mannheim/tesseract/wiki
```

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu):**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your Claude API key
# CLAUDE_API_KEY=sk-your-key-here

# Run backend
python run.py
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### Step 3: Frontend Setup (in new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend will be available at `http://localhost:5173`

## Testing the System

1. Open `http://localhost:5173` in your browser
2. Click **Upload Claim** tab
3. Upload a sample PDF file (or create a test PDF with claim information)
4. System will:
   - Extract text using OCR
   - Validate against insurance policies
   - Generate approval recommendation
5. Click **Review Dashboard** to see pending claims
6. Approve or deny claims with optional notes

## Environment Variables

Create `backend/.env` file:

```
# API Configuration
CLAUDE_API_KEY=sk-your-api-key
DATABASE_URL=sqlite:///claims.db
TESSERACT_PATH=/usr/bin/tesseract

# Server
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=True
LOG_LEVEL=INFO

# File uploads
UPLOAD_DIR=./uploads

# RAG
USE_RAG=True
POLICY_VECTOR_STORE=./data/policies_vectorstore
```

## Docker Setup (Optional)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

## Project Structure

```
claim_review_assistant/
├── backend/
│   ├── app/
│   │   ├── agents/        # OCR, Validation, Recommendation agents
│   │   ├── rag/          # RAG policy retrieval
│   │   ├── api/          # FastAPI routes
│   │   ├── utils/        # PDF handling
│   │   ├── models.py     # Database models
│   │   ├── schemas.py    # Request/response schemas
│   │   └── main.py       # FastAPI app
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── styles/       # CSS files
│   │   ├── services/     # API client
│   │   └── App.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
└── docker-compose.yml
```

## API Endpoints

### Claims
- `POST /api/claims/upload` - Upload and process claim PDF
- `GET /api/claims` - List all claims
- `GET /api/claims/{claim_id}` - Get claim details
- `GET /api/claims/pending` - Get pending claims for review
- `POST /api/claims/{claim_id}/approve` - Approve claim
- `POST /api/claims/{claim_id}/deny` - Deny claim

### Health
- `GET /health` - Health check
- `GET /` - Service info

## Troubleshooting

### Tesseract not found
```bash
# Windows - Set path in .env
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe

# Linux - Verify installation
which tesseract
```

### Database errors
```bash
# Reset database
rm claims.db
python -c "from app.database import init_db; init_db()"
```

### API connection errors
- Ensure backend is running on port 8000
- Check frontend proxy in `vite.config.js`
- Verify CORS settings in `app/main.py`

### Claude API errors
- Verify API key is set in `.env`
- Check API key has correct permissions
- Monitor API usage and rate limits

## Development

### Running Tests

```bash
# Backend
cd backend
pytest tests/

# Frontend
cd frontend
npm test
```

### Code Style

```bash
# Backend (optional)
pip install black flake8
black app/
flake8 app/

# Frontend (optional)
npm install --save-dev eslint prettier
npx prettier --write src/
```

## Production Deployment

1. Update `DATABASE_URL` to PostgreSQL
2. Set `API_RELOAD=False` in backend `.env`
3. Build frontend: `npm run build`
4. Use Docker Compose or Kubernetes
5. Set up SSL/TLS certificates
6. Configure proper CORS origins
7. Enable authentication layer

## Next Steps

1. Add user authentication
2. Implement audit logging
3. Create analytics dashboard
4. Add support for multiple file formats
5. Implement claim appeal workflow
6. Add email notifications
7. Create admin panel

## Support

For issues or questions, check:
- API docs: `http://localhost:8000/docs`
- Console logs in terminal
- `data/policies/` for policy configuration
