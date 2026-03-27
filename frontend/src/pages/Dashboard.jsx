import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import ResumeScoreCard from '../components/ResumeScoreCard';
import SkillsList from '../components/SkillsList';
import SuggestionsPanel from '../components/SuggestionsPanel';

/**
 * Dashboard Page — Full analysis results
 */
export default function Dashboard({ data, onReset }) {
  if (!data) return null;

  const {
    file_name = '',
    email = '',
    phone = '',
    score = 0,
    skills = [],
    education = '',
    experience_years = 0,
    analysis = {},
  } = data;

  const {
    score_breakdown = {},
    suggestions = [],
    sections_count = 0,
  } = analysis;

  // Pie chart data for score breakdown
  const pieData = Object.entries(score_breakdown)
    .filter(([, v]) => v > 0)
    .map(([key, value]) => ({
      name: formatLabel(key),
      value: parseFloat(value.toFixed(1)),
    }));

  const COLORS = ['#6c63ff', '#ff6584', '#00d68f', '#ffaa00', '#38bdf8', '#a78bfa'];

  return (
    <div className="min-h-screen px-4 py-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 animate-fade-in">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Analysis Results</h1>
          <p className="text-sm mt-1" style={{ color: 'var(--color-text-muted)' }}>
            📄 {file_name}
          </p>
        </div>
        <button onClick={onReset} className="btn-primary mt-4 md:mt-0">
          ← Analyze Another Resume
        </button>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatCard icon="📊" label="ATS Score" value={`${Math.round(score)}/100`} color="var(--color-accent-primary)" delay={1} />
        <StatCard icon="🎯" label="Skills Found" value={skills.length} color="var(--color-accent-info)" delay={2} />
        <StatCard icon="💼" label="Experience" value={`${experience_years} yrs`} color="var(--color-accent-success)" delay={3} />
        <StatCard icon="🎓" label="Education" value={education || 'Not detected'} color="var(--color-accent-warning)" delay={4} small />
      </div>

      {/* Contact Info */}
      {(email || phone) && (
        <div className="glass-card p-4 mb-8 flex flex-wrap gap-6 animate-fade-in animate-fade-in-delay-1">
          {email && (
            <div className="flex items-center gap-2 text-sm">
              <span>📧</span>
              <span style={{ color: 'var(--color-text-secondary)' }}>{email}</span>
            </div>
          )}
          {phone && (
            <div className="flex items-center gap-2 text-sm">
              <span>📱</span>
              <span style={{ color: 'var(--color-text-secondary)' }}>{phone}</span>
            </div>
          )}
          <div className="flex items-center gap-2 text-sm">
            <span>📋</span>
            <span style={{ color: 'var(--color-text-secondary)' }}>
              Sections detected: {sections_count} / 5
            </span>
          </div>
        </div>
      )}

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Score Card */}
        <ResumeScoreCard score={score} breakdown={score_breakdown} />

        {/* Pie Chart */}
        <div className="glass-card p-6 animate-fade-in animate-fade-in-delay-1" id="score-pie-chart">
          <h2 className="text-xl font-bold mb-4 gradient-text">Score Distribution</h2>
          {pieData.length > 0 ? (
            <div style={{ width: '100%', height: 260 }}>
              <ResponsiveContainer>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    dataKey="value"
                    paddingAngle={3}
                    strokeWidth={0}
                  >
                    {pieData.map((_, index) => (
                      <Cell key={index} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      background: '#1a1a2e',
                      border: '1px solid rgba(255,255,255,0.1)',
                      borderRadius: 8,
                      color: '#e4e4f0',
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p style={{ color: 'var(--color-text-muted)' }}>No data available</p>
          )}
          {/* Legend */}
          <div className="flex flex-wrap gap-3 mt-4 justify-center">
            {pieData.map((entry, index) => (
              <div key={index} className="flex items-center gap-1.5 text-xs">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ background: COLORS[index % COLORS.length] }}
                />
                <span style={{ color: 'var(--color-text-secondary)' }}>{entry.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Skills */}
        <SkillsList skills={skills} />

        {/* Suggestions (full width) */}
        <div className="lg:col-span-2">
          <SuggestionsPanel suggestions={suggestions} />
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, color, delay = 0, small = false }) {
  return (
    <div className={`glass-card p-5 text-center animate-fade-in animate-fade-in-delay-${delay}`}>
      <div className="text-2xl mb-2">{icon}</div>
      <div
        className={`font-bold mb-1 ${small ? 'text-sm' : 'text-2xl'}`}
        style={{ color }}
      >
        {value}
      </div>
      <div className="text-xs" style={{ color: 'var(--color-text-muted)' }}>{label}</div>
    </div>
  );
}

function formatLabel(key) {
  const labels = {
    skills: 'Skills',
    experience: 'Experience',
    education: 'Education',
    keywords: 'Keywords',
    jd_match: 'JD Match',
    sections: 'Sections',
  };
  return labels[key] || key;
}
