import re

with open('src/phase5_dashboard/frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add states
state_injection = """
  const [explorerFilter, setExplorerFilter] = useState('All')

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
      const response = await fetch('http://localhost:8000/api/ask', {
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
"""
content = re.sub(r'const \[explorerFilter, setExplorerFilter\] = useState\(\'All\'\)', state_injection, content)

# 2. Add Tab 07 to tabs array
tabs_injection = """
  const tabs = [
    { id: '01', label: '01 — OVERVIEW' },
    { id: '02', label: '02 — EVIDENCE' },
    { id: '03', label: '03 — BEHAVIORAL INSIGHTS' },
    { id: '04', label: '04 — CROSS-SOURCE' },
    { id: '05', label: '05 — WISHLIST LENS' },
    { id: '06', label: '06 — OPPORTUNITIES' },
    { id: '07', label: '07 — ASK AI (COPILOT)' }
  ]
"""
content = re.sub(r'const tabs = \[.*?\]', tabs_injection.strip(), content, flags=re.DOTALL)

# 3. Add Investigate Opportunity button
investigate_btn = """
                      <td>
                        <span className="badge">{opp.overall_opportunity_score}</span>
                        <br/>
                        <button 
                          className="badge" 
                          style={{marginTop:'8px', cursor:'pointer', background:'var(--accent-secondary)'}}
                          onClick={() => {
                            setActiveTab('07');
                            handleAskAI(`Investigate Opportunity: ${opp.opportunity_name}. Tell me the segment, evidence, behavior, underlying need, workarounds, contradictions, unknowns, and 5-7 interview questions about past behavior.`);
                          }}
                        >
                          Investigate ↗
                        </button>
                      </td>
"""
content = re.sub(r'<td><span className="badge">\{opp\.overall_opportunity_score\}</span></td>', investigate_btn.strip(), content)

# 4. Add Tab 07 JSX and Evidence Modal
tab7_jsx = """
        {/* TAB 07 - ASK AI */}
        {activeTab === '07' && (
          <div style={{display:'flex', flexDirection:'column', height:'75vh'}}>
            <h3>Research Copilot</h3>
            <p className="text-secondary mb-2">Interrogate the raw evidence data. The AI does not replace your PM judgment.</p>
            
            {/* Suggested Questions */}
            <div className="mb-2" style={{display:'flex', gap:'1rem', overflowX:'auto', paddingBottom:'0.5rem'}}>
              {suggestedQuestions.map((group, i) => (
                <div key={i} style={{minWidth:'200px'}}>
                  <strong style={{fontSize:'0.8rem', color:'var(--accent-secondary)', textTransform:'uppercase'}}>{group.category}</strong>
                  <div style={{display:'flex', flexDirection:'column', gap:'0.4rem', marginTop:'0.4rem'}}>
                    {group.questions.map((q, j) => (
                      <button key={j} className="glass-panel" style={{textAlign:'left', fontSize:'0.75rem', padding:'0.5rem', cursor:'pointer', border:'1px solid rgba(255,255,255,0.1)'}} onClick={() => handleAskAI(q)}>
                        {q}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* Chat History */}
            <div className="glass-panel overflow-auto mb-2" style={{flexGrow: 1, display:'flex', flexDirection:'column', gap:'1rem', padding:'1.5rem'}}>
              {chatHistory.length === 0 && <p className="text-secondary" style={{textAlign:'center', marginTop:'2rem'}}>Ask a question to begin exploring the evidence.</p>}
              
              {chatHistory.map((msg, i) => (
                <div key={i} style={{alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start', maxWidth:'85%', background: msg.role === 'user' ? 'rgba(255,255,255,0.1)' : 'transparent', padding: msg.role === 'user' ? '1rem' : '0', borderRadius:'8px'}}>
                  {msg.role === 'user' ? (
                    <strong>{msg.content}</strong>
                  ) : (
                    <div style={{borderLeft: '4px solid var(--accent-primary)', paddingLeft:'1rem'}}>
                      <h4 style={{margin:'0 0 0.5rem 0', color:'var(--text-primary)'}}>{msg.content.direct_answer}</h4>
                      
                      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'1rem', fontSize:'0.85rem', marginBottom:'1rem'}}>
                        <div>
                          <strong style={{color:'var(--accent-secondary)'}}>What Users Are Doing:</strong><br/>
                          <span className="text-secondary">{msg.content.what_users_are_doing}</span>
                        </div>
                        <div>
                          <strong style={{color:'var(--accent-secondary)'}}>Underlying Need:</strong><br/>
                          <span className="text-secondary">{msg.content.underlying_need}</span>
                        </div>
                        <div>
                          <strong style={{color:'var(--accent-secondary)'}}>Workarounds:</strong><br/>
                          <span className="text-secondary">{msg.content.workarounds}</span>
                        </div>
                        <div>
                          <strong style={{color:'var(--accent-secondary)'}}>Segment Differences:</strong><br/>
                          <span className="text-secondary">{msg.content.segment_differences}</span>
                        </div>
                      </div>

                      <div style={{background:'rgba(255,63,108,0.05)', padding:'0.8rem', borderRadius:'4px', marginBottom:'1rem', fontSize:'0.85rem'}}>
                        <strong>Contradicting Evidence / Unknowns:</strong><br/>
                        <span className="text-secondary">{msg.content.contradicting_evidence} {msg.content.what_we_dont_know}</span>
                      </div>

                      <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
                        <span className="badge">Strength: {msg.content.evidence_strength}</span>
                        {msg.content.evidence_ids && msg.content.evidence_ids.length > 0 && (
                          <button className="badge" style={{cursor:'pointer', background:'var(--text-primary)', color:'var(--bg-dark)'}} onClick={() => setEvidenceModal({isOpen: true, ids: msg.content.evidence_ids})}>
                            View Evidence ({msg.content.evidence_ids.length})
                          </button>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              ))}
              {isAiThinking && <div style={{alignSelf: 'flex-start'}}><span className="badge">Analyzing Evidence...</span></div>}
            </div>

            {/* Input Box */}
            <div style={{display:'flex', gap:'1rem'}}>
              <input 
                type="text" 
                className="glass-panel" 
                style={{flexGrow: 1, padding:'1rem', color:'var(--text-primary)', border:'1px solid rgba(255,255,255,0.2)'}} 
                placeholder="Ask a question about user behavior, barriers, or segments..."
                value={aiQuery}
                onChange={(e) => setAiQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAskAI(aiQuery)}
              />
              <button 
                className="glass-panel" 
                style={{padding:'0 2rem', background:'var(--accent-primary)', color:'white', cursor:'pointer', fontWeight:'bold'}}
                onClick={() => handleAskAI(aiQuery)}
              >
                ASK AI
              </button>
            </div>
          </div>
        )}
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
    </div>
"""
content = re.sub(r'      </div>\n    </div>\n  \)\n}\n\nexport default App', tab7_jsx + "\n  )\n}\n\nexport default App", content)

with open('src/phase5_dashboard/frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied.")
