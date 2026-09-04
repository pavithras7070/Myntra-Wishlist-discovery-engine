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
                        <div style={{background: '#ffffff', borderRadius: '8px', border: '1px solid #e0e0e0', padding: '1.5rem', flexGrow: 1}}>
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
                          <p style={{margin:'0 0 2rem 0', color:'#282c3f', fontSize:'0.9rem', lineHeight:'1.5'}}>
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
                        </div>
                      </>
                    )}
                  </div>
                ))}"""

start_str = "{chatHistory.map((msg, i) => ("
end_str = "{isAiThinking && <div style={{alignSelf: 'flex-start'}}><span className=\"badge\">Analyzing Evidence...</span></div>}"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + new_chat_block + "\n                " + content[end_idx:]
    with open('src/phase5_dashboard/frontend/src/App.jsx', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("AI Bubble styling successfully applied.")
else:
    print("Could not find the target string blocks.", start_idx, end_idx)
