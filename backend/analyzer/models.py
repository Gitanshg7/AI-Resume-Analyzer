"""
MongoEngine document models for resume storage and analysis results.
Uses MongoEngine ODM (not Django ORM) for MongoDB Atlas.
"""

import datetime
from mongoengine import (
    Document,
    StringField,
    ListField,
    FloatField,
    IntField,
    DictField,
    DateTimeField,
    ReferenceField,
    CASCADE,
)


class Resume(Document):
    """
    Stores uploaded resume data and extracted information.
    """

    file_name = StringField(required=True, max_length=255)
    parsed_text = StringField(default="")
    email = StringField(default="")
    phone = StringField(default="")
    skills = ListField(StringField(), default=list)
    education = StringField(default="")
    experience_years = FloatField(default=0.0)
    score = FloatField(default=0.0)
    uploaded_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        "collection": "resumes",
        "ordering": ["-uploaded_at"],
    }

    def __str__(self):
        return f"Resume({self.file_name}, score={self.score})"


class ResumeAnalysis(Document):
    """
    Stores detailed ATS analysis results linked to a Resume.
    """

    resume = ReferenceField(Resume, required=True, reverse_delete_rule=CASCADE)
    suggestions = ListField(StringField(), default=list)
    score_breakdown = DictField(default=dict)
    sections_count = IntField(default=0)
    job_description = StringField(default="")
    analyzed_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        "collection": "resume_analyses",
        "ordering": ["-analyzed_at"],
    }

    def __str__(self):
        return f"Analysis(resume={self.resume.file_name})"
