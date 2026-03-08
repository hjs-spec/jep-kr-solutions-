# JEP Mapping to Korea's AI Basic Act (시행 2026. 1. 22.)

**Detailed Article-by-Article Mapping with Code Examples and Verification Methods**

## 📋 Overview

This document provides a comprehensive mapping between the **Judgment Event Protocol (JEP)** and Korea's **Framework Act on the Development of Artificial Intelligence and the Creation of a Foundation for Trust** (AI Basic Act), which took effect **January 22, 2026** .

The Act establishes Korea as the **second nation globally** (after the EU) and the **first in Asia** to enact comprehensive AI legislation, combining innovation promotion with robust governance of high-impact and generative AI systems .

---

## 📊 Chapter I: General Provisions

### Article 2: Key Definitions

| Term | Definition (Korean) | JEP Implementation |
|------|---------------------|-------------------|
| **High-Impact AI** (고영향 AI) | AI systems that may have significant effect on or pose risks to human life, physical safety or fundamental rights, utilized in 10 specified sectors  | `risk_level="HIGH"` + sector classification |
| **Generative AI** (생성형 AI) | AI systems that generate text, sound, images, videos by imitating input data structures  | `content_type` parameter |
| **AI Business Operator** (AI사업자) | Developers and providers of AI products/services  | `entity_type` (developer/provider/deployer) |
| **User** (이용자) | Person provided with AI products/services | `user_id` tracking |
| **Impacted Person** (영향을 받는 사람) | Person whose life, safety, rights are significantly affected by AI  | `consumer_id` + `affected_person` flag |

**Code Example:**
```python
from jep.kr import KoreaAITracker

# Different roles in the AI supply chain
developer = KoreaAITracker(entity_type="developer", org="AI Lab")
provider = KoreaAITracker(entity_type="provider", org="AI Services Inc.")
deployer = KoreaAITracker(entity_type="deployer", org="Bank of Korea")

# Track impacted persons
decision = deployer.log_consequential_decision({
    "consumer_id": "USER-123",
    "decision": "REJECT",
    "affected_person": True,
    "impact_assessment": "Loan denial affects fundamental rights"
})
```

### Article 3: Basic Principles

| Principle | JEP Implementation | Code Example |
|-----------|-------------------|--------------|
| **Human oversight and intervention** | `human_approver` field | `decision["human_approver"] = "manager-456"` |
| **Explainability** (to extent technically feasible) | `explain_decision()` method | `tracker.explain_decision(decision_id)` |
| **Safety and trustworthiness** | Risk management + incident response | `create_risk_plan()`, `log_incident()` |

**Code Example:**
```python
# Article 3(2): Right to explanation (technically feasible)
if tracker.is_explainability_feasible(system_id):
    explanation = tracker.generate_explanation({
        "decision_id": decision_id,
        "language": "ko",
        "detail_level": "meaningful"
    })
    # Output: Clear explanation of decision factors
```

### Article 4: Scope of Application

| Requirement | JEP Implementation | Code Example |
|-------------|-------------------|--------------|
| **Extraterritorial application** - applies to overseas activities affecting Korean market/users  | `jurisdiction="foreign"` + local representative | `tracker.appoint_local_representative()` |
| **National defense exemption** | `exemption="national_defense"` | `tracker.apply_exemption()` |

---

## 📊 Chapter II: Governance Structure

### Articles 6-8: National AI Committee & Policy Center

| Structure | Role | JEP Alignment |
|-----------|------|---------------|
| **National AI Committee** (President-led) | Deliberate major AI policies  | Compliance reporting |
| **AI Policy Center** (within MSIT) | Technical support, policy assistance | Technical consultation |
| **AI Safety Research Institute** | Risk analysis, safety standards  | Incident response integration |

---

## 📊 Chapter III: Transparency Obligations (제3장 투명성 확보)

### Article 31: Transparency Obligations for AI Business Operators

The Act establishes three-tier transparency obligations based on extensive industry consultation :

| Requirement | Details | JEP Implementation | Verification |
|-------------|---------|-------------------|--------------|
| **§31(1) Advance Notice** | Users must be informed that service uses generative/high-impact AI | `advance_notice()` | `verify-korea.py --notice` |
| **§31(2) Output Labeling** | Generative AI outputs must be labeled as AI-generated | `label_output()` | `verify-korea.py --label` |
| **§31(3) Deepfake Disclosure** | Realistic synthetic content must be clearly disclosed | `disclose_deepfake()` | `verify-korea.py --deepfake` |

