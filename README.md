# Autocorrect Keyboard Prototype

A predictive keyboard assistant that provides autocorrection and next-word suggestions using an N-gram model and FastAPI. This project demonstrates a core implementation of intelligent text input features similar to those found on mobile devices.

## 🚀 Project Overview

The **Autocorrect Keyboard Prototype** is designed to enhance typing efficiency by:
1.  **Correcting Spelling Errors**: Automatically fixing common misspellings using Levenshtein distance.
2.  **Predicting Next Words**: Suggesting the most probable next words based on context using a Bigram/Trigram Language Model with Backoff.

The system is built with a modular Python backend (handling the logic and API) and a lightweight HTML/JS frontend (providing the visual keyboard interface).

## ✨ Key Features

-   **N-Gram Language Model**: Implements a custom N-gram model (supporting variable N) with Katz Backoff smoothing to handle unseen contexts.
-   **Autocorrection Engine**: Uses `pyspellchecker` to generate candidates and ranks them based on edit distance and frequency.
-   **Real-time Suggestions**: A FastAPI backend processes keystrokes and returns suggestions instantly.
-   **Interactive Frontend**: A web-based keyboard interface to visualize predictions and corrections in real-time.

## 📂 Project Structure

```
Autocrt_keyboard/
├── project/
│   ├── app/                 # Frontend (HTML/JS/CSS)
│   ├── data/                # Training data (corpus.txt)
│   ├── models/              # Saved model files (.pkl)
│   ├── src/                 # Source Code
│   │   ├── api.py           # FastAPI application & endpoints
│   │   ├── ngram.py         # N-Gram training & probability logic
│   │   ├── autocorrect.py   # Spell checking wrapper
│   │   ├── suggestion.py    # Orchestrates Autocorrect & N-Gram modules
│   │   └── utils.py         # Text preprocessing utilities
│   └── main.py              # Application entry point
├── run_app.bat              # One-click launch script for Windows
├── run_demo.sh              # One-click launch script for Linux/Mac
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## 🛠️ Setup & Installation

### 1. Prerequisites
- Python 3.8 or higher

### 2. Create Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
```

**Activate it:**
- **Windows:** `.\venv\Scripts\activate`
- **Linux/Mac:** `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚦 Usage

### 1. Train the Model
Before running the application, you must train the N-Gram model on a text corpus. A sample corpus is expected in `project/data/corpus.txt`.

```bash
# Run from the root directory
python project/src/ngram.py --train project/data/corpus.txt --out project/models/ngram_counts.pkl
```

### 2. Run the Application
You can run the full stack (Backend API + Frontend) using the main script.

**Using Python:**
```bash
python project/main.py
```

**Using Helper Scripts:**
- **Windows:** Double-click `run_app.bat` or run it in terminal.
- **Linux/Mac:** Run `./run_demo.sh`

### 3. Access the Interface
Once running, open your browser to:
- **Web Interface:** [http://localhost:8000](http://localhost:8000)
- **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

---

## 📡 API Endpoints

The backend exposes the following endpoints:

-   `POST /suggest`:
    -   **Input**: `{"text": "The quick brow"}`
    -   **Output**: Returns corrected text and a list of next-word suggestions with probability scores.
-   `GET /health`: Checks if the API is running and the model is loaded.

---

## 🔧 Troubleshooting

### Module Import Errors
If you see `ModuleNotFoundError: No module named 'project'`, ensure you are running commands from the **root directory** (`d:\Internship\Autocrt_keyboard`), NOT from inside the `project` folder.

### Model Not Found
If the API starts but gives warnings about the model, ensure you have run the **Training** step (step 1 in Usage) and that `ngram_counts.pkl` exists in `project/models/`.

### Network Issues
If `pip install` fails, check your internet connection or try installing packages individually: `fastapi`, `uvicorn`, `pyspellchecker`.
