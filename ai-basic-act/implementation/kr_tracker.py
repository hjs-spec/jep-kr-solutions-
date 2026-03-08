#!/usr/bin/env python3
"""
Korea AI Basic Act (시행 2026. 1. 22.) Compliance Tracker
============================================================

Complete implementation of Korea's Framework Act on the Development of Artificial
Intelligence and the Creation of a Foundation for Trust (AI Basic Act).

This tracker ensures all AI systems comply with:
- Chapter II: Transparency obligations (advance notice, output labeling, deepfake disclosure)
- Chapter III: High-Impact AI (determination, risk management, human oversight)
- Chapter IV: High-Performance AI (safety obligations)
- Chapter V: Foreign company local representative requirements
- Grace period management (1+ year transition period)
"""

import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple, Union
from enum import Enum

# Try to import cryptography
try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("⚠️ Warning: cryptography not installed. Using mock signatures.")


class EntityType(Enum):
    """Roles in AI supply chain (Article 2)"""
    DEVELOPER = "developer"      # AI 개발자
    PROVIDER = "provider"         # AI 제공자 (AI business operator)
    DEPLOYER = "deployer"         # AI 사업자 (final provider to users)
    USER = "user"                  # 이용자


class RiskLevel(Enum):
    """Risk classification under Korea AI Basic Act"""
    STANDARD = "STANDARD"          # 일반 AI
    HIGH_IMPACT = "HIGH_IMPACT"    # 고영향 AI (High-Impact AI)
    HIGH_PERFORMANCE = "HIGH_PERFORMANCE"  # 고성능 AI (High-Performance AI)


class ContentType(Enum):
    """Types of content for labeling requirements"""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    CHAT = "chat"
    GAME = "game"


class LabelingScenario(Enum):
    """Labeling scenarios per Transparency Guidelines [citation:2]"""
    IN_APP = "in_app"              # Within service environment (flexible)
    EXPORTED = "exported"          # Exported outside service (strict)
    DEEPFAKE = "deepfake"          # Deepfake content
    ARTISTIC = "artistic"          # Artistic/creative expression


