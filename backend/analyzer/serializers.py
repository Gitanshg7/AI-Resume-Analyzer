"""
DRF Serializers for the analyzer app.

Since MongoEngine does not use the Django ORM, we use plain
serializers.Serializer (NOT ModelSerializer) with explicit fields
and manual validation.
"""

from rest_framework import serializers

# ── Allowed file types and size limit ────────────────────────────────────
ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class ResumeUploadSerializer(serializers.Serializer):
    """Validates the uploaded resume file and optional job description."""

    file = serializers.FileField(required=True, help_text="PDF or DOCX resume file (max 10 MB)")
    job_description = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        help_text="Optional job description text for ATS matching",
    )

    def validate_file(self, value):
        # Extension check
        ext = value.name.rsplit(".", 1)[-1].lower() if "." in value.name else ""
        if ext not in ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(
                f"Unsupported file type '.{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        # Size check
        if value.size > MAX_FILE_SIZE:
            raise serializers.ValidationError(
                f"File too large ({value.size / 1024 / 1024:.1f} MB). Maximum is 10 MB."
            )
        return value


# ── Helpers for MongoEngine → dict conversion ────────────────────────────


def serialize_resume(doc) -> dict:
    """Convert a Resume MongoEngine document to a plain dictionary."""
    return {
        "id": str(doc.id),
        "file_name": doc.file_name,
        "email": doc.email,
        "phone": doc.phone,
        "skills": doc.skills,
        "education": doc.education,
        "experience_years": doc.experience_years,
        "score": doc.score,
        "uploaded_at": doc.uploaded_at.isoformat() if doc.uploaded_at else None,
    }


def serialize_analysis(doc) -> dict:
    """Convert a ResumeAnalysis MongoEngine document to a plain dictionary."""
    return {
        "id": str(doc.id),
        "resume_id": str(doc.resume.id) if doc.resume else None,
        "suggestions": doc.suggestions,
        "score_breakdown": doc.score_breakdown,
        "sections_count": doc.sections_count,
        "analyzed_at": doc.analyzed_at.isoformat() if doc.analyzed_at else None,
    }
