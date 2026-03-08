#!/usr/bin/env python3
"""
Korea AI Basic Act - Foreign Company Local Representative Example (Article 27)
===============================================================================

This example demonstrates compliance with Korea's AI Basic Act requirements
for foreign AI providers to appoint a local representative in Korea.

Key Requirements (Article 27 + Public Notice 2025-1):
----------------------------------------------------------------
1. Thresholds (meet ANY):
   - Global annual revenue ≥ ₩1 trillion (~$681M USD)
   - Korea-specific sales ≥ ₩10 billion (~$6.8M USD)
   - Korea daily active users ≥ 1 million

2. Representative Responsibilities:
   - Receive communications from Korean authorities
   - Respond to user complaints and inquiries
   - Maintain compliance documentation
   - Cooperate with investigations

3. Appointment Requirements:
   - Physical address in Korea
   - Designated authorized officer
   - 24/7 contact availability
   - Powers of attorney documentation

4. Penalties for Non-Compliance:
   - Fines up to ₩30 million
   - Service suspension in Korea
   - Public naming and shaming
"""

import json
import time
import sys
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from dataclasses import dataclass, field
import uuid

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from ai_basic_act.implementation.kr_tracker import (
    KoreaAITracker,
    EntityType,
    ContentType,
    LabelingScenario
)


# ============================================================================
# Enums and Data Classes
# ============================================================================

class RepresentativeStatus(Enum):
    """Status of local representative appointment."""
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    UNDER_REVIEW = "under_review"


class AuthorityType(Enum):
    """Korean regulatory authorities."""
    MSIT = "Ministry of Science and ICT"
    KCC = "Korea Communications Commission"
    PIPC = "Personal Information Protection Commission"
    KISA = "Korea Internet & Security Agency"
    KOSA = "Korea AI & Software Industry Association"
    FAIR_TRADE = "Korea Fair Trade Commission"


class CommunicationPriority(Enum):
    """Priority levels for regulatory communications."""
    LOW = "low"          # General inquiries
    MEDIUM = "medium"    # User complaints
    HIGH = "high"        # Investigation notices
    URGENT = "urgent"    # Immediate action required


class CommunicationType(Enum):
    """Types of communications from Korean authorities."""
    INQUIRY = "inquiry"                       # General questions
    COMPLAINT = "complaint"                    # User complaints
    INVESTIGATION = "investigation"            # Official investigation
    DOCUMENT_REQUEST = "document_request"      # Request for documents
    INSPECTION = "inspection"                  # On-site inspection notice
    PENALTY = "penalty"                         # Fine or sanction notice
    GUIDANCE = "guidance"                       # Regulatory guidance
    INFORMATION = "information"                  # General information


@dataclass
class CommunicationRecord:
    """Record of communication with Korean authorities."""
    comm_id: str
    authority: AuthorityType
    type: CommunicationType
    priority: CommunicationPriority
    subject: str
    content: str
    received_date: float
    response_date: Optional[float] = None
    response_content: Optional[str] = None
    attachments: List[str] = field(default_factory=list)
    requires_action: bool = True
    closed: bool = False
    closed_date: Optional[float] = None
    notes: str = ""


@dataclass
class UserComplaint:
    """Record of user complaints about AI services."""
    complaint_id: str
    user_id: str
    service_name: str
    complaint_type: str  # "accuracy", "bias", "privacy", "transparency", etc.
    description: str
    received_date: float
    status: str  # "pending", "investigating", "resolved", "appealed"
    resolution: Optional[str] = None
    resolution_date: Optional[float] = None
    escalated_to_authority: bool = False
    escalation_date: Optional[float] = None
    notes: str = ""


@dataclass
class ComplianceDocument:
    """Compliance documentation maintained by local representative."""
    doc_id: str
    doc_type: str  # "risk_assessment", "impact_assessment", "incident_report", etc.
    title: str
    content: Dict[str, Any]
    created_date: float
    last_updated: float
    version: int
    language: str  # "ko", "en"
    submitted_to_authority: bool = False
    submission_date: Optional[float] = None
    authority_response: Optional[str] = None


@dataclass
class LocalRepresentative:
    """Local representative appointed by foreign AI provider."""
    rep_id: str
    name: str
    company_name: str  # Korean entity name
    business_registration: str
    address: str
    authorized_officer: str
    officer_title: str
    officer_contact: str
    officer_email: str
    appointment_date: float
    expiry_date: Optional[float] = None
    status: RepresentativeStatus = RepresentativeStatus.PENDING
    power_of_attorney_doc: Optional[str] = None
    languages: List[str] = field(default_factory=lambda: ["ko", "en"])
    notes: str = ""


