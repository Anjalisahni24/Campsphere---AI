/**
 * CAMSPHER-AI Job Recommender - React Component
 * 
 * Integration example for your React/Vite website.
 * 
 * Usage:
 *   import JobRecommender from './JobRecommender';
 *   <JobRecommender apiUrl="http://localhost:8000" />
 */

import { useState, useEffect } from 'react';

const styles = {
  container: {
    maxWidth: '1000px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  },
  card: {
    background: 'white',
    borderRadius: '16px',
    padding: '25px',
    marginBottom: '20px',
    boxShadow: '0 8px 30px rgba(0,0,0,0.08)',
  },
  title: {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '20px',
    color: '#333',
  },
  sectionTitle: {
    fontSize: '18px',
    fontWeight: 'bold',
    margin: '20px 0 15px',
    paddingBottom: '8px',
    borderBottom: '2px solid #f0f0f0',
    color: '#444',
  },
  input: {
    width: '100%',
    padding: '12px 15px',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    fontSize: '14px',
    marginBottom: '12px',
    fontFamily: 'inherit',
  },
  select: {
    width: '100%',
    padding: '12px 15px',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    fontSize: '14px',
    marginBottom: '12px',
    background: 'white',
  },
  textarea: {
    width: '100%',
    minHeight: '100px',
    padding: '12px 15px',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    fontSize: '14px',
    resize: 'vertical',
    fontFamily: 'inherit',
  },
  btn: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    padding: '12px 30px',
    borderRadius: '8px',
    fontSize: '15px',
    cursor: 'pointer',
    marginTop: '10px',
    transition: 'transform 0.2s',
  },
  btnDisabled: {
    opacity: 0.6,
    cursor: 'not-allowed',
  },
  jobCard: {
    background: '#fafbff',
    borderRadius: '12px',
    padding: '20px',
    marginBottom: '15px',
    border: '1px solid #e8ecff',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  jobHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '10px',
  },
  jobTitle: {
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#333',
  },
  company: {
    fontSize: '14px',
    color: '#667eea',
    marginTop: '2px',
  },
  matchBadge: {
    padding: '6px 14px',
    borderRadius: '20px',
    fontSize: '13px',
    fontWeight: 'bold',
    color: 'white',
  },
  highMatch: { background: 'linear-gradient(135deg, #11998e, #38ef7d)' },
  mediumMatch: { background: 'linear-gradient(135deg, #f093fb, #f5576c)' },
  lowMatch: { background: 'linear-gradient(135deg, #f39c12, #e67e22)' },
  skillTag: {
    display: 'inline-block',
    padding: '4px 10px',
    borderRadius: '12px',
    fontSize: '12px',
    margin: '3px',
  },
  matchedSkill: {
    background: '#e8f8e8',
    color: '#27ae60',
  },
  missingSkill: {
    background: '#fdeaea',
    color: '#e74c3c',
  },
  gapSkill: {
    background: '#fff8e6',
    color: '#f39c12',
  },
  statRow: {
    display: 'flex',
    gap: '15px',
    marginTop: '10px',
    flexWrap: 'wrap',
  },
  stat: {
    fontSize: '13px',
    color: '#666',
  },
  suggestionCard: {
    background: '#f8f9ff',
    borderLeft: '4px solid #667eea',
    padding: '12px 15px',
    marginBottom: '10px',
    borderRadius: '0 8px 8px 0',
  },
  suggestionHigh: {
    borderLeftColor: '#e74c3c',
    background: '#fdeaea',
  },
  suggestionMedium: {
    borderLeftColor: '#f39c12',
    background: '#fff8e6',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '15px',
  },
  categoryBadge: {
    display: 'inline-block',
    padding: '5px 12px',
    borderRadius: '15px',
    fontSize: '12px',
    background: '#f0f0f0',
    color: '#555',
    margin: '3px',
  },
  error: {
    background: '#fdeaea',
    color: '#e74c3c',
    padding: '12px',
    borderRadius: '8px',
    marginBottom: '15px',
  },
  tab: {
    padding: '10px 20px',
    cursor: 'pointer',
    borderBottom: '2px solid transparent',
    marginBottom: '-2px',
    display: 'inline-block',
  },
  tabActive: {
    borderBottomColor: '#667eea',
    color: '#667eea',
    fontWeight: 'bold',
  },
  spinner: {
    display: 'inline-block',
    width: '16px',
    height: '16px',
    border: '2px solid #fff',
    borderTopColor: 'transparent',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
    marginRight: '6px',
    verticalAlign: 'middle',
  },
};

