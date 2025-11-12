/**
 * Performance Logger Component for React Frontend
 * Displays real-time grading performance metrics
 */

import React, { useState, useEffect } from 'react';
import './performance_logger.css';

export const PerformanceLogger = () => {
  const [metrics, setMetrics] = useState({
    one_word: [],
    list: [],
    numerical: [],
    short_phrase: []
  });

  const [isCollecting, setIsCollecting] = useState(true);
  const [showDetails, setShowDetails] = useState(true);

  useEffect(() => {
    // Listen for grading events
    const handleGradingComplete = (event) => {
      const { questionType, timeMs } = event.detail;
      
      setMetrics(prev => ({
        ...prev,
        [questionType]: [...prev[questionType], timeMs]
      }));
    };

    window.addEventListener('grading-complete', handleGradingComplete);

    // Make the logging function globally available
    window.logGrading = (questionType, timeMs) => {
      console.log(`⏱️  ${questionType}: ${timeMs}ms`);
      window.dispatchEvent(new CustomEvent('grading-complete', { 
        detail: { questionType, timeMs } 
      }));
    };

    return () => {
      window.removeEventListener('grading-complete', handleGradingComplete);
    };
  }, []);

  const calculateStats = (times) => {
    if (times.length === 0) return null;
    
    const sum = times.reduce((a, b) => a + b, 0);
    const avg = sum / times.length;
    const min = Math.min(...times);
    const max = Math.max(...times);
    const median = [...times].sort((a, b) => a - b)[Math.floor(times.length / 2)];
    
    return { 
      avg: avg.toFixed(2), 
      min: min.toFixed(2), 
      max: max.toFixed(2),
      median: median.toFixed(2),
      count: times.length,
      total: sum.toFixed(2)
    };
  };

  const exportMetrics = () => {
    const stats = {};
    
    Object.entries(metrics).forEach(([type, times]) => {
      stats[type] = calculateStats(times);
    });
    
    const exportData = {
      metrics: stats,
      raw_data: metrics,
      timestamp: new Date().toISOString(),
      metadata: {
        browser: navigator.userAgent,
        collected_at: new Date().toLocaleString()
      }
    };
    
    // Log to console
    console.log('📊 Performance Metrics for Abstract:');
    console.table(stats);
    
    // Download as JSON
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { 
      type: 'application/json' 
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `grading_performance_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    alert('Metrics exported! Check your downloads folder.');
  };

  const clearMetrics = () => {
    if (window.confirm('Clear all collected metrics?')) {
      setMetrics({
        one_word: [],
        list: [],
        numerical: [],
        short_phrase: []
      });
    }
  };

  const formatQuestionType = (type) => {
    const labels = {
      one_word: '📝 One-Word',
      list: '📋 List',
      numerical: '🔢 Numerical',
      short_phrase: '🤖 Short-Phrase (AI)'
    };
    return labels[type] || type;
  };

  const getTotalSamples = () => {
    return Object.values(metrics).reduce((sum, times) => sum + times.length, 0);
  };

  return (
    <div className={`performance-logger ${showDetails ? 'expanded' : 'collapsed'}`}>
      <div className="logger-header">
        <h4>📊 Performance Metrics</h4>
        <div className="header-controls">
          <button 
            className="toggle-btn"
            onClick={() => setShowDetails(!showDetails)}
            title={showDetails ? 'Collapse' : 'Expand'}
          >
            {showDetails ? '−' : '+'}
          </button>
        </div>
      </div>

      {showDetails && (
        <>
          <div className="logger-status">
            <span className={`status-indicator ${isCollecting ? 'collecting' : 'paused'}`}>
              {isCollecting ? '🔴 Collecting' : '⏸️ Paused'}
            </span>
            <span className="sample-count">
              {getTotalSamples()} samples
            </span>
          </div>

          <div className="metrics-list">
            {Object.entries(metrics).map(([type, times]) => {
              const stats = calculateStats(times);
              if (!stats) return null;

              return (
                <div key={type} className="metric-item">
                  <div className="metric-header">
                    <strong>{formatQuestionType(type)}</strong>
                    <span className="sample-count">{stats.count}</span>
                  </div>
                  <div className="metric-stats">
                    <div className="stat">
                      <span className="stat-label">Avg:</span>
                      <span className="stat-value">{stats.avg}ms</span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">Min:</span>
                      <span className="stat-value">{stats.min}ms</span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">Max:</span>
                      <span className="stat-value">{stats.max}ms</span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">Median:</span>
                      <span className="stat-value">{stats.median}ms</span>
                    </div>
                  </div>
                  
                  {/* Visual bar for comparison */}
                  <div className="metric-bar">
                    <div 
                      className="metric-bar-fill"
                      style={{ 
                        width: `${Math.min((parseFloat(stats.avg) / 5000) * 100, 100)}%` 
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>

          <div className="logger-actions">
            <button 
              className="btn-primary"
              onClick={exportMetrics}
              disabled={getTotalSamples() === 0}
            >
              📥 Export Metrics
            </button>
            <button 
              className="btn-secondary"
              onClick={clearMetrics}
              disabled={getTotalSamples() === 0}
            >
              🗑️ Clear
            </button>
            <button 
              className="btn-secondary"
              onClick={() => setIsCollecting(!isCollecting)}
            >
              {isCollecting ? '⏸️ Pause' : '▶️ Resume'}
            </button>
          </div>

          <div className="logger-footer">
            <small>
              Use exported data for your abstract/research paper
            </small>
          </div>
        </>
      )}
    </div>
  );
};

export default PerformanceLogger;