# ============================================================================
# Foreign AI Provider Class
# ============================================================================

class ForeignAIProvider:
    """
    Foreign AI company operating in Korea, demonstrating compliance with
    Article 27 local representative requirements.
    
    This class simulates the obligations of major global AI providers
    like OpenAI, Google, Meta, etc. when operating in the Korean market.
    """
    
    def __init__(self, company_name: str, headquarters: str):
        self.company_name = company_name
        self.headquarters = headquarters
        self.company_id = f"FOREIGN-{int(time.time())}-{hash(company_name) % 10000:04d}"
        
        # Korea operations status
        self.korea_operations = {
            "registered": False,
            "business_registration": None,
            "representative": None,
            "commencement_date": None,
            "last_compliance_check": None
        }
        
        # Track compliance metrics (Article 27 thresholds)
        self.korea_users = 0
        self.korea_revenue = 0.0  # in KRW
        self.global_revenue = 0.0  # in KRW
        self.daily_active_users = 0
        self.monthly_active_users = 0
        
        # Compliance components
        self.representative: Optional[LocalRepresentative] = None
        self.communications: List[CommunicationRecord] = []
        self.complaints: List[UserComplaint] = []
        self.documents: List[ComplianceDocument] = []
        
        # AI services offered in Korea
        self.korea_services = []
        
        # Tracker for compliance reporting
        self.tracker = KoreaAITracker(
            organization=company_name,
            entity_type=EntityType.PROVIDER,
            jurisdiction="foreign"
        )
        
        print("="*80)
        print(f"🌏 Foreign AI Provider: {company_name}")
        print(f"   Headquarters: {headquarters}")
        print(f"   Company ID: {self.company_id}")
        print("="*80)
        print(f"Korea AI Basic Act - Article 27: Local Representative")
        print(f"   Thresholds (must meet ANY):")
        print(f"   • Global Revenue ≥ ₩1T (≈ $681M USD)")
        print(f"   • Korea Revenue ≥ ₩10B (≈ $6.8M USD)")
        print(f"   • Korea DAU ≥ 1M users")
        print("="*80)
    
    # ========================================================================
    # Article 27 Threshold Assessment
    # ========================================================================
    
    def check_thresholds(self) -> Dict[str, Any]:
        """
        Check if company meets any threshold requiring local representative.
        Article 27: Foreign providers meeting ANY threshold must appoint.
        """
        meets_global_revenue = self.global_revenue >= 1_000_000_000_000  # ₩1T
        meets_korea_revenue = self.korea_revenue >= 10_000_000_000  # ₩10B
        meets_dau = self.daily_active_users >= 1_000_000  # 1M DAU
        
        meets_any = meets_global_revenue or meets_korea_revenue or meets_dau
        
        result = {
            "company": self.company_name,
            "assessment_date": time.time(),
            "metrics": {
                "global_revenue_krw": self.global_revenue,
                "global_revenue_usd": self.global_revenue * 0.00068,  # Approx
                "meets_global_threshold": meets_global_revenue,
                "korea_revenue_krw": self.korea_revenue,
                "korea_revenue_usd": self.korea_revenue * 0.00068,
                "meets_korea_threshold": meets_korea_revenue,
                "daily_active_users": self.daily_active_users,
                "meets_dau_threshold": meets_dau,
                "monthly_active_users": self.monthly_active_users
            },
            "requires_representative": meets_any,
            "notification_sent": False
        }
        
        # Send notification if required
        if meets_any and not self.representative:
            self._send_threshold_notification(result)
            result["notification_sent"] = True
        
        print(f"\n📊 Article 27 Threshold Assessment")
        print(f"   Global Revenue: ₩{self.global_revenue:,.0f} ({'✅ Meets' if meets_global_revenue else '❌ Below'} ₩1T)")
        print(f"   Korea Revenue: ₩{self.korea_revenue:,.0f} ({'✅ Meets' if meets_korea_revenue else '❌ Below'} ₩10B)")
        print(f"   Korea DAU: {self.daily_active_users:,} ({'✅ Meets' if meets_dau else '❌ Below'} 1M)")
        print(f"   Requires Representative: {'✅ YES' if meets_any else '❌ NO'}")
        
        return result
    
    def _send_threshold_notification(self, assessment: Dict[str, Any]) -> None:
        """Send internal notification that representative is required."""
        notification = {
            "notification_id": f"NOTIFY-{int(time.time())}",
            "sent_to": ["legal@company.com", "compliance@company.com"],
            "subject": "URGENT: Korea AI Act Local Representative Required",
            "message": f"""
            {self.company_name} meets the threshold for requiring a local representative in Korea.
            
            Thresholds Met:
            - Global Revenue: {'✅' if assessment['metrics']['meets_global_threshold'] else '❌'} ₩{self.global_revenue:,.0f}
            - Korea Revenue: {'✅' if assessment['metrics']['meets_korea_threshold'] else '❌'} ₩{self.korea_revenue:,.0f}
            - Korea DAU: {'✅' if assessment['metrics']['meets_dau_threshold'] else '❌'} {self.daily_active_users:,}
            
            Action Required: Appoint local representative within 30 days.
            """,
            "sent_date": time.time()
        }
        print(f"   📧 Notification sent to compliance team")
    
    # ========================================================================
    # Local Representative Appointment
    # ========================================================================
    
    def appoint_local_representative(self, rep_data: Dict[str, Any]) -> LocalRepresentative:
        """
        Appoint a local representative in Korea.
        Article 27(2): Must designate a domestic representative.
        Public Notice 2025-1: Detailed requirements for appointment.
        """
        # Check if already appointed
        if self.representative and self.representative.status == RepresentativeStatus.ACTIVE:
            print(f"   ⚠️ Representative already active: {self.representative.name}")
            return self.representative
        
        # Generate representative ID
        rep_id = f"REP-{int(time.time())}-{uuid.uuid4().hex[:8].upper()}"
        
        # Create power of attorney document
        poa_doc = self._create_power_of_attorney(rep_data)
        
        # Create representative record
        representative = LocalRepresentative(
            rep_id=rep_id,
            name=rep_data.get('name', 'Korea AI Compliance Office'),
            company_name=rep_data.get('company_name', f"{self.company_name} Korea LLC"),
            business_registration=rep_data.get('business_registration', f"110-{int(time.time())%100000:05d}-{int(time.time())%10000:04d}"),
            address=rep_data.get('address', '20F, Seoul Finance Center, 136 Sejong-daero, Jung-gu, Seoul'),
            authorized_officer=rep_data.get('authorized_officer', 'Kim Min-su'),
            officer_title=rep_data.get('officer_title', 'Compliance Director'),
            officer_contact=rep_data.get('officer_contact', '+82-2-1234-5678'),
            officer_email=rep_data.get('officer_email', 'compliance@company.kr'),
            appointment_date=time.time(),
            expiry_date=time.time() + (365 * 24 * 60 * 60),  # 1 year
            status=RepresentativeStatus.ACTIVE,
            power_of_attorney_doc=poa_doc['doc_id'],
            languages=rep_data.get('languages', ['ko', 'en'])
        )
        
        self.representative = representative
        self.korea_operations['representative'] = representative.rep_id
        self.korea_operations['registered'] = True
        self.korea_operations['commencement_date'] = time.time()
        
        # Add compliance document
        self.documents.append(ComplianceDocument(
            doc_id=poa_doc['doc_id'],
            doc_type='power_of_attorney',
            title=f"Power of Attorney - {representative.name}",
            content=poa_doc,
            created_date=time.time(),
            last_updated=time.time(),
            version=1,
            language='ko'
        ))
        
        print(f"\n📋 Local Representative Appointed - Article 27 Compliance")
        print(f"   Representative ID: {representative.rep_id}")
        print(f"   Name: {representative.name}")
        print(f"   Company: {representative.company_name}")
        print(f"   Business Registration: {representative.business_registration}")
        print(f"   Address: {representative.address}")
        print(f"   Authorized Officer: {representative.authorized_officer} ({representative.officer_title})")
        print(f"   Contact: {representative.officer_contact} / {representative.officer_email}")
        print(f"   Appointment Date: {datetime.fromtimestamp(representative.appointment_date).strftime('%Y-%m-%d')}")
        print(f"   Power of Attorney: {poa_doc['doc_id']}")
        
        # Register with MSIT (simulated)
        self._register_with_msit()
        
        return representative
    
    def _create_power_of_attorney(self, rep_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create power of attorney document for local representative."""
        doc_id = f"POA-{int(time.time())}-{uuid.uuid4().hex[:8].upper()}"
        
        poa = {
            "doc_id": doc_id,
            "type": "power_of_attorney",
            "principal": self.company_name,
            "principal_headquarters": self.headquarters,
            "representative": rep_data.get('name', 'Korea AI Compliance Office'),
            "authorized_officer": rep_data.get('authorized_officer', 'Kim Min-su'),
            "effective_date": time.time(),
            "expiry_date": time.time() + (365 * 24 * 60 * 60),
            "authority": [
                "Receive official communications from Korean authorities",
                "Respond to user complaints and inquiries",
                "Maintain compliance documentation",
                "Cooperate with investigations",
                "Accept service of process",
                "Represent company in regulatory proceedings"
            ],
            "limitations": [
                "Cannot modify AI systems without headquarters approval",
                "Must consult HQ for penalties exceeding ₩10M",
                "Quarterly reporting required"
            ],
            "language": "ko",
            "notarized": True,
            "notarization_date": time.time(),
            "notary": "Seoul Notary Public"
        }
        
        return poa
    
    def _register_with_msit(self) -> Dict[str, Any]:
        """Simulate registration with Ministry of Science and ICT."""
        registration = {
            "registration_id": f"MSIT-{int(time.time())}-{uuid.uuid4().hex[:6].upper()}",
            "company": self.company_name,
            "representative": self.representative.name if self.representative else None,
            "registration_date": time.time(),
            "status": "registered",
            "acknowledgment": "MSIT acknowledges receipt of local representative appointment"
        }
        
        print(f"   ✅ Registered with MSIT: {registration['registration_id']}")
        
        return registration
    
    # ========================================================================
    # Representative Responsibilities
    # ========================================================================
    
    def receive_communication(self, comm_data: Dict[str, Any]) -> CommunicationRecord:
        """
        Receive and log communication from Korean authorities.
        Article 27(3): Representative must receive all official communications.
        """
        comm_id = f"COMM-{int(time.time())}-{uuid.uuid4().hex[:8].upper()}"
        
        # Parse authority
        authority_map = {
            'msit': AuthorityType.MSIT,
            'kcc': AuthorityType.KCC,
            'pipc': AuthorityType.PIPC,
            'kisa': AuthorityType.KISA,
            'kosa': AuthorityType.KOSA,
            'ftc': AuthorityType.FAIR_TRADE
        }
        authority = authority_map.get(comm_data.get('authority', '').lower(), AuthorityType.MSIT)
        
        # Parse type
        type_map = {
            'inquiry': CommunicationType.INQUIRY,
            'complaint': CommunicationType.COMPLAINT,
            'investigation': CommunicationType.INVESTIGATION,
            'document_request': CommunicationType.DOCUMENT_REQUEST,
            'inspection': CommunicationType.INSPECTION,
            'penalty': CommunicationType.PENALTY,
            'guidance': CommunicationType.GUIDANCE,
            'information': CommunicationType.INFORMATION
        }
        comm_type = type_map.get(comm_data.get('type', '').lower(), CommunicationType.INQUIRY)
        
        # Determine priority
        priority = CommunicationPriority.MEDIUM
        if comm_type in [CommunicationType.INVESTIGATION, CommunicationType.INSPECTION, CommunicationType.PENALTY]:
            priority = CommunicationPriority.HIGH
        elif comm_type == CommunicationType.COMPLAINT:
            priority = CommunicationPriority.MEDIUM
        else:
            priority = CommunicationPriority.LOW
        
        # Create record
        communication = CommunicationRecord(
            comm_id=comm_id,
            authority=authority,
            type=comm_type,
            priority=priority,
            subject=comm_data.get('subject', 'No Subject'),
            content=comm_data.get('content', ''),
            received_date=time.time(),
            attachments=comm_data.get('attachments', []),
            requires_action=comm_type not in [CommunicationType.INFORMATION, CommunicationType.GUIDANCE]
        )
        
        self.communications.append(communication)
        
        print(f"\n📨 Communication Received from {authority.value}")
        print(f"   Comm ID: {comm_id}")
        print(f"   Type: {comm_type.value}")
        print(f"   Priority: {priority.value}")
        print(f"   Subject: {communication.subject}")
        print(f"   Requires Action: {communication.requires_action}")
        
        # Auto-respond for low priority if possible
        if priority == CommunicationPriority.LOW and not communication.requires_action:
            self.respond_to_communication(comm_id, {
                'response': f"Thank you for your communication. This has been logged and acknowledged."
            })
        
        return communication
    
    def respond_to_communication(self, comm_id: str, response_data: Dict[str, Any]) -> CommunicationRecord:
        """
        Respond to communication from Korean authorities.
        Article 27(4): Representative must respond in timely manner.
        """
        # Find communication
        communication = next((c for c in self.communications if c.comm_id == comm_id), None)
        if not communication:
            raise ValueError(f"Communication not found: {comm_id}")
        
        # Record response
        communication.response_date = time.time()
        communication.response_content = response_data.get('response', '')
        communication.closed = True
        communication.closed_date = time.time()
        
        # Calculate response time
        response_time = communication.response_date - communication.received_date
        response_hours = response_time / 3600
        
        print(f"\n📤 Response Sent to {communication.authority.value}")
        print(f"   Comm ID: {comm_id}")
        print(f"   Response Time: {response_hours:.1f} hours")
        print(f"   Response: {communication.response_content[:100]}..." if len(communication.response_content) > 100 else f"   Response: {communication.response_content}")
        
        # Check if response was timely
        if communication.priority == CommunicationPriority.URGENT and response_hours > 24:
            print(f"   ⚠️ WARNING: Response took >24 hours for URGENT communication")
        elif communication.priority == CommunicationPriority.HIGH and response_hours > 72:
            print(f"   ⚠️ WARNING: Response took >72 hours for HIGH priority communication")
        elif response_hours > 168:  # 7 days
            print(f"   ⚠️ WARNING: Response took >7 days")
        
        return communication
    
    def receive_user_complaint(self, complaint_data: Dict[str, Any]) -> UserComplaint:
        """
        Receive and process user complaint.
        Article 27(5): Representative must handle user complaints.
        """
        complaint_id = f"CMP-{int(time.time())}-{uuid.uuid4().hex[:8].upper()}"
        
        complaint = UserComplaint(
            complaint_id=complaint_id,
            user_id=complaint_data.get('user_id', 'anonymous'),
            service_name=complaint_data.get('service_name', 'Unknown Service'),
            complaint_type=complaint_data.get('complaint_type', 'other'),
            description=complaint_data.get('description', ''),
            received_date=time.time(),
            status='pending'
        )
        
        self.complaints.append(complaint)
        
        print(f"\n👤 User Complaint Received")
        print(f"   Complaint ID: {complaint_id}")
        print(f"   Service: {complaint.service_name}")
        print(f"   Type: {complaint.complaint_type}")
        print(f"   Description: {complaint.description[:100]}..." if len(complaint.description) > 100 else f"   Description: {complaint.description}")
        print(f"   Status: {complaint.status}")
        
        # Auto-acknowledge
        self._acknowledge_complaint(complaint_id)
        
        return complaint
    
    def _acknowledge_complaint(self, complaint_id: str) -> None:
        """Acknowledge receipt of complaint to user."""
        complaint = next((c for c in self.complaints if c.complaint_id == complaint_id), None)
        if complaint:
            print(f"   ✅ Acknowledgment sent to user {complaint.user_id}")
    
    def resolve_complaint(self, complaint_id: str, resolution: str) -> UserComplaint:
        """Resolve user complaint."""
        complaint = next((c for c in self.complaints if c.complaint_id == complaint_id), None)
        if not complaint:
            raise ValueError(f"Complaint not found: {complaint_id}")
        
        complaint.status = 'resolved'
        complaint.resolution = resolution
        complaint.resolution_date = time.time()
        
        resolution_time = complaint.resolution_date - complaint.received_date
        resolution_days = resolution_time / (24 * 3600)
        
        print(f"\n✅ Complaint Resolved")
        print(f"   Complaint ID: {complaint_id}")
        print(f"   Resolution Time: {resolution_days:.1f} days")
        print(f"   Resolution: {resolution}")
        
        return complaint
    
    # ========================================================================
    # Compliance Documentation
    # ========================================================================
    
    def create_compliance_document(self, doc_data: Dict[str, Any]) -> ComplianceDocument:
        """
        Create compliance documentation maintained by local representative.
        Article 27(6): Representative must maintain records.
        """
        doc_id = f"DOC-{int(time.time())}-{uuid.uuid4().hex[:8].upper()}"
        
        document = ComplianceDocument(
            doc_id=doc_id,
            doc_type=doc_data.get('doc_type', 'general'),
            title=doc_data.get('title', 'Untitled Document'),
            content=doc_data.get('content', {}),
            created_date=time.time(),
            last_updated=time.time(),
            version=1,
            language=doc_data.get('language', 'ko')
        )
        
        self.documents.append(document)
        
        print(f"\n📄 Compliance Document Created")
        print(f"   Document ID: {doc_id}")
        print(f"   Type: {document.doc_type}")
        print(f"   Title: {document.title}")
        print(f"   Language: {document.language}")
        
        return document
    
    def submit_document_to_authority(self, doc_id: str, authority: AuthorityType) -> ComplianceDocument:
        """Submit compliance document to Korean authority."""
        document = next((d for d in self.documents if d.doc_id == doc_id), None)
        if not document:
            raise ValueError(f"Document not found: {doc_id}")
        
        document.submitted_to_authority = True
        document.submission_date = time.time()
        
        # Simulate authority response
        document.authority_response = f"Received by {authority.value} on {datetime.fromtimestamp(document.submission_date).strftime('%Y-%m-%d')}"
        
        print(f"\n📤 Document Submitted to {authority.value}")
        print(f"   Document ID: {doc_id}")
        print(f"   Title: {document.title}")
        print(f"   Submission Date: {datetime.fromtimestamp(document.submission_date).strftime('%Y-%m-%d')}")
        
        return document
    
    # ========================================================================
    # Compliance Reporting
    # ========================================================================
    
    def generate_compliance_report(self) -> Dict[str, Any]:
        """Generate comprehensive compliance report for regulators."""
        report = {
            "company": self.company_name,
            "company_id": self.company_id,
            "headquarters": self.headquarters,
            "report_date": time.time(),
            "report_id": f"RPT-{int(time.time())}-{uuid.uuid4().hex[:8].upper()}",
            "article_27_compliance": {
                "thresholds_met": self.check_thresholds(),
                "representative_appointed": self.representative is not None,
                "representative": {
                    "name": self.representative.name if self.representative else None,
                    "status": self.representative.status.value if self.representative else None,
                    "appointment_date": self.representative.appointment_date if self.representative else None
                } if self.representative else None
            },
            "communications": {
                "total": len(self.communications),
                "pending_response": len([c for c in self.communications if not c.closed]),
                "by_priority": {
                    "urgent": len([c for c in self.communications if c.priority == CommunicationPriority.URGENT]),
                    "high": len([c for c in self.communications if c.priority == CommunicationPriority.HIGH]),
                    "medium": len([c for c in self.communications if c.priority == CommunicationPriority.MEDIUM]),
                    "low": len([c for c in self.communications if c.priority == CommunicationPriority.LOW])
                },
                "avg_response_time_hours": self._calculate_avg_response_time()
            },
            "complaints": {
                "total": len(self.complaints),
                "pending": len([c for c in self.complaints if c.status == 'pending']),
                "investigating": len([c for c in self.complaints if c.status == 'investigating']),
                "resolved": len([c for c in self.complaints if c.status == 'resolved']),
                "avg_resolution_days": self._calculate_avg_resolution_time()
            },
            "documents": {
                "total": len(self.documents),
                "submitted": len([d for d in self.documents if d.submitted_to_authority]),
                "by_type": self._count_documents_by_type()
            }
        }
        
        # Generate tracker report
        tracker_report = self.tracker.generate_compliance_report()
        report["tracker_report"] = tracker_report
        
        print("\n" + "="*80)
        print("📊 Article 27 Compliance Report")
        print("="*80)
        print(f"Company: {self.company_name}")
        print(f"Representative: {self.representative.name if self.representative else 'NOT APPOINTED'}")
        print(f"Status: {'✅ COMPLIANT' if self.representative else '❌ NON-COMPLIANT'}")
        print("-"*80)
        print(f"Communications Received: {report['communications']['total']}")
        print(f"   - Pending Response: {report['communications']['pending_response']}")
        print(f"   - Avg Response Time: {report['communications']['avg_response_time_hours']:.1f} hours")
        print(f"Complaints Received: {report['complaints']['total']}")
        print(f"   - Resolved: {report['complaints']['resolved']}")
        print(f"   - Avg Resolution: {report['complaints']['avg_resolution_days']:.1f} days")
        print(f"Documents Maintained: {report['documents']['total']}")
        print(f"   - Submitted to Authorities: {report['documents']['submitted']}")
        print("="*80)
        
        return report
    
    def _calculate_avg_response_time(self) -> float:
        """Calculate average response time to communications."""
        responded = [c for c in self.communications if c.response_date]
        if not responded:
            return 0.0
        total_time = sum(c.response_date - c.received_date for c in responded)
        return total_time / len(responded) / 3600  # hours
    
    def _calculate_avg_resolution_time(self) -> float:
        """Calculate average resolution time for complaints."""
        resolved = [c for c in self.complaints if c.resolution_date]
        if not resolved:
            return 0.0
        total_time = sum(c.resolution_date - c.received_date for c in resolved)
        return total_time / len(resolved) / (24 * 3600)  # days
    
    def _count_documents_by_type(self) -> Dict[str, int]:
        """Count documents by type."""
        counts = {}
        for doc in self.documents:
            counts[doc.doc_type] = counts.get(doc.doc_type, 0) + 1
        return counts
    
    # ========================================================================
    # Business Operations in Korea
    # ========================================================================
    
    def launch_service_in_korea(self, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """Launch AI service in Korean market."""
        service_id = f"SVC-KR-{int(time.time())}-{uuid.uuid4().hex[:8].upper()}"
        
        service = {
            "service_id": service_id,
            "name": service_data.get('name', 'AI Service'),
            "type": service_data.get('type', 'chatbot'),
            "launch_date": time.time(),
            "users": 0,
            "revenue": 0.0,
            "status": "active"
        }
        
        self.korea_services.append(service)
        
        print(f"\n🚀 Service Launched in Korea")
        print(f"   Service ID: {service_id}")
        print(f"   Name: {service['name']}")
        print(f"   Type: {service['type']}")
        
        # Check if this triggers representative requirement
        self.check_thresholds()
        
        return service
    
    def update_korea_metrics(self, users: int = None, revenue: float = None, dau: int = None, mau: int = None):
        """Update Korea market metrics."""
        if users is not None:
            self.korea_users = users
        if revenue is not None:
            self.korea_revenue = revenue
        if dau is not None:
            self.daily_active_users = dau
        if mau is not None:
            self.monthly_active_users = mau
        
        print(f"\n📈 Korea Metrics Updated")
        print(f"   Total Users: {self.korea_users:,}")
        print(f"   Revenue: ₩{self.korea_revenue:,.0f}")
        print(f"   DAU: {self.daily_active_users:,}")
        print(f"   MAU: {self.monthly_active_users:,}")
        
        # Re-check thresholds
        self.check_thresholds()


# ============================================================================
# Demonstration
# ============================================================================

def run_demo():
    """Run complete local representative demonstration."""
    
    print("\n" + "="*80)
    print("🇰🇷 KOREA AI BASIC ACT - ARTICLE 27 LOCAL REPRESENTATIVE DEMO")
    print("="*80)
    
    # ========================================================================
    # DEMO 1: Create foreign AI provider (simulating OpenAI)
    # ========================================================================
    
    print("\n📋 DEMO 1: Foreign AI Provider Setup")
    print("-"*60)
    
    openai_korea = ForeignAIProvider(
        company_name="OpenAI Global, Inc.",
        headquarters="San Francisco, USA"
    )
    
    # Initial metrics (below thresholds)
    openai_korea.global_revenue = 500_000_000_000  # ₩500B (below ₩1T)
    openai_korea.korea_revenue = 5_000_000_000     # ₩5B (below ₩10B)
    openai_korea.daily_active_users = 500_000       # 500K (below 1M)
    
    # Check thresholds - should NOT require representative yet
    assessment = openai_korea.check_thresholds()
    
    # ========================================================================
    # DEMO 2: Launch services and grow to meet thresholds
    # ========================================================================
    
    print("\n📋 DEMO 2: Service Launch and Growth")
    print("-"*60)
    
    # Launch ChatGPT in Korea
    openai_korea.launch_service_in_korea({
        "name": "ChatGPT Korea",
        "type": "conversational AI"
    })
    
    # Update metrics - now meeting thresholds
    openai_korea.update_korea_metrics(
        users=2_500_000,
        revenue=15_000_000_000,  # ₩15B (above ₩10B)
        dau=1_200_000,            # 1.2M (above 1M)
        mau=3_500_000
    )
    
    # ========================================================================
    # DEMO 3: Appoint Local Representative
    # ========================================================================
    
    print("\n📋 DEMO 3: Local Representative Appointment")
    print("-"*60)
    
    representative = openai_korea.appoint_local_representative({
        "name": "OpenAI Korea Compliance Office",
        "company_name": "OpenAI Korea LLC",
        "business_registration": "110-2026-12345",
        "address": "20F, Seoul Finance Center, 136 Sejong-daero, Jung-gu, Seoul, 04520 South Korea",
        "authorized_officer": "Park Ji-sung",
        "officer_title": "Korea Compliance Director",
        "officer_contact": "+82-2-5555-1234",
        "officer_email": "jisung.park@openai.kr",
        "languages": ["ko", "en"]
    })
    
    # ========================================================================
    # DEMO 4: Receive Communications from Authorities
    # ========================================================================
    
    print("\n📋 DEMO 4: Regulatory Communications")
    print("-"*60)
    
    # Receive inquiry from MSIT
    comm1 = openai_korea.receive_communication({
        "authority": "msit",
        "type": "inquiry",
        "subject": "Request for Information: AI Safety Measures",
        "content": "Please provide documentation on safety measures implemented in ChatGPT Korea within 30 days.",
        "attachments": ["MSIT-2026-001.pdf"]
    })
    
    # Receive user complaint (escalated to authority)
    comm2 = openai_korea.receive_communication({
        "authority": "kcc",
        "type": "complaint",
        "subject": "User Complaint: AI-generated misinformation",
        "content": "User claims ChatGPT provided false medical information. Please investigate and respond within 14 days.",
        "attachments": ["complaint-2026-001.pdf"]
    })
    
    # Respond to communications
    openai_korea.respond_to_communication(comm1.comm_id, {
        "response": "We have prepared the requested documentation on AI safety measures. Please find attached our comprehensive safety report including: 1) Model card, 2) Red teaming results, 3) Mitigation strategies, 4) Ongoing monitoring protocols."
    })
    
    openai_korea.respond_to_communication(comm2.comm_id, {
        "response": "We have investigated the user complaint regarding medical misinformation. Our investigation found that the model did provide incomplete information. We have: 1) Updated our safety filters for medical queries, 2) Added disclaimer for health-related responses, 3) Reached out to the user directly with corrective information and apology."
    })
    
    # ========================================================================
    # DEMO 5: Handle User Complaints
    # ========================================================================
    
    print("\n📋 DEMO 5: User Complaint Handling")
    print("-"*60)
    
    # Receive user complaint directly
    complaint1 = openai_korea.receive_user_complaint({
        "user_id": "user123",
        "service_name": "ChatGPT Korea",
        "complaint_type": "bias",
        "description": "ChatGPT gave biased response about Korean history, favoring one political perspective."
    })
    
    # Investigate and resolve
    openai_korea.resolve_complaint(complaint1.complaint_id, 
        "After investigation, we found the model's training data had imbalanced historical sources. We have: 1) Updated training data with more diverse Korean historical sources, 2) Implemented additional debiasing techniques, 3) Provided user with corrected historical information and apology.")
    
    # ========================================================================
    # DEMO 6: Maintain Compliance Documents
    # ========================================================================
    
    print("\n📋 DEMO 6: Compliance Documentation")
    print("-"*60)
    
    # Create risk assessment document
    doc1 = openai_korea.create_compliance_document({
        "doc_type": "risk_assessment",
        "title": "ChatGPT Korea Risk Assessment 2026",
        "language": "ko",
        "content": {
            "assessment_date": time.time(),
            "risks_identified": ["misinformation", "bias", "privacy", "security"],
            "mitigation_measures": ["content filtering", "debiasing", "data minimization", "encryption"],
            "residual_risk": "low",
            "human_oversight": "24/7 monitoring team"
        }
    })
    
    # Create incident report
    doc2 = openai_korea.create_compliance_document({
        "doc_type": "incident_report",
        "title": "Q1 2026 Incident Report",
        "language": "en",
        "content": {
            "incidents": [
                {"date": "2026-01-15", "type": "misinformation", "severity": "medium", "resolved": True},
                {"date": "2026-02-03", "type": "outage", "severity": "low", "resolved": True},
                {"date": "2026-03-22", "type": "bias_complaint", "severity": "medium", "resolved": True}
            ],
            "total_incidents": 3,
            "avg_response_time": "4.2 hours",
            "improvements_implemented": ["enhanced monitoring", "faster response protocols"]
        }
    })
    
    # Submit documents to authorities
    openai_korea.submit_document_to_authority(doc1.doc_id, AuthorityType.MSIT)
    openai_korea.submit_document_to_authority(doc2.doc_id, AuthorityType.KCC)
    
    # ========================================================================
    # DEMO 7: Generate Compliance Report
    # ========================================================================
    
    print("\n📋 DEMO 7: Final Compliance Report")
    print("-"*60)
    
    report = openai_korea.generate_compliance_report()
    
    # Save report
    with open("korea_foreign_provider_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\n✅ Report saved: korea_foreign_provider_report.json")
    
    # ========================================================================
    # Summary
    # ========================================================================
    
    print("\n" + "="*80)
    print("📊 ARTICLE 27 COMPLIANCE SUMMARY")
    print("="*80)
    print(f"Company: OpenAI Global, Inc.")
    print(f"Headquarters: San Francisco, USA")
    print(f"Local Representative: ✅ APPOINTED")
    print(f"   - Name: OpenAI Korea Compliance Office")
    print(f"   - Authorized Officer: Park Ji-sung")
    print(f"   - Address: 20F, Seoul Finance Center")
    print(f"   - Contact: +82-2-5555-1234")
    print(f"   - Status: ACTIVE")
    print(f"Communications Handled: {len(openai_korea.communications)}")
    print(f"Complaints Resolved: {len([c for c in openai_korea.complaints if c.status == 'resolved'])}")
    print(f"Documents Maintained: {len(openai_korea.documents)}")
    print(f"Documents Submitted: {len([d for d in openai_korea.documents if d.submitted_to_authority])}")
    print("="*80)
    print("✅ FULL COMPLIANCE WITH ARTICLE 27")
    print("="*80)
    
    return report


if __name__ == "__main__":
    report = run_demo()
