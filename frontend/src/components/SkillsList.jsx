/**
 * SkillsList Component
 * Displays detected skills as a tag cloud.
 */
export default function SkillsList({ skills = [] }) {
    if (skills.length === 0) {
        return (
            <div className="glass-card p-6 animate-fade-in animate-fade-in-delay-2" id="skills-list">
                <h2 className="text-xl font-bold mb-4 gradient-text">Detected Skills</h2>
                <p style={{ color: 'var(--color-text-muted)' }}>No skills detected.</p>
            </div>
        );
    }

    return (
        <div className="glass-card p-6 animate-fade-in animate-fade-in-delay-2" id="skills-list">
            <h2 className="text-xl font-bold mb-4 gradient-text">Detected Skills</h2>
            <div className="flex flex-wrap gap-2">
                {skills.map((skill, index) => (
                    <span key={index} className="skill-tag">
                        {skill}
                    </span>
                ))}
            </div>
            <p className="mt-4 text-sm" style={{ color: 'var(--color-text-muted)' }}>
                {skills.length} skill{skills.length !== 1 ? 's' : ''} detected
            </p>
        </div>
    );
}
