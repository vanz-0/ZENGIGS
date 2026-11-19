"""
swear_filter.py - Intelligent Profanity Tracker and Censor Engine

Tracks and censors swear words for YouTube Shorts, TikTok, and Instagram Reels
compliance. Replaces middle characters with '*' while keeping initial and final
letters recognizable (e.g., 'fucking' -> 'f*****g', 'bitch' -> 'b***h').
"""

import re
from typing import List, Optional

# Default high-priority list of profanities and variations
DEFAULT_SWEAR_WORDS = [
    # F-words
    "fuck", "fucking", "fucked", "fucker", "fuckers", "fucks", "fuckin", "fucka", "mothafucka", "motherfucker",
    # S-words
    "shit", "shits", "shitting", "shitty", "bullshit", "horseshit", "dipshit",
    # B-words
    "bitch", "bitches", "bitching", "bitchass", "bastard", "bastards",
    # A-words
    "ass", "asshole", "assholes", "dumbass", "jackass", "badass",
    # D & C words
    "dick", "dicks", "dickhead", "cock", "cocks", "cunt", "cunts", "pussy", "pussies",
    # Slurs and extreme profanity (always censored)
    "nigga", "niggas", "nigger", "niggers", "faggot", "fag", "whore", "whores", "slut", "sluts",
    # Minor profanity
    "damn", "damned", "damnit", "goddamn", "crap", "piss", "pissed", "hell",
]

class SwearTracker:
    def __init__(self, custom_words: Optional[List[str]] = None):
        words = list(set(DEFAULT_SWEAR_WORDS + (custom_words or [])))
        # Sort by length descending to match longest phrases first
        words.sort(key=len, reverse=True)
        self.pattern = re.compile(
            r"\b(" + "|".join(re.escape(w) for w in words) + r")\b",
            re.IGNORECASE,
        )

    @staticmethod
    def censor_token(word: str) -> str:
        """Censors middle letters: 'fucking' -> 'f*****g', 'ass' -> 'a*s'."""
        if len(word) <= 2:
            return word[0] + "*"
        return word[0] + "*" * (len(word) - 2) + word[-1]

    def clean(self, text: str) -> str:
        """Replaces all matched swear words with asterisks in place."""
        if not text:
            return ""
        return self.pattern.sub(lambda m: self.censor_token(m.group(0)), text)

    def find_swears(self, text: str) -> List[str]:
        """Returns all swear words detected in the input text."""
        return [m.group(0) for m in self.pattern.finditer(text)]

# Global default instance
_default_tracker = SwearTracker()

def clean(text: str) -> str:
    """Convenience function: clean text using default swear tracker."""
    return _default_tracker.clean(text)

def has_swears(text: str) -> bool:
    """Convenience function: check if text contains profanity."""
    return len(_default_tracker.find_swears(text)) > 0
