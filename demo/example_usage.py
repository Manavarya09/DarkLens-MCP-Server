#!/usr/bin/env python3
"""
Demo script showing how to interact with the DarkLens MCP Server.
This demonstrates the various tools and their usage.
"""

import json
from darklens_mcp_server.server import (
    detect_dark_patterns,
    classify_pattern,
    explain_manipulation,
    risk_score,
    suggest_ethical_alternative
)

def demo_dark_pattern_detection():
    """Demonstrate dark pattern detection on sample text."""
    print("=== Dark Pattern Detection Demo ===\n")
    
    # Sample text with confirmshaming
    sample_text = """
    Welcome to our newsletter signup!
    Subscribe now to get exclusive deals and save money.
    No thanks, I don't want to save money.
    """
    
    print("Sample UI Text:")
    print(sample_text.strip())
    print("\nDetected Patterns:")
    
    results = detect_dark_patterns("text", sample_text)
    print(json.dumps(results, indent=2))
    
    if results and not results[0].get("error"):
        pattern_id = results[0]["pattern_id"]
        
        print(f"\n=== Classification for {pattern_id} ===")
        classification = classify_pattern(pattern_id)
        print(json.dumps(classification, indent=2))
        
        print(f"\n=== Explanation for {pattern_id} ===")
        explanation = explain_manipulation(pattern_id, "average user")
        print(json.dumps(explanation, indent=2))
        
        print(f"\n=== Risk Assessment for {pattern_id} (EU) ===")
        risk = risk_score(pattern_id, "EU")
        print(json.dumps(risk, indent=2))
        
        print(f"\n=== Ethical Alternative for {pattern_id} ===")
        alternative = suggest_ethical_alternative(pattern_id)
        print(json.dumps(alternative, indent=2))

def demo_url_analysis():
    """Demonstrate URL analysis (requires internet connection)."""
    print("\n=== URL Analysis Demo ===\n")
    
    # Note: This would analyze a real website
    # For demo purposes, we'll use sample text
    print("Note: URL analysis requires internet connection.")
    print("For this demo, we're using sample text instead.")
    
    sample_html = """
    <html>
    <body>
        <button>Accept All Cookies</button>
        <button style="font-size: 10px;">Reject Cookies</button>
        <p>Limited time offer! Only 2 left!</p>
    </body>
    </html>
    """
    
    print("Sample HTML:")
    print(sample_html.strip())
    print("\nDetected Patterns:")
    
    results = detect_dark_patterns("html", sample_html)
    print(json.dumps(results, indent=2))

def demo_social_proof_detection():
    """Demonstrate social proof pattern detection from Kaggle dataset."""
    print("\n=== Social Proof Detection Demo (Kaggle Dataset) ===\n")
    
    # Example from Kaggle dataset
    social_proof_text = "1,142 people have added to cart recently"
    
    print("Sample UI Text:")
    print(f'"{social_proof_text}"')
    print("\nDetected Patterns:")
    
    results = detect_dark_patterns("text", social_proof_text)
    print(json.dumps(results, indent=2))
    
    if results:
        pattern_id = results[0]["pattern_id"]
        
        print(f"\n=== Classification for {pattern_id} ===")
        classification = classify_pattern(pattern_id)
        print(json.dumps(classification, indent=2))
        
        print(f"\n=== Ethical Alternative for {pattern_id} ===")
        alternative = suggest_ethical_alternative(pattern_id)
        print(json.dumps(alternative, indent=2))

def demo_compliance_report():
    """Demonstrate generating a compliance report."""
    print("\n=== Compliance Report Demo ===\n")
    
    patterns = ["confirmshaming", "forced_consent", "roach_motel"]
    
    print(f"Generating compliance report for patterns: {patterns}")
    print("Region: EU\n")
    
    report = {
        "title": "UX Ethics Compliance Report",
        "region": "EU",
        "patterns_analyzed": patterns,
        "findings": []
    }
    
    for pattern_id in patterns:
        risk = risk_score(pattern_id, "EU")
        alternative = suggest_ethical_alternative(pattern_id)
        
        finding = {
            "pattern_id": pattern_id,
            "risk_score": risk["compliance_risk_score"],
            "violations": risk["violated_regulation_references"],
            "recommendation": alternative["redesigned_flow_description"]
        }
        
        report["findings"].append(finding)
    
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    demo_dark_pattern_detection()
    demo_url_analysis()
    demo_social_proof_detection()
    demo_compliance_report()
    
    print("\n=== Demo Complete ===")
    print("To run the MCP server: uv run darklens-server")
    print("Or: python -m darklens_mcp_server.server")