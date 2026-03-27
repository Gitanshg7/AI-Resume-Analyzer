import { useState } from 'react';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import './index.css';

/**
 * App Component — Root of the AI Resume Analyzer
 * Switches between Home (upload) and Dashboard (results) views.
 */
export default function App() {
  const [analysisData, setAnalysisData] = useState(null);

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleReset = () => {
    setAnalysisData(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="relative overflow-hidden">
      {/* Navigation Bar */}
      <nav
        className="sticky top-0 z-50 px-6 py-4 flex items-center justify-between"
        style={{
          background: 'rgba(15, 15, 26, 0.8)',
          backdropFilter: 'blur(12px)',
          borderBottom: '1px solid var(--color-border-glass)',
        }}
      >
        <div className="flex items-center gap-2">
          <span className="text-2xl">🤖</span>
          <span className="text-lg font-bold gradient-text">AI Resume Analyzer</span>
        </div>
        {analysisData && (
          <button
            onClick={handleReset}
            className="text-sm px-4 py-2 rounded-lg transition-all hover:translate-y-[-1px]"
            style={{
              background: 'var(--color-bg-glass)',
              border: '1px solid var(--color-border-glass)',
              color: 'var(--color-text-secondary)',
            }}
          >
            New Analysis
          </button>
        )}
      </nav>

      {/* Page Content */}
      {analysisData ? (
        <Dashboard data={analysisData} onReset={handleReset} />
      ) : (
        <Home onAnalysisComplete={handleAnalysisComplete} />
      )}

      {/* Footer */}
      <footer className="text-center py-6" style={{ color: 'var(--color-text-muted)' }}>
        <p className="text-sm">
          AI Resume Analyzer — Built with React, Django, spaCy & MongoDB Atlas
        </p>
      </footer>
    </div>
  );
}
