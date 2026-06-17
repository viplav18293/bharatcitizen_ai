import os

domains = [
    "aadhaar", "pan", "passport", "voterid", "driving_license",
    "digilocker", "neet", "jee", "upsc", "pm_kisan",
    "ayushman_bharat", "pm_awas", "rti", "consumer_rights", "labour_rights"
]

os.makedirs("data/knowledge", exist_ok=True)

for domain in domains:
    content = f"""# {domain.replace('_', ' ').title()}

## Overview
Brief overview of {domain.replace('_', ' ')}.

## Eligibility
* Criterion 1
* Criterion 2

## Benefits
* Benefit 1
* Benefit 2

## Required Documents
* Doc 1
* Doc 2

## Application Process
1. Step 1
2. Step 2

## Fees
Details about fees.

## Processing Time
Time duration.

## Important Notes
Important notes.

## Official Portal
https://example.gov.in
"""
    with open(f"data/knowledge/{domain}.md", "w", encoding="utf-8") as f:
        f.write(content)
print("Created knowledge files.")
