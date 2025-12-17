from .autocorrect import AutocorrectService
from .ngram import NGramModel
from .utils import tokenize, clean_text

class SuggestionEngine:
    def __init__(self, ngram_model_path: str):
        self.autocorrect = AutocorrectService()
        self.ngram = NGramModel()
        try:
            self.ngram.load_model(ngram_model_path)
            print(f"Loaded NGram model from {ngram_model_path}")
        except FileNotFoundError:
            print("Warning: NGram model not found. Predictions will be empty until trained.")

    def get_suggestions(self, text: str, top_k: int = 3) -> dict:
        """
        Input: Raw text typed so far
        Output: {
           "corrected": "...", 
           "suggestions": [{"word": "...", "score": ...}, ...]
        }
        """
        # 1. Correct the existing text
        # We assume the user wants the WHOLE sentence corrected typically, 
        # but for a keyboard we often just want to ensure the last word is valid 
        # before predicting the next one.
        
        # Strategy:
        # - Correct the entire input to display as "Corrected: ..."
        # - Use the corrected tokens to predict the NEXT word.
        
        corrected_text = self.autocorrect.correct_sentence(text)
        
        # 2. Predict Next Word (or Completion)
        # Using the CORRECTED text for context is usually better.
        
        # Check if user is starting a new word
        is_new_word_start = text.endswith(' ')
        
        # Clean and tokenize
        # Note: clean_text might strip the trailing space, so we rely on 'is_new_word_start' flag
        tokens = tokenize(clean_text(corrected_text))
        
        # Logic:
        # If new word start: Context is ALL tokens. We want any likelihood next.
        # If NOT new word start: Context is ALL tokens EXCEPT last. We want candidates that START with the last token.
        
        predictions = []
        
        if is_new_word_start or not tokens:
            # Case 1: "I love " -> Context ["i", "love"]. Predict anything next.
            predictions = self.ngram.predict_next(tokens, top_k=top_k)
        else:
            # Case 2: "I lov" -> Context ["i"]. 
            # We want: 
            # A) Words completing "lov" from our corpus (N-gram)
            # B) Spelling corrections for "lov" (Autocorrect)
            
            partial_word = tokens[-1]
            context = tokens[:-1]
            
            # Strategy:
            # 1. Try to Autocorrect the partial word (e.g. "helo" -> "hello")
            # 2. Try to Autocomplete (e.g. "he" -> "hello", "help")
            
            partial_word = tokens[-1]
            context = tokens[:-1] # Context BEFORE the current word being typed
            
            suggestions_map = {} # word -> score
            
            # 1. SPELL CHECK (Correct the mistake)
            # If the user typed "helo", we want "hello".
            spell_candidates = self.autocorrect.get_candidates(partial_word)
            best_spell = self.autocorrect.correct_word(partial_word)
            
            if best_spell and best_spell != partial_word:
                 # High score for the best correction
                 suggestions_map[best_spell] = 50.0 
            
            for cand in list(spell_candidates)[:3]:
                if cand not in suggestions_map:
                    suggestions_map[cand] = 20.0 # moderate score
            
            # 2. AUTOCOMPLETE (Predict intent)
            raw_candidates = self.ngram.predict_next(context, top_k=100)
            for w, s in raw_candidates:
                if w.startswith(partial_word) and w != partial_word:
                    # Score based on N-gram probability, but boost it slightly
                    suggestions_map[w] = max(suggestions_map.get(w, 0), s + 10.0)

            # 3. PREDICT NEXT WORDS (Advanced)
            # If the user typed "is" (valid), we show "the", "a".
            # If the best spell correction is a valid word, maybe we show what comes AFTER it? 
            # (e.g. user typed "nam" -> correction "name". We show "name". 
            # We rarely show "is" (next word for name) in the SAME bar unless "name" is automatically inserted.)
            # We will stick to correcting the CURRENT word.
            
            # Sort by score
            predictions = sorted(suggestions_map.items(), key=lambda x: x[1], reverse=True)[:top_k]
            
            # Special case: If the word is already valid (e.g. "the"), 
            # we should definitely show next words or allow the user to keep typing?
            # Actually, if "the" is valid, spell check is empty/same. 
            # Then we show Completions ("these", "there").
            # If no completions, THEN we might show next words for "the"? 
            # No, usually you hit space to see next words.
            
        next_word_suggestions = predictions

        next_word_suggestions = predictions
        
        formatted_suggestions = [
            {"word": w, "score": s} for w, s in next_word_suggestions
        ]

        return {
            "corrected": corrected_text,
            "suggestions": formatted_suggestions
        }
