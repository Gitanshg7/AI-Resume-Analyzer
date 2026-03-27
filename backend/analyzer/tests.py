"""
Unit tests for the analyzer services.

Tests cover:
    - resume_parser: text cleaning, NLP preprocessing
    - skill_extractor: skill detection from sample text
    - education_extractor: degree and field detection
    - experience_estimator: years extraction
    - ats_scoring: score calculation
"""

import unittest


class TestResumeParser(unittest.TestCase):
    """Test text cleaning and NLP preprocessing."""

    def test_clean_text_lowercase(self):
        from analyzer.services.resume_parser import clean_text

        result = clean_text("Hello WORLD")
        self.assertEqual(result, "hello world")

    def test_clean_text_whitespace(self):
        from analyzer.services.resume_parser import clean_text

        result = clean_text("  hello   world  \n\t test  ")
        self.assertEqual(result, "hello world test")

    def test_clean_text_preserves_plus(self):
        from analyzer.services.resume_parser import clean_text

        result = clean_text("C++ and Node.js")
        self.assertIn("c++", result)
        self.assertIn("node.js", result)

    def test_extract_email(self):
        from analyzer.services.resume_parser import extract_email

        text = "Contact me at john.doe@example.com for details"
        self.assertEqual(extract_email(text), "john.doe@example.com")

    def test_extract_email_none(self):
        from analyzer.services.resume_parser import extract_email

        self.assertEqual(extract_email("no email here"), "")

    def test_extract_phone(self):
        from analyzer.services.resume_parser import extract_phone

        text = "Phone: +1 555-1234567"
        result = extract_phone(text)
        self.assertTrue(len(result) > 0)

    def test_preprocess_nlp(self):
        from analyzer.services.resume_parser import preprocess_nlp

        result = preprocess_nlp("the quick brown foxes are running quickly")
        # Stopwords (the, are) should be removed, words lemmatized
        self.assertNotIn("the", result.split())
        self.assertNotIn("are", result.split())


class TestSkillExtractor(unittest.TestCase):
    """Test skill extraction from sample resume text."""

    def test_extract_known_skills(self):
        from analyzer.services.skill_extractor import extract_skills

        text = (
            "experienced in python, java, react, and machine learning. "
            "also worked with docker."
        )
        skills = extract_skills(text)
        skills_lower = [s.lower() for s in skills]

        self.assertIn("python", skills_lower)
        self.assertIn("java", skills_lower)
        self.assertIn("react", skills_lower)
        self.assertIn("docker", skills_lower)

    def test_multiword_skills(self):
        from analyzer.services.skill_extractor import extract_skills

        text = "deep learning and machine learning are my focus areas"
        skills = extract_skills(text)
        skills_lower = [s.lower() for s in skills]

        self.assertIn("deep learning", skills_lower)
        self.assertIn("machine learning", skills_lower)

    def test_empty_text(self):
        from analyzer.services.skill_extractor import extract_skills

        skills = extract_skills("")
        self.assertEqual(skills, [])


class TestEducationExtractor(unittest.TestCase):
    """Test degree and education detection."""

    def test_detect_btech(self):
        from analyzer.services.education_extractor import detect_degrees

        degrees = detect_degrees("completed b.tech in computer science")
        self.assertIn("B.Tech", degrees)

    def test_detect_mba(self):
        from analyzer.services.education_extractor import detect_degrees

        degrees = detect_degrees("holds an mba from harvard")
        self.assertIn("MBA", degrees)

    def test_detect_phd(self):
        from analyzer.services.education_extractor import detect_degrees

        degrees = detect_degrees("pursuing ph.d. in ai")
        self.assertIn("PhD", degrees)

    def test_extract_education_full(self):
        from analyzer.services.education_extractor import extract_education

        text = "b.tech in computer science from iit delhi"
        result = extract_education(text)
        self.assertIn("B.Tech", result)

    def test_empty_education(self):
        from analyzer.services.education_extractor import extract_education

        result = extract_education("hello world nothing here")
        self.assertEqual(result, "")


class TestExperienceEstimator(unittest.TestCase):
    """Test experience year estimation."""

    def test_explicit_years(self):
        from analyzer.services.experience_estimator import estimate_experience

        text = "i have 5 years of experience in software development"
        self.assertEqual(estimate_experience(text), 5.0)

    def test_explicit_plus(self):
        from analyzer.services.experience_estimator import estimate_experience

        text = "3+ years experience in python"
        self.assertEqual(estimate_experience(text), 3.0)

    def test_date_range(self):
        from analyzer.services.experience_estimator import estimate_experience

        text = "software engineer 2020 - 2023 at google"
        result = estimate_experience(text)
        self.assertGreaterEqual(result, 2.0)

    def test_no_experience(self):
        from analyzer.services.experience_estimator import estimate_experience

        result = estimate_experience("fresh graduate looking for opportunities")
        self.assertEqual(result, 0.0)


class TestATSScoring(unittest.TestCase):
    """Test ATS score calculation."""

    def test_score_range(self):
        from analyzer.services.ats_scoring import compute_ats_score

        result = compute_ats_score(
            resume_text="python java react sql git docker experience education skills projects",
            skills=["Python", "Java", "React"],
            education="B.Tech Computer Science",
            experience_years=3.0,
        )
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

    def test_breakdown_keys(self):
        from analyzer.services.ats_scoring import compute_ats_score

        result = compute_ats_score(
            resume_text="test text",
            skills=[],
            education="",
            experience_years=0,
        )
        expected_keys = {"skills", "experience", "education", "keywords", "jd_match", "sections"}
        self.assertEqual(set(result["breakdown"].keys()), expected_keys)

    def test_with_job_description(self):
        from analyzer.services.ats_scoring import compute_ats_score

        result = compute_ats_score(
            resume_text="python machine learning data analysis sql",
            skills=["Python", "Machine Learning", "Sql"],
            education="M.Sc Data Science",
            experience_years=2.0,
            jd_text="looking for python developer with machine learning experience and sql skills",
        )
        self.assertGreater(result["breakdown"]["jd_match"], 0)

    def test_section_detection(self):
        from analyzer.services.ats_scoring import detect_sections

        text = "education: btech from iit. experience: 3 years at google. skills: python java"
        count = detect_sections(text)
        self.assertGreaterEqual(count, 3)

    def test_score_returns_dict(self):
        from analyzer.services.ats_scoring import compute_ats_score

        result = compute_ats_score(
            resume_text="test",
            skills=[],
            education="",
            experience_years=0,
        )
        self.assertIn("score", result)
        self.assertIn("breakdown", result)
        self.assertIsInstance(result["score"], int)
        self.assertIsInstance(result["breakdown"], dict)


if __name__ == "__main__":
    unittest.main()
