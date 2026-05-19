/**
 * CAMSPHER-AI Resume Analyzer - React Component
 * 
 * Integration example for your React/Vite website.
 * 
 * Usage:
 *   import ResumeAnalyzer from './ResumeAnalyzer';
 *   <ResumeAnalyzer apiUrl="http://localhost:8000" />
 */

import { useState, useRef } from 'react';

// ========================================
// STYLES (CSS-in-JS for easy copy-paste)
// ========================================
const styles = {
  container: {
    maxWidth: '900px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  },
  card: {
    background: 'white',
    borderRadius: '16px',
    padding: '30px',
    marginBottom: '20px',
    boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
  },
  uploadArea: {
    border: '2px dashed #ddd',
    borderRadius: '12px',
    padding: '40px 20px',
    textAlign: 'center',
    cursor: 'pointer',
    transition: 'all 0.3s',
  },
  uploadAreaHover: {
    borderColor: '#667eea',
    background: '#f8f9ff',
  },
  button: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    padding: '14px 40px',
    borderRadius: '8px',
    fontSize: '16px',
    cursor: 'pointer',
    marginTop: '15px',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  buttonDisabled: {
    opacity: 0.6,
    cursor: 'not-allowed',
  },
  scoreCircle: {
    width: '150px',
    height: '150px',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    margin: '0 auto 20px',
    position: 'relative',
  },
  scoreValue: {
    position: 'relative',
    zIndex: 1,
    fontSize: '36px',
    fontWeight: 'bold',
    color: '#333',
  },
  statGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
    gap: '15px',
    marginBottom: '25px',
  },
  statBox: {
    background: '#f8f9ff',
    borderRadius: '10px',
    padding: '15px',
    textAlign: 'center',
  },
  statValue: {
    fontSize: '28px',
    fontWeight: 'bold',
    color: '#667eea',
  },
  statLabel: {
    fontSize: '12px',
    color: '#888',
    marginTop: '5px',
  },
  skillBar: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '10px',
  },
  skillName: {
    width: '200px',
    fontSize: '14px',
    color: '#444',
  },
  skillProgress: {
    flex: 1,
    height: '20px',
    background: '#f0f0f0',
    borderRadius: '10px',
    overflow: 'hidden',
  },
  skillFill: {
    height: '100%',
    borderRadius: '10px',
    background: 'linear-gradient(90deg, #667eea, #764ba2)',
    transition: 'width 0.8s ease',
  },
  skillScore: {
    width: '50px',
    textAlign: 'right',
    fontSize: '14px',
    fontWeight: 'bold',
    color: '#667eea',
  },
  skillTag: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    padding: '6px 14px',
    borderRadius: '20px',
    fontSize: '13px',
    display: 'inline-block',
    margin: '4px',
  },
  demandTag: {
    background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  },
  recommendation: {
    padding: '12px 15px',
    marginBottom: '10px',
    borderRadius: '0 8px 8px 0',
    borderLeft: '4px solid #f39c12',
    background: '#fff8e6',
  },
  recHigh: {
    borderLeftColor: '#e74c3c',
    background: '#fdeaea',
  },
  recLow: {
    borderLeftColor: '#27ae60',
    background: '#e8f8e8',
  },
  sectionTitle: {
    fontSize: '18px',
    fontWeight: 'bold',
    margin: '25px 0 15px',
    paddingBottom: '8px',
    borderBottom: '2px solid #f0f0f0',
  },
  error: {
    background: '#fdeaea',
    color: '#e74c3c',
    padding: '15px',
    borderRadius: '8px',
    marginBottom: '15px',
  },
  spinner: {
    display: 'inline-block',
    width: '20px',
    height: '20px',
    border: '3px solid #fff',
    borderTopColor: 'transparent',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
    marginRight: '8px',
    verticalAlign: 'middle',
  },
};

