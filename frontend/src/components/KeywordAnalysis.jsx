import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

/**
 * KeywordAnalysis Component
 * Bar chart showing matched vs missing keywords.
 */
export default function KeywordAnalysis({ keywordMatches = [], missingKeywords = [] }) {
    const matchedData = keywordMatches.map((kw) => ({
        name: kw.replace(/\b\w/g, c => c.toUpperCase()),
        status: 'matched',
        value: 1,
    }));

    const missingData = missingKeywords.slice(0, 10).map((kw) => ({
        name: kw.replace(/\b\w/g, c => c.toUpperCase()),
        status: 'missing',
        value: 1,
    }));

    const chartData = [...matchedData, ...missingData];

    return (
        <div className="glass-card p-6 animate-fade-in animate-fade-in-delay-4" id="keyword-analysis">
            <h2 className="text-xl font-bold mb-2 gradient-text">Keyword Analysis</h2>
            <p className="text-sm mb-6" style={{ color: 'var(--color-text-muted)' }}>
                ATS keyword match breakdown
            </p>

            {/* Summary stats */}
            <div className="grid grid-cols-2 gap-4 mb-6">
                <div
                    className="p-4 rounded-xl text-center"
                    style={{ background: 'rgba(0, 214, 143, 0.1)', border: '1px solid rgba(0, 214, 143, 0.2)' }}
                >
                    <div className="text-2xl font-bold" style={{ color: 'var(--color-accent-success)' }}>
                        {keywordMatches.length}
                    </div>
                    <div className="text-xs mt-1" style={{ color: 'var(--color-text-muted)' }}>
                        Keywords Found
                    </div>
                </div>
                <div
                    className="p-4 rounded-xl text-center"
                    style={{ background: 'rgba(255, 101, 132, 0.1)', border: '1px solid rgba(255, 101, 132, 0.2)' }}
                >
                    <div className="text-2xl font-bold" style={{ color: 'var(--color-accent-secondary)' }}>
                        {missingKeywords.length}
                    </div>
                    <div className="text-xs mt-1" style={{ color: 'var(--color-text-muted)' }}>
                        Keywords Missing
                    </div>
                </div>
            </div>

            {/* Bar chart */}
            {chartData.length > 0 && (
                <div style={{ width: '100%', height: 280 }}>
                    <ResponsiveContainer>
                        <BarChart data={chartData} layout="vertical" margin={{ left: 20, right: 20 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                            <XAxis type="number" hide />
                            <YAxis
                                type="category"
                                dataKey="name"
                                width={120}
                                tick={{ fill: '#a0a0c0', fontSize: 12 }}
                            />
                            <Tooltip
                                contentStyle={{
                                    background: '#1a1a2e',
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    borderRadius: 8,
                                    color: '#e4e4f0',
                                }}
                                formatter={(value, name, props) =>
                                    [props.payload.status === 'matched' ? '✓ Found' : '✗ Missing', 'Status']
                                }
                            />
                            <Bar dataKey="value" radius={[0, 6, 6, 0]} barSize={16}>
                                {chartData.map((entry, index) => (
                                    <Cell
                                        key={index}
                                        fill={entry.status === 'matched' ? '#00d68f' : '#ff6584'}
                                        fillOpacity={0.8}
                                    />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            )}

            {/* Keyword lists */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                <div>
                    <h4 className="text-sm font-semibold mb-2" style={{ color: 'var(--color-accent-success)' }}>
                        ✓ Matched Keywords
                    </h4>
                    <div className="flex flex-wrap gap-1.5">
                        {keywordMatches.map((kw, i) => (
                            <span
                                key={i}
                                className="text-xs px-2 py-1 rounded-full"
                                style={{ background: 'rgba(0, 214, 143, 0.15)', color: '#00d68f' }}
                            >
                                {kw}
                            </span>
                        ))}
                    </div>
                </div>
                <div>
                    <h4 className="text-sm font-semibold mb-2" style={{ color: 'var(--color-accent-secondary)' }}>
                        ✗ Missing Keywords
                    </h4>
                    <div className="flex flex-wrap gap-1.5">
                        {missingKeywords.slice(0, 10).map((kw, i) => (
                            <span
                                key={i}
                                className="text-xs px-2 py-1 rounded-full"
                                style={{ background: 'rgba(255, 101, 132, 0.15)', color: '#ff6584' }}
                            >
                                {kw}
                            </span>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
