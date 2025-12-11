# Autocorrect Keyboard Prototype

A predictive keyboard assistant that provides autocorrection and next-word suggestions using an N-gram model and FastAPI.

## Setup

1. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Train the N-Gram Model
Before running the API, you must train the model using the provided sample corpus (or your own).

```bash
python project/src/ngram_module.py --train project/data/corpus.txt --out project/models/ngram_counts.pkl
```

### 2. Run the Integrated App
Start the full application (Backend + Frontend) with the main script:

```bash
python project/main.py
```

- **Frontend**: `http://localhost:8000`
- **API**: `http://localhost:8000/suggest`
- **Health**: `http://localhost:8000/health`

## Features

- **Autocorrect**: Corrects misspellings using Levenshtein distance (via `pyspellchecker`).
- **Next-Word Prediction**: Suggests the next likely words using a Bigram/Trigram model with backoff.
- **Real-time API**: Fast suggestions via HTTP POST requests.
- **Interactive UI**: A simple, clean keyboard interface to test the functionality.

## Troubleshooting

### Network/Installation Issues
If you encounter network errors during `pip install`:
1. Check your internet connection
2. Try installing packages individually:
   ```bash
   pip install fastapi
   pip install uvicorn
   pip install pyspellchecker
   ```
3. If behind a proxy, configure pip with your proxy settings

### Module Import Errors
If you see `ModuleNotFoundError: No module named 'project'`:
- Make sure you're running `python project/main.py` from the **root directory** (`d:\Internship\Autocrt_keyboard`)
- Verify `__init__.py` files exist in `project/` and `project/src/` directories
