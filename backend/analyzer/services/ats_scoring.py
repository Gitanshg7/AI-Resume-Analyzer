"""
ATS Scoring Module
==================

Computes an ATS-style score for a resume using weighted factors.

Scoring Factors:

    1. Skill Match              → 25%
    2. Experience Relevance     → 20%
    3. Education                → 10%
    4. Keyword Density          → 15%
    5. Job Description Match    → 20%
    6. Section Completeness     → 10%

Returns:
    {
        "score": int,
        "breakdown": {
            "skills": float,
            "experience": float,
            "education": float,
            "keywords": float,
            "jd_match": float,
            "sections": float
        }
    }
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ── Section Detection ───────────────────────────────────────────────────

SECTION_KEYWORDS = {
    "education": ["education", "degree", "university"],
    "experience": ["experience", "work experience", "employment"],
    "projects": ["projects", "personal projects"],
    "skills": ["skills", "technical skills"],
    "certifications": ["certifications", "courses"]
}


def detect_sections(text: str):
    """
    Detect presence of key resume sections.

    Returns:
        number_of_sections_found
    """

    text_lower = text.lower()

    found = 0

    for section, keywords in SECTION_KEYWORDS.items():

        for kw in keywords:

            if kw in text_lower:
                found += 1
                break

    return found


# ── Job Description Matching ────────────────────────────────────────────


def compute_jd_similarity(resume_text: str, jd_text: str):
    """
    Compute similarity between resume and job description using TF-IDF.
    """

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform([resume_text, jd_text])

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return float(similarity)


# ── ATS Score Calculation ───────────────────────────────────────────────


def compute_ats_score(
    resume_text: str,
    skills: list,
    experience_years: float = 0,
    education: str = "",
    jd_text: str = None
):
    """
    Compute ATS score using weighted scoring system.
    """

    score = 0

    breakdown = {}

    # ── Skill Match (25%) ─────────────────────────

    skill_score = min(len(skills) * 3, 25)

    breakdown["skills"] = round(skill_score, 2)

    score += skill_score

    # ── Experience Score (20%) ────────────────────

    exp_score = min(experience_years * 5, 20)

    breakdown["experience"] = round(exp_score, 2)

    score += exp_score

    # ── Education Score (10%) ─────────────────────

    if education:
        edu_score = 10
    else:
        edu_score = 5

    breakdown["education"] = edu_score

    score += edu_score

    # ── Keyword Density (15%) ─────────────────────

    keyword_score = min(len(skills), 15)

    breakdown["keywords"] = round(keyword_score, 2)

    score += keyword_score

    # ── Job Description Matching (20%) ────────────

    if jd_text:

        similarity = compute_jd_similarity(resume_text, jd_text)

        jd_score = similarity * 20

    else:

        jd_score = 0

    breakdown["jd_match"] = round(jd_score, 2)

    score += jd_score

    # ── Section Completeness (10%) ────────────────

    section_count = detect_sections(resume_text)

    section_score = min(section_count * 2, 10)

    breakdown["sections"] = round(section_score, 2)

    score += section_score

    return {
        "score": int(round(score)),
        "breakdown": breakdown
    }