export default function JobRecommender({ apiUrl = 'http://localhost:8000' }) {
  const [activeTab, setActiveTab] = useState('skills');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  // Form states
  const [skills, setSkills] = useState('');
  const [cgpa, setCgpa] = useState(7.5);
  const [branch, setBranch] = useState('CSE');
  const [hasBacklogs, setHasBacklogs] = useState(false);
  const [resumeText, setResumeText] = useState('');

  const handleRecommend = async () => {
    setError('');
    setLoading(true);

    try {
      let response;

      if (activeTab === 'skills') {
        const skillList = skills.split(',').map(s => s.trim()).filter(Boolean);
        if (skillList.length === 0) throw new Error('Please enter at least one skill');

        response = await fetch(`${apiUrl}/api/recommend-jobs`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            skills: skillList,
            cgpa: parseFloat(cgpa),
            branch,
            has_backlogs: hasBacklogs,
            top_n: 10,
          }),
        });
      } else {
        if (!resumeText.trim()) throw new Error('Please paste your resume text');

        response = await fetch(`${apiUrl}/api/recommend-from-resume`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            resume_text: resumeText,
            cgpa: parseFloat(cgpa),
            branch,
            has_backlogs: hasBacklogs,
            top_n: 10,
          }),
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

  const getMatchStyle = (score) => {
    if (score >= 75) return { ...styles.matchBadge, ...styles.highMatch };
    if (score >= 50) return { ...styles.matchBadge, ...styles.mediumMatch };
    return { ...styles.matchBadge, ...styles.lowMatch };
  };

  const getMatchLabel = (score) => {
    if (score >= 75) return 'High Match';
    if (score >= 50) return 'Medium Match';
    return 'Low Match';
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>CAMSPHER-AI Job Recommender</h2>

        {/* Tabs */}
        <div style={{ borderBottom: '2px solid #f0f0f0', marginBottom: '20px' }}>
          <div
            onClick={() => setActiveTab('skills')}
            style={{
              ...styles.tab,
              ...(activeTab === 'skills' ? styles.tabActive : {}),
            }}
          >
            By Skills
          </div>
          <div
            onClick={() => setActiveTab('resume')}
            style={{
              ...styles.tab,
              ...(activeTab === 'resume' ? styles.tabActive : {}),
            }}
          >
            By Resume
          </div>
        </div>

        {/* Form */}
        {activeTab === 'skills' ? (
          <div>
            <label style={{ fontSize: '14px', fontWeight: 'bold', color: '#555' }}>
              Your Skills (comma separated)
            </label>
            <input
              style={styles.input}
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
              placeholder="e.g. python, react, node.js, sql, docker"
            />
          </div>
        ) : (
          <div>
            <label style={{ fontSize: '14px', fontWeight: 'bold', color: '#555' }}>
              Paste Resume Text
            </label>
            <textarea
              style={styles.textarea}
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder="Paste your full resume text here..."
            />
          </div>
        )}

        <div style={styles.grid}>
          <div>
            <label style={{ fontSize: '14px', fontWeight: 'bold', color: '#555' }}>CGPA</label>
            <input
              style={styles.input}
              type="number"
              min="0"
              max="10"
              step="0.1"
              value={cgpa}
              onChange={(e) => setCgpa(e.target.value)}
            />
          </div>
          <div>
            <label style={{ fontSize: '14px', fontWeight: 'bold', color: '#555' }}>Branch</label>
            <select style={styles.select} value={branch} onChange={(e) => setBranch(e.target.value)}>
              <option value="CSE">CSE</option>
              <option value="IT">IT</option>
              <option value="ECE">ECE</option>
              <option value="EEE">EEE</option>
              <option value="Mechanical">Mechanical</option>
              <option value="Civil">Civil</option>
              <option value="Biotech">Biotech</option>
            </select>
          </div>
        </div>

        <div style={{ marginTop: '10px' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={hasBacklogs}
              onChange={(e) => setHasBacklogs(e.target.checked)}
            />
            <span style={{ fontSize: '14px', color: '#555' }}>Has active backlogs</span>
          </label>
        </div>

        {error && <div style={styles.error}>{error}</div>}

        <button
          onClick={handleRecommend}
          disabled={loading}
          style={{
            ...styles.btn,
            ...(loading ? styles.btnDisabled : {}),
          }}
        >
          {loading ? (
            <>
              <span style={styles.spinner} />
              Finding Jobs...
            </>
          ) : (
            'Find Best Jobs'
          )}
        </button>
      </div>

      {/* Results */}
      {result && (
        <>
          {/* Summary Stats */}
          <div style={styles.card}>
            <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap' }}>
              <div style={{ ...styles.stat, fontSize: '16px', fontWeight: 'bold', color: '#667eea' }}>
                {result.total_jobs_matched || result.recommendations?.total_jobs_matched} Jobs Matched
              </div>
              <div style={styles.stat}>
                Total in DB: {result.total_jobs_in_db || result.recommendations?.total_jobs_in_db}
              </div>
              <div style={styles.stat}>
                Skills: {result.student_profile?.skills_count || result.recommendations?.student_profile?.skills_count}
              </div>
            </div>

            {/* Categories */}
            <div style={{ marginTop: '15px' }}>
              <span style={{ fontSize: '13px', color: '#888' }}>Categories: </span>
              {Object.entries(result.category_distribution || result.recommendations?.category_distribution || {}).map(([cat, count]) => (
                <span key={cat} style={styles.categoryBadge}>
                  {cat}: {count}
                </span>
              ))}
            </div>
          </div>

          {/* Job Recommendations */}
          <div style={styles.card}>
            <div style={styles.sectionTitle}>Top Job Recommendations</div>
            {(result.top_recommendations || result.recommendations?.top_recommendations || []).map((rec, i) => {
              const job = rec.job;
              return (
                <div key={i} style={styles.jobCard}>
                  <div style={styles.jobHeader}>
                    <div>
                      <div style={styles.jobTitle}>{job.title}</div>
                      <div style={styles.company}>{job.company} | {job.location}</div>
                    </div>
                    <div style={getMatchStyle(rec.match_score)}>
                      {rec.match_score}% {getMatchLabel(rec.match_score)}
                    </div>
                  </div>

                  <div style={styles.statRow}>
                    <span style={styles.stat}>💰 {job.salary_range}</span>
                    <span style={styles.stat}>📋 {job.job_type}</span>
                    <span style={styles.stat}>🎯 {job.experience_level}</span>
                    <span style={styles.stat}>📚 CGPA: {job.cgpa_required}+</span>
                    <span style={styles.stat}>
                      {rec.eligible ? '✅ Eligible' : '❌ Not Eligible'}
                    </span>
                  </div>

                  {/* Matched Skills */}
                  <div style={{ marginTop: '10px' }}>
                    <span style={{ fontSize: '12px', color: '#888' }}>Matched Skills: </span>
                    {rec.required_skills_matched.map(s => (
                      <span key={s} style={{ ...styles.skillTag, ...styles.matchedSkill }}>{s}</span>
                    ))}
                    {rec.preferred_skills_matched.map(s => (
                      <span key={s} style={{ ...styles.skillTag, ...styles.matchedSkill, opacity: 0.7 }}>{s}</span>
                    ))}
                  </div>

                  {/* Missing Skills */}
                  {rec.skill_gaps.length > 0 && (
                    <div style={{ marginTop: '8px' }}>
                      <span style={{ fontSize: '12px', color: '#888' }}>Skill Gaps: </span>
                      {rec.skill_gaps.slice(0, 5).map(s => (
                        <span key={s} style={{ ...styles.skillTag, ...styles.gapSkill }}>{s}</span>
                      ))}
                    </div>
                  )}

                  {/* Eligibility Reason */}
                  {!rec.eligible && (
                    <div style={{ marginTop: '8px', fontSize: '12px', color: '#e74c3c' }}>
                      ⚠️ {rec.eligibility_reason}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Improvement Suggestions */}
          {(result.improvement_suggestions || result.recommendations?.improvement_suggestions)?.length > 0 && (
            <div style={styles.card}>
              <div style={styles.sectionTitle}>Improvement Suggestions</div>
              {(result.improvement_suggestions || result.recommendations?.improvement_suggestions || []).map((sug, i) => (
                <div
                  key={i}
                  style={{
                    ...styles.suggestionCard,
                    ...(sug.priority === 'high'
                      ? styles.suggestionHigh
                      : sug.priority === 'medium'
                      ? styles.suggestionMedium
                      : {}),
                  }}
                >
                  <div style={{ fontSize: '12px', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: '4px' }}>
                    {sug.priority} Priority
                  </div>
                  <b>{sug.title}</b>
                  <div style={{ fontSize: '13px', color: '#555', marginTop: '4px' }}>
                    {sug.description}
                  </div>
                  <div style={{ fontSize: '12px', color: '#667eea', marginTop: '4px' }}>
                    💡 {sug.action}
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
