import { useState, useEffect, useMemo } from 'react'
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ZAxis, ReferenceLine, Cell, ReferenceArea, LabelList } from 'recharts'
import './index.css'

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const SOLUTION_MAP = {
  "Sizing & Fit Solution": [
    "Virtual AR Fit Assistant",
    "Size Prediction ML Engine",
    "Community Fit Reviews Tag"
  ],
  "Quality & Durability Solution": [
    "Macro-Fabric Video Shorts",
    "Verified Material Badges",
    "Durability Score Index"
  ],
  "Price & Value Solution": [
    "Price Drop Anticipation Alerts",
    "Smart Wishlist Bundling",
    "Competitor Price Match Guarantee"
  ],
  "Platform Trust Solution": [
    "Transparent Return Policies UI",
    "Seller Rating Badges",
    "Guaranteed Refund Timeline"
  ],
  "Representation & Accuracy Solution": [
    "User-Generated Photo Gallery",
    "Unedited Video Walkarounds",
    "Strict Content QA Guidelines"
  ],
  "Styling & Comparison Solution": [
    "Visual Outfit Mix-and-Match",
    "Side-by-Side Comparison Grid",
    "Influencer Styling Moodboards"
  ]
};

function App() {
  const [activeTab, setActiveTab] = useState('01')
  const [summary, setSummary] = useState(null)
  const [segments, setSegments] = useState([])
  const [opportunities, setOpportunities] = useState([])
  const [evidence, setEvidence] = useState([])
  const [synthesis, setSynthesis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [fetchingReviews, setFetchingReviews] = useState(false)
  const [totalRawReviews, setTotalRawReviews] = useState(13452)

  const [showFetchModal, setShowFetchModal] = useState(false)
  const [playStoreChecked, setPlayStoreChecked] = useState(true)
  const [appStoreChecked, setAppStoreChecked] = useState(true)
  const [rawStats, setRawStats] = useState({ google_play: 0, app_store: 0, last_fetch_playstore: null, last_fetch_appstore: null })
  
  const [fetchStatus, setFetchStatus] = useState('idle') // 'idle', 'fetching', 'complete'
  const [fetchResult, setFetchResult] = useState(null)

  const fetchRawStats = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/raw-stats`);
      const data = await res.json();
      setRawStats(data);
    } catch(err) {
      console.error(err);
    }
  };

  const openFetchModal = () => {
    setShowFetchModal(true);
    setFetchStatus('idle');
    setFetchResult(null);
    fetchRawStats();
  };

  const executeFetchReviews = async () => {
    const sources = [];
    if (playStoreChecked) sources.push("google_play");
    if (appStoreChecked) sources.push("app_store");

    setFetchingReviews(true);
    setFetchStatus('fetching');
    try {
      const response = await fetch(`${API_BASE_URL}/api/fetch-reviews`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sources })
      });
      const data = await response.json();
      if (data.success) {
        setTotalRawReviews(prev => prev + data.saved_count);
        setFetchResult(data);
        setFetchStatus('complete');
        fetchRawStats(); // Refresh stats in the modal
      } else {
        setFetchResult({ error: data.error });
        setFetchStatus('complete');
      }
    } catch (err) {
      setFetchResult({ error: err.message });
      setFetchStatus('complete');
    } finally {
      setFetchingReviews(false);
    }
  };

  
  const [explorerFilter, setExplorerFilter] = useState('All')
  const [explorerSearch, setExplorerSearch] = useState('')
  const [explorerSource, setExplorerSource] = useState('All')
  const [explorerStage, setExplorerStage] = useState('All')

  // --- ASK AI STATES ---
  const [chatHistory, setChatHistory] = useState([])
  const [aiQuery, setAiQuery] = useState('')
  const [isAiThinking, setIsAiThinking] = useState(false)
  const [evidenceModal, setEvidenceModal] = useState({ isOpen: false, ids: [] })

  const handleAskAI = async (question) => {
    if (!question.trim()) return;
    setAiQuery('');
    setChatHistory(prev => [...prev, { role: 'user', content: question }]);
    setIsAiThinking(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      const data = await response.json();
      setChatHistory(prev => [...prev, { role: 'ai', content: data }]);
    } catch (err) {
      setChatHistory(prev => [...prev, { role: 'ai', content: { direct_answer: "Error connecting to AI backend." } }]);
    } finally {
      setIsAiThinking(false);
    }
  }
  
  const suggestedQuestions = [
    { category: 'Understand', questions: ['Why do users wishlist products?', 'What prevents purchase?', 'What uncertainties remain?'] },
    { category: 'Go Deeper', questions: ['Why does this barrier exist?', 'What is the underlying user need?', 'What are users actually trying to accomplish?'] },
    { category: 'Compare', questions: ['Compare fit vs price uncertainty.', 'Compare bookmarkers vs high-intent shoppers.', 'Which opportunity has stronger evidence?'] },
    { category: 'Challenge', questions: ['What evidence contradicts this finding?', 'What alternative explanations exist?', 'What assumptions are we making?'] }
  ];


  useEffect(() => {
    async function fetchData() {
      try {
        const sumRes = await fetch(`${API_BASE_URL}/api/summary`)
        const sumData = await sumRes.json()
        
        const segRes = await fetch(`${API_BASE_URL}/api/segments`)
        const segData = await segRes.json()
        
        const oppRes = await fetch(`${API_BASE_URL}/api/opportunities`)
        const oppData = await oppRes.json()
        
        const evRes = await fetch(`${API_BASE_URL}/api/evidence`)
        const evData = await evRes.json()
        const allEvidence = evData.evidence || []
        
        try {
            const synRes = await fetch(`${API_BASE_URL}/api/synthesis`)
            const synData = await synRes.json()
            setSynthesis(synData)
        } catch(e) {
            console.error("No synthesis data found")
        }
        
        // Dynamically recalculate metric distributions to ensure they include all sources (e.g. Google Play)
        const decisionDist = {};
        const wishlistDist = {};
        const barrierFreq = {};
        
        allEvidence.forEach(e => {
          let stage = e.shopping_stage || 'Unknown';
          let mappedDs = 'E. Unknown';
          
          if (stage === 'Discovery' || stage === 'Consideration' || stage === 'Product Evaluation') {
            mappedDs = 'A. Pre-Purchase Decision Evidence';
          } else if (stage === 'Purchase') {
            mappedDs = 'D. Post-Purchase Operational Complaint';
          } else if (stage === 'Unknown') {
            mappedDs = 'E. Unknown';
          } else {
            mappedDs = 'C. General Shopping/Fashion Discussion';
          }
          decisionDist[mappedDs] = (decisionDist[mappedDs] || 0) + 1;
          
          let wr = e.wishlist_relevance || 'Unknown';
          if (wr === 'Unknown' || wr === 'N/A') wr = 'General Shopping Evidence';
          if (!wr.includes("Evidence")) wr = 'General Shopping Evidence'; // sanitize
          wishlistDist[wr] = (wishlistDist[wr] || 0) + 1;
          
          let bar = e.purchase_barrier || e.barrier_standardized_category || 'Unknown / Other';
          if (bar === 'Unknown' || bar === 'N/A') bar = 'Unknown / Other';
          barrierFreq[bar] = (barrierFreq[bar] || 0) + 1;
        });

        const enrichedSummary = {
          ...sumData,
          decision_relevance_distribution: decisionDist,
          wishlist_relevance_distribution: wishlistDist,
          barrier_frequencies: barrierFreq
        }
        
        setSummary(enrichedSummary)
        setSegments(segData)
        setOpportunities(oppData)
        setEvidence(allEvidence)
      } catch (err) {
        console.error("Error fetching data", err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  // Cross-source matrix calculations
  const crossSourceMatrix = useMemo(() => {
    if (!summary || !summary.aggregated_barriers) return [];
    const matrix = [];
    for (const [theme, data] of Object.entries(summary.aggregated_barriers)) {
      const counts = data["Raw Counts By Source"] || {};
      matrix.push({
        theme: theme,
        addressing: data['Addressing'] || '',
        'Myntra Web': counts['Myntra Web'] || 0,
        'App Store': counts['App Store'] || 0,
        'YouTube': counts['YouTube'] || 0,
        'Google Play Store': counts['Google Play Store'] || 0,
        'Reddit': counts['Reddit'] || 0,
        total: data['Total Count'] || 0
      });
    }
    return matrix.sort((a,b) => b.total - a.total);
  }, [summary])

  if (loading) return <div className="app-container"><h1 className="animate-fade-in">Loading Intelligence Engine...</h1></div>

    const tabs = [
    { id: '01', label: 'OVERVIEW' },
    { id: '02', label: 'EVIDENCE' },
    { id: '03', label: 'BEHAVIORAL INSIGHTS & CROSS-SOURCE' },
    { id: '04', label: 'AI SYNTHESIS' },
    { id: '05', label: 'WISHLIST LENS' },
    { id: '06', label: 'OPPORTUNITIES' },
    { id: '07', label: 'ASK AI' }
  ]

  return (
    <>
      <div className="app-container animate-fade-in">
      <div className="header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1>Myntra Wishlist Discovery Engine</h1>
          <p>AI-Powered Fashion Discovery — Data-Driven Validation Dashboard</p>
        </div>
        <button 
          onClick={openFetchModal} 
          disabled={fetchingReviews}
          style={{ padding: '0.8rem 1.5rem', background: 'var(--accent)', color: 'white', border: 'none', borderRadius: '4px', cursor: fetchingReviews ? 'not-allowed' : 'pointer', fontWeight: 'bold' }}>
          {fetchingReviews ? 'Fetching...' : 'Fetch Reviews'}
        </button>
      </div>

      <div className="tabs">
        {tabs.map(tab => (
          <button 
            key={tab.id} 
            className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="tab-content animate-fade-in">
        {/* TAB 01 - OVERVIEW */}
        {activeTab === '01' && summary && (
          <div>
            <div className="grid-3 mb-2">
              <div className="glass-panel metric-card">
                <p>Total Raw Reviews Collected</p>
                <div className="metric-value">{totalRawReviews.toLocaleString()}</div>
                <p className="text-secondary">Before LLM Filtering</p>
              </div>
              <div className="glass-panel metric-card">
                <p>Relevant Conversations Extracted</p>
                <div className="metric-value">{evidence.length}</div>
                <p className="text-secondary">Across {new Set(evidence.map(e => e.source_platform)).size} sources</p>
              </div>
              <div className="glass-panel metric-card">
                <p>High-Confidence Pre-Purchase</p>
                <div className="metric-value">{evidence.filter(e => e.shopping_stage !== 'Unknown' && e.shopping_stage !== 'Purchase').length}</div>
                <p className="text-secondary">Actionable Insights</p>
              </div>
            </div>
            


            <div className="glass-panel" style={{borderLeft: '4px solid var(--accent-secondary)', background: 'rgba(255,255,255,0.02)'}}>
              <h3>PM Insight</h3>
              <p><strong>Strongest pre-purchase friction occurs around precise Size/Fit validation and Tactile Material assessment, leading to heavy wishlist abandonment.</strong></p>
              <p className="text-secondary">While explicit "wishlist" keyword mentions are sparse across public channels, customers are currently forced to use extreme workarounds—such as manually measuring owned garments with tapes or ordering duplicate items just to test fabric washability. Solving these underlying confidence barriers via interactive garment sizing or HD material showcases presents a high-impact opportunity to increase wishlist-to-cart conversion.</p>
            </div>
          </div>
        )}

        {/* TAB 02 - EVIDENCE */}
        {activeTab === '02' && summary && (
          <div>
            <h3>A. Source Coverage</h3>
            <div className="glass-panel overflow-auto mb-2">
              <table className="data-table">
                <thead><tr><th>Source Name</th><th>Raw Records</th><th>Relevant Records</th><th>Relevance %</th></tr></thead>
                <tbody>
                  <tr><td>Myntra Web</td><td>113</td><td>{evidence.filter(e => e.source_platform === 'Myntra Web' && e.is_relevant).length}</td><td>{Math.round((evidence.filter(e => e.source_platform === 'Myntra Web' && e.is_relevant).length / 113) * 100)}%</td></tr>
                  <tr><td>Apple App Store</td><td>113</td><td>{evidence.filter(e => e.source_platform === 'App Store' && e.is_relevant).length}</td><td>{Math.round((evidence.filter(e => e.source_platform === 'App Store' && e.is_relevant).length / 113) * 100)}%</td></tr>
                  <tr><td>YouTube</td><td>619</td><td>{evidence.filter(e => e.source_platform === 'YouTube' && e.is_relevant).length}</td><td>{Math.round((evidence.filter(e => e.source_platform === 'YouTube' && e.is_relevant).length / 619) * 100)}%</td></tr>
                  <tr><td>Google Play Store</td><td>212</td><td>{evidence.filter(e => e.source_platform === 'Google Play Store' && e.is_relevant).length}</td><td>{Math.round((evidence.filter(e => e.source_platform === 'Google Play Store' && e.is_relevant).length / 212) * 100)}%</td></tr>
                  <tr><td>Reddit</td><td>75</td><td>{evidence.filter(e => e.source_platform === 'Reddit' && e.is_relevant).length}</td><td>{Math.round((evidence.filter(e => e.source_platform === 'Reddit' && e.is_relevant).length / 75) * 100)}%</td></tr>
                </tbody>
              </table>
            </div>

            <div className="grid-2">
              <div>
                <h3>B. Decision Relevance</h3>
                <p className="text-secondary" style={{fontSize:'0.85rem'}}>These are evidence classifications, not sequential user journey stages.</p>
                <div className="glass-panel overflow-auto">
                  <table className="data-table">
                    <thead><tr><th>Classification</th><th>Count</th></tr></thead>
                    <tbody>
                      {summary.decision_relevance_distribution && Object.entries(summary.decision_relevance_distribution).sort((a,b)=>b[1]-a[1]).map(([k,v]) => (
                        <tr key={k}><td>{k}</td><td>{v}</td></tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
              <div>
                <h3>C. Wishlist Relevance</h3>
                <p className="text-secondary" style={{fontSize:'0.85rem'}}>These are evidence classifications, not sequential user journey stages.</p>
                <div className="glass-panel overflow-auto">
                  <table className="data-table">
                    <thead><tr><th>Classification</th><th>Count</th></tr></thead>
                    <tbody>
                      {summary.wishlist_relevance_distribution && Object.entries(summary.wishlist_relevance_distribution).sort((a,b)=>b[1]-a[1]).map(([k,v]) => (
                        <tr key={k}><td>{k}</td><td>{v}</td></tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 03 - BEHAVIORAL INSIGHTS */}
        {activeTab === '03' && (
          <div>
            <h3>Pre-Purchase Semantic Classification</h3>
            <p className="text-secondary" style={{fontSize:'0.85rem'}}>Breaks down the 566 pre-purchase intents into explicit barriers, implicit doubts, and pure shopping intent.</p>
            <div className="glass-panel overflow-auto mb-4">
              <table className="data-table">
                <thead><tr><th>Behavior Type</th><th>Count</th></tr></thead>
                <tbody>
                  {summary?.pre_purchase_behavior_types && Object.entries(summary.pre_purchase_behavior_types)
                    .sort((a, b) => b[1] - a[1])
                    .map(([type, count]) => (
                    <tr key={type}>
                      <td><span className="badge">{type}</span></td>
                      <td>{count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <h3>Top Semantic Customer Needs (Barriers & Doubts)</h3>
            <div className="glass-panel overflow-auto mb-2">
              <table className="data-table">
                <thead><tr><th>Barrier Theme</th><th>Total Evidence</th><th>Evidence Strength</th></tr></thead>
                <tbody>
                  {summary?.aggregated_barriers && Object.entries(summary.aggregated_barriers)
                    .sort((a, b) => b[1]['Total Count'] - a[1]['Total Count'])
                    .map(([theme, data]) => (
                    <tr key={theme}>
                      <td><span className="badge">{theme}</span></td>
                      <td>{data['Total Count']}</td>
                      <td className="text-secondary" style={{fontSize:'0.85rem'}}>
                        <strong>{data['Addressing']}</strong><br/>
                        {data['Evidence Strength Indicator']} Confidence (Supported by {data['Sources Count']} sources)
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <h3>Behavioral Segments (Phase 3 Outputs)</h3>
            <div className="glass-panel overflow-auto">
              {segments.length === 0 ? <p>Segmentation confidence is limited by available evidence.</p> : (
                <table className="data-table">
                  <thead><tr><th>Segment Name</th><th>Barrier</th><th>Size</th><th>Representative Evidence (Actual Quote)</th></tr></thead>
                  <tbody>
                    {segments.map((seg, i) => (
                      <tr key={i}>
                        <td><strong>{seg.segment_name}</strong></td>
                        <td>{seg.barrier_standardized_category}</td>
                        <td>{seg.size}</td>
                        <td className="text-secondary" style={{fontSize:'0.85rem', fontStyle:'italic'}}>"{seg.representative_quotes?.[0]}"</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          
            <div className="mt-4" style={{marginTop: "2rem"}}>
              <h3>Cross-Source Evidence Matrix</h3>
            {crossSourceMatrix.length > 0 && crossSourceMatrix[0].total < 20 && (
              <p style={{color: 'var(--accent-secondary)'}}>⚠️ Evidence too sparse to establish a reliable cross-source pattern.</p>
            )}
            <div className="glass-panel overflow-auto">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Theme (Barrier)</th>
                    <th>Addressing (Core Problem)</th>
                    <th>Myntra Web</th>
                    <th>App Store</th>
                    <th>YouTube</th>
                    <th>Google Play Store</th>
                    <th>Reddit</th>
                    <th>Total Evidence</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {crossSourceMatrix.map((row, i) => (
                    <tr key={i}>
                      <td><span className="badge">{row.theme}</span></td>
                      <td className="text-secondary" style={{fontSize:'0.85rem'}}>{row.addressing}</td>
                      <td>{row['Myntra Web']}</td>
                      <td>{row['App Store']}</td>
                      <td>{row['YouTube']}</td>
                      <td>{row['Google Play Store']}</td>
                      <td>{row['Reddit']}</td>
                      <td><strong>{row.total}</strong></td>
                      <td>
                        <span style={{fontSize:'0.75rem', color: 'var(--text-secondary)'}}>
                          {row.total < 5 ? 'Insufficient evidence' : ((row['Myntra Web']>0 && row['App Store']>0) || (row['YouTube']>0 && row['Myntra Web']>0)) ? 'Recurring across sources' : 'Source-specific'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          </div>
        )}

        

        {/* TAB 04 - AI SYNTHESIS */}
        {activeTab === '04' && synthesis && (
          <div>
            <div className="glass-panel mb-4" style={{borderLeft: '4px solid var(--accent-secondary)'}}>
              <h3>Strategic Synthesis</h3>
              <p className="text-secondary">AI-generated synthesis of aggregated barriers, categorized into core customer problems and product hypotheses.</p>
            </div>
            
            <h3>Key Customer Problems</h3>
            <div className="grid-2 mb-4">
              {synthesis.key_customer_problems?.map((prob, i) => (
                <div key={i} className="glass-panel">
                  <h4>{prob.problem_name}</h4>
                  <p className="text-secondary" style={{fontSize: '0.9rem'}}>{prob.description}</p>
                  <div style={{marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
                    <p className="text-secondary" style={{fontSize: '0.85rem', margin: 0}}>
                      <strong>Workaround:</strong> {prob.primary_workaround_used}
                    </p>
                    <div>
                      <span className="badge" style={{
                        background: prob.severity_ranking === 'High' ? '#ff4d4d' : 'rgba(255,255,255,0.1)',
                        color: prob.severity_ranking === 'High' ? '#ffffff' : 'inherit',
                        border: prob.severity_ranking === 'High' ? 'none' : ''
                      }}>
                        Severity: {prob.severity_ranking}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <h3>Opportunity Hypotheses</h3>
            <div className="glass-panel overflow-auto">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Hypothesis</th>
                    <th>Rationale</th>
                    <th>Target Metric</th>
                    <th>Impact Score</th>
                  </tr>
                </thead>
                <tbody>
                  {synthesis.opportunity_hypotheses?.map((opp, i) => (
                    <tr key={i}>
                      <td><strong>{opp.hypothesis_title}</strong></td>
                      <td className="text-secondary" style={{fontSize: '0.85rem'}}>{opp.rationale}</td>
                      <td><span className="badge">{opp.target_metric}</span></td>
                      <td>
                        <span className="badge" style={{
                          background: opp.impact_score === 'High' ? 'var(--accent)' : 'rgba(255, 168, 0, 0.1)',
                          color: opp.impact_score === 'High' ? '#ffffff' : 'var(--accent-secondary)',
                          border: opp.impact_score === 'High' ? 'none' : '1px solid rgba(255, 168, 0, 0.3)'
                        }}>
                          {opp.impact_score}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* TAB 05 - WISHLIST LENS */}
        {activeTab === '05' && (
          <div>
            <h3>EVIDENCE NARROWING — NOT A USER CONVERSION FUNNEL</h3>
            <p className="text-secondary mb-2" style={{fontSize:'0.9rem'}}>These categories represent how closely conversations relate to wishlist behavior. They do not represent users moving through sequential stages.</p>
            
            <div className="glass-panel mb-2" style={{textAlign:'center', background:'linear-gradient(to bottom, rgba(255,255,255,0.05), transparent)'}}>
              <div style={{padding:'1rem', borderBottom:'1px solid rgba(255,255,255,0.1)'}}>
                <h4>General Shopping Evidence</h4>
                <h2 style={{margin:0}}>{summary.wishlist_relevance_distribution?.["General Shopping Evidence"] || 0}</h2>
              </div>
              <div style={{padding:'1rem', borderBottom:'1px solid rgba(255,255,255,0.1)', width:'80%', margin:'0 auto'}}>
                <h4 style={{color:'var(--accent-primary)'}}>Indirect Wishlist-Relevant</h4>
                <h2 style={{margin:0, color:'var(--accent-primary)'}}>{summary.wishlist_relevance_distribution?.["Indirect Wishlist-Relevant Evidence"] || 0}</h2>
              </div>
              <div style={{padding:'1rem', width:'60%', margin:'0 auto'}}>
                <h4 style={{color:'var(--accent-secondary)'}}>Direct Wishlist Evidence</h4>
                <h2 style={{margin:0, color:'var(--accent-secondary)'}}>{summary.wishlist_relevance_distribution?.["Direct Wishlist Evidence"] || 0}</h2>
              </div>
            </div>

            <div className="glass-panel mb-2" style={{border:'1px solid rgba(255,255,255,0.1)'}}>
              <h3>Evidence Gap</h3>
              <p className="text-secondary" style={{fontSize:'0.9rem'}}>With the integration of Reddit communities, we now understand <em>why</em> users use the wishlist (price-drop anticipation, restock waiting, and bookmarking for comparison). However, the external dataset still cannot determine:</p>
              <ul className="text-secondary" style={{fontSize:'0.85rem', marginLeft:'1.5rem'}}>
                <li>Time-to-purchase (how long items sit in the wishlist)</li>
                <li>Actual conversion/abandonment rates from the wishlist page</li>
                <li>Clickstream journeys (whether they purchase directly from wishlist vs moving to cart)</li>
                <li>Whether external research on competing apps ultimately leads back to Myntra's wishlist</li>
              </ul>
            </div>

            <h3>Evidence Explorer</h3>
            <div className="glass-panel mb-2" style={{display: 'flex', gap: '1rem', flexWrap: 'wrap', padding: '1rem'}}>
              <input 
                type="text"
                placeholder="Search evidence..."
                className="glass-panel"
                style={{flexGrow: 1, padding: '0.5rem 1rem', background: 'transparent', border: '1px solid rgba(0,0,0,0.1)', color: 'var(--text-primary)', outline: 'none'}}
                value={explorerSearch}
                onChange={e => setExplorerSearch(e.target.value)}
              />
              <select className="glass-panel" style={{padding:'0.5rem', background:'transparent', color:'var(--text-primary)'}} value={explorerSource} onChange={e => setExplorerSource(e.target.value)}>
                <option value="All">All Sources</option>
                <option value="Myntra Web">Myntra Web</option>
                <option value="App Store">App Store</option>
                <option value="YouTube">YouTube</option>
                <option value="Google Play Store">Google Play Store</option>
                <option value="Reddit">Reddit</option>
              </select>
              <select className="glass-panel" style={{padding:'0.5rem', background:'transparent', color:'var(--text-primary)'}} value={explorerStage} onChange={e => setExplorerStage(e.target.value)}>
                <option value="All">All Stages</option>
                <option value="Pre-purchase">Pre-purchase</option>
                <option value="Discovery">Discovery</option>
                <option value="Consideration">Consideration</option>
                <option value="Product Evaluation">Product Evaluation</option>
                <option value="Purchase">Purchase</option>
              </select>
              <select className="glass-panel" style={{padding:'0.5rem', background:'transparent', color:'var(--text-primary)'}} value={explorerFilter} onChange={e => setExplorerFilter(e.target.value)}>
                <option value="All">All Wishlist Relevance</option>
                <option value="Direct Wishlist Evidence">Direct Wishlist Evidence</option>
                <option value="Indirect Wishlist-Relevant Evidence">Indirect Wishlist Evidence</option>
                <option value="General Shopping Evidence">General Shopping Evidence</option>
              </select>
            </div>
            
            <div className="glass-panel overflow-auto" style={{maxHeight:'500px'}}>
              {evidence.filter(e => {
                if (!e.is_relevant) return false;
                if (explorerFilter !== 'All' && e.wishlist_relevance !== explorerFilter) return false;
                if (explorerSource !== 'All' && e.source_platform !== explorerSource) return false;
                if (explorerStage !== 'All' && e.shopping_stage !== explorerStage) return false;
                if (explorerSearch) {
                  const query = explorerSearch.toLowerCase();
                  const text = (e.original_comment || e.original_text || "").toLowerCase();
                  if (!text.includes(query)) return false;
                }
                return true;
              }).map((item, i) => (
                <div key={i} style={{borderBottom:'1px solid rgba(255,255,255,0.1)', paddingBottom:'1rem', marginBottom:'1rem'}}>
                  <div style={{display:'flex', justifyContent:'space-between', marginBottom:'0.5rem'}}>
                    <span className="badge">{item.source_platform}</span>
                    {item.wishlist_relevance && item.wishlist_relevance !== 'Unknown' && (
                      <span className="badge" style={{background: item.wishlist_relevance.includes('Direct') ? 'var(--accent-secondary)' : 'rgba(255,255,255,0.1)'}}>
                        {item.wishlist_relevance}
                      </span>
                    )}
                  </div>
                  <p style={{fontStyle:'italic', margin:'0.5rem 0'}}>"{item.original_comment || item.original_text}"</p>
                  <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'1rem', fontSize:'0.8rem', color:'var(--text-secondary)'}}>
                    <div><strong>Barrier:</strong> {Array.isArray(item.purchase_barrier) ? item.purchase_barrier.join(', ') : (item.purchase_barrier || item.barrier_standardized_category || "Unknown")}</div>
                    <div><strong>Stage:</strong> {item.shopping_stage}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 06 - OPPORTUNITIES */}
        {activeTab === '06' && (
          <div>
            <h3>Impact vs. Effort (RICE) Prioritization</h3>
            <p className="text-secondary mb-2">Visualizing the highest ROI opportunities based on Reach, Impact, Confidence, and Effort.</p>
            <div className="glass-panel mb-4" style={{ height: '400px', padding: '1rem' }}>
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart margin={{ top: 20, right: 30, bottom: 20, left: 40 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis type="number" dataKey="x" name="Effort" unit="" domain={[0, 10]} stroke="var(--text-secondary)" 
                    label={{ value: 'Implementation Effort (Lower is Better)', position: 'insideBottom', offset: -10, fill: 'var(--text-secondary)' }} />
                  <YAxis type="number" dataKey="y" name="Impact" unit="" domain={[0, 10]} stroke="var(--text-secondary)" 
                    label={{ value: 'Business Impact', angle: -90, position: 'insideLeft', offset: -15, fill: 'var(--text-secondary)' }} />
                  <ZAxis type="number" dataKey="z" range={[100, 1000]} name="Reach (Evidence)" />
                  <Tooltip 
                    cursor={{ strokeDasharray: '3 3' }} 
                    contentStyle={{ backgroundColor: 'var(--bg-card)', borderColor: 'rgba(255,255,255,0.1)', color: 'var(--text-primary)' }}
                    formatter={(value, name, props) => {
                      if (props.dataKey === 'x' || name === 'Effort') return [value, 'Effort'];
                      if (props.dataKey === 'y' || name === 'Impact') return [value, 'Impact'];
                      return [value, 'Reach'];
                    }}
                    labelFormatter={() => ''}
                  />
                  <ReferenceLine x={5} stroke="rgba(255,255,255,0.2)" strokeDasharray="3 3" />
                  <ReferenceLine y={5} stroke="rgba(255,255,255,0.2)" strokeDasharray="3 3" />
                  
                  {/* Quadrants */}
                  <ReferenceArea x1={0} x2={5} y1={5} y2={10} fill="#2ECC71" fillOpacity={0.05} />
                  <ReferenceArea x1={5} x2={10} y1={5} y2={10} fill="#F1C40F" fillOpacity={0.05} />
                  <ReferenceArea x1={0} x2={5} y1={0} y2={5} fill="#3498DB" fillOpacity={0.05} />
                  <ReferenceArea x1={5} x2={10} y1={0} y2={5} fill="#E74C3C" fillOpacity={0.05} />
                  
                  {/* Quadrant Labels using svg text for absolute positioning */}
                  <text x="25%" y="15%" textAnchor="middle" fill="#2ECC71" opacity={0.6} fontSize={16} fontWeight="bold">Quick Wins</text>
                  <text x="75%" y="15%" textAnchor="middle" fill="#F1C40F" opacity={0.6} fontSize={16} fontWeight="bold">Major Projects</text>
                  <text x="25%" y="85%" textAnchor="middle" fill="#3498DB" opacity={0.6} fontSize={16} fontWeight="bold">Fill-ins</text>
                  <text x="75%" y="85%" textAnchor="middle" fill="#E74C3C" opacity={0.6} fontSize={16} fontWeight="bold">Avoid</text>
                  <Scatter name="Opportunities" data={opportunities.map(opp => ({
                    name: opp.opportunity_name,
                    label_name: opp.opportunity_name.split(' ')[0], // Short name for the chart label
                    x: 10 - opp.product_leverage_score,
                    y: opp.overall_opportunity_score,
                    z: opp.evidence_count,
                    color: opp.overall_opportunity_score >= 5 && (10 - opp.product_leverage_score) <= 5 ? '#2ECC71' : 
                           opp.overall_opportunity_score >= 5 ? '#F1C40F' : 
                           (10 - opp.product_leverage_score) <= 5 ? '#3498DB' : '#E74C3C'
                  }))}>
                    <LabelList dataKey="label_name" position="top" fill="var(--text-primary)" fontSize={12} offset={10} />
                    {opportunities.map((opp, index) => {
                      const effort = 10 - opp.product_leverage_score;
                      const impact = opp.overall_opportunity_score;
                      const color = impact >= 5 && effort <= 5 ? '#2ECC71' : 
                                    impact >= 5 ? '#F1C40F' : 
                                    effort <= 5 ? '#3498DB' : '#E74C3C';
                      return <Cell key={`cell-${index}`} fill={color} opacity={0.8} />
                    })}
                  </Scatter>
                </ScatterChart>
              </ResponsiveContainer>
            </div>

            <h3>Prioritized Opportunities</h3>
            <p className="text-secondary mb-2">Data-backed product opportunities ranked by evidence strength and strategic relevance.</p>
            <div className="glass-panel overflow-auto">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Opportunity Name</th>
                    <th>R (Reach)</th>
                    <th>I (Impact)</th>
                    <th>C (Confidence)</th>
                    <th>E (Effort)</th>
                    <th>Final RICE Score</th>
                    <th>Strategic Quadrant</th>
                  </tr>
                </thead>
                <tbody>
                  {opportunities.map((opp, idx) => {
                    const effort = 10 - opp.product_leverage_score;
                    const impact = opp.overall_opportunity_score;
                    
                    let quadrant = 'Avoid';
                    let quadColor = '#E74C3C';
                    if (impact >= 5 && effort <= 5) {
                      quadrant = 'Quick Win'; quadColor = '#2ECC71';
                    } else if (impact >= 5 && effort > 5) {
                      quadrant = 'Major Project'; quadColor = '#F1C40F';
                    } else if (impact < 5 && effort <= 5) {
                      quadrant = 'Fill-in'; quadColor = '#3498DB';
                    }

                    return (
                      <tr key={idx}>
                        <td><strong>{opp.opportunity_name.replace(' Solution', '')}</strong><br/><span className="text-secondary" style={{fontSize: '0.8rem'}}>{opp.hypothesis_level}</span></td>
                        <td>{opp.evidence_count}</td>
                        <td>{impact.toFixed(1)}</td>
                        <td>{opp.evidence_strength_score.toFixed(1)}</td>
                        <td>{effort.toFixed(1)}</td>
                        <td>
                          <span className="badge" style={{whiteSpace: 'nowrap'}}>{opp.overall_opportunity_score}</span>
                        </td>
                        <td>
                          <span style={{ backgroundColor: quadColor + '20', color: quadColor, padding: '4px 8px', borderRadius: '4px', fontSize: '0.85rem', fontWeight: 'bold' }}>
                            {quadrant}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                  {opportunities.length === 0 && (
                    <tr><td colSpan="7" style={{textAlign:'center'}}>No opportunities generated.</td></tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* SUGGESTED SOLUTIONS SECTION */}
            <h3 style={{ marginTop: '2rem' }}>Actionable Feature Solutions</h3>
            <p className="text-secondary mb-2">High-impact product feature recommendations designed to directly solve the Top 3 biggest customer barriers.</p>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
              {[...opportunities].sort((a, b) => b.evidence_count - a.evidence_count).slice(0, 3).map((opp, idx) => {
                const solutions = SOLUTION_MAP[opp.opportunity_name] || ["General UX Enhancements"];
                return (
                  <div key={idx} className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', borderTop: '4px solid var(--accent)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <span className="badge" style={{ backgroundColor: 'var(--accent)', color: 'white', padding: '4px 8px', fontSize: '0.75rem', fontWeight: 'bold' }}>
                        Priority #{idx + 1}
                      </span>
                      <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Reach: {opp.evidence_count}</span>
                    </div>
                    <h4 style={{ margin: '0.5rem 0 0 0', color: 'var(--text-primary)' }}>{opp.opportunity_name.replace(' Solution', '')}</h4>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>{opp.hypothesis_level}</p>
                    
                    <strong style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Suggested Features:</strong>
                    <ul style={{ margin: '0', paddingLeft: '1.2rem', color: 'var(--text-primary)', fontSize: '0.9rem', lineHeight: '1.6' }}>
                      {solutions.map((sol, sIdx) => (
                        <li key={sIdx}>{sol}</li>
                      ))}
                    </ul>
                  </div>
                );
              })}
            </div>
          </div>
        )}

                {/* TAB 07 - ASK AI */}
        {activeTab === '07' && (
          <div style={{display:'flex', flexDirection:'column', height:'85vh', position:'relative'}}>
            
            {/* Header Card */}
            <div className="glass-panel" style={{position:'relative', display:'flex', justifyContent:'space-between', alignItems:'flex-start', padding:'1.5rem', marginBottom:'2rem', borderTop:'4px solid var(--accent)'}}>
              <div>
                <strong style={{fontSize:'0.75rem', color:'var(--accent)', textTransform:'uppercase', letterSpacing:'1px'}}>MYNTRA • VOICE OF CUSTOMER</strong>
                <h2 style={{margin:'0.5rem 0', color:'var(--text-primary)'}}>Myntra Insight Engine</h2>
                <p className="text-secondary" style={{margin:0, fontSize:'0.9rem', maxWidth:'80%'}}>
                  Trained on thousands of Myntra app-store reviews, YouTube comments and fashion community discussions — every answer grounded in what real users said.
                </p>
              </div>
              <button 
                className="glass-panel" 
                style={{display:'flex', alignItems:'center', gap:'0.5rem', padding:'0.5rem 1rem', cursor:'pointer', border:'1px solid rgba(0,0,0,0.1)', background:'white', color:'var(--text-secondary)'}}
                onClick={() => setChatHistory([])}
              >
                <span>↻</span> Clear chat
              </button>
            </div>            {/* Chat Area Combined Container */}
            <div className="glass-panel" style={{flexGrow: 1, display:'flex', flexDirection:'column', position:'relative', overflow:'hidden'}}>
              
              {chatHistory.length === 0 ? (
                <div style={{flexGrow: 1, padding:'1.5rem', overflow:'auto'}}>
                  <h4 style={{fontSize:'0.85rem', textTransform:'uppercase', letterSpacing:'1px', marginBottom:'1rem'}}>SUGGESTED QUESTIONS</h4>
                  <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'1rem'}}>
                    {suggestedQuestions.flatMap(g => g.questions).slice(0, 8).map((q, j) => (
                      <button 
                        key={j} 
                        style={{background:'var(--accent)', color:'#fff', border:'none', borderRadius:'4px', padding:'1rem', fontSize:'0.9rem', fontWeight:'500', cursor:'pointer', textAlign:'center', boxShadow:'0 2px 4px rgba(0,0,0,0.1)'}} 
                        onClick={() => handleAskAI(q)}
                      >
                        {q}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="overflow-auto" style={{flexGrow: 1, display:'flex', flexDirection:'column', gap:'1rem', padding:'1.5rem', paddingBottom:'2rem'}}>
                  {chatHistory.map((msg, i) => (
                    <div key={i} style={{
                      alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start', 
                      maxWidth: '85%', 
                      display: 'flex', 
                      gap: '1rem', 
                      alignItems: 'flex-start'
                    }}>
                      {msg.role === 'user' ? (
                        <>
                          <div style={{background: 'var(--accent)', color: '#fff', padding: '1rem', borderRadius: '8px', fontWeight: '500'}}>
                            {msg.content}
                          </div>
                          <div style={{background: 'var(--accent)', color: '#fff', width: '40px', height: '40px', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                          </div>
                        </>
                      ) : (
                        <>
                          <div style={{background: '#1a1c23', color: 'var(--accent)', width: '40px', height: '40px', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2l2.5 6 6 2.5-6 2.5-2.5 6-2.5-6-6-2.5 6-2.5 2.5-6z"/></svg>
                          </div>
                          <div style={{background: '#ffffff', borderRadius: '8px', border: '1px solid #e0e0e0', padding: '1.5rem', flexGrow: 1}}>
                            {msg.content.is_out_of_domain ? (
                              <>
                                <strong style={{fontSize:'0.7rem', color:'#696e79', textTransform:'uppercase', letterSpacing:'1px', marginBottom: '1rem', display: 'block'}}>SYSTEM RESPONSE</strong>
                                <p style={{margin:0, color:'#282c3f', fontSize:'0.95rem', lineHeight:'1.5'}}>{msg.content.direct_answer}</p>
                              </>
                            ) : (
                              <>
                                <strong style={{fontSize:'0.7rem', color:'#696e79', textTransform:'uppercase', letterSpacing:'1px', marginBottom: '1rem', display: 'block'}}>WHAT USERS SAY</strong>
                                
                                <p style={{margin:'0 0 1.5rem 0', color:'#282c3f', fontSize:'0.95rem', lineHeight:'1.5'}}>{msg.content.direct_answer}</p>
                                
                                <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'2rem', marginBottom:'2rem'}}>
                                  <div>
                                    <strong style={{fontSize:'0.7rem', color:'#696e79', textTransform:'uppercase', letterSpacing:'1px', marginBottom: '1rem', display: 'block'}}>THEME BREAKDOWN & NEEDS</strong>
                                    <ul style={{margin:0, paddingLeft:'1.2rem', color:'#282c3f', fontSize:'0.9rem', lineHeight:'1.5'}}>
                                      <li style={{marginBottom:'0.5rem'}}>{msg.content.what_users_are_doing}</li>
                                      <li>{msg.content.underlying_need}</li>
                                    </ul>
                                  </div>
                                  <div>
                                    <strong style={{fontSize:'0.7rem', color:'#696e79', textTransform:'uppercase', letterSpacing:'1px', marginBottom: '1rem', display: 'block'}}>AFFECTED SEGMENTS & WORKAROUNDS</strong>
                                    <ul style={{margin:0, paddingLeft:'1.2rem', color:'#282c3f', fontSize:'0.9rem', lineHeight:'1.5'}}>
                                      <li style={{marginBottom:'0.5rem'}}>{msg.content.segment_differences}</li>
                                      <li>{msg.content.workarounds}</li>
                                    </ul>
                                  </div>
                                </div>
                                
                                <strong style={{fontSize:'0.7rem', color:'#696e79', textTransform:'uppercase', letterSpacing:'1px', marginBottom: '1rem', display: 'block'}}>CONTRADICTIONS & UNKNOWNS</strong>
                                <p style={{margin:'0 0 1.5rem 0', color:'#282c3f', fontSize:'0.9rem', lineHeight:'1.6'}}>
                                  {msg.content.contradicting_evidence} {msg.content.what_we_dont_know}
                                </p>
          
                                <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: '1rem'}}>
                                  <strong style={{fontSize:'0.7rem', color:'#696e79', textTransform:'uppercase', letterSpacing:'1px'}}>SUPPORTING EVIDENCE</strong>
                                  <span style={{fontSize:'0.75rem', color:'#696e79'}}>Strength: {msg.content.evidence_strength}</span>
                                </div>
                                
                                {msg.content.evidence_ids && msg.content.evidence_ids.length > 0 ? (
                                  <div style={{display:'flex', flexDirection:'column', gap:'0.8rem'}}>
                                    {msg.content.evidence_ids.map((id, idx) => {
                                      const record = evidence.find(e => e.id === id);
                                      if (!record) return null;
                                      return (
                                        <div key={id} style={{display:'flex', gap:'1rem', alignItems:'flex-start'}}>
                                          <span style={{background:'#1a1c23', color:'#fff', padding:'2px 8px', borderRadius:'4px', fontSize:'0.75rem', fontWeight:'bold', flexShrink:0}}>
                                            [{idx + 1}]
                                          </span>
                                          <span style={{color:'var(--accent-secondary)', border:'1px solid var(--accent-secondary)', padding:'2px 8px', borderRadius:'12px', fontSize:'0.7rem', fontWeight:'500', whiteSpace:'nowrap'}}>
                                            {record.source_platform}
                                          </span>
                                          <span style={{fontSize:'0.85rem', color:'#282c3f', fontStyle:'italic'}}>
                                            "{record.original_comment || record.original_text}"
                                          </span>
                                        </div>
                                      );
                                    })}
                                  </div>
                                ) : (
                                  <p style={{margin:0, color:'#696e79', fontSize:'0.85rem'}}>No specific evidence IDs referenced.</p>
                                )}
                              </>
                            )}
                          </div>
                        </>
                      )}
                    </div>
                  ))}
                  {isAiThinking && <div style={{alignSelf: 'flex-start'}}><span className="badge">Analyzing Evidence...</span></div>}
                </div>
              )}
  
              {/* Input Box at Bottom inside the same container */}
              <div style={{padding:'1rem 1.5rem', background:'transparent', borderTop:'1px solid var(--card-border)'}}>
                <div style={{display:'flex', width:'100%', border:'1px solid rgba(0,0,0,0.1)', borderRadius:'8px', overflow:'hidden', background:'#ffffff', boxShadow: '0 2px 8px rgba(0,0,0,0.05)'}}>
                  <div style={{width:'4px', background:'var(--accent-primary)'}}></div>
                  <input 
                    type="text" 
                    style={{flexGrow: 1, padding:'1rem', background:'transparent', border:'none', color:'var(--text-primary)', outline:'none', fontSize:'0.95rem'}} 
                    placeholder="Ask about barriers, categories, segments, discovery..."
                    value={aiQuery}
                    onChange={(e) => setAiQuery(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleAskAI(aiQuery)}
                  />
                  <button 
                    style={{padding:'0 1.5rem', background:'transparent', border:'none', color:'var(--accent-primary)', cursor:'pointer', fontSize:'1.2rem', display:'flex', alignItems:'center', justifyContent:'center'}}
                    onClick={() => handleAskAI(aiQuery)}
                  >
                    ➤
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>

      {/* Evidence Modal */}
      {evidenceModal.isOpen && (
        <div style={{position:'fixed', top:0, left:0, right:0, bottom:0, background:'rgba(0,0,0,0.8)', display:'flex', alignItems:'center', justifyContent:'center', zIndex: 1000}}>
          <div className="glass-panel" style={{width:'80%', maxWidth:'800px', maxHeight:'80vh', overflow:'auto', padding:'2rem', background:'var(--bg-dark)'}}>
            <div style={{display:'flex', justifyContent:'space-between', marginBottom:'1rem'}}>
              <h3>Supporting Evidence</h3>
              <button className="badge" style={{cursor:'pointer'}} onClick={() => setEvidenceModal({isOpen: false, ids: []})}>Close</button>
            </div>
            {evidenceModal.ids.map(id => {
              const record = evidence.find(e => e.id === id);
              if (!record) return <div key={id} className="text-secondary mb-1">Evidence ID {id} not found in current dataset.</div>
              return (
                <div key={id} style={{borderBottom:'1px solid rgba(255,255,255,0.1)', paddingBottom:'1rem', marginBottom:'1rem'}}>
                  <div style={{display:'flex', gap:'0.5rem', marginBottom:'0.5rem'}}>
                    <span className="badge">{record.source_platform}</span>
                    <span className="badge" style={{background: 'rgba(255,255,255,0.1)'}}>{record.shopping_stage}</span>
                  </div>
                  <p style={{fontStyle:'italic', margin:'0.5rem 0', fontSize:'0.9rem'}}>"{record.original_comment || record.original_text}"</p>
                  <p className="text-secondary" style={{fontSize:'0.8rem', margin:0}}><strong>Barrier:</strong> {record.purchase_barrier || record.barrier_standardized_category}</p>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Fetch Reviews Modal */}
      {showFetchModal && (
        <div style={{position:'fixed', top:0, left:0, right:0, bottom:0, background:'rgba(0,0,0,0.5)', display:'flex', alignItems:'center', justifyContent:'center', zIndex: 2000}}>
          <div style={{background: '#ffffff', color: '#333', borderRadius: '12px', padding: '2rem', width: '450px', boxShadow: '0 4px 20px rgba(0,0,0,0.15)', position: 'relative'}}>
            <button 
              onClick={() => setShowFetchModal(false)}
              style={{position: 'absolute', top: '1.5rem', right: '1.5rem', background: 'none', border: 'none', fontSize: '1.2rem', cursor: 'pointer', color: '#666'}}>
              ✕
            </button>
            <h2 style={{margin: '0 0 2rem 0', fontSize: '1.4rem', color: '#111'}}>Fetch Latest Reviews</h2>
            
            <h4 style={{margin: '0 0 1rem 0', fontSize: '1rem', color: '#333'}}>Review Sources</h4>
            <div style={{display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '2rem'}}>
              <label style={{display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', fontSize: '0.95rem'}}>
                <input type="checkbox" checked={playStoreChecked} onChange={(e) => setPlayStoreChecked(e.target.checked)} style={{accentColor: '#e91e63', width: '18px', height: '18px'}} />
                Google Play Reviews
              </label>
              <label style={{display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', fontSize: '0.95rem'}}>
                <input type="checkbox" checked={appStoreChecked} onChange={(e) => setAppStoreChecked(e.target.checked)} style={{accentColor: '#e91e63', width: '18px', height: '18px'}} />
                App Store Reviews
              </label>
            </div>
            
            <hr style={{border: 'none', borderTop: '1px solid #eee', marginBottom: '2rem'}} />
            
            <h4 style={{margin: '0 0 1.5rem 0', fontSize: '1rem', color: '#333'}}>Total Reviews Stored</h4>
            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '2rem'}}>
              <div>
                <p style={{margin: '0 0 0.5rem 0', fontSize: '0.85rem', color: '#666', display: 'flex', alignItems: 'center', gap: '4px'}}>Google Play ⓘ</p>
                <div style={{fontSize: '2rem', fontWeight: '500', color: '#111'}}>{rawStats.google_play.toLocaleString()}</div>
              </div>
              <div>
                <p style={{margin: '0 0 0.5rem 0', fontSize: '0.85rem', color: '#666', display: 'flex', alignItems: 'center', gap: '4px'}}>App Store ⓘ</p>
                <div style={{fontSize: '2rem', fontWeight: '500', color: '#111'}}>{rawStats.app_store.toLocaleString()}</div>
              </div>
            </div>
            
            <hr style={{border: 'none', borderTop: '1px solid #eee', marginBottom: '2rem'}} />
            
            <button 
              onClick={executeFetchReviews}
              disabled={(!playStoreChecked && !appStoreChecked) || fetchStatus === 'fetching'}
              style={{width: '100%', padding: '0.8rem', background: '#fff', color: '#8a2be2', border: '1px solid #8a2be2', borderRadius: '8px', fontSize: '1rem', cursor: (!playStoreChecked && !appStoreChecked || fetchStatus === 'fetching') ? 'not-allowed' : 'pointer', opacity: (!playStoreChecked && !appStoreChecked || fetchStatus === 'fetching') ? 0.5 : 1}}>
              {fetchStatus === 'fetching' ? 'Fetching...' : 'Fetch Latest Reviews'}
            </button>
            
            {fetchStatus === 'fetching' && (
              <div style={{marginTop: '1.5rem', display: 'flex', gap: '1rem', alignItems: 'center'}}>
                <div style={{width: '20px', height: '20px', border: '3px solid #eee', borderTop: '3px solid #333', borderRadius: '50%', animation: 'spin 1s linear infinite'}} />
                <p style={{margin: 0, fontSize: '0.9rem', color: '#333'}}>
                  Connecting to sources and fetching new reviews after {rawStats.last_fetch_playstore || 'N/A'} (Play Store) and {rawStats.last_fetch_appstore || 'N/A'} (App Store)...
                </p>
                <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
              </div>
            )}
            
            {fetchStatus === 'complete' && fetchResult && !fetchResult.error && (
              <div style={{marginTop: '1.5rem', padding: '1rem', background: '#eef6fc', borderRadius: '8px', color: '#0056b3'}}>
                {fetchResult.saved_count === 0 ? (
                  <p style={{margin: 0, fontSize: '0.95rem'}}>Data is up to date! No new reviews present.</p>
                ) : (
                  <p style={{margin: 0, fontSize: '0.95rem'}}>Successfully fetched {fetchResult.saved_count} new reviews.</p>
                )}
              </div>
            )}
            
            {fetchStatus === 'complete' && fetchResult && fetchResult.error && (
              <div style={{marginTop: '1.5rem', padding: '1rem', background: '#ffebee', borderRadius: '8px', color: '#c62828'}}>
                <p style={{margin: 0, fontSize: '0.95rem'}}>Error: {fetchResult.error}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </>

  )
}

export default App
