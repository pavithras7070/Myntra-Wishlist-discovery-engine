import re

with open('src/phase5_dashboard/frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Find the Cross-Source matrix block in TAB 04
cross_source_pattern = r'(\{\/\* TAB 04 - CROSS SOURCE \*\/\}\s*\{activeTab === \'04\' && \(\s*<div>\s*<h3>Cross-Source Evidence Matrix</h3>.*?</div>\s*\)\})'
cross_source_match = re.search(cross_source_pattern, content, re.DOTALL)

if cross_source_match:
    full_tab4_block = cross_source_match.group(1)
    
    # Extract just the inner div content to put in Tab 3
    inner_matrix_pattern = r'\{activeTab === \'04\' && \(\s*<div>\s*(<h3>Cross-Source Evidence Matrix</h3>.*?</div>\s*</div>)\s*\)\}'
    inner_matrix_match = re.search(inner_matrix_pattern, full_tab4_block, re.DOTALL)
    
    if inner_matrix_match:
        matrix_jsx = inner_matrix_match.group(1)
        
        # 2. Delete the old TAB 04 block
        content = content.replace(full_tab4_block, '')
        
        # 3. Insert matrix_jsx at the bottom of TAB 03
        tab3_end_pattern = r'(<h3>Behavioral Segments \(Phase 3 Outputs\)</h3>.*?</div>\s*)(</div>\s*\)\})'
        
        def tab3_replacement(m):
            return f'{m.group(1)}\n            <div className="mt-4" style={{{{marginTop: "2rem"}}}}\n              {matrix_jsx}\n            </div>\n{m.group(2)}'
            
        content = re.sub(tab3_end_pattern, tab3_replacement, content, flags=re.DOTALL)

with open('src/phase5_dashboard/frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("UI Re-arrangement applied correctly.")
