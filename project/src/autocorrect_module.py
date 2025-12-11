from spellchecker import SpellChecker

class AutocorrectService:
    def __init__(self):
        self.spell = SpellChecker()

    def correct_word(self, word: str) -> str:
        """
        Corrects a single word using Levenshtein distance.
        """
        # spell.correction returns None if word is unknown/not found in some versions, 
        # but usually returns the best guess.
        corrected = self.spell.correction(word)
        return corrected if corrected else word

    def correct_sentence(self, sentence: str) -> str:
        """
        Corrects words in a sentence while preserving basic structure.
        """
        words = sentence.split()
        corrected_words = []
        for word in words:
            # Check if it has punctuation attached
            # For simplicity, strip trailing punctuation to check, then reattach
            # Ideally use regex tokenization, but simple split is safer for prototype speed
            clean_w = word.strip(".,?!;:")
            if not clean_w.isalpha():
                corrected_words.append(word)
                continue
            
            # Start/End punctuation preservation
            prefix = word[:len(word)-len(word.lstrip(".,?!;:"))]
            suffix = word[len(word.rstrip(".,?!;:")):]
            
            corrected_core = self.correct_word(clean_w)
            corrected_words.append(f"{prefix}{corrected_core}{suffix}")
            
        return " ".join(corrected_words)

    def add_word(self, word: str):
        """
        Adds a custom word to the dictionary.
        """
        self.spell.word_frequency.load_words([word])

    def get_candidates(self, word: str) -> set:
        """
        Returns a set of possible spelling corrections for the word.
        """
        # .candidates() returns a set of strings
        res = self.spell.candidates(word)
        return res if res else set()
