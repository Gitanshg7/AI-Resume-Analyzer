"""
API views for the analyzer app.

Endpoints:
    POST /api/upload-resume/   – Upload and analyze a resume
    GET  /api/resume/<id>/     – Retrieve stored analysis by resume id
"""

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Resume, ResumeAnalysis
from .serializers import (
    ResumeUploadSerializer,
    serialize_resume,
    serialize_analysis,
)
from .services.resume_parser import parse_file, clean_text, extract_email, extract_phone, preprocess_nlp
from .services.skill_extractor import extract_skills
from .services.education_extractor import extract_education
from .services.experience_estimator import estimate_experience
from .services.ats_scoring import compute_ats_score, detect_sections
from .services.suggestion_engine import generate_suggestions

logger = logging.getLogger(__name__)


class ResumeUploadView(APIView):
    """
    POST /api/upload-resume/

    Accepts a resume file (PDF/DOCX) and an optional job description.
    Parses, analyzes, scores, and stores the results in MongoDB.
    Returns the full analysis as JSON.
    """

    def post(self, request):
        serializer = ResumeUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Validation failed", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        uploaded_file = serializer.validated_data["file"]
        job_description = serializer.validated_data.get("job_description", "")

        try:
            # 1. Parse file → raw text
            raw_text = parse_file(uploaded_file)
            if not raw_text.strip():
                return Response(
                    {"error": "Could not extract text from the uploaded file."},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            # 2. Clean and preprocess
            cleaned = clean_text(raw_text)
            preprocessed = preprocess_nlp(cleaned)

            # 3. Extract structured data
            email = extract_email(raw_text)
            phone = extract_phone(raw_text)
            skills = extract_skills(cleaned)
            education = extract_education(cleaned)
            experience_years = estimate_experience(cleaned)

            # 4. ATS scoring
            score_result = compute_ats_score(
                resume_text=cleaned,
                skills=skills,
                education=education,
                experience_years=experience_years,
                jd_text=job_description if job_description else None,
            )

            # 5. Detect sections (returns int count)
            sections_count = detect_sections(cleaned)

            # 6. Generate suggestions
            suggestions = generate_suggestions(
                skills=skills,
                education=education,
                experience_years=experience_years,
                score_breakdown=score_result["breakdown"],
                sections_count=sections_count,
            )

            # 7. Save to MongoDB
            resume_doc = Resume(
                file_name=uploaded_file.name,
                parsed_text=cleaned,
                email=email,
                phone=phone,
                skills=skills,
                education=education,
                experience_years=experience_years,
                score=score_result["score"],
            )
            resume_doc.save()

            analysis_doc = ResumeAnalysis(
                resume=resume_doc,
                suggestions=suggestions,
                score_breakdown=score_result["breakdown"],
                sections_count=sections_count,
                job_description=job_description,
            )
            analysis_doc.save()

            # 8. Build response
            response_data = {
                **serialize_resume(resume_doc),
                "analysis": serialize_analysis(analysis_doc),
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as exc:
            logger.exception("Resume analysis failed")
            return Response(
                {"error": f"Analysis failed: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ResumeDetailView(APIView):
    """
    GET /api/resume/<id>/

    Retrieves a previously analyzed resume and its analysis by resume ID.
    """

    def get(self, request, resume_id):
        try:
            resume_doc = Resume.objects.get(id=resume_id)
        except Resume.DoesNotExist:
            return Response(
                {"error": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            return Response(
                {"error": "Invalid resume ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch linked analysis
        analysis_doc = ResumeAnalysis.objects(resume=resume_doc).first()
        response_data = serialize_resume(resume_doc)
        if analysis_doc:
            response_data["analysis"] = serialize_analysis(analysis_doc)

        return Response(response_data, status=status.HTTP_200_OK)
