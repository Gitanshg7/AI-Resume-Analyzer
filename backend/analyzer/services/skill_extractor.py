"""
Skill Extraction Module
=======================

Detects technical skills from resume text using a hybrid approach:

    1. PhraseMatcher (spaCy)  → multi-word skills (machine learning, rest api)
    2. Regex word-boundary matching → prevents substring errors
    3. Skill dictionary filtering

Pipeline:
    extract_skills(text)
        → normalize text
        → run phrase matcher
        → run dictionary regex matcher
        → deduplicate skills
"""

import re
import spacy
from spacy.matcher import PhraseMatcher

# Lazy load spaCy
_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


# ── Skill Database ───────────────────────────────────────────────────────

SKILLS_DATABASE = [
    "python",
    "c++",
    "java",
    "javascript",
    "react",
    "angular",
    "node.js",
    "django",
    "flask",
    "mongodb",
    "mysql",
    "postgresql",
    "sql",
    "docker",
    "kubernetes",
    "git",
    "github",
    "rest api",
    "web services",
    "machine learning",
    "deep learning",
    "numpy",
    "pandas",
    "excel",
]

# ── Phrase Matcher Setup ─────────────────────────────────────────────────

_phrase_matcher = None


def _get_phrase_matcher():
    """
    Create spaCy PhraseMatcher for multi-word skills.
    """
    global _phrase_matcher

    if _phrase_matcher is None:

        nlp = _get_nlp()

        matcher = PhraseMatcher(nlp.vocab)

        patterns = [nlp(skill) for skill in SKILLS_DATABASE]

        matcher.add("SKILLS", patterns)

        _phrase_matcher = matcher

    return _phrase_matcher


# ── Skill Extraction ─────────────────────────────────────────────────────


def extract_skills(text: str):
    """
    Extract technical skills from resume text.

    Args:
        text: Cleaned resume text

    Returns:
        List[str]: Detected skills
    """

    nlp = _get_nlp()

    doc = nlp(text)

    matcher = _get_phrase_matcher()

    found_skills = set()

    # ── PhraseMatcher Detection ─────────────────────

    matches = matcher(doc)

    for match_id, start, end in matches:

        span = doc[start:end]

        found_skills.add(span.text.title())

    # ── Regex Dictionary Matching ───────────────────

    text_lower = text.lower()

    for skill in SKILLS_DATABASE:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text_lower):

            found_skills.add(skill.title())

    return sorted(found_skills)