import { useEffect, useState } from 'react';

/**
 * ResumeScoreCard Component
 * Animated circular SVG score gauge with score breakdown.
 */
export default function ResumeScoreCard({ score = 0, breakdown = {} }) {
    const [animatedScore, setAnimatedScore] = useState(0);

    // Animate the score from 0 to target
    useEffect(() => {
        let start = 0;
        const target = Math.round(score);
        const duration = 1500;
        const stepTime = duration / target || duration;

        const timer = setInterval(() => {
            start += 1;
            if (start >= target) {
                setAnimatedScore(target);
                clearInterval(timer);
            } else {
                setAnimatedScore(start);
            }
        }, stepTime);

        return () => clearInterval(timer);
    }, [score]);

    // SVG circle params
    const radius = 75;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (animatedScore / 100) * circumference;

    // Color based on score
    const getScoreColor = (s) => {
        if (s >= 80) return 'var(--color-accent-success)';
        if (s >= 60) return 'var(--color-accent-warning)';
        return 'var(--color-accent-secondary)';
    };

    const scoreColor = getScoreColor(animatedScore);

    return (
        <div className="glass-card p-8 animate-fade-in" id="score-card">
            <h2 className="text-xl font-bold mb-6 gradient-text">ATS Resume Score</h2>

            <div className="flex flex-col items-center gap-6 md:flex-row md:items-start">
                {/* Score Ring */}
                <div className="score-ring flex-shrink-0">
                    <svg width="180" height="180" viewBox="0 0 180 180">
                        {/* Background ring */}
                        <circle
                            cx="90" cy="90" r={radius}
                            fill="none"
                            stroke="rgba(255,255,255,0.08)"
                            strokeWidth="12"
                        />
                        {/* Score ring */}
                        <circle
                            cx="90" cy="90" r={radius}
                            fill="none"
                            stroke={scoreColor}
                            strokeWidth="12"
                            strokeLinecap="round"
                            strokeDasharray={circumference}
                            strokeDashoffset={offset}
                            style={{ transition: 'stroke-dashoffset 1.5s ease-out' }}
                        />
                    </svg>
                    <div className="score-value" style={{ color: scoreColor }}>
                        {animatedScore}
                    </div>
                </div>

                {/* Breakdown */}
                <div className="flex-1 w-full">
                    <h3 className="text-sm font-semibold mb-4" style={{ color: 'var(--color-text-secondary)' }}>
                        Score Breakdown
                    </h3>
                    <div className="space-y-3">
                        {Object.entries(breakdown).map(([key, value]) => (
                            <BreakdownBar key={key} label={formatLabel(key)} value={value} max={getMaxForKey(key)} />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

function formatLabel(key) {
    const labels = {
        skills: 'Skill Match',
        experience: 'Experience',
        education: 'Education',
        keywords: 'Keyword Density',
        jd_match: 'JD Match',
        sections: 'Sections',
    };
    return labels[key] || key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function getMaxForKey(key) {
    const maxes = { skills: 25, experience: 20, education: 10, keywords: 15, jd_match: 20, sections: 10 };
    return maxes[key] || 25;
}

function BreakdownBar({ label, value, max }) {
    const pct = max > 0 ? Math.min((value / max) * 100, 100) : 0;

    return (
        <div>
            <div className="flex justify-between text-sm mb-1">
                <span style={{ color: 'var(--color-text-secondary)' }}>{label}</span>
                <span style={{ color: 'var(--color-text-primary)' }}>
                    {value.toFixed(1)} / {max}
                </span>
            </div>
            <div className="progress-bar-track">
                <div
                    className="progress-bar-fill"
                    style={{ width: `${pct}%`, transition: 'width 1s ease-out' }}
                />
            </div>
        </div>
    );
}
