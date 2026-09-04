import re

with open('src/phase5_dashboard/frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 1: Extract the Cross-Source Evidence Matrix JSX from Tab 04
cross_source_match = re.search(r'(<h3>Cross-Source Evidence Matrix</h3>.*?</div>\s*</div>)', content, re.DOTALL)
cross_source_jsx = cross_source_match.group(1) if cross_source_match else ""

# Step 2: Delete the Tab 04 block completely
content = re.sub(r'\{\/\* TAB 04 - CROSS-SOURCE \*\/\}\s*\{activeTab === \'04\' && \(\s*<div>\s*<h3>Cross-Source Evidence Matrix</h3>.*?</div>\s*\)\}', '', content, flags=re.DOTALL)

# Step 3: Inject the Cross-Source matrix at the bottom of Tab 03
tab3_end_pattern = r'(<h3>D\. Key Friction Points \[Myntra Web\]</h3>.*?</table>\s*</div>\s*</div>\s*</div>\s*</div>)'
replacement = r'\1\n\n            <div className="mt-4" style={{marginTop: "2rem"}}>\n              ' + cross_source_jsx + '\n            </div>'
content = re.sub(tab3_end_pattern, replacement, content, flags=re.DOTALL)

# Step 4: Renumber the tabs array
new_tabs = """  const tabs = [
    { id: '01', label: '01 — OVERVIEW' },
    { id: '02', label: '02 — EVIDENCE' },
    { id: '03', label: '03 — BEHAVIORAL INSIGHTS & CROSS-SOURCE' },
    { id: '04', label: '04 — WISHLIST LENS' },
    { id: '05', label: '05 — OPPORTUNITIES' },
    { id: '06', label: '06 — ASK AI (COPILOT)' }
  ]"""
content = re.sub(r'const tabs = \[.*?\]', new_tabs, content, flags=re.DOTALL)

# Step 5: Renumber the activeTab checks
content = content.replace("activeTab === '05'", "activeTab === '04'")
content = content.replace("activeTab === '06'", "activeTab === '05'")
content = content.replace("activeTab === '07'", "activeTab === '06'")
content = content.replace("setActiveTab('07')", "setActiveTab('06')")

with open('src/phase5_dashboard/frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("UI Re-arrangement applied.")
