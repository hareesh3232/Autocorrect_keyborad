import pickle
import collections
from typing import List, Tuple, Dict
import os
from .utils import clean_text, tokenize

class NGramModel:
    def __init__(self, n: int = 3):
        self.n = n
        self.unigrams = collections.Counter()
        self.bigrams = collections.Counter()
        self.trigrams = collections.Counter()
        
    def train(self, corpus_path: str, output_path: str = None):
        """
        Reads a corpus file, tokenizes, and builds N-gram counts.
        """
        with open(corpus_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = clean_text(line)
                tokens = tokenize(line)
                if not tokens:
                    continue
                
                # Update Unigrams
                self.unigrams.update(tokens)
                
                # Update Bigrams
                for i in range(len(tokens) - 1):
                    bg = (tokens[i], tokens[i+1])
                    self.bigrams[bg] += 1
                    
                # Update Trigrams
                for i in range(len(tokens) - 2):
                    tg = (tokens[i], tokens[i+1], tokens[i+2])
                    self.trigrams[tg] += 1

        if output_path:
            self.save_model(output_path)
            
    def save_model(self, path: str):
        """
        Serializes the model counts to a pickle file.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        model_data = {
            'unigrams': self.unigrams,
            'bigrams': self.bigrams,
            'trigrams': self.trigrams
        }
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
            
    def load_model(self, path: str):
        """
        Loads the model counts from a pickle file.
        """
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
            self.unigrams = model_data.get('unigrams', collections.Counter())
            self.bigrams = model_data.get('bigrams', collections.Counter())
            self.trigrams = model_data.get('trigrams', collections.Counter())

    def predict_next(self, prefix_tokens: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Predicts the next word using Backoff: Trigram -> Bigram -> Unigram.
        IMPORTANT: This logic assumes 'prefix_tokens' are the words typed SO FAR.
        
        Refined Logic:
        - If the user just typed a word (e.g. "I love ") -> predict "pizza", "you" (full next word).
        - If the user is typing (e.g. "I lov") -> predict completions like "love", "loving".
        
        However, the current API `tokenize` usually eats spaces. 
        So "I love " -> ["i", "love"] and "I lov" -> ["i", "lov"].
        
        We will carry over the logic from `suggest_engine` where we assumed we always want the NEXT word.
        But to get better suggestions, we should effectively check if the last token is a valid word.
        If it's NOT a common word, maybe we treat it as a prefix?
        
        For this simplified prototype, we will stick to NEXT WORD prediction based on the context of the last N words.
        BUT, we will relax the matching to ensure we return *something*.
        """
        candidates = {} # map word -> score
        
        # 1. Trigram Context (needs last 2 tokens)
        if len(prefix_tokens) >= 2:
            context = tuple(prefix_tokens[-2:]) # e.g. ('i', 'love')
            # Find all trigrams starting with these two
            matches = {k[2]: v for k, v in self.trigrams.items() if k[:2] == context}
            
            if matches:
                 total = sum(matches.values())
                 for word, count in matches.items():
                     candidates[word] = (count / total) * 100.0

        # 2. Bigram Context (needs last 1 token)
        # We perform bigram lookup if we have < top_k candidates OR just to mix in more frequent options
        if len(candidates) < top_k * 3 and len(prefix_tokens) >= 1:
            context = prefix_tokens[-1] # e.g. 'love'
            matches = {k[1]: v for k, v in self.bigrams.items() if k[0] == context}
            
            if matches:
                total = sum(matches.values())
                for word, count in matches.items():
                    # If we already have it from trigram, add to score (simple interpolation)
                    score = (count / total) * 10.0
                    candidates[word] = candidates.get(word, 0) + score

        # 3. Unigram Fallback
        # If we still have very few suggestions, fill up with common words
        if len(candidates) < top_k:
            total = sum(self.unigrams.values()) or 1
            for word, count in self.unigrams.most_common(top_k * 5):
                if word not in candidates:
                    candidates[word] = (count / total) * 1.0

        # Optimization: Filter out stop words or punctuation if desired?
        # For now, just sort.
        sorted_cands = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        return sorted_cands[:top_k]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", help="Path to corpus file")
    parser.add_argument("--out", help="Path to output model pickle")
    args = parser.parse_args()
    
    if args.train and args.out:
        model = NGramModel()
        print(f"Training on {args.train}...")
        model.train(args.train, args.out)
        print(f"Model saved to {args.out}")
