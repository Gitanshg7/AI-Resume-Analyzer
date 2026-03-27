import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadResume } from '../services/api';

/**
 * ResumeUpload Component
 * Drag-and-drop resume upload with optional job description and progress indicator.
 */
export default function ResumeUpload({ onAnalysisComplete }) {
    const [uploading, setUploading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [error, setError] = useState('');
    const [jobDescription, setJobDescription] = useState('');
    const [fileName, setFileName] = useState('');

    const onDrop = useCallback(async (acceptedFiles) => {
        if (acceptedFiles.length === 0) return;

        const file = acceptedFiles[0];
        const ext = file.name.split('.').pop().toLowerCase();

        // Validate file type
        if (!['pdf', 'docx'].includes(ext)) {
            setError('Only PDF and DOCX files are supported.');
            return;
        }

        // Validate file size (10 MB)
        if (file.size > 10 * 1024 * 1024) {
            setError('File size exceeds 10 MB limit.');
            return;
        }

        setFileName(file.name);
        setError('');
        setUploading(true);
        setProgress(0);

        try {
            const result = await uploadResume(file, jobDescription, (pct) => setProgress(pct));
            setUploading(false);
            setProgress(100);
            if (onAnalysisComplete) {
                onAnalysisComplete(result);
            }
        } catch (err) {
            setUploading(false);
            setProgress(0);
            const msg = err.response?.data?.error || err.response?.data?.details?.file?.[0] || 'Upload failed. Please try again.';
            setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
        }
    }, [jobDescription, onAnalysisComplete]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
        },
        maxFiles: 1,
        disabled: uploading,
    });

    return (
        <div className="w-full max-w-2xl mx-auto">
            {/* Dropzone */}
            <div
                {...getRootProps()}
                id="resume-dropzone"
                className={`dropzone ${isDragActive ? 'active' : ''} ${uploading ? 'opacity-50 pointer-events-none' : ''}`}
            >
                <input {...getInputProps()} />
                <div className="flex flex-col items-center gap-4">
                    <div className="text-5xl">📄</div>
                    {isDragActive ? (
                        <p className="text-lg" style={{ color: 'var(--color-accent-primary)' }}>
                            Drop your resume here...
                        </p>
                    ) : (
                        <>
                            <p className="text-lg" style={{ color: 'var(--color-text-primary)' }}>
                                Drag & drop your resume here
                            </p>
                            <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>
                                or click to browse — PDF, DOCX (max 10 MB)
                            </p>
                        </>
                    )}
                    {fileName && !uploading && (
                        <p className="text-sm" style={{ color: 'var(--color-accent-success)' }}>
                            ✓ {fileName}
                        </p>
                    )}
                </div>
            </div>

            {/* Job Description (optional) */}
            <div className="mt-6">
                <label
                    htmlFor="job-description"
                    className="block text-sm font-medium mb-2"
                    style={{ color: 'var(--color-text-secondary)' }}
                >
                    Job Description (optional — improves ATS matching)
                </label>
                <textarea
                    id="job-description"
                    rows={4}
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    placeholder="Paste the job description here to compare against your resume..."
                    disabled={uploading}
                    className="w-full p-4 rounded-xl text-sm resize-none focus:outline-none focus:ring-2"
                    style={{
                        background: 'var(--color-bg-glass)',
                        border: '1px solid var(--color-border-glass)',
                        color: 'var(--color-text-primary)',
                        focusRingColor: 'var(--color-accent-primary)',
                    }}
                />
            </div>

            {/* Progress Bar */}
            {uploading && (
                <div className="mt-6 animate-fade-in">
                    <div className="flex justify-between text-sm mb-2">
                        <span style={{ color: 'var(--color-text-secondary)' }}>Analyzing {fileName}...</span>
                        <span style={{ color: 'var(--color-accent-primary)' }}>{progress}%</span>
                    </div>
                    <div className="progress-bar-track">
                        <div className="progress-bar-fill" style={{ width: `${progress}%` }} />
                    </div>
                </div>
            )}

            {/* Error Message */}
            {error && (
                <div
                    className="mt-4 p-4 rounded-xl text-sm animate-fade-in"
                    style={{
                        background: 'rgba(255, 101, 132, 0.1)',
                        border: '1px solid rgba(255, 101, 132, 0.3)',
                        color: 'var(--color-accent-secondary)',
                    }}
                >
                    ⚠ {error}
                </div>
            )}
        </div>
    );
}
