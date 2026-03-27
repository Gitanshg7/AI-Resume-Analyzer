"""
Suggestion Engine Module
========================
Generates dynamic, actionable improvement suggestions based on
the resume analysis results.
"""

from typing import List, Dict


# ── Suggestion Rules ─────────────────────────────────────────────────────

IMPORTANT_SKILLS = [
    "Python", "Java", "Javascript", "React", "Node.Js",
    "Sql", "Git", "Docker", "Aws", "Machine Learning",
]


def generate_suggestions(
    skills: List[str],
    education: str,
    experience_years: float,
    score_breakdown: Dict[str, float],
    sections_count: int = 0,
) -> List[str]:
    """
    Generate dynamic resume improvement suggestions.

    Args:
        skills: List of detected skills.
        education: Education summary string.
        experience_years: Estimated years of experience.
        score_breakdown: Dict of sub-scores from ATS scoring.
        sections_count: Number of detected resume sections (int).

    Returns:
        List of actionable suggestion strings.
    """
    suggestions = []

    # ── Section completeness ─────────────────────────────────────────
    if sections_count < 4:
        suggestions.append(
            "Your resume is missing key sections. A complete resume typically "
            "includes: Education, Experience, Skills, Projects, and Certifications."
        )

    # ── Skills suggestions ───────────────────────────────────────────
    skills_lower = {s.lower() for s in skills}
    missing_important = [
        s for s in IMPORTANT_SKILLS
        if s.lower() not in skills_lower
    ]

    if len(skills) < 5:
        suggestions.append(
            "Your resume lists very few skills. Add more relevant technical "
            "skills to improve your ATS score."
        )

    if missing_important:
        top_missing = missing_important[:5]
        suggestions.append(
            f"Consider adding these in-demand skills if applicable: "
            f"{', '.join(top_missing)}."
        )

    # ── Education suggestions ────────────────────────────────────────
    if not education:
        suggestions.append(
            "No education details detected. Include your highest degree, "
            "major, and university name."
        )

    # ── Experience suggestions ───────────────────────────────────────
    if experience_years == 0:
        suggestions.append(
            "No work experience detected. Add your work history with dates, "
            "job titles, and measurable achievements."
        )
    elif experience_years < 2:
        suggestions.append(
            "Limited experience detected. Highlight internships, freelance "
            "work, or academic projects to strengthen this section."
        )

    # ── Score-based suggestions ──────────────────────────────────────
    if score_breakdown.get("keywords", 0) < 10:
        suggestions.append(
            "Your resume has low keyword density. Use more industry-standard "
            "terms and buzzwords relevant to your target role."
        )

    if score_breakdown.get("jd_match", 0) < 10 and score_breakdown.get("jd_match") is not None:
        suggestions.append(
            "Your resume has low alignment with the job description. Tailor "
            "your resume content to match the job requirements."
        )

    # ── General best practices ───────────────────────────────────────
    if "github" not in " ".join(skills).lower():
        suggestions.append(
            "Include links to your GitHub profile or portfolio website."
        )

    suggestions.append(
        "Use measurable achievements (e.g., 'Reduced API latency by 40%') "
        "instead of generic descriptions."
    )

    suggestions.append(
        "Keep your resume to 1-2 pages and use a clean, ATS-friendly format "
        "without complex tables or graphics."
    )

    return suggestions
