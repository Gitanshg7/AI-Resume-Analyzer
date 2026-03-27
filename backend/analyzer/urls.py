"""URL routes for the analyzer app."""

from django.urls import path
from .views import ResumeUploadView, ResumeDetailView

urlpatterns = [
    path("upload-resume/", ResumeUploadView.as_view(), name="upload-resume"),
    path("resume/<str:resume_id>/", ResumeDetailView.as_view(), name="resume-detail"),
]