### Article 22 of Enforcement Decree & Transparency Guidelines

The Transparency Guidelines provide **scenario-specific labeling requirements** based on whether content stays within service environment or is exported :

#### Scenario 1: AI Products Provided Only Within Service Environment

| Service Type | Labeling Requirement | JEP Implementation |
|--------------|----------------------|-------------------|
| **Chatbots/Interactive Services** | Pre-use guidance + on-screen symbol/logo | `add_chatbot_disclosure()` |
| **Games/Virtual Environments** | Login guidance, on-screen indicators for AI characters | `add_game_watermark()` |
| **In-App AI Features** | UI indicators, symbols | `add_ui_indicator()` |

**Code Example - Flexible In-App Labeling:**
```python
# For chatbot services (in-app only)
def deploy_chatbot():
    tracker = KoreaAITracker(organization="AI Chatbot Co.")
    
    # Pre-use guidance at login
    tracker.add_login_disclosure({
        "message": "This service uses AI to generate responses",
        "language": "ko",
        "position": "login_screen"
    })
    
    # On-screen indicator during chat
    tracker.add_ui_indicator({
        "type": "symbol",
        "symbol": "🤖",
        "position": "chat_header",
        "tooltip": "AI-generated response"
    })
    
    # Each chat response labeled (flexible UI)
    response = tracker.generate_response(user_input)
    return {
        "content": response,
        "ui_indicator": "🤖",  # Visible in UI only
        "metadata": {"ai_generated": True}  # Machine-readable
    }
```

#### Scenario 2: AI Products Exported Outside Service Environment

| Content Type | Labeling Requirement | JEP Implementation |
|--------------|----------------------|-------------------|
| **Downloadable Text/Images/Videos** | Option A: Visible/audible watermark OR Option B: Metadata + text/audio guidance  | `add_download_watermark()` |
| **Deepfake Content** | Clear human-readable indication to prevent misunderstanding  | `add_deepfake_label()` |
| **Artistic/Creative Works** | Flexible labeling that doesn't interfere with appreciation  | `add_artistic_label()` |

**Code Example - Strict Labeling for Exported Content:**
```python
# For downloadable AI-generated images
def generate_downloadable_image(prompt):
    tracker = KoreaAITracker(organization="AI Image Gen")
    
    image = tracker.generate_image(prompt)
    
    # Option A: Visible watermark (strict labeling)
    watermarked = tracker.add_visible_watermark({
        "image": image,
        "watermark_text": "AI 생성",
        "position": "bottom_right",
        "opacity": 0.7,
        "permanent": True
    })
    
    # Alternative Option B: Metadata + user guidance
    # metadata_only = tracker.add_metadata_label({
    #     "content": image,
    #     "metadata": {"ai_generated": True, "model": "v2.1"},
    #     "user_guidance": {
    #         "text": "This image was created by AI",
    #         "audio": "audio_guidance.mp3"
    #     }
    # })
    
    return watermarked

# For deepfake videos (must be clearly distinguishable from reality)
def create_deepfake_video(source_person, target_speech):
    tracker = KoreaAITracker(organization="Media Corp")
    
    video = tracker.generate_deepfake({
        "source_person": source_person,
        "target_speech": target_speech,
        "consent_obtained": True
    })
    
    # Add clear visible warning (required for deepfakes)
    labeled = tracker.add_deepfake_label({
        "video": video,
        "warning_text": "⚠️ 딥페이크: 실제 인물을 모방한 AI 생성 콘텐츠",
        "display_duration": "entire_video",
        "position": "top_left",
        "size": "large"
    })
    
    return labeled
```

### Exemptions from Transparency Obligations

| Exemption | Criteria | JEP Implementation |
|-----------|----------|-------------------|
| **Obvious AI Use** | Clearly identifiable as AI from product/service name  | `check_obvious_ai()` |
| **Internal Business Use** | AI used only as productivity tool by employees  | `use_case="internal"` |

**Code Example - Exemption Check:**
```python
def check_exemption(use_case, product_name):
    tracker = KoreaAITracker()
    
    # Exemption 1: Obvious AI use (e.g., product named "AI Assistant")
    if tracker.is_obvious_ai(product_name):
        return {"exempt": True, "reason": "obvious_ai_use"}
    
    # Exemption 2: Internal business use only
    if use_case == "internal":
        return {"exempt": True, "reason": "internal_use"}
    
    return {"exempt": False}
```

