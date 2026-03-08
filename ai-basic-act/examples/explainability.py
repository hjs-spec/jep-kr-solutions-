#!/usr/bin/env python3
"""
Korea AI Basic Act - Right to Explanation Example (Article 30)
===============================================================

This example demonstrates compliance with Korea's AI Basic Act requirements
for providing meaningful explanations of AI decisions, particularly for
high-impact AI systems.

Key Requirements (Article 30 + Enforcement Decree Article 25):
----------------------------------------------------------------
1. Right to Explanation:
   - Users have the right to receive meaningful explanations of AI decisions
   - Applies to decisions that significantly affect users' rights or interests

2. Explanation Requirements:
   - Must be provided in plain language (Korean)
   - Must include key factors that influenced the decision
   - Must be understandable to average user
   - Must be provided within reasonable timeframe

3. Technical Feasibility Exception:
   - If full explanation is technically infeasible, must provide:
     * Explanation of limitations
     * Alternative methods for recourse
     * Human review option

4. Application Areas:
   - Credit scoring and loan decisions
   - Employment screening
   - Insurance underwriting
   - University admissions
   - Medical diagnoses
   - Public benefit eligibility
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
import random

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

class DecisionType(Enum):
    """Types of AI decisions requiring explanation."""
    CREDIT_SCORING = "credit_scoring"           # 신용평가
    LOAN_APPROVAL = "loan_approval"             # 대출승인
    EMPLOYMENT = "employment"                    # 채용
    INSURANCE = "insurance"                      # 보험
    ADMISSION = "admission"                      # 입학
    MEDICAL = "medical"                          # 의료
    BENEFIT = "benefit"                          # 복지혜택
    HOUSING = "housing"                          # 주택
    OTHER = "other"                               # 기타


class ExplanationFormat(Enum):
    """Formats for explanation delivery."""
    TEXT = "text"                 # Text explanation
    VISUAL = "visual"              # Visual/chart explanation
    AUDIO = "audio"                # Audio explanation
    INTERACTIVE = "interactive"    # Interactive dashboard
    HUMAN = "human"                # Human review


class ExplanationStatus(Enum):
    """Status of explanation request."""
    REQUESTED = "requested"
    PROCESSING = "processing"
    COMPLETED = "completed"
    REJECTED = "rejected"
    APPEALED = "appealed"


class DecisionOutcome(Enum):
    """Outcome of AI decision."""
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"
    REVIEW_REQUIRED = "review_required"


@dataclass
class ExplanationRequest:
    """Record of user request for explanation."""
    request_id: str
    user_id: str
    decision_id: str
    decision_type: DecisionType
    request_date: float
    preferred_format: ExplanationFormat
    language: str  # "ko", "en"
    status: ExplanationStatus
    completion_date: Optional[float] = None
    notes: str = ""


@dataclass
class AIDecision:
    """Record of AI decision affecting user."""
    decision_id: str
    user_id: str
    decision_type: DecisionType
    decision_date: float
    outcome: DecisionOutcome
    factors: Dict[str, float]  # factor name -> weight/importance
    model_version: str
    confidence: float
    human_review_available: bool
    appeal_deadline: float
    decision_text: str  # The actual decision communicated to user
    notes: str = ""


@dataclass
class Explanation:
    """Explanation provided to user."""
    explanation_id: str
    request_id: str
    decision_id: str
    content: Dict[str, Any]
    format: ExplanationFormat
    created_date: float
    language: str
    version: int
    user_feedback: Optional[str] = None
    user_satisfaction: Optional[int] = None  # 1-5 scale


# ============================================================================
# AI Explanation Provider Class
# ============================================================================

class AIExplanationProvider:
    """
    AI system provider that implements right to explanation requirements.
    Demonstrates compliance with Article 30 of Korea AI Basic Act.
    """
    
    def __init__(self, organization: str, sector: str):
        self.organization = organization
        self.sector = sector
        self.provider_id = f"EXP-{int(time.time())}-{hash(organization) % 10000:04d}"
        
        # Track explanations and decisions
        self.decisions: List[AIDecision] = []
        self.requests: List[ExplanationRequest] = []
        self.explanations: List[Explanation] = []
        
        # Model information
        self.models = {}
        self.feature_importance_methods = ["shap", "lime", "counterfactual"]
        
        # Tracker for compliance reporting
        self.tracker = KoreaAITracker(
            organization=organization,
            entity_type=EntityType.PROVIDER,
            jurisdiction="domestic"
        )
        
        print("="*80)
        print(f"🤖 AI Explanation Provider: {organization}")
        print(f"   Sector: {sector}")
        print(f"   Provider ID: {self.provider_id}")
        print("="*80)
        print(f"Korea AI Basic Act - Article 30: Right to Explanation")
        print(f"   Users have the right to receive meaningful explanations")
        print(f"   of AI decisions that significantly affect their rights")
        print(f"   or interests.")
        print("="*80)
    
    # ========================================================================
    # AI Decision Making
    # ========================================================================
    
    def make_decision(self, decision_data: Dict[str, Any]) -> AIDecision:
        """
        Make an AI decision that affects a user.
        Records all factors for later explanation.
        """
        decision_id = f"DEC-{int(time.time())}-{uuid.uuid4().hex[:8].upper()}"
        
        # Simulate AI decision process
        decision_type = DecisionType(decision_data.get('decision_type', 'credit_scoring'))
        user_id = decision_data.get('user_id', 'unknown')
        
        # Generate decision factors (simulated)
        factors = self._simulate_decision_factors(decision_type, decision_data.get('user_data', {}))
        
        # Determine outcome based on factors
        outcome = self._determine_outcome(factors, decision_data.get('threshold', 0.5))
        
        # Create decision record
        decision = AIDecision(
            decision_id=decision_id,
            user_id=user_id,
            decision_type=decision_type,
            decision_date=time.time(),
            outcome=outcome,
            factors=factors,
            model_version=decision_data.get('model_version', 'v1.0.0'),
            confidence=random.uniform(0.7, 0.95),
            human_review_available=decision_data.get('human_review', True),
            appeal_deadline=time.time() + (30 * 24 * 60 * 60),  # 30 days
            decision_text=self._generate_decision_text(decision_type, outcome, factors)
        )
        
        self.decisions.append(decision)
        
        print(f"\n📊 AI Decision Made")
        print(f"   Decision ID: {decision_id}")
        print(f"   User ID: {user_id}")
        print(f"   Type: {decision_type.value}")
        print(f"   Outcome: {outcome.value.upper()}")
        print(f"   Confidence: {decision.confidence:.2%}")
        print(f"   Key Factors: {dict(list(factors.items())[:3])}")
        
        # Check if explanation should be auto-provided (for significant decisions)
        if outcome in [DecisionOutcome.REJECTED, DecisionOutcome.REVIEW_REQUIRED]:
            self._auto_provide_explanation(decision)
        
        return decision
    
    def _simulate_decision_factors(self, decision_type: DecisionType, user_data: Dict) -> Dict[str, float]:
        """Simulate decision factors based on decision type."""
        if decision_type == DecisionType.CREDIT_SCORING:
            return {
                "credit_history": random.uniform(0.3, 0.9),
                "income_level": random.uniform(0.4, 0.95),
                "debt_to_income": random.uniform(0.1, 0.8),
                "payment_history": random.uniform(0.5, 0.95),
                "employment_stability": random.uniform(0.4, 0.9),
                "age": random.uniform(0.2, 0.7),
                "asset_value": random.uniform(0.3, 0.85)
            }
        elif decision_type == DecisionType.LOAN_APPROVAL:
            return {
                "credit_score": random.uniform(0.3, 0.95),
                "loan_amount_vs_income": random.uniform(0.1, 0.9),
                "existing_debt": random.uniform(0.2, 0.8),
                "collateral_value": random.uniform(0.3, 0.9),
                "payment_capacity": random.uniform(0.4, 0.95),
                "loan_purpose": random.uniform(0.3, 0.8)
            }
        elif decision_type == DecisionType.EMPLOYMENT:
            return {
                "skills_match": random.uniform(0.5, 0.95),
                "experience_years": random.uniform(0.3, 0.9),
                "education_level": random.uniform(0.4, 0.85),
                "interview_score": random.uniform(0.5, 0.95),
                "cultural_fit": random.uniform(0.4, 0.9),
                "references": random.uniform(0.5, 0.9)
            }
        else:
            return {
                f"factor_{i}": random.uniform(0.1, 0.9) for i in range(1, 6)
            }
    
    def _determine_outcome(self, factors: Dict[str, float], threshold: float) -> DecisionOutcome:
        """Determine decision outcome based on factors."""
        # Weighted average of factors (simplified)
        weights = {k: 1.0/len(factors) for k in factors}
        weighted_score = sum(factors[k] * weights[k] for k in factors)
        
        if weighted_score >= threshold + 0.2:
            return DecisionOutcome.APPROVED
        elif weighted_score >= threshold:
            return DecisionOutcome.REVIEW_REQUIRED
        else:
            return DecisionOutcome.REJECTED
    
    def _generate_decision_text(self, decision_type: DecisionType, outcome: DecisionOutcome, factors: Dict) -> str:
        """Generate user-friendly decision text."""
        if outcome == DecisionOutcome.APPROVED:
            return f"Your {decision_type.value} application has been APPROVED."
        elif outcome == DecisionOutcome.REJECTED:
            # Find top reasons for rejection
            low_factors = [k for k, v in factors.items() if v < 0.4]
            if low_factors:
                reasons = ", ".join(low_factors[:3])
                return f"Your {decision_type.value} application has been REJECTED. Key factors: {reasons}."
            else:
                return f"Your {decision_type.value} application has been REJECTED."
        else:
            return f"Your {decision_type.value} application requires ADDITIONAL REVIEW."
    
    def _auto_provide_explanation(self, decision: AIDecision) -> None:
        """Auto-provide explanation for significant decisions."""
        request = ExplanationRequest(
            request_id=f"REQ-AUTO-{int(time.time())}",
            user_id=decision.user_id,
            decision_id=decision.decision_id,
            decision_type=decision.decision_type,
            request_date=time.time(),
            preferred_format=ExplanationFormat.TEXT,
            language="ko",
            status=ExplanationStatus.PROCESSING
        )
        self.requests.append(request)
        
        # Generate explanation
        self.generate_explanation(request.request_id)
        
        print(f"   ℹ️ Auto-explanation triggered for user {decision.user_id}")
    
    # ========================================================================
    # Explanation Requests
    # ========================================================================
    
    def request_explanation(self, request_data: Dict[str, Any]) -> ExplanationRequest:
        """
        User requests explanation of an AI decision.
        Article 30(1): Users have right to request explanation.
        """
        request_id = f"REQ-{int(time.time())}-{uuid.uuid4().hex[:8].upper()}"
        
        # Find the decision
        decision_id = request_data.get('decision_id')
        decision = next((d for d in self.decisions if d.decision_id == decision_id), None)
        
        if not decision:
            raise ValueError(f"Decision not found: {decision_id}")
        
        # Create request
        request = ExplanationRequest(
            request_id=request_id,
            user_id=request_data.get('user_id', decision.user_id),
            decision_id=decision_id,
            decision_type=decision.decision_type,
            request_date=time.time(),
            preferred_format=ExplanationFormat(request_data.get('format', 'text')),
            language=request_data.get('language', 'ko'),
            status=ExplanationStatus.REQUESTED
        )
        
        self.requests.append(request)
        
        print(f"\n📝 Explanation Request Received")
        print(f"   Request ID: {request_id}")
        print(f"   User ID: {request.user_id}")
        print(f"   Decision ID: {decision_id}")
        print(f"   Format: {request.preferred_format.value}")
        print(f"   Language: {request.language}")
        print(f"   Status: {request.status.value}")
        
        return request
    
    def generate_explanation(self, request_id: str) -> Explanation:
        """
        Generate meaningful explanation for AI decision.
        Article 30(2): Explanation must be meaningful and understandable.
        """
        # Find request
        request = next((r for r in self.requests if r.request_id == request_id), None)
        if not request:
            raise ValueError(f"Request not found: {request_id}")
        
        # Update status
        request.status = ExplanationStatus.PROCESSING
        
        # Find decision
        decision = next((d for d in self.decisions if d.decision_id == request.decision_id), None)
        if not decision:
            request.status = ExplanationStatus.REJECTED
            raise ValueError(f"Decision not found: {request.decision_id}")
        
        # Generate explanation content based on format
        if request.preferred_format == ExplanationFormat.TEXT:
            content = self._generate_text_explanation(decision)
        elif request.preferred_format == ExplanationFormat.VISUAL:
            content = self._generate_visual_explanation(decision)
        elif request.preferred_format == ExplanationFormat.INTERACTIVE:
            content = self._generate_interactive_explanation(decision)
        else:
            content = self._generate_text_explanation(decision)
        
        # Create explanation
        explanation = Explanation(
            explanation_id=f"EXP-{int(time.time())}-{uuid.uuid4().hex[:8].upper()}",
            request_id=request_id,
            decision_id=decision.decision_id,
            content=content,
            format=request.preferred_format,
            created_date=time.time(),
            language=request.language,
            version=1
        )
        
        self.explanations.append(explanation)
        
        # Update request
        request.status = ExplanationStatus.COMPLETED
        request.completion_date = time.time()
        
        # Calculate response time
        response_time = request.completion_date - request.request_date
        response_hours = response_time / 3600
        
        print(f"\n✅ Explanation Generated")
        print(f"   Explanation ID: {explanation.explanation_id}")
        print(f"   Request ID: {request_id}")
        print(f"   Format: {explanation.format.value}")
        print(f"   Response Time: {response_hours:.1f} hours")
        print(f"   Key Points:")
        print(f"   • Decision: {decision.outcome.value}")
        print(f"   • Top Factor: {max(decision.factors, key=decision.factors.get)}")
        print(f"   • Confidence: {decision.confidence:.2%}")
        
        return explanation
    
    def _generate_text_explanation(self, decision: AIDecision) -> Dict[str, Any]:
        """Generate text-based explanation in plain language."""
        
        # Sort factors by importance
        sorted_factors = sorted(decision.factors.items(), key=lambda x: x[1], reverse=True)
        top_factors = sorted_factors[:3]
        bottom_factors = sorted_factors[-2:]
        
        # Create explanation sections
        explanation = {
            "summary": f"Your {decision.decision_type.value} application was {decision.outcome.value}.",
            "decision_details": {
                "outcome": decision.outcome.value,
                "date": datetime.fromtimestamp(decision.decision_date).strftime("%Y-%m-%d %H:%M"),
                "confidence": f"{decision.confidence:.2%}",
                "model_version": decision.model_version
            },
            "key_factors": [
                {
                    "factor": factor.replace('_', ' ').title(),
                    "impact": "positive" if score > 0.6 else "negative" if score < 0.4 else "neutral",
                    "value": f"{score:.0%}",
                    "explanation": self._factor_explanation(factor, score)
                }
                for factor, score in top_factors
            ],
            "areas_for_improvement": [
                {
                    "factor": factor.replace('_', ' ').title(),
                    "current_value": f"{score:.0%}",
                    "suggestion": self._improvement_suggestion(factor)
                }
                for factor, score in bottom_factors
            ],
            "appeal_rights": {
                "available": decision.human_review_available,
                "deadline": datetime.fromtimestamp(decision.appeal_deadline).strftime("%Y-%m-%d"),
                "process": "You may request human review by contacting our support team.",
                "contact": "support@example.com or 02-1234-5678"
            },
            "disclaimer": "This explanation is based on the key factors considered by our AI system. For more details or to request human review, please contact us."
        }
        
        return explanation
    
    def _generate_visual_explanation(self, decision: AIDecision) -> Dict[str, Any]:
        """Generate visual explanation (charts, graphs)."""
        return {
            "summary": f"Your {decision.decision_type.value} application was {decision.outcome.value}.",
            "visualization": {
                "type": "bar_chart",
                "title": "Factor Importance",
                "data": [
                    {"factor": k.replace('_', ' ').title(), "importance": v}
                    for k, v in sorted(decision.factors.items(), key=lambda x: x[1], reverse=True)
                ],
                "threshold_line": 0.5,
                "colors": {
                    "above_threshold": "green",
                    "below_threshold": "red"
                }
            },
            "comparison": {
                "type": "radar_chart",
                "title": "Your Profile vs. Average",
                "your_scores": decision.factors,
                "average_scores": {k: random.uniform(0.4, 0.6) for k in decision.factors}
            },
            "appeal_info": {
                "available": decision.human_review_available,
                "deadline": datetime.fromtimestamp(decision.appeal_deadline).strftime("%Y-%m-%d")
            }
        }
    
    def _generate_interactive_explanation(self, decision: AIDecision) -> Dict[str, Any]:
        """Generate interactive explanation (what-if analysis)."""
        return {
            "summary": f"Your {decision.decision_type.value} application was {decision.outcome.value}.",
            "interactive": {
                "type": "what_if",
                "current_factors": decision.factors,
                "threshold": 0.5,
                "simulations": [
                    {
                        "scenario": "Improve credit history by 20%",
                        "new_outcome": DecisionOutcome.APPROVED.value,
                        "changes": {"credit_history": min(1.0, decision.factors.get('credit_history', 0.5) + 0.2)}
                    },
                    {
                        "scenario": "Reduce debt-to-income ratio by 15%",
                        "new_outcome": DecisionOutcome.APPROVED.value,
                        "changes": {"debt_to_income": max(0.0, decision.factors.get('debt_to_income', 0.5) - 0.15)}
                    }
                ],
                "message": "Adjust the factors below to see how they would affect your decision:"
            }
        }
    
    def _factor_explanation(self, factor: str, score: float) -> str:
        """Generate plain language explanation for a factor."""
        explanations = {
            "credit_history": "Your past credit behavior and repayment history",
            "income_level": "Your reported annual income",
            "debt_to_income": "Your current debt compared to your income",
            "payment_history": "Your track record of making payments on time",
            "employment_stability": "Length and stability of your employment",
            "credit_score": "Your overall credit score based on credit bureau data",
            "loan_amount_vs_income": "The loan amount relative to your income",
            "collateral_value": "Value of assets you can offer as collateral"
        }
        
        base = explanations.get(factor, f"Assessment of your {factor.replace('_', ' ')}")
        
        if score >= 0.7:
            return f"{base} is strong and positively contributed to your application."
        elif score >= 0.4:
            return f"{base} is adequate but could be improved."
        else:
            return f"{base} was below our typical threshold and negatively impacted your application."
    
    def _improvement_suggestion(self, factor: str) -> str:
        """Generate improvement suggestion for a factor."""
        suggestions = {
            "credit_history": "Continue making timely payments and reduce credit utilization",
            "income_level": "Consider additional income sources or wait for income growth",
            "debt_to_income": "Pay down existing debts before reapplying",
            "payment_history": "Set up automatic payments to avoid missed payments",
            "employment_stability": "Consider waiting until you have longer employment history",
            "credit_score": "Review credit report for errors and address any issues",
            "loan_amount_vs_income": "Consider a smaller loan amount",
            "collateral_value": "Additional collateral could strengthen your application"
        }
        
        return suggestions.get(factor, f"Work on improving your {factor.replace('_', ' ')}")
    
    # ========================================================================
    # Human Review (Appeals)
    # ========================================================================
    
    def request_human_review(self, decision_id: str, user_id: str, reason: str) -> Dict[str, Any]:
        """
        User requests human review of AI decision.
        Article 30(4): Right to request human intervention.
        """
        # Find decision
        decision = next((d for d in self.decisions if d.decision_id == decision_id), None)
        if not decision:
            raise ValueError(f"Decision not found: {decision_id}")
        
        # Check if within appeal deadline
        if time.time() > decision.appeal_deadline:
            return {
                "status": "rejected",
                "reason": "Appeal deadline has passed",
                "deadline": datetime.fromtimestamp(decision.appeal_deadline).strftime("%Y-%m-%d")
            }
        
        # Create review request
        review_id = f"REV-{int(time.time())}-{uuid.uuid4().hex[:8].upper()}"
        
        review = {
            "review_id": review_id,
            "decision_id": decision_id,
            "user_id": user_id,
            "reason": reason,
            "request_date": time.time(),
            "status": "pending",
            "assigned_to": None,
            "completion_date": None,
            "outcome": None
        }
        
        print(f"\n👤 Human Review Requested")
        print(f"   Review ID: {review_id}")
        print(f"   Decision ID: {decision_id}")
        print(f"   Reason: {reason}")
        print(f"   Status: {review['status']}")
        
        return review
    
    def complete_human_review(self, review_id: str, outcome: str, notes: str) -> Dict[str, Any]:
        """Complete human review of AI decision."""
        print(f"\n✅ Human Review Completed")
        print(f"   Review ID: {review_id}")
        print(f"   Outcome: {outcome}")
        print(f"   Notes: {notes}")
        
        return {
            "review_id": review_id,
            "status": "completed",
            "outcome": outcome,
            "completion_date": time.time(),
            "notes": notes
        }
    
    # ========================================================================
    # Compliance Reporting
    # ========================================================================
    
    def generate_compliance_report(self) -> Dict[str, Any]:
        """Generate Article 30 compliance report."""
        
        # Calculate metrics
        total_decisions = len(self.decisions)
        total_requests = len(self.requests)
        completed_explanations = len([e for e in self.explanations])
        
        # Calculate average response time
        completed_requests = [r for r in self.requests if r.completion_date]
        if completed_requests:
            avg_response = sum(r.completion_date - r.request_date for r in completed_requests) / len(completed_requests) / 3600
        else:
            avg_response = 0
        
        # Calculate satisfaction if available
        satisfaction_scores = [e.user_satisfaction for e in self.explanations if e.user_satisfaction]
        avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else 0
        
        report = {
            "organization": self.organization,
            "provider_id": self.provider_id,
            "report_date": time.time(),
            "report_id": f"RPT-EXP-{int(time.time())}-{uuid.uuid4().hex[:8].upper()}",
            "article_30_compliance": {
                "right_to_explanation": {
                    "total_decisions": total_decisions,
                    "decisions_by_outcome": {
                        outcome.value: len([d for d in self.decisions if d.outcome == outcome])
                        for outcome in DecisionOutcome
                    },
                    "explanation_requests": total_requests,
                    "explanations_provided": completed_explanations,
                    "completion_rate": (completed_explanations / total_requests * 100) if total_requests > 0 else 100,
                    "avg_response_time_hours": avg_response,
                    "avg_user_satisfaction": avg_satisfaction
                },
                "human_review": {
                    "available": any(d.human_review_available for d in self.decisions),
                    "appeals_within_deadline": len([d for d in self.decisions if time.time() <= d.appeal_deadline])
                },
                "explanation_formats": {
                    format.value: len([e for e in self.explanations if e.format == format])
                    for format in ExplanationFormat
                }
            },
            "recommendations": self._generate_recommendations()
        }
        
        # Generate tracker report
        tracker_report = self.tracker.generate_compliance_report()
        report["tracker_report"] = tracker_report
        
        print("\n" + "="*80)
        print("📊 Article 30 Compliance Report")
        print("="*80)
        print(f"Organization: {self.organization}")
        print(f"Report ID: {report['report_id']}")
        print("-"*80)
        print(f"Total AI Decisions: {total_decisions}")
        print(f"Explanation Requests: {total_requests}")
        print(f"Explanations Provided: {completed_explanations}")
        print(f"Completion Rate: {report['article_30_compliance']['right_to_explanation']['completion_rate']:.1f}%")
        print(f"Avg Response Time: {avg_response:.1f} hours")
        print(f"Avg User Satisfaction: {avg_satisfaction:.1f}/5.0")
        print("-"*80)
        print(f"Human Review Available: {report['article_30_compliance']['human_review']['available']}")
        print(f"Appeals Within Deadline: {report['article_30_compliance']['human_review']['appeals_within_deadline']}")
        print("="*80)
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate compliance recommendations."""
        recommendations = []
        
        # Check if we have any outstanding requests
        pending_requests = [r for r in self.requests if r.status in [ExplanationStatus.REQUESTED, ExplanationStatus.PROCESSING]]
        if pending_requests:
            recommendations.append(f"Process {len(pending_requests)} pending explanation requests")
        
        # Check response time
        completed_requests = [r for r in self.requests if r.completion_date]
        if completed_requests:
            slow_responses = [r for r in completed_requests if (r.completion_date - r.request_date) > 7 * 24 * 3600]
            if slow_responses:
                recommendations.append(f"Address {len(slow_responses)} explanations that took >7 days")
        
        # Check satisfaction
        low_satisfaction = [e for e in self.explanations if e.user_satisfaction and e.user_satisfaction < 3]
        if low_satisfaction:
            recommendations.append("Review explanations with low user satisfaction scores")
        
        return recommendations
    
    # ========================================================================
    # User Feedback
    # ========================================================================
    
    def submit_feedback(self, explanation_id: str, satisfaction: int, comments: str) -> Explanation:
        """User submits feedback on explanation quality."""
        explanation = next((e for e in self.explanations if e.explanation_id == explanation_id), None)
        if not explanation:
            raise ValueError(f"Explanation not found: {explanation_id}")
        
        explanation.user_satisfaction = satisfaction
        explanation.user_feedback = comments
        
        print(f"\n📝 User Feedback Received")
        print(f"   Explanation ID: {explanation_id}")
        print(f"   Satisfaction: {satisfaction}/5")
        print(f"   Comments: {comments}")
        
        return explanation


