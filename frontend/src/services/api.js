import axios from 'axios';

/**
 * Axios instance pre-configured for the Resume Analyzer API.
 * In production, requests go through Nginx.
 * In dev, Vite proxy forwards /api/ to Django.
 */
const api = axios.create({
    baseURL: '/api',
    timeout: 60000,
    headers: {
        Accept: 'application/json',
    },
});

/**
 * Upload a resume file (and optional job description) for analysis.
 * @param {File} file - The PDF or DOCX resume file.
 * @param {string} [jobDescription=''] - Optional job description text.
 * @param {function} [onProgress] - Upload progress callback (0–100).
 * @returns {Promise<object>} Analysis result from the API.
 */
export async function uploadResume(file, jobDescription = '', onProgress = null) {
    const formData = new FormData();
    formData.append('file', file);
    if (jobDescription) {
        formData.append('job_description', jobDescription);
    }

    const response = await api.post('/upload-resume/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (event) => {
            if (onProgress && event.total) {
                const pct = Math.round((event.loaded * 100) / event.total);
                onProgress(pct);
            }
        },
    });

    return response.data;
}

/**
 * Fetch a previously analyzed resume by its ID.
 * @param {string} resumeId - MongoDB document ID.
 * @returns {Promise<object>} Resume + analysis data.
 */
export async function getResumeAnalysis(resumeId) {
    const response = await api.get(`/resume/${resumeId}/`);
    return response.data;
}

export default api;