---

## 📊 Chapter IV: High-Impact AI (고영향 AI)

### Article 33: Determination of High-Impact AI

**Two-Step Test** per Determination Guidelines :

1. **Sector Test**: Is the AI utilized in one of 10 enumerated sectors?
2. **Impact Test**: Does it have significant impact or pose risks to human life, physical safety, or fundamental rights?

**10 High-Impact Sectors** (Article 2, Subparagraph 4) :

| Sector | Korean | JEP Classification |
|--------|--------|-------------------|
| **Energy** | 에너지 공급 | `sector="energy"` |
| **Drinking Water** | 먹는물 생산 | `sector="water"` |
| **Healthcare** | 의료서비스 | `sector="healthcare"` |
| **Medical Devices** | 의료기기·디지털의료기기 | `sector="medical_devices"` |
| **Nuclear Safety** | 원자력 시설 | `sector="nuclear"` |
| **Biometric Analysis** | 생체정보 분석·활용 | `sector="biometric"` |
| **Employment & Loan Decisions** | 채용·대출심사 | `sector="employment", "financial"` |
| **Transportation** | 교통수단·시설 운영 | `sector="transportation"` |
| **Government Decision-Making** | 공공 서비스 제공 | `sector="government"` |
| **Student Evaluation** | 학생 평가 | `sector="education"` |

**Code Example - Two-Step Determination:**
```python
def classify_high_impact(system_data):
    tracker = KoreaAITracker()
    
    # Step 1: Sector test
    sector = system_data.get("sector")
    high_impact_sectors = [
        "energy", "water", "healthcare", "medical_devices", "nuclear",
        "biometric", "employment", "financial", "transportation", 
        "government", "education"
    ]
    
    if sector not in high_impact_sectors:
        return {"high_impact": False, "reason": "Not in designated sectors"}
    
    # Step 2: Impact test 
    impact_score = 0
    if system_data.get("affects_safety"):
        impact_score += 30
    if system_data.get("affects_rights"):
        impact_score += 30
    if system_data.get("automation_level") == "high":
        impact_score += 20
    if system_data.get("user_scale") > 100000:
        impact_score += 20
    
    is_high_impact = impact_score >= 50
    
    return {
        "high_impact": is_high_impact,
        "sector": sector,
        "impact_score": impact_score,
        "risk_level": "HIGH" if is_high_impact else "STANDARD"
    }

# Example usage
result = classify_high_impact({
    "sector": "employment",
    "affects_rights": True,
    "automation_level": "medium",
    "user_scale": 50000
})
```

### Article 34: Obligations for High-Impact AI Providers

| Obligation | Korean | JEP Implementation | Verification |
|------------|--------|-------------------|--------------|
| **Risk Management Plan** | 위험관리계획 수립·운영 | `create_risk_plan()` | `verify-korea.py --risk-plan` |
| **Explainability** | 설명 방안 마련 (기술적 범위 내) | `enable_explainability()` | `verify-korea.py --explain` |
| **User Protection** | 이용자 보호 방안 마련 | `user_protection_plan()` | `verify-korea.py --protection` |
| **Human Oversight** | 인적 관리·감독 | `human_approver` field | `verify-korea.py --oversight` |
| **Documentation** | 관련 자료 작성·보존 | `maintain_documentation()` | `verify-korea.py --docs` |

**Code Example - High-Impact AI Compliance:**
```python
class HighImpactAITracker:
    def __init__(self, system_id):
        self.tracker = KoreaAITracker()
        self.system_id = system_id
        
        # 1. Risk Management Plan (Article 34.1)
        self.risk_plan = self.tracker.create_risk_plan({
            "system_id": system_id,
            "risk_identification": ["bias", "safety", "security"],
            "risk_assessment": "quarterly",
            "mitigation_measures": [
                "bias_testing",
                "human_oversight",
                "continuous_monitoring"
            ],
            "responsible_officer": "risk-manager@company.kr"
        })
        
        # 2. Explainability (Article 34.2) - "to the extent technically feasible"
        if self.tracker.is_explainability_feasible(system_id):
            self.tracker.enable_explainability({
                "system_id": system_id,
                "explanation_level": "meaningful",
                "language_support": ["ko", "en"],
                "factor_breakdown": True
            })
        
        # 3. Human Oversight (Article 34.4)
        self.tracker.configure_oversight({
            "system_id": system_id,
            "mechanism": "dual_approval",
            "approvers": ["loan_officer", "credit_manager"],
            "override_capability": True,
            "escalation_procedure": "automatic_for_high_risk"
        })
    
    def log_decision_with_oversight(self, decision_data):
        # Ensure human oversight for high-impact decisions
        decision = self.tracker.log_consequential_decision({
            **decision_data,
            "human_approver": "supervisor-456",  # Required
            "human_review_available": True,
            "explanation": self._generate_explanation(decision_data)
        })
        return decision
```

