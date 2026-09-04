import sqlite3

conn = sqlite3.connect('e:/Pavithra Study/NextLeap/NL Graduation Projects/Myntra_wishlist_discovery_engine/src/phase1_data_foundation/phase1_data.db')
cursor = conn.cursor()

rows = cursor.execute("SELECT original_comment, purchase_status, evidence_strength, relevance FROM analyzed_insights WHERE shopping_stage IN ('browsing', 'cart');").fetchall()

print(f"Found {len(rows)} discovery reviews.")
strong_evidence_count = 0

for r in rows:
    comment, status, evidence, relevance = r
    print(f"\nStatus: {status} | Evidence: {evidence} | Relevance: {relevance}")
    safe_comment = comment[:200].encode('ascii', 'ignore').decode('ascii')
    print(f"Comment: {safe_comment}...")
    if evidence == 'strong':
        strong_evidence_count += 1
        
print(f"\nTotal strong evidence records: {strong_evidence_count} out of {len(rows)}")
