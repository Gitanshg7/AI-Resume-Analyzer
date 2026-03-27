import ResumeUpload from '../components/ResumeUpload';

/**
 * Home Page — Landing with upload CTA
 */
export default function Home({ onAnalysisComplete }) {
    return (
        <div className="min-h-screen flex flex-col">
            {/* Hero Section */}
            <section className="flex-1 flex flex-col items-center justify-center px-4 py-16">
                {/* Background glow effects */}
                <div
                    className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full opacity-20 blur-3xl pointer-events-none"
                    style={{ background: 'radial-gradient(circle, var(--color-accent-primary), transparent)' }}
                />
                <div
                    className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full opacity-15 blur-3xl pointer-events-none"
                    style={{ background: 'radial-gradient(circle, var(--color-accent-secondary), transparent)' }}
                />

                {/* Hero Content */}
                <div className="relative z-10 text-center mb-12 animate-fade-in">
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm mb-6"
                        style={{
                            background: 'rgba(108, 99, 255, 0.1)',
                            border: '1px solid rgba(108, 99, 255, 0.2)',
                            color: 'var(--color-accent-primary)',
                        }}
                    >
                        🤖 AI-Powered Resume Analysis
                    </div>
                    <h1 className="text-5xl md:text-6xl font-extrabold mb-4 leading-tight">
                        <span className="gradient-text">AI Resume</span>
                        <br />
                        <span style={{ color: 'var(--color-text-primary)' }}>Analyzer</span>
                    </h1>
                    <p className="text-lg max-w-xl mx-auto" style={{ color: 'var(--color-text-secondary)' }}>
                        Get instant ATS scoring, skill extraction, and personalized improvement
                        suggestions powered by advanced NLP.
                    </p>
                </div>

                {/* Upload Area */}
                <div className="relative z-10 w-full animate-fade-in animate-fade-in-delay-1">
                    <ResumeUpload onAnalysisComplete={onAnalysisComplete} />
                </div>

                {/* Feature badges */}
                <div className="relative z-10 flex flex-wrap justify-center gap-4 mt-12 animate-fade-in animate-fade-in-delay-2">
                    {[
                        { icon: '📊', label: 'ATS Score' },
                        { icon: '🎯', label: 'Skill Detection' },
                        { icon: '🎓', label: 'Education Analysis' },
                        { icon: '💼', label: 'Experience Estimation' },
                        { icon: '🔑', label: 'Keyword Matching' },
                        { icon: '💡', label: 'Smart Suggestions' },
                    ].map(({ icon, label }) => (
                        <div
                            key={label}
                            className="flex items-center gap-2 px-4 py-2 rounded-full text-sm"
                            style={{
                                background: 'var(--color-bg-glass)',
                                border: '1px solid var(--color-border-glass)',
                                color: 'var(--color-text-secondary)',
                            }}
                        >
                            <span>{icon}</span>
                            <span>{label}</span>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
}