### Article 35: AI Impact Assessment

| Assessment Stage | Requirements | JEP Implementation |
|------------------|--------------|-------------------|
| **Pre-assessment** | Identify potential risk scenarios  | `identify_risks()` |
| **Main assessment** | Record risk scenarios, identify affected fundamental rights | `assess_impact()` |
| **Post-assessment** | Document results, implement safeguards | `document_assessment()` |

---

## 📊 Chapter V: Safety of High-Performance AI

### Article 32: Obligation to Ensure Safety

**High-Performance AI Criteria** (similar to EU frontier models) :

| Criteria | Threshold | JEP Implementation |
|----------|-----------|-------------------|
| **Computational Volume** | ≥ 10²⁶ FLOPs | `track_compute()` |
| **Advanced Technology** | Most advanced AI technologies | `track_capabilities()` |
| **Significant Risk** | Broad impact on life, safety, rights | `risk_assessment()` |

**Code Example - High-Performance AI Compliance:**
```python
# For AI systems exceeding computational thresholds
if tracker.calculate_flops(model) >= 1e26:
    # Establish risk management system throughout lifecycle
    tracker.establish_risk_system({
        "model_id": "frontier-model-v2",
        "risk_identification": "continuous",
        "mitigation_gates": ["pre-training", "pre-deployment"],
        "monitoring_frequency": "real-time",
        "incident_response": "24-hour reporting"
    })
    
    # Submit results to MSIT
    tracker.submit_safety_results({
        "reporting_period": "2026-Q1",
        "risk_assessments": assessments,
        "incidents": incidents,
        "mitigations": implemented_measures
    })
```

---

## 📊 Chapter VI: Foreign Companies & Local Representatives

### Article 4 + Enforcement Decree: Domestic Agent Requirement

**Applicability Thresholds** (meet ANY) :

| Threshold | Value | JEP Implementation |
|-----------|-------|-------------------|
| **Global Annual Revenue** | ≥ ₩1 trillion (~$681M) | `check_revenue()` |
| **Korea Sales** | ≥ ₩10 billion (~$6.8M) | `check_korea_sales()` |
| **Korea Daily Active Users** | ≥ 1 million users | `check_dau()` |

**Code Example - Foreign Company Compliance:**
```python
class ForeignAIProvider:
    def __init__(self, company_name):
        self.tracker = KoreaAITracker(
            organization=company_name,
            jurisdiction="foreign"
        )
        
        # Check if local representative required
        if self._requires_local_representative():
            self.appoint_representative()
    
    def _requires_local_representative(self):
        # Check thresholds 
        revenue_check = self.annual_revenue >= 1e12  # ₩1 trillion
        korea_sales_check = self.korea_sales >= 1e10  # ₩10 billion
        dau_check = self.korea_dau >= 1_000_000
        
        return revenue_check or korea_sales_check or dau_check
    
    def appoint_representative(self):
        """Appoint domestic agent as required by law"""
        self.tracker.appoint_local_representative({
            "representative_name": "Korea Compliance Office",
            "entity_type": "corporation",
            "address": "Seoul, South Korea",
            "contact": "compliance@foreignai.kr",
            "authorized_officer": "Kim Min-su",
            "authorization_document": "power_of_attorney_2026.pdf",
            "effective_date": time.time()
        })
        
        print(f"✅ Local representative appointed: Korea Compliance Office")
        print(f"   Authorized officer: Kim Min-su")
        print(f"   Authority: All compliance matters under AI Basic Act")
```

---

## 📊 Chapter VII: Penalties & Grace Period

### Article 43: Penalties

