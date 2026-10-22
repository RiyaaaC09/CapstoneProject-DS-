# KP Population Health - RAW / DIRTY dataset (for Phase 1 cleaning)

Same members and structure as the clean star schema, but with realistic data-quality problems injected.
The clean version (KP_Population_Health_Data) is your reference to check that cleaning worked.

Raw row counts -> expected after cleaning
- Dim_Member 10,150 -> 10,000 | Dim_Member_Profile 10,100 -> 10,000
- Each fact table 15,285 -> 15,000 (150 exact duplicates + 75 same-record-different-ID duplicates + 60 orphan rows removed)

Issue families: missing values in mixed forms, duplicates (exact / conflicting / different PK), inconsistent category labels,
impossible values, unit mix-ups (mmol/L vs mg/dL), BP text formats and swapped values, mixed date formats and future dates,
numbers stored as text ($ and commas), cross-field rule violations (Costs vs components, Preventive > Visits),
Member_ID formatting noise and orphans, dirty free text (HTML, emojis, placeholders, non-English).
Lookup dims (Region, Facility, Program, Date, RLS) are unchanged reference data.

answer_key/Data_Quality_Issue_Log.csv lists every injected issue, rows affected, how to detect and fix it.
Do not use the answer_key files as model features.
