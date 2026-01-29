# 🔍 AI Document Search & Knowledge Retrieval System

A full-stack application that allows users to upload documents (PDF, DOCX, TXT) and ask questions about them using AI-powered semantic search and natural language processing - **completely free** using Hugging Face models.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)

## ✨ Features

- 📄 **Multi-format Support**: Upload PDF, DOCX, and TXT files
- 🤖 **AI-Powered Search**: Semantic search using sentence transformers
- 💬 **Conversational Interface**: Ask questions in natural language
- 🎯 **Context-Aware Answers**: Get accurate answers based on your documents
- 📚 **Source Attribution**: See which documents your answers come from
- 🗄️ **Vector Database**: Efficient document storage and retrieval using ChromaDB
- 🆓 **100% Free**: Uses Hugging Face free tier models
- 🚀 **Fast & Lightweight**: Optimized for performance

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS)
       ↓
   REST API
       ↓
Backend (FastAPI)
       ↓
   ┌─────────────┐
   │  Document   │
   │  Processing │
   └─────────────┘
       ↓
   ┌─────────────┐
   │  Embedding  │
   │   Model     │
   └─────────────┘
       ↓
   ┌─────────────┐
   │  ChromaDB   │
   │  (Vector)   │
   └─────────────┘
       ↓
   ┌─────────────┐
   │ HuggingFace │
   │     LLM     │
   └─────────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Sentence Transformers** - For text embeddings (all-MiniLM-L6-v2)
- **ChromaDB** - Vector database for semantic search
- **Hugging Face Transformers** - LLM integration
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX text extraction

### Frontend
- **HTML5/CSS3/JavaScript** - Clean, responsive UI
- **Bootstrap 5** - Modern styling
- **Fetch API** - Backend communication

### AI Models (Free Tier)
- **Embeddings**: all-MiniLM-L6-v2 (local)
- **LLM**: Mistral-7B-Instruct-v0.2 (Hugging Face API)

## 📋 Prerequisites

- **Python**: 3.9 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: ~2GB for models and dependencies
- **OS**: Windows, macOS, or Linux
- **Hugging Face Account**: Free account for API access

## 🚀 Installation & Setup

### Step 1: Clone or Download the Project

```bash
# Create project directory
mkdir ai-document-search
cd ai-document-search

# Create backend and frontend folders
mkdir backend frontend
```

### Step 2: Backend Setup

#### 2.1 Navigate to Backend Directory
```bash
cd backend
```

#### 2.2 Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2.3 Create `requirements.txt`
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
sentence-transformers==2.2.2
chromadb==0.4.18
transformers==4.35.2
torch==2.1.1
PyPDF2==3.0.1
python-docx==1.1.0
python-dotenv==1.0.0
huggingface-hub==0.19.4
```

#### 2.4 Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2.5 Get Hugging Face API Token

1. Go to [https://huggingface.co/](https://huggingface.co/)
2. Sign up for a free account
3. Navigate to Settings → Access Tokens
4. Create a new token with "read" permissions
5. Copy the token

#### 2.6 Create `.env` File
```bash
# Create .env file in backend directory
echo "HUGGINGFACE_API_TOKEN=your_token_here" > .env
```

Replace `your_token_here` with your actual token.

#### 2.7 Create `app.py`
Copy the backend code provided in the full-stack guide into `backend/app.py`

### Step 3: Frontend Setup

#### 3.1 Navigate to Frontend Directory
```bash
cd ../frontend
```

#### 3.2 Create Frontend Files
Create the following files:
- `index.html` - Main HTML file
- `app.js` - JavaScript logic
- `styles.css` - Custom styles


### Step 4: Project Structure



```
ai-document-search/
├── backend/
│   ├── venv/                 # Virtual environment (auto-generated)
│   ├── chroma_db/            # Database files (auto-generated)
│   ├── app.py                # Main backend application
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Environment variables (create this)
├── frontend/
│   ├── index.html           # Main frontend page
│   ├── app.js               # Frontend logic
│   └── styles.css           # Custom styles
└── README.md                # This file
```

## 🎯 Running the Application

### Option 1: Run Both Services (Recommended)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

Backend will run at: `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend

# Option A: Simple Python server
python -m http.server 3000

# Option B: Just open index.html in your browser
```

Frontend will be available at: `http://localhost:3000` or directly via browser

### Option 2: Development Mode (Auto-reload)

For backend auto-reload during development:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## 📖 Usage Guide

### 1. Upload Documents
- Click "Choose Files" in the sidebar
- Select PDF, DOCX, or TXT files (multiple files allowed)
- Click "Upload & Process"
- Wait for processing confirmation

### 2. Ask Questions
- Type your question in the chat input box
- Press Enter or click "Ask"
- View AI-generated answer with source references

### 3. Manage Database
- View total chunks in the sidebar
- Click "Clear Database" to remove all documents