| Violation | Penalty | JEP Mitigation |
|-----------|---------|----------------|
| **Failure to provide advance notice** | Up to ₩30M (~$21,000)  | `advance_notice()` |
| **No output labeling** | Up to ₩30M | `label_output()` |
| **No local representative** | Up to ₩30M | `appoint_local_representative()` |
| **Failure to comply with corrective orders** | Up to ₩30M | `track_compliance()` |

### Grace Period Implementation

The MSIT has announced a **minimum one-year grace period** :

| Feature | Duration | JEP Support |
|---------|----------|-------------|
| **Fact-finding investigations** | Suspended (except exceptional cases) | `track_grace_period()` |
| **Fines** | Suspended for ≥1 year | `compliance_timeline()` |
| **Industry consultations** | Ongoing | `participate_in_consultations()` |

**Code Example - Grace Period Management:**
```python
class GracePeriodTracker:
    def __init__(self, effective_date="2026-01-22"):
        self.effective_date = datetime.strptime(effective_date, "%Y-%m-%d")
        self.grace_period_end = self.effective_date + timedelta(days=365)
        
    def check_status(self):
        now = time.time()
        in_grace_period = now < self.grace_period_end.timestamp()
        
        return {
            "in_grace_period": in_grace_period,
            "grace_period_end": self.grace_period_end,
            "days_remaining": max(0, (self.grace_period_end - datetime.now()).days),
            "enforcement_priority": "low" if in_grace_period else "normal"
        }
    
    def is_exceptional_case(self, incident):
        """Fact-finding only in exceptional circumstances during grace period """
        exceptional = incident.get("severity") in ["fatal_accident", "human_rights_violation", "national_damage"]
        return exceptional
```

---

## 📊 Support Infrastructure

### AI Basic Act Support Desk (through KOSA) 

| Service | Response Time | JEP Integration |
|---------|---------------|-----------------|
| **General inquiries** | Within 72 hours | `submit_inquiry()` |
| **Complex legal questions** | Within 14 days | `request_consultation()` |
| **Confidential consulting** | Upon request | `confidential_mode()` |

---

## ✅ Complete Verification

```bash
# Run complete Korea AI Basic Act compliance verification
python tests/verify-korea.py --all

# Output:
# ========================================
# KOREA AI BASIC ACT COMPLIANCE VERIFICATION
# ========================================
#
# 📋 Chapter I: General Provisions
#   ✅ Article 2: Definitions
#   ✅ Article 3: Basic principles
#   ✅ Article 4: Scope (extraterritorial)
#
# 📋 Chapter III: Transparency
#   ✅ Article 31(1): Advance notice
#   ✅ Article 31(2): Output labeling
#   ✅ Article 31(3): Deepfake disclosure
#   ✅ Flexible labeling (in-app)
#   ✅ Strict labeling (exported)
#
# 📋 Chapter IV: High-Impact AI
#   ✅ Article 33: Two-step determination
#   ✅ Article 34: Risk management plan
#   ✅ Article 34: Human oversight
#   ✅ Article 34: Explainability
#
# 📋 Chapter V: High-Performance AI
#   ✅ Article 32: Safety obligations
#
# 📋 Chapter VI: Foreign Companies
#   ✅ Local representative appointment
#
# 📋 Chapter VII: Penalties
#   ✅ Grace period tracking
#
# ========================================
# ✅ FULL COMPLIANCE VERIFIED
# ========================================
```

## 📚 References

- [AI Basic Act (시행 2026. 1. 22.) - Full English Text](https://elaw.klri.re.kr/eng_mobile/viewer.do?hseq=71019) 
- [Enforcement Decree (대통령령 제35249호)](https://www.msit.go.kr/) 
- [Transparency Guidelines (2026.1. 개정)](https://www.msit.go.kr/) 
- [High-Impact AI Determination Guidelines](https://digitalpolicyalert.org/event/37415) 
- [AI Basic Act Support Desk (through KOSA)](https://www.kosa.or.kr/) 

## 📬 Contact

For Korea-specific inquiries:
- **Email**: korea@humanjudgment.org
- **GitHub**: [hjs-spec/jep-kr-solutions](https://github.com/hjs-spec/jep-kr-solutions)
- **Support**: 72-hour response for general inquiries, 14 days for complex legal questions 

---

*Last Updated: March 2026*
*대한민국 AI 기본법 완전 준수*
```
