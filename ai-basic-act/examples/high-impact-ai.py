#!/usr/bin/env python3
"""
Korea AI Basic Act - High-Impact AI Example (Articles 33-35)
================================================================

This example demonstrates a complete high-impact AI system (loan approval for a Korean bank)
that complies with Korea's AI Basic Act, covering:

- Two-step high-impact determination (Article 33)
- Risk management plan (Article 34)
- Human oversight mechanisms (Article 34)
- AI impact assessment (Article 35)
- Explainability obligations (Article 34.2)
- Grace period management (≥1 year transition)
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from ai_basic_act.implementation.kr_tracker import (
    KoreaAITracker,
    EntityType,
    RiskLevel,
    ContentType,
    LabelingScenario
)


class KoreanLoanApprovalSystem:
    """
    Complete loan approval system for a Korean bank,
    demonstrating compliance with Korea AI Basic Act for high-impact AI.
    
    Under Article 33, financial services (loan decisions) are designated
    as high-impact sectors, requiring full compliance with Articles 33-35.
    """
    
    def __init__(self, bank_name: str):
        self.bank_name = bank_name
        self.tracker = KoreaAITracker(
            organization=bank_name,
            entity_type=EntityType.DEPLOYER,
            jurisdiction="domestic"
        )
        
        self.customers = {}
        self.loan_applications = []
        self.risk_plans = []
        self.assessments = []
        self.oversight_logs = []
        
        print("="*80)
        print(f"🏦 High-Impact Loan Approval System - {bank_name}")
        print("="*80)
        print(f"Korea AI Basic Act Effective: January 22, 2026")
        print(f"Grace Period: At least 1 year (until early 2027)")
        print(f"Sector: Financial (고영향 AI - High-Impact)")
        print(f"Requirements: Articles 33-35 (Risk Management, Human Oversight, Impact Assessment)")
    
    def register_system(self):
        """
        Step 1: Two-step high-impact determination (Article 33)
        """
        print("\n📋 Article 33: Two-Step High-Impact Determination")
        
        # Step 1: Sector test + Step 2: Impact test
        determination = self.tracker.determine_high_impact({
            "system_name": "AI Loan Approval System",
            "sector": "financial",  # Designated high-impact sector
            "affects_rights": True,  # Loan decisions affect fundamental rights
            "automation_level": "high",  # Fully automated initial screening
            "user_scale": 500000  # Serves 500,000+ customers
        })
        
        self.system_id = determination["system_id"]
        
        if determination["is_high_impact"]:
            print(f"\n✅ System classified as HIGH-IMPACT AI")
            print(f"   Impact Score: {determination['impact_test']['score']}/100")
            print(f"   Factors: {', '.join(determination['impact_test']['factors'])}")
        else:
            print(f"\n❌ System NOT classified as high-impact")
        
        return determination
    
    def create_risk_management_plan(self):
        """
        Step 2: Risk Management Plan (Article 34.1)
        """
        print("\n📋 Article 34.1: Risk Management Plan")
        
        # Identify risks and mitigation measures
        risk_plan = self.tracker.create_risk_management_plan(
            system_id=self.system_id,
            risk_identification=[
                "Algorithmic bias against certain demographics",
                "Model drift over time reducing accuracy",
                "Data privacy breaches in customer information",
                "Over-reliance on automated decisions without human review",
                "Adversarial attacks manipulating loan decisions"
            ],
            mitigation_measures=[
                "Quarterly bias testing across all protected groups",
                "Continuous monitoring for model drift (daily accuracy checks)",
                "Encryption of all customer data (AES-256)",
                "Human oversight for all high-risk decisions (>₩100M)",
                "Adversarial testing before deployment and quarterly"
            ],
            monitoring_frequency="daily",
            responsible_officer="chief-risk-officer@bank.kr"
        )
        
        self.risk_plans.append(risk_plan)
        
        print(f"   Risk Plan ID: {risk_plan['plan_id']}")
        print(f"   Risks Identified: {len(risk_plan['risk_identification'])}")
        print(f"   Mitigation Measures: {len(risk_plan['mitigation_measures'])}")
        print(f"   Monitoring: {risk_plan['monitoring_frequency']}")
        
        return risk_plan
    
    def configure_human_oversight(self):
        """
        Step 3: Human Oversight Mechanisms (Article 34.4)
        """
        print("\n📋 Article 34.4: Human Oversight Configuration")
        
        oversight = self.tracker.configure_human_oversight(
            system_id=self.system_id,
            mechanism="tiered_approval",
            approvers=[
                "loan_officer",      # First level (loans < ₩50M)
                "branch_manager",    # Second level (loans ₩50M-₩100M)
                "credit_committee"   # Third level (loans > ₩100M)
            ],
            override_capability=True
        )
        
        self.oversight_config = oversight
        
        print(f"   Oversight ID: {oversight['oversight_id']}")
        print(f"   Mechanism: {oversight['mechanism']}")
        print(f"   Approvers: {', '.join(oversight['approvers'])}")
        print(f"   Override Capability: {oversight['override_capability']}")
        
        return oversight
    
    def conduct_impact_assessment(self):
        """
        Step 4: AI Impact Assessment (Article 35)
        
        Three-stage assessment:
        - Pre-assessment: Identify risk scenarios
        - Main assessment: Record risks, identify affected rights
        - Post-assessment: Document results, implement safeguards
        """
        print("\n📋 Article 35: AI Impact Assessment")
        
        assessment = self.tracker.conduct_impact_assessment(
            system_id=self.system_id,
            assessment_data={
                "risk_scenarios": [
                    {
                        "scenario": "Bias against elderly applicants",
                        "probability": "LOW",
                        "impact": "HIGH",
                        "affected_rights": ["equal_treatment", "non-discrimination"]
                    },
                    {
                        "scenario": "Bias against foreign residents",
                        "probability": "MEDIUM",
                        "impact": "HIGH",
                        "affected_rights": ["equal_treatment", "non-discrimination"]
                    },
                    {
                        "scenario": "Data breach during processing",
                        "probability": "LOW",
                        "impact": "CRITICAL",
                        "affected_rights": ["privacy", "data_protection"]
                    }
                ],
                "affected_rights": [
                    "equal_treatment",
                    "non-discrimination",
                    "privacy",
                    "access_to_credit"
                ],
                "impact_descriptions": {
                    "equal_treatment": "AI system must not discriminate based on age, gender, or nationality",
                    "non-discrimination": "Decisions must be based solely on creditworthiness factors",
                    "privacy": "Customer data must be protected throughout processing",
                    "access_to_credit": "System must not systematically exclude vulnerable groups"
                },
                "safeguards": [
                    "Bias testing dashboard",
                    "Automated fairness metrics",
                    "Human review workflow",
                    "Data encryption at rest and in transit",
                    "Audit trail for all decisions"
                ]
            }
        )
        
        self.assessments.append(assessment)
        
        print(f"   Assessment ID: {assessment['assessment_id']}")
        print(f"   Risk Scenarios: {len(assessment['pre_assessment']['risk_scenarios'])}")
        print(f"   Affected Rights: {len(assessment['main_assessment']['affected_rights'])}")
        print(f"   Safeguards Implemented: {len(assessment['post_assessment']['safeguards'])}")
        
        return assessment
    
    def add_customer(self, customer_data: dict) -> str:
        """Add a customer to the system."""
        customer_id = f"CUST-{int(time.time())}-{hash(customer_data['name']) % 1000:03d}"
        
        self.customers[customer_id] = {
            "customer_id": customer_id,
            "name": customer_data['name'],
            "age": customer_data['age'],
            "gender": customer_data.get('gender'),
            "nationality": customer_data.get('nationality', '한국'),
            "income": customer_data['income'],
            "employment_years": customer_data['employment_years'],
            "credit_score": customer_data['credit_score'],
            "existing_loans": customer_data.get('existing_loans', 0),
            "monthly_debt": customer_data.get('monthly_debt', 0),
            "assets": customer_data.get('assets', 0),
            "created_date": time.time()
        }
        
        print(f"\n👤 Customer Added: {customer_data['name']} (ID: {customer_id})")
        print(f"   Age: {customer_data['age']}, Credit Score: {customer_data['credit_score']}")
        
        return customer_id
    
    def process_loan_application(self, application_data: dict) -> dict:
        """
        Process a loan application with full high-impact AI compliance.
        
        This demonstrates:
        - Article 34.2: Explainability (to extent technically feasible)
        - Article 34.4: Human oversight (tiered approval)
        - Article 35: Ongoing impact monitoring
        """
        customer = self.customers.get(application_data['customer_id'])
        if not customer:
            return {"error": "Customer not found"}
        
        loan_amount = application_data['amount']
        
        print(f"\n📝 Processing Loan Application")
        print(f"   Customer: {customer['name']}")
        print(f"   Amount: ₩{loan_amount:,.0f}")
        print(f"   Purpose: {application_data['purpose']}")
        
        # Determine required approval level based on amount
        if loan_amount > 100_000_000:
            required_approver = "credit_committee"
            risk_level = "CRITICAL"
        elif loan_amount > 50_000_000:
            required_approver = "branch_manager"
            risk_level = "HIGH"
        else:
            required_approver = "loan_officer"
            risk_level = "MEDIUM"
        
        # Calculate risk score
        risk_result = self._calculate_loan_risk(customer, application_data)
        
        # Make AI decision
        ai_approved = risk_result['score'] >= 70
        
        # Log decision with explainability (Article 34.2)
        decision = self.tracker.log_consequential_decision({
            "consumer_id": customer['customer_id'],
            "decision": "APPROVED" if ai_approved else "DENIED",
            "principal_reasons": risk_result['reasons'],
            "explanation": self._generate_explanation(risk_result, ai_approved, loan_amount),
            "decision_factors": risk_result['factors'],
            "ai_was_determining_factor": True,
            "human_approver": required_approver if risk_level in ["HIGH", "CRITICAL"] else None,
            "human_review_available": True,
            "appeal_rights_provided": True,
            "metadata": {
                "loan_amount": loan_amount,
                "loan_purpose": application_data['purpose'],
                "customer_age": customer['age'],
                "customer_nationality": customer.get('nationality'),
                "customer_income": customer['income'],
                "risk_score": risk_result['score'],
                "risk_level": risk_level,
                "required_approver": required_approver
            }
        })
        
        # Log human oversight for high-risk decisions
        if risk_level in ["HIGH", "CRITICAL"]:
            oversight_log = {
                "decision_id": decision.get('decision_id'),
                "required_approver": required_approver,
                "status": "PENDING_APPROVAL",
                "escalation_time": time.time()
            }
            self.oversight_logs.append(oversight_log)
            
            print(f"\n👤 Human Oversight Required")
            print(f"   Approver: {required_approver}")
            print(f"   Status: Pending Approval")
        
        # Store application
        application = {
            "application_id": f"APP-{int(time.time())}",
            "customer_id": customer['customer_id'],
            "amount": loan_amount,
            "purpose": application_data['purpose'],
            "decision": decision['decision'],
            "risk_score": risk_result['score'],
            "risk_level": risk_level,
            "required_approver": required_approver if risk_level in ["HIGH", "CRITICAL"] else None,
            "decision_id": decision.get('decision_id'),
            "timestamp": time.time()
        }
        
        self.loan_applications.append(application)
        
        print(f"\n📊 AI Decision:")
        print(f"   Decision: {decision['decision']}")
        print(f"   Risk Score: {risk_result['score']:.1f}/100")
        print(f"   Risk Level: {risk_level}")
        print(f"   Reasons: {', '.join(risk_result['reasons'])}")
        
        return application
    
    def _calculate_loan_risk(self, customer: dict, application: dict) -> dict:
        """Calculate loan risk using AI model."""
        
        score = 0
        factors = {}
        reasons = []
        
        # Credit score (0-40 points)
        credit_score = customer['credit_score']
        if credit_score >= 850:
            score += 40
            factors['credit_score'] = {"score": 40, "rating": "excellent"}
            reasons.append("Credit score excellent (850+)")
        elif credit_score >= 800:
            score += 35
            factors['credit_score'] = {"score": 35, "rating": "very good"}
            reasons.append("Credit score very good (800-849)")
        elif credit_score >= 750:
            score += 30
            factors['credit_score'] = {"score": 30, "rating": "good"}
            reasons.append("Credit score good (750-799)")
        elif credit_score >= 700:
            score += 25
            factors['credit_score'] = {"score": 25, "rating": "fair"}
            reasons.append("Credit score fair (700-749)")
        else:
            score += 15
            factors['credit_score'] = {"score": 15, "rating": "below average"}
            reasons.append("Credit score below optimal (<700)")
        
        # Debt-to-income ratio (0-30 points)
        monthly_income = customer['income'] / 12
        monthly_debt = customer.get('monthly_debt', 0)
        dti = (monthly_debt / monthly_income) * 100 if monthly_income > 0 else 0
        
        if dti <= 30:
            score += 30
            factors['dti'] = {"score": 30, "value": dti}
            reasons.append(f"Debt-to-income ratio excellent ({dti:.1f}%)")
        elif dti <= 40:
            score += 20
            factors['dti'] = {"score": 20, "value": dti}
            reasons.append(f"Debt-to-income ratio acceptable ({dti:.1f}%)")
        else:
            score += 10
            factors['dti'] = {"score": 10, "value": dti}
            reasons.append(f"Debt-to-income ratio high ({dti:.1f}%)")
        
        # Employment stability (0-20 points)
        if customer['employment_years'] >= 5:
            score += 20
            factors['employment'] = {"score": 20, "years": customer['employment_years']}
            reasons.append("Stable employment history (5+ years)")
        elif customer['employment_years'] >= 2:
            score += 15
            factors['employment'] = {"score": 15, "years": customer['employment_years']}
            reasons.append("Adequate employment history")
        else:
            score += 5
            factors['employment'] = {"score": 5, "years": customer['employment_years']}
            reasons.append("Limited employment history")
        
        # Loan-to-value (if applicable)
        if 'property_value' in application:
            ltv = (application['amount'] / application['property_value']) * 100
            if ltv <= 60:
                score += 10
                factors['ltv'] = {"score": 10, "value": ltv}
                reasons.append(f"Loan-to-value ratio excellent ({ltv:.1f}%)")
            elif ltv <= 80:
                score += 5
                factors['ltv'] = {"score": 5, "value": ltv}
                reasons.append(f"Loan-to-value ratio acceptable ({ltv:.1f}%)")
        
        return {
            "score": score,
            "factors": factors,
            "reasons": reasons[:3]  # Top 3 reasons for explainability
        }
    
    def _generate_explanation(self, risk_result: dict, approved: bool, amount: float) -> str:
        """Generate human-readable explanation (Article 34.2)."""
        if approved:
            return (
                f"Your loan application for ₩{amount:,.0f} has been APPROVED "
                f"with a score of {risk_result['score']:.1f}/100. "
                f"Key factors: {', '.join(risk_result['reasons'][:2])}. "
                f"If you disagree with this decision, you have the right to request "
                f"human review or appeal."
            )
        else:
            return (
                f"Your loan application for ₩{amount:,.0f} has been DECLINED "
                f"with a score of {risk_result['score']:.1f}/100. "
                f"Key factors: {', '.join(risk_result['reasons'][:2])}. "
                f"You have the right to request human review or correction of your data."
            )
    
    def run_demo(self):
        """Run complete high-impact AI demonstration."""
        
        # Step 1: Register and classify system
        determination = self.register_system()
        
        if not determination.get("is_high_impact"):
            print("\n❌ System not classified as high-impact - exiting demo")
            return
        
        # Step 2: Create risk management plan
        risk_plan = self.create_risk_management_plan()
        
        # Step 3: Configure human oversight
        oversight = self.configure_human_oversight()
        
        # Step 4: Conduct impact assessment
        assessment = self.conduct_impact_assessment()
        
        # Step 5: Add customers (diverse demographics)
        customers = [
            {
                "name": "Kim Min-su",
                "age": 45,
                "gender": "male",
                "nationality": "한국",
                "income": 60_000_000,
                "employment_years": 12,
                "credit_score": 820,
                "monthly_debt": 1_000_000,
                "assets": 200_000_000
            },
            {
                "name": "Lee Ji-eun",
                "age": 32,
                "gender": "female",
                "nationality": "한국",
                "income": 45_000_000,
                "employment_years": 5,
                "credit_score": 780,
                "monthly_debt": 800_000,
                "assets": 50_000_000
            },
            {
                "name": "Park Jae-hyun",
                "age": 28,
                "gender": "male",
                "nationality": "한국",
                "income": 35_000_000,
                "employment_years": 3,
                "credit_score": 720,
                "monthly_debt": 600_000,
                "assets": 20_000_000
            },
            {
                "name": "Choi Soo-young",
                "age": 55,
                "gender": "female",
                "nationality": "한국",
                "income": 80_000_000,
                "employment_years": 20,
                "credit_score": 850,
                "monthly_debt": 500_000,
                "assets": 500_000_000
            }
        ]
        
        customer_ids = []
        for cust in customers:
            cid = self.add_customer(cust)
            customer_ids.append(cid)
        
        # Step 6: Process loan applications (varying amounts)
        applications = [
            {"customer_id": customer_ids[0], "amount": 30_000_000, "purpose": "home_improvement"},
            {"customer_id": customer_ids[1], "amount": 20_000_000, "purpose": "education"},
            {"customer_id": customer_ids[2], "amount": 10_000_000, "purpose": "business"},
            {"customer_id": customer_ids[3], "amount": 80_000_000, "purpose": "real_estate"},
            {"customer_id": customer_ids[0], "amount": 120_000_000, "purpose": "business_expansion"}  # >100M - credit committee
        ]
        
        for app in applications:
            self.process_loan_application(app)
        
        # Step 7: Generate compliance report
        print("\n📊 Compliance Report")
        report = self.tracker.generate_compliance_report()
        print(f"   Report ID: {report['report_id']}")
        print(f"   High-Impact Systems: {report['statistics']['high_impact_systems']}")
        print(f"   Risk Assessments: {report['statistics']['risk_assessments']}")
        
        # Step 8: Verify compliance
        print("\n📋 Compliance Verification")
        verification = self.tracker.verify_compliance()
        print(f"   Status: {verification['status']}")
        
        print("\n" + "="*80)
        print("✅ High-Impact AI Demo Complete")
        print("="*80)
        print(f"   Customers: {len(customer_ids)}")
        print(f"   Applications: {len(self.loan_applications)}")
        print(f"   Human Oversight Events: {len(self.oversight_logs)}")
        print(f"   Risk Plan: Active")
        print(f"   Impact Assessment: Complete")
        print(f"\n📋 Article 33-35 Compliance:")
        print(f"   ✅ High-Impact Determination")
        print(f"   ✅ Risk Management Plan")
        print(f"   ✅ Human Oversight (Tiered Approval)")
        print(f"   ✅ AI Impact Assessment")
        print(f"   ✅ Explainability (Technically Feasible)")


if __name__ == "__main__":
    system = KoreanLoanApprovalSystem("KEB Hana Bank")
    system.run_demo()
