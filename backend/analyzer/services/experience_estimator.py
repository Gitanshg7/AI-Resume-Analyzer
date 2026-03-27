"""
Experience Estimator Module
============================
Estimates total years of professional experience from resume text.

Techniques:
    1. Explicit mention: "X years of experience", "X+ years"
    2. Date range detection: "Jan 2020 – Dec 2023", "2018-2022"
    3. Duration keywords: "Software Engineer (2 years)"
"""

import re
from typing import List, Tuple
from datetime import datetime


# ── Pattern 1: Explicit experience mentions ──────────────────────────────

EXPLICIT_PATTERNS = [
    # "5 years of experience", "3+ years experience", "over 2 years"
    re.compile(
        r"(?:over\s+|more\s+than\s+)?(\d+(?:\.\d+)?)\s*\+?\s*years?\s*(?:of\s+)?experience",
        re.IGNORECASE,
    ),
    # "experience of 5 years"
    re.compile(
        r"experience\s+(?:of\s+)?(\d+(?:\.\d+)?)\s*\+?\s*years?",
        re.IGNORECASE,
    ),
    # "5 yrs experience"
    re.compile(
        r"(\d+(?:\.\d+)?)\s*\+?\s*yrs?\s*(?:of\s+)?experience",
        re.IGNORECASE,
    ),
]


def _extract_explicit_years(text: str) -> List[float]:
    """Extract explicitly stated years of experience."""
    years = []
    for pattern in EXPLICIT_PATTERNS:
        matches = pattern.findall(text)
        for m in matches:
            try:
                years.append(float(m))
            except ValueError:
                continue
    return years


# ── Pattern 2: Date range detection ──────────────────────────────────────

# Matches: "Jan 2020 - Dec 2023", "2018 – 2022", "2019-present"
MONTH_NAMES = (
    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
    r"jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
)

DATE_RANGE_PATTERNS = [
    # "Jan 2020 - Dec 2023" or "January 2020 – December 2023"
    re.compile(
        rf"{MONTH_NAMES}\s*(\d{{4}})\s*[-\u2013\u2014to]+\s*(?:{MONTH_NAMES}\s*)?(\d{{4}}|present|current|now)",
        re.IGNORECASE,
    ),
    # "2020 - 2023" or "2020 – present"
    re.compile(
        r"(\d{4})\s*[-\u2013\u2014to]+\s*(\d{4}|present|current|now)",
        re.IGNORECASE,
    ),
]

CURRENT_YEAR = datetime.now().year


def _parse_year(value: str) -> int:
    """Parse a year string, treating 'present'/'current'/'now' as current year."""
    value = value.strip().lower()
    if value in ("present", "current", "now"):
        return CURRENT_YEAR
    try:
        return int(value)
    except ValueError:
        return CURRENT_YEAR


def _extract_date_range_years(text: str) -> List[float]:
    """Calculate years from date ranges found in text."""
    durations = []

    for pattern in DATE_RANGE_PATTERNS:
        matches = pattern.findall(text)
        for match in matches:
            # match is a tuple; we need the year values
            years_in_match = []
            for group in match:
                group = group.strip()
                if re.match(r"^\d{4}$", group) or group.lower() in ("present", "current", "now"):
                    years_in_match.append(_parse_year(group))

            if len(years_in_match) >= 2:
                start_year = min(years_in_match)
                end_year = max(years_in_match)
                duration = end_year - start_year
                if 0 < duration <= 50:  # sanity check
                    durations.append(float(duration))

    return durations


# ── Pattern 3: Duration keywords ────────────────────────────────────────

DURATION_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
    re.IGNORECASE,
)


def _extract_duration_keywords(text: str) -> List[float]:
    """Extract duration mentions like '2 years' near job-related context."""
    durations = []
    matches = DURATION_PATTERN.findall(text)
    for m in matches:
        try:
            val = float(m)
            if 0 < val <= 50:
                durations.append(val)
        except ValueError:
            continue
    return durations


# ── Main Entry Point ────────────────────────────────────────────────────


def estimate_experience(text: str) -> float:
    """
    Estimate total years of professional experience from resume text.

    Strategy:
        1. If explicit mentions exist (e.g. "5 years of experience"),
           return the maximum explicit value.
        2. Otherwise, sum non-overlapping date range durations.
        3. Fallback: use duration keyword mentions.

    Args:
        text: Cleaned resume text.

    Returns:
        Estimated years of experience as a float (rounded to 1 decimal).
    """
    # Priority 1: Explicit statements
    explicit = _extract_explicit_years(text)
    if explicit:
        return round(max(explicit), 1)

    # Priority 2: Date ranges (sum all, cap at reasonable max)
    date_ranges = _extract_date_range_years(text)
    if date_ranges:
        total = sum(date_ranges)
        return round(min(total, 50.0), 1)

    # Priority 3: Duration keywords
    durations = _extract_duration_keywords(text)
    if durations:
        return round(max(durations), 1)

    return 0.0
