"""
RAG Pipeline Configuration

Chunk size rationale:
- 512 tokens (~2000 chars) balances context granularity with retrieval precision
- Policy documents contain discrete clauses that typically fit within this size
- Small enough for focused answers, large enough for complete context
- Overlap prevents information loss at chunk boundaries
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "policies"
PROMPTS_DIR = BASE_DIR / "prompts"

# Chunking Configuration
CHUNK_SIZE = 2000  # characters (~512 tokens)
CHUNK_OVERLAP = 200  # 10% overlap to preserve context at boundaries

# Retrieval Configuration
TOP_K = 3  # Number of chunks to retrieve
SIMILARITY_THRESHOLD = 0.3  # Minimum similarity score for relevance

# Model Configuration
EMBEDDING_MODEL = "models/gemini-embedding-001"  # Correct Gemini embedding model
LLM_MODEL = "gemini-2.0-flash"
TEMPERATURE = 0.1  # Low temperature for factual, grounded responses

# Pinecone Configuration
PINECONE_INDEX_NAME = "rag-policy-docs"
PINECONE_CLOUD = "aws"
PINECONE_REGION = "us-east-1"  # Default region
EMBEDDING_DIMENSION = 3072  # Native dimension for gemini-embedding-001