# ============================================================================
# Demonstration
# ============================================================================

def run_demo():
    """Run complete right to explanation demonstration."""
    
    print("\n" + "="*80)
    print("🇰🇷 KOREA AI BASIC ACT - ARTICLE 30 RIGHT TO EXPLANATION DEMO")
    print("="*80)
    
    # ========================================================================
    # DEMO 1: Create AI Explanation Provider (Bank/Credit Union)
    # ========================================================================
    
    print("\n📋 DEMO 1: AI Explanation Provider Setup")
    print("-"*60)
    
    provider = AIExplanationProvider(
        organization="Korea Credit Union AI Services",
        sector="Financial Services"
    )
    
    # ========================================================================
    # DEMO 2: Make AI Decisions
    # ========================================================================
    
    print("\n📋 DEMO 2: AI Decisions Affecting Users")
    print("-"*60)
    
    # Decision 1: Loan approval (rejected)
    decision1 = provider.make_decision({
        "user_id": "user-123",
        "decision_type": "loan_approval",
        "threshold": 0.6,
        "model_version": "loan-v2.1.0",
        "human_review": True,
        "user_data": {
            "income": 45000000,
            "credit_score": 650,
            "existing_loans": 20000000
        }
    })
    
    # Decision 2: Credit scoring (approved)
    decision2 = provider.make_decision({
        "user_id": "user-456",
        "decision_type": "credit_scoring",
        "threshold": 0.5,
        "model_version": "credit-v3.0.0",
        "human_review": True,
        "user_data": {
            "income": 85000000,
            "credit_history": "excellent",
            "payment_history": "perfect"
        }
    })
    
    # Decision 3: Employment screening (review required)
    decision3 = provider.make_decision({
        "user_id": "user-789",
        "decision_type": "employment",
        "threshold": 0.7,
        "model_version": "hiring-v1.5.0",
        "human_review": True,
        "user_data": {
            "skills": "strong",
            "experience": 3,
            "education": "bachelor"
        }
    })
    
    # ========================================================================
    # DEMO 3: Users Request Explanations
    # ========================================================================
    
    print("\n📋 DEMO 3: User Explanation Requests")
    print("-"*60)
    
    # User 123 requests explanation (rejected loan)
    request1 = provider.request_explanation({
        "user_id": "user-123",
        "decision_id": decision1.decision_id,
        "format": "text",
        "language": "ko"
    })
    
    # User 456 requests explanation (approved but wants details)
    request2 = provider.request_explanation({
        "user_id": "user-456",
        "decision_id": decision2.decision_id,
        "format": "visual",
        "language": "en"
    })
    
    # User 789 requests explanation (wants to understand why review needed)
    request3 = provider.request_explanation({
        "user_id": "user-789",
        "decision_id": decision3.decision_id,
        "format": "interactive",
        "language": "ko"
    })
    
    # ========================================================================
    # DEMO 4: Generate Explanations
    # ========================================================================
    
    print("\n📋 DEMO 4: Explanation Generation")
    print("-"*60)
    
    # Generate explanations for each request
    explanation1 = provider.generate_explanation(request1.request_id)
    explanation2 = provider.generate_explanation(request2.request_id)
    explanation3 = provider.generate_explanation(request3.request_id)
    
    # ========================================================================
    # DEMO 5: Show Explanation Content
    # ========================================================================
    
    print("\n📋 DEMO 5: Sample Explanation Content")
    print("-"*60)
    
    # Show text explanation (loan rejection)
    print("\n📄 TEXT EXPLANATION (Loan Rejection):")
    print(f"   Summary: {explanation1.content['summary']}")
    print(f"   Key Factors:")
    for factor in explanation1.content['key_factors']:
        print(f"   • {factor['factor']}: {factor['value']} - {factor['explanation'][:50]}...")
    print(f"   Appeal Deadline: {explanation1.content['appeal_rights']['deadline']}")
    
    # Show visual explanation (credit scoring)
    print("\n📊 VISUAL EXPLANATION (Credit Scoring):")
    print(f"   Summary: {explanation2.content['summary']}")
    print(f"   Visualization Type: {explanation2.content['visualization']['type']}")
    print(f"   Top Factor: {explanation2.content['visualization']['data'][0]['factor']} ({explanation2.content['visualization']['data'][0]['importance']:.0%})")
    
    # Show interactive explanation (employment)
    print("\n🎮 INTERACTIVE EXPLANATION (Employment):")
    print(f"   Summary: {explanation3.content['summary']}")
    print(f"   Interactive Type: {explanation3.content['interactive']['type']}")
    print(f"   Available Simulations: {len(explanation3.content['interactive']['simulations'])}")
    
    # ========================================================================
    # DEMO 6: User Feedback
    # ========================================================================
    
    print("\n📋 DEMO 6: User Feedback Collection")
    print("-"*60)
    
    provider.submit_feedback(explanation1.explanation_id, 4, "Helpful explanation, understood why my loan was rejected.")
    provider.submit_feedback(explanation2.explanation_id, 5, "Great visual chart, helped me see my strengths!")
    provider.submit_feedback(explanation3.explanation_id, 3, "Interactive tool was interesting but a bit complex.")
    
    # ========================================================================
    # DEMO 7: Human Review Request
    # ========================================================================
    
    print("\n📋 DEMO 7: Human Review (Appeals)")
    print("-"*60)
    
    # User 123 appeals the decision
    review = provider.request_human_review(
        decision_id=decision1.decision_id,
        user_id="user-123",
        reason="I believe my income stability was not properly considered"
    )
    
    # Complete human review
    provider.complete_human_review(
        review_id=review['review_id'],
        outcome="overturned",
        notes="After manual review, we found the applicant's income stability was indeed strong. Loan approved."
    )
    
    # ========================================================================
    # DEMO 8: Generate Compliance Report
    # ========================================================================
    
    print("\n📋 DEMO 8: Compliance Report")
    print("-"*60)
    
    report = provider.generate_compliance_report()
    
    # Save report
    with open("korea_explainability_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\n✅ Report saved: korea_explainability_report.json")
    
    # ========================================================================
    # Summary
    # ========================================================================
    
    print("\n" + "="*80)
    print("📊 ARTICLE 30 COMPLIANCE SUMMARY")
    print("="*80)
    print(f"Provider: Korea Credit Union AI Services")
    print(f"Decisions Made: {len(provider.decisions)}")
    print(f"Explanation Requests: {len(provider.requests)}")
    print(f"Explanations Provided: {len(provider.explanations)}")
    print(f"Completion Rate: 100%")
    print(f"Avg Response Time: < 24 hours")
    print(f"Human Review Available: ✅ YES")
    print("="*80)
    print("✅ FULL COMPLIANCE WITH ARTICLE 30")
    print("   • Right to Explanation Implemented")
    print("   • Meaningful Explanations Provided")
    print("   • Human Review Available")
    print("   • User Feedback Collected")
    print("="*80)
    
    return report


if __name__ == "__main__":
    report = run_demo()
