# Quick Start Guide

## 🚀 Get Running in 10 Minutes

### 1. Install Tesseract (1 min)

**Windows:**
```bash
choco install tesseract
```

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

### 2. Backend (3 min)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # or: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add: CLAUDE_API_KEY=sk-your-key
python run.py
```

✅ Backend running at `http://localhost:8000`

### 3. Frontend (3 min)

Open **new terminal**:
```bash
cd frontend
npm install
npm run dev
```

✅ Frontend running at `http://localhost:5173`

### 4. Test It! (3 min)

1. Open browser → `http://localhost:5173`
2. Click **Upload Claim**
3. Upload any PDF file
4. See AI process it!
5. Click **Review Dashboard** to approve/deny

---

## 📁 Project Files Created

```
✓ Backend: FastAPI app with OCR, validation, recommendation agents
✓ Frontend: React dashboard for claim review
✓ Database: SQLite with claim tracking
✓ RAG: Insurance policy retrieval system
✓ Docker: Full deployment setup
```

---

## 🔧 Environment Setup

**backend/.env** (after running `cp .env.example .env`):
```
CLAUDE_API_KEY=sk-your-api-key-here
DATABASE_URL=sqlite:///claims.db
TESSERACT_PATH=/usr/bin/tesseract
```

---

## 📚 Next Steps

1. **Read full docs:** See `SETUP.md` for detailed configuration
2. **API docs:** Visit `http://localhost:8000/docs` while backend is running
3. **Add policies:** Update `backend/app/rag/policy_loader.py` with real insurance policies
4. **Customize agents:** Edit `backend/app/agents/` to match your logic

---

## 🆘 Troubleshooting

**Tesseract not found?**
```bash
# Set in .env:
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

**Port already in use?**
```bash
# Change port in run.py or use:
python run.py --port 8001
npm run dev -- --port 5174
```

**Claude API error?**
- Verify API key in `.env`
- Check API key has necessary permissions
- Monitor rate limits

---

## 🎯 What You Get

✅ Full OCR claim processing
✅ Intelligent validation against policies  
✅ AI-powered approval recommendations
✅ Human review workflow
✅ Audit logging
✅ Professional UI
✅ Dockerized deployment
✅ Production-ready code

---

**You're all set!** 🎉

Start with the **Upload Claim** tab, upload a PDF, and watch the AI analyze it!
