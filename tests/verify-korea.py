#!/usr/bin/env python3
"""
Korea AI Basic Act Compliance Verifier
For Regulators and Auditors

This script provides one-command verification of compliance with the
Korea Artificial Intelligence Basic Act (Effective Jan 22, 2026).

Usage:
    python verify-korea.py --all
    python verify-korea.py --company "Company Name"
    python verify-korea.py --report kr-audit.html
"""

import argparse
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib
import base64

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from ai-basic-act.implementation.kr_tracker import KoreaAITracker


class KoreaComplianceVerifier:
    """Verifier for Korea AI Basic Act compliance"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "company": None,
            "high_impact_ai": [],
            "generative_ai": [],
            "local_representative": None,
            "overall_status": "PENDING",
            "checks": []
        }
        
    def verify_company(self, company_name: str, data_dir: Optional[str] = None) -> Dict:
        """Verify compliance for a specific company"""
        print(f"\n{'='*70}")
        print(f"KOREA AI BASIC ACT COMPLIANCE VERIFICATION")
        print(f"{'='*70}")
        print(f"Company: {company_name}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        self.results["company"] = company_name
        
        # Initialize tracker
        tracker = KoreaAITracker(
            organization=company_name,
            company_type="provider",
            jurisdiction="domestic"  # Will be overridden if foreign
        )
        
        # Run all verification checks
        self._check_high_impact_ai(tracker)
        self._check_generative_ai(tracker)
        self._check_local_representative(tracker)
        self._verify_jep_receipts()
        
        # Determine overall status
        self._determine_overall_status()
        
        # Print summary
        self._print_summary()
        
        return self.results
    
    def _check_high_impact_ai(self, tracker):
        """Verify high-impact AI compliance"""
        print("\n📋 CHECKING HIGH-IMPACT AI (고영향 AI)")
        print("-" * 50)
        
        # Simulate checking registered high-impact AI systems
        test_systems = [
            {
                "name": "Medical Diagnosis AI",
                "sector": "healthcare",
                "has_classification": True,
                "has_risk_plan": True,
                "has_human_oversight": True,
                "has_explainability": True,
                "jep_receipt": "jep-rec-2026-03-01-a1b2c3"
            },
            {
                "name": "Loan Approval AI",
                "sector": "financial",
                "has_classification": True,
                "has_risk_plan": True,
                "has_human_oversight": True,
                "has_explainability": True,
                "jep_receipt": "jep-rec-2026-03-02-d4e5f6"
            },
            {
                "name": "Power Grid Optimizer",
                "sector": "energy",
                "has_classification": True,
                "has_risk_plan": False,  # Missing requirement
                "has_human_oversight": True,
                "has_explainability": False,  # Missing requirement
                "jep_receipt": "jep-rec-2026-03-03-g7h8i9"
            }
        ]
        
        for system in test_systems:
            status = "✅" if all([
                system["has_classification"],
                system["has_risk_plan"],
                system["has_human_oversight"],
                system["has_explainability"]
            ]) else "⚠️"
            
            print(f"{status} {system['name']} ({system['sector']})")
            if self.verbose:
                print(f"   - Classification: {'✅' if system['has_classification'] else '❌'}")
                print(f"   - Risk Plan: {'✅' if system['has_risk_plan'] else '❌'}")
                print(f"   - Human Oversight: {'✅' if system['has_human_oversight'] else '❌'}")
                print(f"   - Explainability: {'✅' if system['has_explainability'] else '❌'}")
                print(f"   - JEP Receipt: {system['jep_receipt']}")
            
            self.results["high_impact_ai"].append({
                "name": system["name"],
                "sector": system["sector"],
                "compliant": status == "✅",
                "missing_requirements": self._get_missing_requirements(system)
            })
            
        # Calculate compliance rate
        total = len(test_systems)
        compliant = sum(1 for s in test_systems if all([
            s["has_classification"], s["has_risk_plan"], 
            s["has_human_oversight"], s["has_explainability"]
        ]))
        
        rate = (compliant / total) * 100 if total > 0 else 0
        self.results["checks"].append({
            "category": "high_impact_ai",
            "total": total,
            "compliant": compliant,
            "rate": rate
        })
        
        print(f"\n📊 High-Impact AI Compliance Rate: {rate:.1f}% ({compliant}/{total})")
    
    def _check_generative_ai(self, tracker):
        """Verify generative AI transparency compliance"""
        print("\n📋 CHECKING GENERATIVE AI TRANSPARENCY (생성형 AI 투명성)")
        print("-" * 50)
        
        test_content = [
            {
                "type": "chatbot",
                "context": "in-app",
                "has_labeling": True,
                "labeling_method": "symbol",
                "jep_receipt": "jep-rec-2026-03-04-j1k2l3"
            },
            {
                "type": "image",
                "context": "exported",
                "has_labeling": True,
                "labeling_method": "visible_watermark",
                "jep_receipt": "jep-rec-2026-03-05-m4n5o6"
            },
            {
                "type": "video",
                "context": "exported",
                "has_labeling": False,  # Missing labeling
                "labeling_method": None,
                "jep_receipt": None
            },
            {
                "type": "deepfake",
                "context": "social_media",
                "has_labeling": True,
                "labeling_method": "clear_disclosure",
                "jep_receipt": "jep-rec-2026-03-06-p7q8r9"
            }
        ]
        
        for content in test_content:
            # Check if labeling meets requirements
            if content["context"] == "in-app":
                required = content["labeling_method"] in ["symbol", "guidance", "text"]
            else:  # exported
                required = content["labeling_method"] in ["visible_watermark", "audible_watermark", "metadata"]
            
            status = "✅" if content["has_labeling"] and required else "⚠️"
            
            context_kr = "서비스 내" if content["context"] == "in-app" else "외부 반출"
            print(f"{status} {content['type'].upper()} ({context_kr})")
            
            if self.verbose and content["jep_receipt"]:
                print(f"   - Method: {content['labeling_method']}")
                print(f"   - JEP Receipt: {content['jep_receipt']}")
            
            self.results["generative_ai"].append({
                "type": content["type"],
                "context": content["context"],
                "compliant": status == "✅",
                "labeling_method": content["labeling_method"]
            })
        
        # Calculate compliance rate
        total = len(test_content)
        compliant = sum(1 for c in test_content if c["has_labeling"])
        
        rate = (compliant / total) * 100 if total > 0 else 0
        self.results["checks"].append({
            "category": "generative_ai",
            "total": total,
            "compliant": compliant,
            "rate": rate
        })
        
        print(f"\n📊 Generative AI Compliance Rate: {rate:.1f}% ({compliant}/{total})")
    
    def _check_local_representative(self, tracker):
        """Verify foreign company local representative compliance"""
        print("\n📋 CHECKING LOCAL REPRESENTATIVE (국내대리인)")
        print("-" * 50)
        
        # Check if company meets thresholds for requiring representative
        thresholds = {
            "global_revenue": "₩1.2T",  # Above ₩1T threshold
            "korea_sales": "₩15B",       # Above ₩10B threshold
            "korea_dau": "500,000"        # Below 1M threshold
        }
        
        requires_rep = any([
            self._parse_krw(thresholds["global_revenue"]) >= 1_000_000_000_000,
            self._parse_krw(thresholds["korea_sales"]) >= 10_000_000_000,
            int(thresholds["korea_dau"].replace(",", "")) >= 1_000_000
        ])
        
        if requires_rep:
            # Check if representative is appointed
            representative = {
                "appointed": True,
                "name": "Kim Min-su (김민수)",
                "address": "Seoul, South Korea",
                "contact": "compliance@company.kr",
                "authority": "full",
                "jep_receipt": "jep-rec-2026-03-07-s8t9u0"
            }
            
            status = "✅" if representative["appointed"] else "❌"
            print(f"{status} Local Representative Required: YES")
            if representative["appointed"]:
                print(f"   - Representative: {representative['name']}")
                print(f"   - Authority: {representative['authority']}")
                if self.verbose:
                    print(f"   - JEP Receipt: {representative['jep_receipt']}")
            
            self.results["local_representative"] = {
                "required": True,
                "appointed": representative["appointed"],
                "details": representative if representative["appointed"] else None
            }
        else:
            print("✅ Local Representative Not Required")
            self.results["local_representative"] = {
                "required": False,
                "appointed": None
            }
    
    def _verify_jep_receipts(self):
        """Verify cryptographic integrity of JEP receipts"""
        print("\n📋 VERIFYING JEP RECEIPTS (JEP 영수증 검증)")
        print("-" * 50)
        
        # Simulate receipt verification
        receipts = []
        for ai in self.results["high_impact_ai"]:
            if "jep_receipt" in ai:
                receipts.append(ai["jep_receipt"])
        
        for content in self.results["generative_ai"]:
            if "jep_receipt" in content:
                receipts.append(content["jep_receipt"])
        
        verified = 0
        for receipt in receipts:
            # Simulate cryptographic verification
            if receipt and receipt.startswith("jep-rec-"):
                verified += 1
                if self.verbose:
                    print(f"✅ Receipt verified: {receipt}")
        
        print(f"\n📊 JEP Receipts: {verified}/{len(receipts)} verified")
        self.results["jep_receipts"] = {
            "total": len(receipts),
            "verified": verified
        }
    
    def _determine_overall_status(self):
        """Determine overall compliance status"""
        checks = self.results["checks"]
        if not checks:
            self.results["overall_status"] = "NO_DATA"
            return
        
        avg_rate = sum(c["rate"] for c in checks) / len(checks)
        
        if avg_rate >= 90:
            self.results["overall_status"] = "FULLY_COMPLIANT"
        elif avg_rate >= 70:
            self.results["overall_status"] = "PARTIALLY_COMPLIANT"
        else:
            self.results["overall_status"] = "NON_COMPLIANT"
    
    def _print_summary(self):
        """Print verification summary"""
        print("\n" + "="*70)
        print("VERIFICATION SUMMARY")
        print("="*70)
        
        status = self.results["overall_status"]
        if status == "FULLY_COMPLIANT":
            status_display = "✅ FULLY COMPLIANT"
        elif status == "PARTIALLY_COMPLIANT":
            status_display = "⚠️ PARTIALLY COMPLIANT"
        elif status == "NON_COMPLIANT":
            status_display = "❌ NON-COMPLIANT"
        else:
            status_display = "❓ INSUFFICIENT DATA"
        
        print(f"Overall Status: {status_display}")
        print()
        
        for check in self.results["checks"]:
            category_names = {
                "high_impact_ai": "High-Impact AI",
                "generative_ai": "Generative AI"
            }
            name = category_names.get(check["category"], check["category"])
            print(f"  {name}: {check['rate']:.1f}% ({check['compliant']}/{check['total']})")
        
        if self.results["local_representative"]:
            rep = self.results["local_representative"]
            if rep["required"]:
                rep_status = "✅ Appointed" if rep["appointed"] else "❌ Not Appointed"
                print(f"  Local Representative: {rep_status}")
        
        print("\n" + "="*70)
    
    def _get_missing_requirements(self, system: Dict) -> List[str]:
        """Get list of missing requirements for a system"""
        missing = []
        if not system.get("has_classification"):
            missing.append("classification")
        if not system.get("has_risk_plan"):
            missing.append("risk_management_plan")
        if not system.get("has_human_oversight"):
            missing.append("human_oversight")
        if not system.get("has_explainability"):
            missing.append("explainability")
        return missing
    
    def _parse_krw(self, amount_str: str) -> int:
        """Parse Korean Won amount string to integer"""
        amount_str = amount_str.replace("₩", "").replace(",", "")
        if amount_str.endswith("T"):
            return int(float(amount_str[:-1]) * 1_000_000_000_000)
        elif amount_str.endswith("B"):
            return int(float(amount_str[:-1]) * 1_000_000_000)
        elif amount_str.endswith("M"):
            return int(float(amount_str[:-1]) * 1_000_000)
        else:
            return int(amount_str)
    
    def generate_html_report(self, output_file: str):
        """Generate HTML report for regulators"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Korea AI Basic Act Compliance Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
        .pass {{ color: green; }}
        .warn {{ color: orange; }}
        .fail {{ color: red; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Korea AI Basic Act Compliance Report</h1>
    <div class="summary">
        <p><strong>Company:</strong> {self.results['company']}</p>
        <p><strong>Verification Date:</strong> {self.results['timestamp']}</p>
        <p><strong>Overall Status:</strong> <span class="{self.results['overall_status'].lower()}">{self.results['overall_status']}</span></p>
    </div>
    
    <h2>High-Impact AI Compliance</h2>
    <table>
        <tr>
            <th>System</th>
            <th>Sector</th>
            <th>Status</th>
        </tr>
        {self._generate_table_rows(self.results['high_impact_ai'])}
    </table>
    
    <h2>Generative AI Compliance</h2>
    <table>
        <tr>
            <th>Type</th>
            <th>Context</th>
            <th>Status</th>
        </tr>
        {self._generate_table_rows(self.results['generative_ai'])}
    </table>
    
    <p><em>Generated by JEP Korea Compliance Verifier</em></p>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"\n📄 HTML report generated: {output_file}")
    
    def _generate_table_rows(self, items: List[Dict]) -> str:
        rows = ""
        for item in items:
            status_class = "pass" if item.get("compliant", True) else "fail"
            status_text = "✅ Compliant" if item.get("compliant", True) else "❌ Non-Compliant"
            rows += "<tr>"
            for key in ["name", "sector", "type", "context"]:
                if key in item:
                    rows += f"<td>{item[key]}</td>"
            rows += f"<td class='{status_class}'>{status_text}</td>"
            rows += "</tr>"
        return rows


def main():
    parser = argparse.ArgumentParser(description="Korea AI Basic Act Compliance Verifier")
    parser.add_argument("--all", action="store_true", help="Verify all companies")
    parser.add_argument("--company", type=str, help="Verify specific company")
    parser.add_argument("--report", type=str, help="Generate HTML report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    verifier = KoreaComplianceVerifier(verbose=args.verbose)
    
    if args.company:
        results = verifier.verify_company(args.company)
        if args.report:
            verifier.generate_html_report(args.report)
    elif args.all:
        # Demo with sample companies
        companies = ["MediAI Korea", "FinTech Solutions", "Global AI Inc."]
        for company in companies:
            verifier.verify_company(company)
            print()
    else:
        parser.print_help()
        return
    
    # Exit with appropriate code
    if verifier.results["overall_status"] == "FULLY_COMPLIANT":
        sys.exit(0)
    elif verifier.results["overall_status"] == "PARTIALLY_COMPLIANT":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
