# Festive Flix - RAG Holiday Movie Search

Semantic search for holiday movies using Django, MongoDB Atlas, and Voyage AI embeddings. Uses Retrieval Augmented Generation (RAG) to find movies by meaning rather than keywords.

## Quick Setup

**Prerequisites**: Python 3.8+, MongoDB Atlas account, Voyage AI API key

1. **Clone & install**:
```bash
git clone <repository-url> && cd django-rag
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt && pip install django==5.2.7
```

2. **Configure** - Create `.env`:
```env
VOYAGE_API_KEY=your_api_key
MONGO_URI=your_mongodb_connection_string
```

3. **Load data**:
```bash
python json_upload.py
python langchain_integration.py
```

4. **Run**:
```bash
python manage.py runserver
# Visit http://127.0.0.1:8000/search/
```

## How It Works

Converts movie plots to vector embeddings using Voyage AI, stores them in MongoDB with vector index, then searches by semantic similarity. Example queries: "magical Christmas story" or "angel helps someone in need".

## Tech Stack

- **Django 5.2.7** - Web framework
- **MongoDB Atlas** - Used as both operation and vector database
- **Voyage AI** - Embeddings model (`voyage-3-lite`)
- **LangChain** - Framework for building AI applications

## Key Files

- `json_upload.py` - Load movies into MongoDB
- `langchain_integration.py` - Generate embeddings
- `festive_flix/views.py` - Search logic
- `holiday_movies.json` - Sample dataset

## Troubleshooting

**Missing API key**: Ensure `.env` has `VOYAGE_API_KEY` and `MONGO_URI`

**No results**: Run both `json_upload.py` and `langchain_integration.py`

**Vector index error**: Create vector search index in MongoDB Atlas named `vector_index`

## Disclaimer

Use at your own risk; not a supported MongoDB product
