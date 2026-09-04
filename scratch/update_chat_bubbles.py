import re

with open('src/phase5_dashboard/frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

new_chat_block = """                {chatHistory.map((msg, i) => (
                  <div key={i} style={{
                    alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start', 
                    maxWidth: '85%', 
                    display: 'flex', 
                    gap: '1rem', 
                    alignItems: 'flex-start'
                  }}>
                    {msg.role === 'user' ? (
                      <>
                        <div style={{background: 'var(--accent-secondary)', color: '#000', padding: '1rem', borderRadius: '8px', fontWeight: '500'}}>
                          {msg.content}
                        </div>
                        <div style={{background: 'var(--accent-secondary)', color: '#000', width: '40px', height: '40px', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
                          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                        </div>
                      </>
                    ) : (
                      <>
                        <div style={{background: '#1a1c23', color: 'var(--accent-secondary)', width: '40px', height: '40px', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
                          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2l2.5 6 6 2.5-6 2.5-2.5 6-2.5-6-6-2.5 6-2.5 2.5-6z"/></svg>
                        </div>
                        <div className="glass-panel" style={{padding: '1.5rem', flexGrow: 1}}>
                          <strong style={{fontSize:'0.75rem', color:'var(--text-secondary)', textTransform:'uppercase', letterSpacing:'1px', marginBottom: '1rem', display: 'block'}}>WHAT USERS SAY</strong>
                          
                          <h4 style={{margin:'0 0 1rem 0', color:'var(--text-primary)'}}>{msg.content.direct_answer}</h4>
                          
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
                      </>
                    )}
                  </div>
                ))}"""

pattern = r'\{\s*chatHistory\.map\(\(msg, i\).*?\}\)\}\s*\}\s*\{\s*isAiThinking'
content = re.sub(pattern, new_chat_block + '\n                {isAiThinking', content, flags=re.DOTALL)

with open('src/phase5_dashboard/frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Avatar and bubble styling applied.")
