import re
import string

def clean_text(text: str) -> str:
    """
    Cleans input text by lowercasing and removing punctuation/special chars.
    """
    if not text:
        return ""
    text = text.lower()
    # Remove punctuation but leave inner apostrophes? 
    # For now, simplistic approach: remove all non-alphanuedric except space
    text = re.sub(r'[^a-z0-9\s\']', '', text)
    return text.strip()

def tokenize(text: str) -> list[str]:
    """
    Splits text into tokens (words).
    """
    return text.split()
