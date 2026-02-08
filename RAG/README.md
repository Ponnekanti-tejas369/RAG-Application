# 🔍 RAG Pipeline - Policy Document Q&A

A CLI-based Retrieval-Augmented Generation (RAG) system for answering questions about company policy documents using **Pinecone** vector database and **Google Gemini** AI.

---

## ✨ Features

- 📄 **Multi-format document support**: PDF, TXT, Markdown
- 🔍 **Semantic search**: Pinecone with Gemini embeddings
- 🤖 **Grounded responses**: Answers based solely on document context
- 📊 **Built-in evaluation**: Scoring rubric for quality assessment
- 🚫 **Hallucination control**: Strict prompts with source citations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI (main.py)                           │
│                    ingest | ask | evaluate                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                       RAG Pipeline                               │
│  ┌────────────┐    ┌─────────────┐    ┌───────────────────┐     │
│  │  Retriever │───▶│   Context   │───▶│   Gemini LLM      │     │
│  │ (Pinecone) │    │   Builder   │    │  + System Prompt  │     │
│  └────────────┘    └─────────────┘    └───────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Google AI Studio API Key](https://aistudio.google.com/app/apikey)
- [Pinecone Account & API Key](https://app.pinecone.io/)

### 1. Clone or Extract the Project

```bash
# If cloning from GitHub
git clone https://github.com/YOUR_USERNAME/RAG.git
cd RAG

# Or if extracting from ZIP
unzip RAG.zip
cd RAG
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# Use any text editor:
nano .env
# or
code .env
```

Your `.env` file should look like:
```env
GOOGLE_API_KEY=AIzaSy...your_actual_key
PINECONE_API_KEY=pcsk_...your_actual_key
```

### 5. Ingest Documents

```bash
# Ingest the sample policy documents
python main.py ingest

# Or ingest from a custom directory
python main.py ingest --docs /path/to/your/docs
```

This will:
- Create a Pinecone index called `rag-policy-docs`
- Embed your documents using Gemini embeddings
- Store the vectors in Pinecone

### 6. Ask Questions

```bash
# Ask a question
python main.py ask "What is the refund policy?"

# Show retrieved context chunks
python main.py ask "How do I cancel my order?" --show-context

# Use a different prompt version
python main.py ask "What are the shipping options?" --prompt-version 1
```

### 7. Run Evaluation

```bash
python main.py evaluate
```

---

## 📁 Project Structure

```
RAG/
├── main.py                 # CLI entry point
├── config.py               # Configuration (models, chunk size, Pinecone settings)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template (DO NOT put real keys here)
├── .env                    # Your actual API keys (git-ignored)
├── .gitignore              # Git ignore rules
│
├── src/
│   ├── document_loader.py  # PDF/TXT/MD loading & chunking
│   ├── vector_store.py     # Pinecone operations
│   ├── retriever.py        # Semantic search
│   ├── llm_chain.py        # Gemini LLM + prompts
│   └── evaluator.py        # Evaluation framework
│
├── prompts/
│   ├── system_prompt_v1.txt  # Basic prompt
│   └── system_prompt_v2.txt  # Enhanced prompt with citations
│
├── data/policies/          # Sample policy documents
│   ├── refund_policy.md
│   ├── shipping_policy.md
│   └── cancellation_policy.md
│
└── evaluation/
    └── questions.json      # Test questions for evaluation
```

---

## ⚙️ Configuration

### Pinecone Settings (in `config.py`)

| Setting | Value | Description |
|---------|-------|-------------|
| Index Name | `rag-policy-docs` | Auto-created on first ingest |
| Cloud | `aws` | AWS serverless |
| Region | `us-east-1` | Default region |
| Dimension | `3072` | Matches Gemini embedding model |
| Metric | `cosine` | Similarity measurement |

### Model Settings

| Setting | Value | Description |
|---------|-------|-------------|
| Embedding Model | `gemini-embedding-001` | Google's text embedding model |
| LLM Model | `gemini-2.0-flash` | Fast, capable chat model |
| Temperature | `0.1` | Low for factual responses |

---

## 📝 Prompt Engineering

### Prompt v1 (Basic)
Simple, direct instructions:
- Answer from context only
- Say "I don't know" when information is missing

### Prompt v2 (Enhanced) - Default
Enhanced with:
- **Structured output format** (Answer, Source, Confidence)
- **Explicit citation requirements**
- **Confidence levels** (Full/Partial/None)
- **Stricter hallucination guards**

---

## 📊 Evaluation

Run `python main.py evaluate` to test the pipeline with predefined questions.

**Scoring Rubric:**

| Symbol | Meaning | Criteria |
|--------|---------|----------|
| ✅ | Pass | Accurate, grounded, proper format |
| ⚠️ | Partial | Correct but incomplete |
| ❌ | Fail | Hallucination or incorrect behavior |

Results are saved to `evaluation/results.json`.

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. `PINECONE_API_KEY environment variable is not set`
Make sure you've:
- Created a `.env` file (copy from `.env.example`)
- Added your Pinecone API key to the file
- The file is in the project root directory

#### 2. `429 RESOURCE_EXHAUSTED` (Quota Error)
Your Google API free tier quota is exhausted. Options:
- Wait until quota resets (usually daily)
- Enable billing on your Google Cloud project
- Use a different API key

#### 3. `Index not found` or `No vector store found`
Run `python main.py ingest` to create the index and embed documents.

#### 4. Import Errors with Pinecone
Make sure you're using the correct package:
```bash
pip uninstall pinecone-client  # Remove old package if present
pip install pinecone>=5.0.0    # Install correct package
```

---

## 📄 License

MIT License - feel free to use and modify.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Contact

For questions or issues, please open a GitHub issue or contact the maintainer.
