## 🇰🇷 JEP Korea Solutions

**AI Accountability for the Republic of Korea**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/downloads/)
[![AI Basic Act](https://img.shields.io/badge/AI%20Basic%20Act-Effective%20Jan%2022%2C%202026-red)](https://www.msit.go.kr/)
[![98% Companies Need Compliance](https://img.shields.io/badge/98%25%20Companies-Need%20Compliance-orange)](https://www.kosa.or.kr/)


## 📋 Overview

The Republic of Korea's **Artificial Intelligence Basic Act (AI Basic Act)** took effect **January 22, 2026**, making Korea the **second nation globally** (after the EU) and the **first in Asia** to enact comprehensive AI legislation . This landmark law establishes a dual-focused framework promoting AI innovation while ensuring public trust through robust governance of high-impact and generative AI systems .

### Why Korea Matters NOW

| Reason | Significance |
|--------|--------------|
| **Asia's First AI Law** | Korea sets the regulatory standard for the entire Asian market |
| **Effective Date** | **January 22, 2026** - **Already in effect!** No waiting period  |
| **Market Opportunity** | **98% of Korean AI startups lack compliance** – only 2% are ready  |
| **Foreign Company Reach** | OpenAI, Google, and others must now comply  |
| **Grace Period** | At least **1 year** before fines, but companies need solutions NOW  |
| **Penalties** | Up to **₩30 million** (approx. $23,000 USD) for violations  |


## 🎯 Korea AI Basic Act Core Requirements

The Act establishes three main pillars of compliance :

### 1. High-Impact AI (고영향 AI)

| Requirement | Description | Applicable Sectors | JEP Solution |
|-------------|-------------|---------------------|--------------|
| **Pre-Assessment** | Determine if AI qualifies as "high-impact" | Healthcare, Energy, Transportation, Employment, Loan Reviews, Education, Public Services  | `classify_high_impact()` |
| **Risk Management Plan** | Identify and mitigate risks throughout lifecycle | All high-impact sectors | `create_risk_plan()` |
| **Human Oversight** | Establish human monitoring and intervention mechanisms | Critical infrastructure, life-safety applications | `human_approver` field |
| **Explainability** | Provide meaningful explanations for AI decisions | Any consequential decision affecting users | `explain_decision()` |
| **Documentation** | Maintain compliance records | All high-impact AI | `generate_documentation()` |

**Currently, only Level 4+ autonomous vehicles are officially designated as high-impact, but this list is expected to expand rapidly** .

### 2. Generative AI Transparency (생성형 AI 투명성)

| Scenario | Labeling Requirement | JEP Solution |
|----------|----------------------|--------------|
| **Within Service Environment** (in-app, on-screen, chatbots, games) | Flexible labeling – UI symbols, login guidance, on-screen indicators | `add_service_watermark()` |
| **Exported Outside Service** (downloadable/shareable content: text, images, video) | **Strict labeling** – visible/audible watermark OR metadata + text/audio guidance | `add_download_watermark()` |
| **Deepfakes** (difficult to distinguish from reality) | Clear, unambiguous disclosure to prevent misunderstanding | `add_deepfake_label()` |
| **Artistic/Creative Works** | Labeling that does not interfere with artistic appreciation | `add_creative_label()`  |

### 3. Foreign Company Local Representative (국내대리인)

| Threshold (meet ANY) | Requirement | JEP Solution |
|----------------------|-------------|--------------|
| **Global Annual Revenue** | ≥ ₩1 trillion (≈ $681M USD) | `appoint_local_representative()` |
| **Korea Sales** | ≥ ₩10 billion (≈ $6.8M USD) | `appoint_local_representative()` |
| **Korea Daily Active Users** | ≥ 1 million users | `appoint_local_representative()` |

**Applicable to**: OpenAI, Google, Meta, and other major global AI providers .


## 📊 Korea AI Basic Act vs. Other Jurisdictions

| Aspect | Korea | EU AI Act | Vietnam | JEP Alignment |
|--------|-------|-----------|---------|---------------|
| **Risk Classification** | "High-Impact AI" (flexible) | 4-tier (unacceptable/high/limited/minimal) | 3-tier (high/medium/low) | ✅ Adaptable |
| **Generative AI Labeling** | **Flexible in-app, strict for exports**  | Article 50 (machine-readable) | Mandatory watermarks | ✅ Content provenance module |
| **Human Oversight** | Required for high-impact | Article 14 | "Human-in-command" | ✅ Delegate primitive |
| **Explainability** | "Technically feasible"  | Article 86 | Explicit right | ✅ Decision factors |
| **Foreign Representative** | Yes (₩1T revenue/1M DAU) | Yes (Art. 27) | Yes (Art. 14) | ✅ Universal agent mechanism |
| **Grace Period** | **≥1 year**  | 6-36 months | 12-18 months | ✅ Transition support |
| **Enforcement** | Fines up to ₩30M  | €35M or 7% revenue | Case-by-case | ✅ Compliance reporting |


## 🚨 The 98% Opportunity

According to Korean media surveys :

- **Only 2%** of Korean AI startups have established compliance systems
- **98%** express difficulty meeting the Act's requirements
- **SMEs and startups** lack resources for expensive legal consultation
- **Large foreign providers** (OpenAI, Google) urgently need compliance solutions

**JEP provides the answer** – an open-source, ready-to-implement compliance framework that any company can adopt immediately.


## 🚀 Quick Start

```python
from jep.kr import KoreaAITracker

# Initialize tracker
tracker = KoreaAITracker(
    organization="Your Company",
    company_type="developer",  # or "provider", "deployer"
    jurisdiction="domestic"    # or "foreign"
)

# 1. Classify high-impact AI
classification = tracker.classify_high_impact({
    "system_name": "Loan Approval AI",
    "sector": "financial",
    "description": "AI for creditworthiness assessment",
    "human_oversight": True,
    "risk_management_plan": "RMP-2026-001"
})

# 2. Apply appropriate labeling based on deployment scenario
# For in-app/chatbot use (flexible labeling)
watermark = tracker.add_service_watermark({
    "content": "AI-generated response",
    "context": "chatbot",
    "disclosure": "symbol"
})

# For downloadable content (strict labeling)
download_watermark = tracker.add_download_watermark({
    "content": ai_generated_image,
    "content_type": "image",
    "watermark_type": "visible"
})

# 3. For foreign companies: appoint local representative
if tracker.requires_local_representative():
    tracker.appoint_local_representative({
        "representative_name": "Korea Compliance Office",
        "address": "Seoul, South Korea",
        "contact": "compliance@yourcompany.kr",
        "authorized_officer": "Kim Min-su"
    })

# 4. Generate compliance report
report = tracker.generate_compliance_report()
```


## 📁 Repository Structure

```
jep-kr-solutions/
├── README.md                          # This file
├── ai-basic-act/                        # AI Basic Act (effective Jan 22, 2026)
│   ├── README.md                         # Act overview (한국어/English)
│   ├── mapping.md                         # Detailed article mapping
│   ├── implementation/
│   │   └── kr_tracker.py                   # Core implementation
│   └── examples/
│       ├── high-impact-ai.py                # Healthcare/Finance/Energy examples
│       ├── content-labeling.py               # Flexible vs strict labeling demo
│       ├── local-representative.py            # Foreign company compliance
│       └── explainability.py                  # Right to explanation demo
└── tests/
    └── verify-korea.py                      # Compliance verification script
```


## 🔍 Verification for Regulators

```bash
# One-command compliance verification
python tests/verify-korea.py --all --output html --report kr-audit.html

# Output:
# ========================================
# KOREA AI BASIC ACT COMPLIANCE VERIFICATION
# ========================================
# ✅ High-Impact AI Classification
# ✅ Human Oversight Mechanisms
# ✅ Risk Management Plan
# ✅ In-App Labeling (flexible)
# ✅ Downloadable Content Labeling (strict)
# ✅ Explainability (technically feasible)
# ✅ Foreign Representative (if applicable)
# ========================================
# ✅ FULL COMPLIANCE VERIFIED
# ========================================
```


## 🏛️ Legal Foundation

JEP is stewarded by **HJS Foundation LTD** (Singapore CLG), a non-profit organization with permanent asset lock. The foundation's constitution explicitly prohibits:

- Distribution of profits to members (Article 7B)
- Transfer or sale of core assets (Article 67A)

**Registered Address**: 101 Thomson Road #28-03A, United Square, Singapore 307591


## 📚 References

- [AI Basic Act (시행 2026. 1. 22.)](https://www.law.go.kr/) - Korea Law Translation Center 
- [Transparency Guidelines (2026.1. 개정)](https://www.msit.go.kr/) - Ministry of Science and ICT 
- [Enforcement Decree (대통령령 제35249호)](https://www.msit.go.kr/) - Effective Jan 22, 2026 
- [AI Support Desk](https://www.kosa.or.kr/) - Korea AI & Software Industry Association (KOSA) 


## 📬 Contact

For Korea-specific inquiries:
- **Email**: signal@humanjudgment.org
- **GitHub**: [hjs-spec/jep-kr-solutions](https://github.com/hjs-spec/jep-kr-solutions)
- **Support**: 72-hour response for general inquiries, 14 days for complex legal questions 


## ⚠️ Note on Grace Period

The Ministry of Science and ICT (MSIT) has announced a **minimum one-year grace period** before imposing fines . During this period:

- Fact-finding investigations will occur only in **exceptional circumstances** (e.g., fatal accidents, human rights violations) 
- Companies have time to adapt and implement compliance systems
- JEP is the ideal solution to achieve compliance during this window

---

*Designed for the Republic of Korea 🇰🇷, serving Asia's AI future*
