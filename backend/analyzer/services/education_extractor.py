"""
Education Extractor Module
==========================
Detects education degrees and university names from resume text.

Techniques:
    - Regex patterns for common degree abbreviations
    - spaCy NER (ORG entities) for university name detection
"""

import re
from typing import List, Tuple

# Lazy-loaded spaCy model
_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is None:
        import spacy
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


# ── Degree Patterns ─────────────────────────────────────────────────────

DEGREE_PATTERNS = [
    # Doctorates
    (r"\bph\.?d\.?\b", "PhD"),
    (r"\bdoctorate\b", "PhD"),
    # Masters
    (r"\bm\.?\s*tech\.?\b", "M.Tech"),
    (r"\bm\.?\s*sc\.?\b", "M.Sc"),
    (r"\bm\.?\s*s\.?\b", "M.S"),
    (r"\bm\.?\s*a\.?\b", "M.A"),
    (r"\bm\.?\s*e\.?\b", "M.E"),
    (r"\bm\.?\s*b\.?\s*a\.?\b", "MBA"),
    (r"\bmaster(?:'?s)?\s+(?:of\s+)?(?:science|engineering|technology|arts|business)\b", "Masters"),
    (r"\bmaster(?:'?s)?\s+degree\b", "Masters"),
    # Bachelors
    (r"\bb\.?\s*tech\.?\b", "B.Tech"),
    (r"\bb\.?\s*e\.?\b", "B.E"),
    (r"\bb\.?\s*sc\.?\b", "B.Sc"),
    (r"\bb\.?\s*s\.?\b", "B.S"),
    (r"\bb\.?\s*a\.?\b", "B.A"),
    (r"\bb\.?\s*c\.?\s*a\.?\b", "BCA"),
    (r"\bbachelor(?:'?s)?\s+(?:of\s+)?(?:science|engineering|technology|arts)\b", "Bachelors"),
    (r"\bbachelor(?:'?s)?\s+degree\b", "Bachelors"),
    # Diplomas
    (r"\bdiploma\b", "Diploma"),
    # Certifications (general)
    (r"\bcertificat(?:e|ion)\b", "Certification"),
]

# Common university-related keywords (to filter NER results)
UNIVERSITY_KEYWORDS = [
    "university", "college", "institute", "school",
    "academy", "polytechnic", "iit", "nit", "iiit", "bits",
]

# Fields of study
FIELD_PATTERNS = [
    r"computer\s*science",
    r"information\s*technology",
    r"software\s*engineering",
    r"electrical\s*engineering",
    r"mechanical\s*engineering",
    r"electronics",
    r"data\s*science",
    r"artificial\s*intelligence",
    r"mathematics",
    r"physics",
    r"business\s*administration",
    r"commerce",
    r"economics",
    r"statistics",
]


def detect_degrees(text: str) -> List[str]:
    """
    Detect degree abbreviations in text.

    Args:
        text: Cleaned resume text.

    Returns:
        List of detected degree names (deduplicated).
    """
    found = set()
    for pattern, degree_name in DEGREE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            found.add(degree_name)
    return sorted(found)


def detect_fields_of_study(text: str) -> List[str]:
    """Detect fields of study mentioned in text."""
    found = []
    for pattern in FIELD_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            found.append(match.group().title())
    return found


def detect_universities(text: str) -> List[str]:
    """
    Detect university names using spaCy NER (ORG entities)
    filtered by university-related keywords.
    """
    nlp = _get_nlp()
    doc = nlp(text)

    universities = set()
    for ent in doc.ents:
        if ent.label_ == "ORG":
            ent_lower = ent.text.lower()
            if any(kw in ent_lower for kw in UNIVERSITY_KEYWORDS):
                universities.add(ent.text.strip())

    return sorted(universities)


def extract_education(text: str) -> str:
    """
    Extract a summary education string from resume text.

    Combines detected degrees, fields of study, and universities
    into a readable summary.

    Args:
        text: Cleaned resume text.

    Returns:
        Education summary string, e.g. "B.Tech Computer Science"
    """
    degrees = detect_degrees(text)
    fields = detect_fields_of_study(text)
    universities = detect_universities(text)

    parts = []

    if degrees:
        # Use the highest degree found
        priority = ["PhD", "M.Tech", "M.E", "M.Sc", "M.S", "M.A", "MBA", "Masters",
                     "B.Tech", "B.E", "B.Sc", "B.S", "B.A", "BCA", "Bachelors",
                     "Diploma", "Certification"]
        best = next((d for d in priority if d in degrees), degrees[0])
        parts.append(best)

    if fields:
        parts.append(fields[0])  # primary field

    if universities:
        parts.append(f"from {universities[0]}")

    return " ".join(parts) if parts else ""