### Example Questions
```
- "What is this document about?"
- "Summarize the main points"
- "What are the key findings?"
- "Explain the methodology used"
- "What conclusions were drawn?"
```

## 🔧 Configuration

### Adjust Chunk Size
In `app.py`, modify the `chunk_text()` function:
```python
def chunk_text(text, chunk_size=500, overlap=50):  # Adjust these values
```

### Change Number of Search Results
In `app.js`, modify the query request:
```javascript
body: JSON.stringify({
    question: question,
    n_results: 3  // Change this number
})
```

### Switch LLM Model
In `app.py`, change the model:
```python
response = hf_client.text_generation(
    prompt,
    model="mistralai/Mistral-7B-Instruct-v0.2",  # Change model here
    max_new_tokens=500,
    temperature=0.7
)
```

**Alternative Free Models:**
- `google/flan-t5-large`
- `bigscience/bloom-560m`
- `tiiuae/falcon-7b-instruct`

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is already in use
# Windows:
netstat -ano | findstr :8000

# Mac/Linux:
lsof -i :8000

# Kill the process or use a different port
uvicorn app:app --port 8001
```

### CORS errors
Make sure backend CORS is configured to allow your frontend origin.

### Model download fails
```bash
# Manually download models
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Out of memory
- Reduce `chunk_size` in `chunk_text()`
- Use a smaller embedding model
- Reduce `max_new_tokens` in LLM generation

### Hugging Face API rate limit
- Free tier: 30 requests/minute
- Wait a minute and try again
- Consider using local models instead

## 🚢 Deployment

### Deploy Backend (Free Options)

**Render.com:**
```yaml
# render.yaml
services:
  - type: web
    name: ai-doc-search-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app:app --host 0.0.0.0 --port $PORT
```

**Railway.app:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
railway login
railway init
railway up
```

**Heroku:**
```bash
# Create Procfile
echo "web: uvicorn app:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create
git push heroku main
```

### Deploy Frontend (Free Options)

**Netlify:**
```bash
# Drag and drop frontend folder to netlify.com
```

**Vercel:**
```bash
npm i -g vercel
vercel
```

**GitHub Pages:**
```bash
# Push frontend folder to GitHub
# Enable GitHub Pages in repository settings
```

**Important**: Update `API_URL` in `app.js` to your deployed backend URL.

## 🔐 Security Considerations

### For Production:

1. **Environment Variables**
   - Never commit `.env` files
   - Use environment-specific configs

2. **CORS**
   - Restrict `allow_origins` to specific domains
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

3. **API Rate Limiting**
   - Implement rate limiting to prevent abuse
   ```python
   from slowapi import Limiter
   ```

4. **File Upload Validation**
   - Limit file sizes
   - Validate file types
   - Scan for malware

5. **Authentication**
   - Add user authentication
   - Implement JWT tokens

## 🎨 Customization Ideas

- [ ] Add user authentication
- [ ] Support more file formats (CSV, HTML, Markdown)
- [ ] Add conversation history
- [ ] Implement document tagging/categorization
- [ ] Add multi-language support
- [ ] Create mobile app version
- [ ] Add export functionality (answers to PDF)
- [ ] Implement collaborative features
- [ ] Add voice input/output
- [ ] Create browser extension

## 📊 Performance Optimization

### For Better Speed:
1. Use GPU for embeddings (if available)
2. Cache frequent queries
3. Implement lazy loading for large documents
4. Use CDN for frontend assets
5. Enable compression for API responses

### For Lower Memory:
1. Use smaller embedding models
2. Reduce chunk sizes
3. Limit number of stored documents
4. Implement document archiving

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** - For free LLM access
- **Sentence Transformers** - For embedding models
- **ChromaDB** - For vector database
- **FastAPI** - For excellent Python framework
- **Bootstrap** - For UI components

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-document-search/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-document-search/discussions)
- **Email**: your.email@example.com

## 🗺️ Roadmap

### Version 1.0 (Current)
- ✅ Basic document upload
- ✅ Semantic search
- ✅ Q&A interface

### Version 2.0 (Planned)
- [ ] User authentication
- [ ] Document management dashboard
- [ ] Advanced analytics
- [ ] Team collaboration features

### Version 3.0 (Future)
- [ ] Mobile applications
- [ ] Real-time collaboration
- [ ] Advanced AI features
- [ ] Enterprise features

## 💡 Tips for Best Results

1. **Document Quality**: Use clear, well-formatted documents
2. **Specific Questions**: Ask precise questions for better answers
3. **Context**: Provide context in your questions
4. **Chunk Size**: Adjust based on document type
5. **Model Selection**: Choose appropriate models for your use case

## 🔗 Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Hugging Face Models](https://huggingface.co/models)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)

---

 ##  Application 

<img width="1763" height="897" alt="Screenshot 2026-01-29 094735" src="https://github.com/user-attachments/assets/b5a2d3ba-e9e5-458d-89a9-1d5b7902eb49" />