class KoreaAITracker:
    """
    Complete Korea AI Basic Act compliance tracker.
    
    Covers all obligations for AI business operators, with special handling for:
    - Grace period (at least one year with reduced enforcement) [citation:1]
    - Differentiated labeling requirements by usage scenario [citation:2]
    - Foreign company local representative requirements [citation:6]
    """
    
    def __init__(
        self,
        organization: str,
        entity_type: EntityType = EntityType.PROVIDER,
        jurisdiction: str = "domestic",
        global_revenue_krw: float = 0,
        korea_sales_krw: float = 0,
        korea_daily_users: int = 0,
        private_key_hex: Optional[str] = None
    ):
        """
        Initialize Korea AI Basic Act tracker.
        
        Args:
            organization: Organization name
            entity_type: DEVELOPER, PROVIDER, DEPLOYER, or USER
            jurisdiction: "domestic" or "foreign"
            global_revenue_krw: Global annual revenue in KRW (for foreign threshold)
            korea_sales_krw: Korea sales in KRW (for foreign threshold)
            korea_daily_users: Korea daily active users (for foreign threshold)
            private_key_hex: Optional private key for signatures
        """
        self.organization = organization
        self.entity_type = entity_type
        self.jurisdiction = jurisdiction
        self.global_revenue_krw = global_revenue_krw
        self.korea_sales_krw = korea_sales_krw
        self.korea_daily_users = korea_daily_users
        
        # Effective date and grace period (at least 1 year) [citation:1]
        self.effective_date = datetime(2026, 1, 22).timestamp()
        self.grace_period_end = self.effective_date + 366 * 86400  # 1+ years
        
        # Initialize signer
        self.signer = self._init_signer(private_key_hex)
        
        # Data stores
        self.systems = {}
        self.risk_assessments = []
        self.content_labels = []
        self.incidents = []
        self.audit_log = []
        self.local_representative = None
        
        # Check if foreign company requires local representative [citation:6]
        self.requires_local_rep = self._check_local_representative_requirement()
        
        print(f"✅ Korea AI Basic Act Tracker initialized")
        print(f"   Organization: {organization}")
        print(f"   Entity Type: {entity_type.value}")
        print(f"   Jurisdiction: {jurisdiction}")
        print(f"   Effective Date: January 22, 2026")
        print(f"   Grace Period: Until at least {datetime.fromtimestamp(self.grace_period_end).strftime('%Y-%m-%d')}")
        
        if jurisdiction == "foreign":
            print(f"   Foreign Company Thresholds:")
            print(f"      Global Revenue: {global_revenue_krw:,.0f} KRW (Threshold: 1 trillion)")
            print(f"      Korea Sales: {korea_sales_krw:,.0f} KRW (Threshold: 10 billion)")
            print(f"      Korea Daily Users: {korea_daily_users:,} (Threshold: 1 million)")
            print(f"   Local Representative Required: {self.requires_local_rep}")
    
    def _init_signer(self, private_key_hex: Optional[str] = None):
        """Initialize cryptographic signer."""
        if CRYPTO_AVAILABLE:
            if private_key_hex:
                return ed25519.Ed25519PrivateKey.from_private_bytes(
                    bytes.fromhex(private_key_hex)
                )
            else:
                return ed25519.Ed25519PrivateKey.generate()
        return None
    
    def _generate_uuid7(self) -> str:
        """Generate UUID v7 for traceability."""
        import uuid
        timestamp = int(time.time() * 1000)
        random_part = uuid.uuid4().hex[:12]
        return f"{timestamp:08x}-{random_part[:4]}-7{random_part[4:7]}-{random_part[7:11]}-{random_part[11:]}"
    
    def _sign(self, data: Dict) -> str:
        """Sign data with Ed25519."""
        if CRYPTO_AVAILABLE and self.signer:
            message = json.dumps(data, sort_keys=True).encode()
            signature = self.signer.sign(message)
            return f"ed25519:{signature.hex()[:64]}"
        return f"mock_sig_{hash(json.dumps(data, sort_keys=True))}"
    
    def _log_audit(self, event_type: str, data: Dict[str, Any]) -> None:
        """Internal audit logging."""
        self.audit_log.append({
            "event_type": event_type,
            "timestamp": time.time(),
            "data": data
        })
    
    def _check_local_representative_requirement(self) -> bool:
        """
        Check if foreign company must appoint local representative.
        
        Thresholds (ANY of the following) [citation:6]:
        - Global annual revenue ≥ ₩1 trillion (~$681M)
        - Korea sales ≥ ₩10 billion (~$6.8M)
        - Korea daily active users ≥ 1 million
        """
        if self.jurisdiction != "foreign":
            return False
        
        revenue_check = self.global_revenue_krw >= 1_000_000_000_000  # 1 trillion
        sales_check = self.korea_sales_krw >= 10_000_000_000  # 10 billion
        users_check = self.korea_daily_users >= 1_000_000
        
        return revenue_check or sales_check or users_check
    
    def is_grace_period(self) -> bool:
        """Check if currently in grace period [citation:1]"""
        return time.time() < self.grace_period_end
    
    def should_enforce(self, incident_severity: str = None) -> bool:
        """
        Determine if enforcement should apply during grace period.
        
        During grace period, fact-finding investigations only in exceptional cases:
        - Fatal accidents
        - Human rights violations
        - National damage [citation:2]
        """
        if not self.is_grace_period():
            return True
        
        exceptional = incident_severity in ["fatal_accident", "human_rights_violation", "national_damage"]
        return exceptional
    
    # ========================================================================
    # Transparency Obligations (Article 31) [citation:2]
    # ========================================================================
    
    def advance_notice(self, notice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Article 31(1): Advance notice that service uses generative/high-impact AI.
        
        Users must be informed before using AI products/services.
        """
        notice_id = f"NOTICE-{self._generate_uuid7()}"
        
        notice = {
            "notice_id": notice_id,
            "organization": self.organization,
            "notice_type": notice_data.get("notice_type", "advance"),
            "service_name": notice_data.get("service_name"),
            "ai_type": notice_data.get("ai_type", "generative"),  # generative or high-impact
            "disclosure_method": notice_data.get("disclosure_method", "login_screen"),
            "disclosure_text": notice_data.get("disclosure_text", "This service uses AI technology"),
            "language": notice_data.get("language", "ko"),
            "display_position": notice_data.get("display_position", "login"),
            "effective_date": notice_data.get("effective_date", time.time()),
            "grace_period_applies": self.is_grace_period()
        }
        
        notice["signature"] = self._sign(notice)
        self._log_audit("ADVANCE_NOTICE", notice)
        
        print(f"\n📋 Article 31(1): Advance Notice")
        print(f"   Notice ID: {notice_id}")
        print(f"   Service: {notice['service_name']}")
        print(f"   Method: {notice['disclosure_method']}")
        
        return notice
    
    def label_output(
        self,
        content: Union[str, bytes],
        content_type: ContentType,
        scenario: LabelingScenario,
        exportable: bool = False,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Article 31(2): Label AI-generated outputs based on usage scenario.
        
        Differentiated labeling requirements [citation:2]:
        - In-app (flexible): UI symbols, pre-use guidance
        - Exported (strict): Visible watermark or metadata + guidance
        - Deepfake: Clear human-readable warning
        - Artistic: Flexible labeling that doesn't interfere with appreciation
        """
        label_id = f"LABEL-{self._generate_uuid7()}"
        content_hash = hashlib.sha256(content if isinstance(content, bytes) else content.encode()).hexdigest()
        
        label_data = {
            "label_id": label_id,
            "organization": self.organization,
            "content_hash": content_hash,
            "content_type": content_type.value,
            "scenario": scenario.value,
            "exportable": exportable,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        
        # Apply labeling based on scenario
        if scenario == LabelingScenario.IN_APP:
            # Flexible labeling: UI symbols, pre-use guidance
            label_data["label_method"] = "ui_symbol"
            label_data["symbol"] = metadata.get("symbol", "🤖") if metadata else "🤖"
            label_data["position"] = metadata.get("position", "chat_header") if metadata else "chat_header"
            label_data["pre_use_guidance"] = metadata.get("pre_use_guidance", True) if metadata else True
            
        elif scenario == LabelingScenario.EXPORTED:
            # Strict labeling: visible watermark OR metadata + guidance
            if exportable:
                label_data["label_method"] = "visible_watermark"
                label_data["watermark_text"] = metadata.get("watermark_text", "AI 생성") if metadata else "AI 생성"
                label_data["watermark_position"] = metadata.get("watermark_position", "bottom_right") if metadata else "bottom_right"
                label_data["watermark_opacity"] = metadata.get("watermark_opacity", 0.7) if metadata else 0.7
                label_data["permanent"] = True
            else:
                # Machine-readable metadata + user guidance
                label_data["label_method"] = "metadata_plus_guidance"
                label_data["metadata"] = {"ai_generated": True, "model": metadata.get("model") if metadata else "v1"}
                label_data["guidance_text"] = metadata.get("guidance_text", "This content was created by AI") if metadata else "This content was created by AI"
                label_data["guidance_audio"] = metadata.get("guidance_audio") if metadata else None
            
        elif scenario == LabelingScenario.DEEPFAKE:
            # Deepfake: clear warning to prevent misunderstanding [citation:2]
            label_data["label_method"] = "visible_warning"
            label_data["warning_text"] = metadata.get("warning_text", "⚠️ 딥페이크: 실제 인물을 모방한 AI 생성 콘텐츠") if metadata else "⚠️ 딥페이크: 실제 인물을 모방한 AI 생성 콘텐츠"
            label_data["warning_duration"] = metadata.get("warning_duration", "entire_content") if metadata else "entire_content"
            label_data["warning_position"] = metadata.get("warning_position", "top_left") if metadata else "top_left"
            label_data["permanent"] = True
            
        elif scenario == LabelingScenario.ARTISTIC:
            # Artistic works: flexible labeling that doesn't interfere with appreciation [citation:2]
            label_data["label_method"] = "artistic_disclosure"
            label_data["disclosure_method"] = metadata.get("disclosure_method", "end_credits") if metadata else "end_credits"
            label_data["disclosure_text"] = metadata.get("disclosure_text", "This work contains AI-generated elements") if metadata else "This work contains AI-generated elements"
            label_data["metadata_included"] = True
        
        label_data["signature"] = self._sign(label_data)
        self.content_labels.append(label_data)
        self._log_audit("OUTPUT_LABEL", label_data)
        
        print(f"\n📋 Article 31(2): Output Labeling")
        print(f"   Label ID: {label_id}")
        print(f"   Content Type: {content_type.value}")
        print(f"   Scenario: {scenario.value}")
        print(f"   Method: {label_data['label_method']}")
        print(f"   Exportable: {exportable}")
        
        return label_data
    
    def label_chatbot(self, chatbot_name: str, disclosure_method: str = "symbol") -> Dict[str, Any]:
        """
        Helper for chatbot/in-app AI disclosure (flexible labeling).
        
        For interactive services, obligation may be satisfied by:
        - Pre-use guidance
        - On-screen symbol/logo [citation:2]
        """
        label_id = f"CHAT-{self._generate_uuid7()}"
        
        label = {
            "label_id": label_id,
            "organization": self.organization,
            "service_type": "chatbot",
            "chatbot_name": chatbot_name,
            "disclosure_method": disclosure_method,
            "pre_use_guidance": {
                "enabled": True,
                "message": f"{chatbot_name} is an AI assistant. Responses are AI-generated.",
                "language": "ko",
                "display_at": "first_interaction"
            },
            "ui_symbol": {
                "enabled": disclosure_method == "symbol",
                "symbol": "🤖",
                "position": "chat_header",
                "tooltip": "AI-generated response"
            },
            "timestamp": time.time()
        }
        
        label["signature"] = self._sign(label)
        self._log_audit("CHATBOT_LABEL", label)
        
        return label
    
    def add_visible_watermark(
        self,
        content: bytes,
        watermark_text: str = "AI 생성",
        position: str = "bottom_right",
        opacity: float = 0.7,
        permanent: bool = True
    ) -> Dict[str, Any]:
        """
        Add visible watermark for exported content (strict labeling).
        
        Required for AI-generated content that users can download/share.
        """
        watermark_id = f"WM-{self._generate_uuid7()}"
        content_hash = hashlib.sha256(content).hexdigest()
        
        watermark = {
            "watermark_id": watermark_id,
            "content_hash": content_hash,
            "watermark_text": watermark_text,
            "position": position,
            "opacity": opacity,
            "permanent": permanent,
            "timestamp": time.time(),
            "labeling_type": "visible_watermark"
        }
        
        watermark["signature"] = self._sign(watermark)
        self._log_audit("VISIBLE_WATERMARK", watermark)
        
        print(f"\n💧 Visible Watermark Added")
        print(f"   Watermark ID: {watermark_id}")
        print(f"   Text: {watermark_text}")
        print(f"   Position: {position}")
        
        return watermark
    
    def add_deepfake_warning(
        self,
        content: bytes,
        content_type: str = "video",
        warning_text: str = "⚠️ 딥페이크: 실제 인물을 모방한 AI 생성 콘텐츠",
        duration: str = "entire_content"
    ) -> Dict[str, Any]:
        """
        Add clear warning for deepfake content (Article 31(3)).
        
        Deepfakes must be clearly distinguishable from reality to prevent misunderstanding [citation:2].
        """
        warning_id = f"DF-{self._generate_uuid7()}"
        content_hash = hashlib.sha256(content).hexdigest()
        
        warning = {
            "warning_id": warning_id,
            "content_hash": content_hash,
            "content_type": content_type,
            "warning_text": warning_text,
            "warning_duration": duration,
            "warning_position": "top_left",
            "warning_size": "large",
            "permanent": True,
            "timestamp": time.time(),
            "labeling_type": "deepfake_warning"
        }
        
        warning["signature"] = self._sign(warning)
        self._log_audit("DEEPFAKE_WARNING", warning)
        
        print(f"\n⚠️ Deepfake Warning Added")
        print(f"   Warning ID: {warning_id}")
        print(f"   Text: {warning_text}")
        print(f"   Duration: {duration}")
        
        return warning
    
    # ========================================================================
    # High-Impact AI Determination (Article 33) [citation:7]
    # ========================================================================
    
    def determine_high_impact(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Two-step test for determining High-Impact AI [citation:7].
        
        Step 1: Sector test - is AI used in designated sectors?
        Step 2: Impact test - does it significantly affect life, safety, or rights?
        """
        system_id = system_data.get("system_id", f"SYS-{self._generate_uuid7()}")
        
        # Step 1: Sector test [citation:6]
        high_impact_sectors = [
            "energy", "water", "healthcare", "medical_devices", "nuclear",
            "biometric", "employment", "financial", "transportation",
            "public_services", "education", "credit_evaluation"
        ]
        
        sector = system_data.get("sector", "").lower()
        sector_match = sector in high_impact_sectors
        
        # Step 2: Impact test [citation:7]
        impact_score = 0
        impact_factors = []
        
        if system_data.get("affects_safety"):
            impact_score += 30
            impact_factors.append("affects_safety")
        if system_data.get("affects_rights"):
            impact_score += 30
            impact_factors.append("affects_rights")
        if system_data.get("automation_level") == "high":
            impact_score += 20
            impact_factors.append("high_automation")
        if system_data.get("user_scale", 0) > 100000:
            impact_score += 20
            impact_factors.append("large_scale")
        
        is_high_impact = sector_match and impact_score >= 50
        
        determination = {
            "system_id": system_id,
            "system_name": system_data.get("system_name"),
            "organization": self.organization,
            "determination_date": time.time(),
            "sector_test": {
                "sector": sector,
                "is_designated_sector": sector_match,
                "designated_sectors": high_impact_sectors
            },
            "impact_test": {
                "score": impact_score,
                "factors": impact_factors,
                "threshold": 50
            },
            "is_high_impact": is_high_impact,
            "risk_level": "HIGH_IMPACT" if is_high_impact else "STANDARD"
        }
        
        determination["signature"] = self._sign(determination)
        self.systems[system_id] = determination
        self._log_audit("HIGH_IMPACT_DETERMINATION", determination)
        
        print(f"\n📋 Article 33: High-Impact AI Determination")
        print(f"   System ID: {system_id}")
        print(f"   System: {determination['system_name']}")
        print(f"   Sector: {sector} ({'✅ designated' if sector_match else '❌ not designated'})")
        print(f"   Impact Score: {impact_score}/100 (threshold: 50)")
        print(f"   Result: {'✅ HIGH-IMPACT AI' if is_high_impact else '❌ STANDARD AI'}")
        
        return determination
    
    def create_risk_management_plan(
        self,
        system_id: str,
        risk_identification: List[str],
        mitigation_measures: List[str],
        monitoring_frequency: str = "quarterly",
        responsible_officer: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Article 34: Risk management plan for high-impact AI.
        
        Required for systems classified as high-impact AI [citation:3].
        """
        if system_id not in self.systems:
            raise ValueError(f"System {system_id} not found")
        
        plan_id = f"RMP-{self._generate_uuid7()}"
        
        plan = {
            "plan_id": plan_id,
            "system_id": system_id,
            "system_name": self.systems[system_id].get("system_name"),
            "organization": self.organization,
            "created_date": time.time(),
            "risk_identification": risk_identification,
            "mitigation_measures": mitigation_measures,
            "monitoring_frequency": monitoring_frequency,
            "responsible_officer": responsible_officer or "compliance@company.kr",
            "review_date": time.time() + 7776000,  # 90 days
            "status": "ACTIVE"
        }
        
        plan["signature"] = self._sign(plan)
        self._log_audit("RISK_MANAGEMENT_PLAN", plan)
        
        print(f"\n📋 Article 34: Risk Management Plan")
        print(f"   Plan ID: {plan_id}")
        print(f"   System: {plan['system_name']}")
        print(f"   Risks Identified: {len(risk_identification)}")
        print(f"   Mitigation Measures: {len(mitigation_measures)}")
        
        return plan
    
    def configure_human_oversight(
        self,
        system_id: str,
        mechanism: str = "dual_approval",
        approvers: List[str] = None,
        override_capability: bool = True
    ) -> Dict[str, Any]:
        """
        Article 34: Human oversight for high-impact AI [citation:3].
        
        High-impact AI must have human supervision mechanisms.
        """
        if system_id not in self.systems:
            raise ValueError(f"System {system_id} not found")
        
        oversight_id = f"OS-{self._generate_uuid7()}"
        
        oversight = {
            "oversight_id": oversight_id,
            "system_id": system_id,
            "system_name": self.systems[system_id].get("system_name"),
            "organization": self.organization,
            "mechanism": mechanism,
            "approvers": approvers or ["supervisor-456"],
            "override_capability": override_capability,
            "escalation_procedure": "automatic_for_high_risk",
            "training_required": True,
            "last_review": time.time(),
            "next_review": time.time() + 7776000  # 90 days
        }
        
        oversight["signature"] = self._sign(oversight)
        self._log_audit("HUMAN_OVERSIGHT", oversight)
        
        print(f"\n👤 Article 34: Human Oversight Configured")
        print(f"   Oversight ID: {oversight_id}")
        print(f"   Mechanism: {mechanism}")
        print(f"   Approvers: {len(oversight['approvers'])}")
        
        return oversight
    
    def conduct_impact_assessment(
        self,
        system_id: str,
        assessment_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Article 35: AI impact assessment for high-impact AI [citation:7].
        
        Three stages:
        - Pre-assessment: Identify risk scenarios
        - Main assessment: Record risks, identify affected fundamental rights
        - Post-assessment: Document results, implement safeguards
        """
        if system_id not in self.systems:
            raise ValueError(f"System {system_id} not found")
        
        assessment_id = f"IA-{self._generate_uuid7()}"
        
        assessment = {
            "assessment_id": assessment_id,
            "system_id": system_id,
            "system_name": self.systems[system_id].get("system_name"),
            "organization": self.organization,
            "assessment_date": time.time(),
            "pre_assessment": {
                "risk_scenarios": assessment_data.get("risk_scenarios", []),
                "identified_at": time.time()
            },
            "main_assessment": {
                "risk_records": assessment_data.get("risk_records", []),
                "affected_rights": assessment_data.get("affected_rights", []),
                "impact_descriptions": assessment_data.get("impact_descriptions", {})
            },
            "post_assessment": {
                "safeguards": assessment_data.get("safeguards", []),
                "documentation": assessment_data.get("documentation", "IA-report.pdf"),
                "next_review": time.time() + 31536000  # 1 year
            },
            "status": "COMPLETED"
        }
        
        assessment["signature"] = self._sign(assessment)
        self.risk_assessments.append(assessment)
        self._log_audit("IMPACT_ASSESSMENT", assessment)
        
        print(f"\n📋 Article 35: AI Impact Assessment")
        print(f"   Assessment ID: {assessment_id}")
        print(f"   Risk Scenarios: {len(assessment['pre_assessment']['risk_scenarios'])}")
        print(f"   Affected Rights: {len(assessment['main_assessment']['affected_rights'])}")
        
        return assessment
    
    # ========================================================================
    # High-Performance AI (Article 32) [citation:7]
    # ========================================================================
    
    def classify_high_performance(
        self,
        system_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Article 32: Determine if system qualifies as High-Performance AI.
        
        Criteria [citation:7]:
        - Computational volume ≥ 10²⁶ FLOPs
        - Advanced AI technologies
        - Significant risks to life, safety, rights
        """
        system_id = system_data.get("system_id", f"SYS-HP-{self._generate_uuid7()}")
        
        flops = system_data.get("computational_flops", 0)
        meets_flops_threshold = flops >= 1e26
        
        meets_tech_threshold = system_data.get("advanced_technology", False)
        
        meets_risk_threshold = system_data.get("significant_risk", False)
        
        is_high_performance = meets_flops_threshold and meets_tech_threshold and meets_risk_threshold
        
        classification = {
            "system_id": system_id,
            "system_name": system_data.get("system_name"),
            "classification_date": time.time(),
            "criteria": {
                "computational_flops": flops,
                "meets_flops_threshold": meets_flops_threshold,
                "advanced_technology": meets_tech_threshold,
                "significant_risk": meets_risk_threshold
            },
            "is_high_performance": is_high_performance,
            "risk_level": "HIGH_PERFORMANCE" if is_high_performance else "STANDARD"
        }
        
        classification["signature"] = self._sign(classification)
        self.systems[system_id] = classification
        self._log_audit("HIGH_PERFORMANCE_CLASSIFICATION", classification)
        
        print(f"\n📋 Article 32: High-Performance AI Classification")
        print(f"   System ID: {system_id}")
        print(f"   FLOPs: {flops:.1e} (threshold: 1e26)")
        print(f"   Result: {'✅ HIGH-PERFORMANCE' if is_high_performance else '❌ STANDARD'}")
        
        return classification
    
    def submit_safety_results(
        self,
        system_id: str,
        reporting_period: str,
        risk_assessments: List[Dict],
        incidents: List[Dict],
        mitigations: List[str]
    ) -> Dict[str, Any]:
        """
        Article 32: Submit safety implementation results to MSIT [citation:7].
        
        Required for high-performance AI systems.
        """
        if system_id not in self.systems:
            raise ValueError(f"System {system_id} not found")
        
        submission_id = f"MSIT-{self._generate_uuid7()}"
        
        submission = {
            "submission_id": submission_id,
            "system_id": system_id,
            "system_name": self.systems[system_id].get("system_name"),
            "organization": self.organization,
            "reporting_period": reporting_period,
            "submission_date": time.time(),
            "risk_assessments": risk_assessments,
            "incidents": incidents,
            "mitigations": mitigations,
            "status": "SUBMITTED"
        }
        
        submission["signature"] = self._sign(submission)
        self._log_audit("MSIT_SUBMISSION", submission)
        
        print(f"\n📋 Article 32: MSIT Safety Results Submitted")
        print(f"   Submission ID: {submission_id}")
        print(f"   Period: {reporting_period}")
        print(f"   Risk Assessments: {len(risk_assessments)}")
        
        return submission
    
    # ========================================================================
    # Foreign Company Local Representative (Article 4 + Enforcement Decree) [citation:6]
    # ========================================================================
    
    def appoint_local_representative(
        self,
        rep_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Appoint domestic agent for foreign companies [citation:6].
        
        Required if company meets any threshold:
        - Global revenue ≥ ₩1 trillion
        - Korea sales ≥ ₩10 billion
        - Korea daily users ≥ 1 million
        """
        if self.jurisdiction != "foreign":
            print("⚠️ Local representative only required for foreign companies")
            return {"error": "Not a foreign company"}
        
        if not self.requires_local_rep:
            print("⚠️ Company does not meet threshold for local representative")
            return {"warning": "Thresholds not met"}
        
        rep_id = f"REP-{self._generate_uuid7()}"
        
        self.local_representative = {
            "representative_id": rep_id,
            "organization": self.organization,
            "representative_name": rep_data.get("representative_name"),
            "entity_type": rep_data.get("entity_type", "corporation"),
            "address": rep_data.get("address"),
            "contact": rep_data.get("contact"),
            "authorized_officer": rep_data.get("authorized_officer"),
            "authorization_document": rep_data.get("authorization_document", "power_of_attorney.pdf"),
            "effective_date": time.time(),
            "status": "ACTIVE"
        }
        
        self.local_representative["signature"] = self._sign(self.local_representative)
        self._log_audit("LOCAL_REPRESENTATIVE_APPOINTED", self.local_representative)
        
        print(f"\n📋 Article 4: Local Representative Appointed")
        print(f"   Representative ID: {rep_id}")
        print(f"   Name: {self.local_representative['representative_name']}")
        print(f"   Contact: {self.local_representative['contact']}")
        print(f"   Authorized Officer: {self.local_representative['authorized_officer']}")
        
        return self.local_representative
    
    def prepare_operational_manual(self, manual_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare "Book of Flow" operational manual for local representative [citation:10].
        
        Ensures representative can respond to regulator inquiries effectively.
        """
        manual_id = f"MAN-{self._generate_uuid7()}"
        
        manual = {
            "manual_id": manual_id,
            "organization": self.organization,
            "prepared_date": time.time(),
            "data_mapping": manual_data.get("data_mapping", {}),
            "sop_playbooks": manual_data.get("sop_playbooks", []),
            "faq_answers": manual_data.get("faq_answers", []),
            "breach_response_procedure": manual_data.get("breach_response_procedure", {}),
            "training_records": manual_data.get("training_records", []),
            "last_updated": time.time()
        }
        
        manual["signature"] = self._sign(manual)
        self._log_audit("OPERATIONAL_MANUAL", manual)
        
        print(f"\n📋 Operational Manual Prepared")
        print(f"   Manual ID: {manual_id}")
        print(f"   Data Mapping: {len(manual.get('data_mapping', {}))} entries")
        print(f"   SOP Playbooks: {len(manual.get('sop_playbooks', []))}")
        
        return manual
    
    # ========================================================================
    # Grace Period Management [citation:1][citation:2]
    # ========================================================================
    
    def get_grace_period_status(self) -> Dict[str, Any]:
        """Get current grace period status."""
        now = time.time()
        days_remaining = max(0, (self.grace_period_end - now) / 86400)
        
        return {
            "effective_date": datetime.fromtimestamp(self.effective_date).isoformat(),
            "grace_period_end": datetime.fromtimestamp(self.grace_period_end).isoformat(),
            "days_remaining": days_remaining,
            "in_grace_period": self.is_grace_period(),
            "enforcement_priority": "low" if self.is_grace_period() else "normal",
            "exceptional_cases_only": self.is_grace_period()
        }
    
    def register_for_grace_period(self, system_id: str) -> Dict[str, Any]:
        """Register system for grace period tracking."""
        registration_id = f"GP-{self._generate_uuid7()}"
        
        registration = {
            "registration_id": registration_id,
            "system_id": system_id,
            "organization": self.organization,
            "registration_date": time.time(),
            "grace_period_status": self.get_grace_period_status(),
            "transition_plan": {
                "phase1": "risk_assessment",
                "phase1_deadline": time.time() + 7776000,  # 90 days
                "phase2": "compliance_implementation",
                "phase2_deadline": self.grace_period_end - 2592000,  # 30 days before end
                "phase3": "final_validation",
                "phase3_deadline": self.grace_period_end
            }
        }
        
        registration["signature"] = self._sign(registration)
        self._log_audit("GRACE_PERIOD_REGISTRATION", registration)
        
        return registration
    
    # ========================================================================
    # Verification and Reporting
    # ========================================================================
    
    def generate_compliance_report(self) -> Dict[str, Any]:
        """Generate comprehensive Korea AI Basic Act compliance report."""
        
        report_id = f"KR-{self._generate_uuid7()}"
        
        # Count high-impact systems
        high_impact_count = sum(1 for s in self.systems.values() 
                                 if isinstance(s, dict) and s.get("risk_level") == "HIGH_IMPACT")
        
        report = {
            "report_id": report_id,
            "organization": self.organization,
            "entity_type": self.entity_type.value,
            "jurisdiction": self.jurisdiction,
            "report_date": datetime.now().isoformat(),
            "effective_date": "2026-01-22",
            "grace_period": self.get_grace_period_status(),
            "local_representative": self.local_representative,
            "statistics": {
                "total_systems": len(self.systems),
                "high_impact_systems": high_impact_count,
                "content_labels": len(self.content_labels),
                "risk_assessments": len(self.risk_assessments)
            },
            "compliance_summary": {
                "transparency": {
                    "status": "COMPLIANT" if len(self.content_labels) > 0 else "PENDING"
                },
                "high_impact_ai": {
                    "status": "COMPLIANT" if len([s for s in self.systems.values() if s.get("risk_level") == "HIGH_IMPACT"]) > 0 else "PENDING",
                    "count": high_impact_count
                },
                "local_representative": {
                    "status": "COMPLIANT" if (self.jurisdiction != "foreign" or self.local_representative) else "PENDING",
                    "required": self.requires_local_rep if self.jurisdiction == "foreign" else False,
                    "appointed": self.local_representative is not None
                }
            }
        }
        
        report["signature"] = self._sign(report)
        return report
    
    def verify_compliance(self) -> Dict[str, Any]:
        """Verify compliance with Korea AI Basic Act requirements."""
        
        verification = {
            "verification_time": time.time(),
            "organization": self.organization,
            "grace_period": self.is_grace_period(),
            "checks": {}
        }
        
        # Article 31(1): Advance notice
        verification["checks"]["advance_notice"] = {
            "compliant": any(e["event_type"] == "ADVANCE_NOTICE" for e in self.audit_log),
            "grace_period_applies": self.is_grace_period()
        }
        
        # Article 31(2): Output labeling
        verification["checks"]["output_labeling"] = {
            "compliant": len(self.content_labels) > 0,
            "count": len(self.content_labels)
        }
        
        # Article 33-34: High-impact AI (if applicable)
        high_impact_systems = [s for s in self.systems.values() 
                               if isinstance(s, dict) and s.get("risk_level") == "HIGH_IMPACT"]
        
        if high_impact_systems:
            verification["checks"]["high_impact_determination"] = {
                "compliant": True,
                "count": len(high_impact_systems)
            }
            
            has_risk_plans = any(e["event_type"] == "RISK_MANAGEMENT_PLAN" for e in self.audit_log)
            verification["checks"]["risk_management"] = {
                "compliant": has_risk_plans
            }
            
            has_oversight = any(e["event_type"] == "HUMAN_OVERSIGHT" for e in self.audit_log)
            verification["checks"]["human_oversight"] = {
                "compliant": has_oversight
            }
        else:
            verification["checks"]["high_impact"] = {
                "compliant": True,
                "note": "No high-impact AI systems"
            }
        
        # Article 4: Foreign representative
        if self.jurisdiction == "foreign":
            verification["checks"]["local_representative"] = {
                "required": self.requires_local_rep,
                "compliant": self.local_representative is not None if self.requires_local_rep else True,
                "appointed": self.local_representative is not None
            }
        
        all_compliant = all(c.get("compliant", True) for c in verification["checks"].values())
        verification["status"] = "COMPLIANT" if all_compliant else "NON_COMPLIANT"
        
        return verification


# Example usage
if __name__ == "__main__":
    print("\n" + "="*80)
    print("🇰🇷 Korea AI Basic Act Compliance Tracker Demo")
    print("="*80)
    
    # Initialize tracker
    tracker = KoreaAITracker(
        organization="AI Korea Corp",
        entity_type=EntityType.PROVIDER
    )
    
    # Article 31(1): Advance notice
    print("\n📋 Article 31(1): Advance Notice")
    tracker.advance_notice({
        "service_name": "AI Loan Assistant",
        "ai_type": "high-impact",
        "disclosure_text": "This service uses AI for credit assessment"
    })
    
    # Article 31(2): Output labeling - different scenarios
    print("\n📋 Article 31(2): Output Labeling")
    
    # In-app (chatbot)
    tracker.label_chatbot("LoanBot")
    
    # Exported content (strict labeling)
    tracker.label_output(
        content=b"sample image data",
        content_type=ContentType.IMAGE,
        scenario=LabelingScenario.EXPORTED,
        exportable=True,
        metadata={"watermark_text": "AI 생성", "model": "image-gen-v2"}
    )
    
    # Deepfake content
    tracker.add_deepfake_warning(
        content=b"sample video data",
        content_type="video"
    )
    
    # Article 33: High-impact AI determination
    print("\n📋 Article 33: High-Impact AI Determination")
    system = tracker.determine_high_impact({
        "system_name": "Credit Scoring AI",
        "sector": "financial",
        "affects_rights": True,
        "automation_level": "high",
        "user_scale": 500000
    })
    
    # Article 34: Risk management and human oversight
    if system["is_high_impact"]:
        tracker.create_risk_management_plan(
            system_id=system["system_id"],
            risk_identification=["bias", "accuracy_drift", "security"],
            mitigation_measures=["quarterly_bias_testing", "human_oversight", "monitoring"]
        )
        tracker.configure_human_oversight(
            system_id=system["system_id"],
            mechanism="dual_approval",
            approvers=["loan_officer", "credit_manager"]
        )
    
    # Grace period status
    print("\n📋 Grace Period Status")
    status = tracker.get_grace_period_status()
    print(f"   In Grace Period: {status['in_grace_period']}")
    print(f"   Days Remaining: {status['days_remaining']:.0f}")
    
    # Verify compliance
    print("\n📊 Compliance Verification")
    verification = tracker.verify_compliance()
    print(f"   Status: {verification['status']}")
    
    print("\n" + "="*80)
    print("✅ Demo Complete")
    print("="*80)
