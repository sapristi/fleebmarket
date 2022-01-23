import re
from fuzzywuzzy import fuzz
import logging

logger = logging.getLogger(__name__)

MIN_SIMILAR_GROUPS = 1
MIN_SIMILAR_WORDS = 8
MIN_FUZZ_SIMILARITY = 90


def tokenize_groups(terms):
    tokens = re.split(r",|\|| / | // |; ", terms)
    return [
        token.strip(' ').lower()
        for token in tokens
        if len(token.strip(' ')) > 0
    ]

def similar_groups(terms1, terms2):
    tokens1 = tokenize_groups(terms1)
    tokens2 = tokenize_groups(terms2)
    return len(set(tokens1) & set(tokens2))

def tokenize_words(terms):
    return [
        t.lower()
        for t in terms.split()
        if len(t) > 2
    ]

def similar_words(terms1, terms2):
    tokens1 = tokenize_words(terms1)
    tokens2 = tokenize_words(terms2)
    return len(set(tokens1) & set(tokens2))

def similar_fuzz(terms1, terms2):
    return fuzz.partial_ratio(terms1, terms2)

def duplicate_offers(terms1, terms2):
    return (
        similar_groups(terms1, terms2) >= MIN_SIMILAR_GROUPS or
        similar_fuzz(terms1, terms2) >= MIN_FUZZ_SIMILARITY or
        similar_words(terms1, terms2) >= MIN_SIMILAR_WORDS
    )