// ========================================
// COMPONENT
// ========================================
export default function ResumeAnalyzer({ apiUrl = 'http://localhost:8000' }) {
  const [activeTab, setActiveTab] = useState('file');
  const [file, setFile] = useState(null);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0]);
      setError('');
    }
  };

  const handleAnalyze = async () => {
    setError('');
    setLoading(true);

    try {
      let response;

      if (activeTab === 'file') {
        if (!file) throw new Error('Please select a resume file');
        
        const formData = new FormData();
        formData.append('file', file);

        response = await fetch(`${apiUrl}/api/analyze/file`, {
          method: 'POST',
          body: formData,
        });
      } else {
        if (!text.trim()) throw new Error('Please paste your resume text');

        response = await fetch(`${apiUrl}/api/analyze/text`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ resume_text: text }),
        });
      }

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || `Server error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#27ae60';
    if (score >= 65) return '#3498db';
    if (score >= 50) return '#f39c12';
    return '#e74c3c';
  };

  return (
    <div style={styles.container}>
      {/* Upload Card */}
      <div style={styles.card}>
        {/* Tabs */}
        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', borderBottom: '2px solid #f0f0f0' }}>
          <div
            onClick={() => setActiveTab('file')}
            style={{
              padding: '10px 20px',
              cursor: 'pointer',
              borderBottom: activeTab === 'file' ? '2px solid #667eea' : '2px solid transparent',
              marginBottom: '-2px',
              color: activeTab === 'file' ? '#667eea' : '#666',
              fontWeight: activeTab === 'file' ? 'bold' : 'normal',
            }}
          >
            Upload File
          </div>
          <div
            onClick={() => setActiveTab('text')}
            style={{
              padding: '10px 20px',
              cursor: 'pointer',
              borderBottom: activeTab === 'text' ? '2px solid #667eea' : '2px solid transparent',
              marginBottom: '-2px',
              color: activeTab === 'text' ? '#667eea' : '#666',
              fontWeight: activeTab === 'text' ? 'bold' : 'normal',
            }}
          >
            Paste Text
          </div>
        </div>

        {/* File Upload */}
        {activeTab === 'file' && (
          <div
            style={styles.uploadArea}
            onClick={() => fileInputRef.current?.click()}
          >
            <div style={{ fontSize: '48px', marginBottom: '10px' }}>&#128193;</div>
            <p><strong>Click to upload</strong> or drag and drop</p>
            <p style={{ color: '#888', fontSize: '13px', marginTop: '8px' }}>
              PDF, DOCX (Max 10MB)
            </p>
            {file && (
              <p style={{ color: '#667eea', marginTop: '10px', fontWeight: 'bold' }}>
                {file.name}
              </p>
            )}
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.docx,.doc"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
          </div>
        )}

        {/* Text Input */}
        {activeTab === 'text' && (
          <textarea
            value={text}
            onChange={(e) => { setText(e.target.value); setError(''); }}
            placeholder="Paste your resume text here..."
            style={{
              width: '100%',
              minHeight: '200px',
              padding: '15px',
              border: '2px solid #e0e0e0',
              borderRadius: '8px',
              fontSize: '14px',
              resize: 'vertical',
              fontFamily: 'inherit',
            }}
          />
        )}

        {/* Error */}
        {error && <div style={styles.error}>{error}</div>}

        {/* Analyze Button */}
        <center>
          <button
            onClick={handleAnalyze}
            disabled={loading}
            style={{
              ...styles.button,
              ...(loading ? styles.buttonDisabled : {}),
            }}
          >
            {loading ? (
              <>
                <span style={styles.spinner} />
                Analyzing...
              </>
            ) : (
              'Analyze Resume'
            )}
          </button>
        </center>
      </div>

      {/* Results */}
      {result && (
        <>
          {/* Score Overview */}
          <div style={styles.card}>
            <div style={{
              ...styles.scoreCircle,
              background: `conic-gradient(${getScoreColor(result.summary.overall_score)} ${(result.summary.overall_score / 100) * 360}deg, #e8e8e8 ${(result.summary.overall_score / 100) * 360}deg)`,
            }}>
              <div style={{ width: '120px', height: '120px', background: 'white', borderRadius: '50%', position: 'absolute' }} />
              <span style={styles.scoreValue}>{result.summary.overall_score}</span>
            </div>
            <div style={{
              textAlign: 'center',
              fontSize: '24px',
              fontWeight: 'bold',
              color: getScoreColor(result.summary.overall_score),
              marginBottom: '20px',
            }}>
              Grade: {result.summary.grade}
            </div>

            {/* Stats Grid */}
            <div style={styles.statGrid}>
              <div style={styles.statBox}>
                <div style={styles.statValue}>{result.summary.total_skills}</div>
                <div style={styles.statLabel}>Total Skills</div>
              </div>
              <div style={styles.statBox}>
                <div style={styles.statValue}>{result.summary.technical_skills}</div>
                <div style={styles.statLabel}>Technical</div>
              </div>
              <div style={styles.statBox}>
                <div style={styles.statValue}>{result.summary.high_demand_skills}</div>
                <div style={styles.statLabel}>High-Demand</div>
              </div>
              <div style={styles.statBox}>
                <div style={styles.statValue}>{result.summary.projects_count}</div>
                <div style={styles.statLabel}>Projects</div>
              </div>
              <div style={styles.statBox}>
                <div style={styles.statValue}>{result.summary.experience_count}</div>
                <div style={styles.statLabel}>Experience</div>
              </div>
              <div style={styles.statBox}>
                <div style={styles.statValue}>{result.summary.education_count}</div>
                <div style={styles.statLabel}>Education</div>
              </div>
            </div>
          </div>

          {/* Category Scores */}
          <div style={styles.card}>
            <div style={styles.sectionTitle}>Category Scores</div>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '10px',
            }}>
              {Object.entries(result.analysis.scoring.category_scores).map(([cat, score]) => (
                <div key={cat} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '10px 15px',
                  background: '#f8f9ff',
                  borderRadius: '8px',
                }}>
                  <span style={{ fontSize: '14px', color: '#444' }}>
                    {cat.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </span>
                  <span style={{ fontWeight: 'bold', color: '#667eea' }}>{score}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Top Skills */}
          <div style={styles.card}>
            <div style={styles.sectionTitle}>Top Skills by Strength</div>
            {Object.entries(result.analysis.skills.skill_strengths)
              .sort(([,a], [,b]) => b - a)
              .slice(0, 10)
              .map(([skill, strength]) => (
                <div key={skill} style={styles.skillBar}>
                  <span style={styles.skillName}>{skill}</span>
                  <div style={styles.skillProgress}>
                    <div style={{ ...styles.skillFill, width: `${strength}%` }} />
                  </div>
                  <span style={styles.skillScore}>{strength.toFixed(1)}</span>
                </div>
              ))}
          </div>

          {/* All Skills */}
          <div style={styles.card}>
            <div style={styles.sectionTitle}>Skills Detected ({result.summary.total_skills})</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {result.analysis.skills.found_skills.slice(0, 50).map(skill => (
                <span key={skill} style={styles.skillTag}>{skill}</span>
              ))}
            </div>
          </div>

          {/* High-Demand Skills */}
          {result.analysis.skills.high_demand_matches.length > 0 && (
            <div style={styles.card}>
              <div style={styles.sectionTitle}>High-Demand Skills Matched</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {result.analysis.skills.high_demand_matches.map(skill => (
                  <span key={skill} style={{ ...styles.skillTag, ...styles.demandTag }}>{skill}</span>
                ))}
              </div>
            </div>
          )}

          {/* Recommendations */}
          <div style={styles.card}>
            <div style={styles.sectionTitle}>Recommendations</div>
            {result.analysis.scoring.recommendations.map((rec, i) => (
              <div key={i} style={{
                ...styles.recommendation,
                ...(rec.priority === 'high' ? styles.recHigh : rec.priority === 'low' ? styles.recLow : {}),
              }}>
                <div style={{
                  fontSize: '12px',
                  fontWeight: 'bold',
                  textTransform: 'uppercase',
                  marginBottom: '4px',
                }}>
                  {rec.priority}
                </div>
                <b>[{rec.category}]</b> {rec.issue}
                <div style={{ fontSize: '13px', color: '#666', marginTop: '4px' }}>
                  {rec.action}
                </div>
              </div>
            ))}
          </div>

          {/* Experience */}
          {result.analysis.content.experience.length > 0 && (
            <div style={styles.card}>
              <div style={styles.sectionTitle}>Experience</div>
              {result.analysis.content.experience.map((exp, i) => (
                <div key={i} style={{
                  marginBottom: '15px',
                  padding: '10px',
                  background: '#f8f9ff',
                  borderRadius: '8px',
                }}>
                  <b>{exp.title || 'N/A'}</b> at {exp.company || 'N/A'}<br />
                  <small style={{ color: '#888' }}>{exp.duration || 'N/A'}</small>
                </div>
              ))}
            </div>
          )}

          {/* Projects */}
          {result.analysis.content.projects.length > 0 && (
            <div style={styles.card}>
              <div style={styles.sectionTitle}>Projects</div>
              {result.analysis.content.projects.slice(0, 5).map((proj, i) => (
                <div key={i} style={{
                  marginBottom: '15px',
                  padding: '10px',
                  background: '#f8f9ff',
                  borderRadius: '8px',
                }}>
                  <b>{proj.name || 'Unnamed Project'}</b><br />
                  <small style={{ color: '#888' }}>
                    {proj.technologies?.join(', ') || ''}
                  </small>
                </div>
              ))}
            </div>
          )}

          {/* Education */}
          {result.analysis.content.education.length > 0 && (
            <div style={styles.card}>
              <div style={styles.sectionTitle}>Education</div>
              {result.analysis.content.education.map((edu, i) => (
                <div key={i} style={{
                  marginBottom: '10px',
                  padding: '10px',
                  background: '#f8f9ff',
                  borderRadius: '8px',
                }}>
                  <b>{edu.degree || 'N/A'}</b><br />
                  {edu.institution || 'Unknown Institution'}<br />
                  <small style={{ color: '#888' }}>
                    Grade: {edu.grade || 'N/A'}
                  </small>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
