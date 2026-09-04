import re

with open('src/phase5_dashboard/frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# The new JSX for Tab 06
new_tab06 = """        {/* TAB 06 - ASK AI */}
        {activeTab === '06' && (
          <div style={{display:'flex', flexDirection:'column', height:'80vh', position:'relative', paddingBottom: '80px'}}>
            
            {/* Header Card */}
            <div className="glass-panel" style={{position:'relative', display:'flex', justifyContent:'space-between', alignItems:'flex-start', padding:'1.5rem', marginBottom:'2rem', borderTop:'4px solid var(--accent-secondary)'}}>
              <div>
                <strong style={{fontSize:'0.75rem', color:'var(--accent-secondary)', textTransform:'uppercase', letterSpacing:'1px'}}>MYNTRA • VOICE OF CUSTOMER</strong>
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
            </div>
            
            {chatHistory.length === 0 ? (
              <div style={{flexGrow: 1}}>
                <h4 style={{fontSize:'0.85rem', textTransform:'uppercase', letterSpacing:'1px', marginBottom:'1rem'}}>SUGGESTED QUESTIONS</h4>
                <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'1rem'}}>
                  {suggestedQuestions.flatMap(g => g.questions).slice(0, 8).map((q, j) => (
                    <button 
                      key={j} 
                      style={{background:'var(--accent-secondary)', color:'#000', border:'none', borderRadius:'4px', padding:'1rem', fontSize:'0.9rem', fontWeight:'500', cursor:'pointer', textAlign:'center', boxShadow:'0 2px 4px rgba(0,0,0,0.1)'}} 
                      onClick={() => handleAskAI(q)}
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="glass-panel overflow-auto mb-2" style={{flexGrow: 1, display:'flex', flexDirection:'column', gap:'1rem', padding:'1.5rem'}}>
                {chatHistory.map((msg, i) => (
                  <div key={i} style={{alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start', maxWidth:'85%', background: msg.role === 'user' ? 'var(--accent-secondary)' : 'transparent', color: msg.role === 'user' ? '#000' : 'inherit', padding: msg.role === 'user' ? '1rem' : '0', borderRadius:'8px', fontWeight: msg.role === 'user' ? '500' : 'normal'}}>
                    {msg.role === 'user' ? (
                      msg.content
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
            )}

            {/* Input Box Fixed at Bottom */}
            <div style={{position:'absolute', bottom:0, left:0, right:0, background:'#1a1c23', padding:'1rem 2rem', borderRadius:'0 0 16px 16px', display:'flex', alignItems:'center'}}>
              <div style={{display:'flex', width:'100%', border:'1px solid rgba(255,255,255,0.2)', borderRadius:'8px', overflow:'hidden', background:'#242630'}}>
                <div style={{width:'4px', background:'var(--accent-primary)'}}></div>
                <input 
                  type="text" 
                  style={{flexGrow: 1, padding:'1rem', background:'transparent', border:'none', color:'white', outline:'none', fontSize:'0.95rem'}} 
                  placeholder="Ask about barriers, categories, segments, discovery..."
                  value={aiQuery}
                  onChange={(e) => setAiQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleAskAI(aiQuery)}
                />
                <button 
                  style={{padding:'0 1.5rem', background:'transparent', border:'none', color:'white', cursor:'pointer', fontSize:'1.2rem', display:'flex', alignItems:'center', justifyContent:'center'}}
                  onClick={() => handleAskAI(aiQuery)}
                >
                  ➤
                </button>
              </div>
            </div>
          </div>
        )}"""

# We need to replace everything from {/* TAB 07 - ASK AI */} to the end of the activeTab === '06' block.
# Since my previous renaming changed the comment to {/* TAB 07 - ASK AI */} but the block is activeTab === '06'.
pattern = r'\{\/\* TAB 07 - ASK AI \*\/\}\s*\{activeTab === \'06\' && \(\s*<div style=\{\{display:\'flex\', flexDirection:\'column\', height:\'75vh\'\}\}\>.*?\s*<\/div>\s*\)\}'
content = re.sub(pattern, new_tab06, content, flags=re.DOTALL)

with open('src/phase5_dashboard/frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Ask AI UI updated to match screenshot.")
