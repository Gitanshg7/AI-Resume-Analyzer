/**
 * SuggestionsPanel Component
 * Displays resume improvement suggestions with icons and categories.
 */
export default function SuggestionsPanel({ suggestions = [] }) {
    if (suggestions.length === 0) {
        return (
            <div className="glass-card p-6 animate-fade-in animate-fade-in-delay-3" id="suggestions-panel">
                <h2 className="text-xl font-bold mb-4 gradient-text">Improvement Suggestions</h2>
                <p style={{ color: 'var(--color-accent-success)' }}>
                    ✓ Your resume looks great! No major suggestions.
                </p>
            </div>
        );
    }

    return (
        <div className="glass-card p-6 animate-fade-in animate-fade-in-delay-3" id="suggestions-panel">
            <h2 className="text-xl font-bold mb-4 gradient-text">Improvement Suggestions</h2>
            <div className="space-y-3">
                {suggestions.map((suggestion, index) => (
                    <SuggestionItem key={index} text={suggestion} index={index} />
                ))}
            </div>
        </div>
    );
}

function SuggestionItem({ text, index }) {
    const getIcon = (txt) => {
        const lower = txt.toLowerCase();
        if (lower.includes('skill')) return '🎯';
        if (lower.includes('experience') || lower.includes('work')) return '💼';
        if (lower.includes('education') || lower.includes('degree')) return '🎓';
        if (lower.includes('project')) return '🚀';
        if (lower.includes('certif')) return '📜';
        if (lower.includes('keyword')) return '🔑';
        if (lower.includes('format') || lower.includes('page')) return '📐';
        if (lower.includes('github') || lower.includes('portfolio') || lower.includes('link')) return '🔗';
        if (lower.includes('achievement') || lower.includes('measur')) return '📊';
        return '💡';
    };

    return (
        <div
            className="flex items-start gap-3 p-3 rounded-xl transition-all hover:translate-x-1"
            style={{
                background: 'rgba(255, 255, 255, 0.03)',
                borderLeft: '3px solid var(--color-accent-primary)',
            }}
        >
            <span className="text-xl flex-shrink-0 mt-0.5">{getIcon(text)}</span>
            <p className="text-sm leading-relaxed" style={{ color: 'var(--color-text-secondary)' }}>
                {text}
            </p>
        </div>
    );
}
