import json
import re
from typing import Dict, List, Any
import requests
from bs4 import BeautifulSoup

# Load dark patterns data
with open('/Users/manavaryasingh/DarkLens-MCP-Server/data/dark_patterns.json', 'r') as f:
    DARK_PATTERNS_DATA = json.load(f)

DARK_PATTERNS = DARK_PATTERNS_DATA['patterns']

# MCP Server setup
from mcp import Server, Tool

server = Server("darklens")

@server.tool()
def detect_dark_patterns(input_type: str, content: str) -> List[Dict[str, Any]]:
    """
    Detect dark patterns in UI text, HTML, or URL.

    Args:
        input_type: "html", "text", or "url"
        content: The HTML content, plain text, or URL to analyze

    Returns:
        List of detected patterns with pattern_id, pattern_type, confidence, evidence
    """
    text_content = ""
    
    if input_type == "url":
        try:
            response = requests.get(content, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text(separator=' ', strip=True)
        except Exception as e:
            return [{"error": f"Failed to fetch URL: {str(e)}"}]
    elif input_type == "html":
        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text(separator=' ', strip=True)
    elif input_type == "text":
        text_content = content
    else:
        return [{"error": "Invalid input_type. Must be 'html', 'text', or 'url'"}]
    
    # Simple rule-based detection
    detected_patterns = []
    
    for pattern in DARK_PATTERNS:
        confidence = 0.0
        evidence = []
        
        # Check for exact matches in examples
        for example in pattern.get('examples', []):
            if re.search(re.escape(example.lower()), text_content.lower()):
                confidence = max(confidence, 0.9)
                evidence.append(example)
        
        # Additional heuristics
        if pattern['id'] == 'confirmshaming':
            shame_words = ['no thanks', 'i don\'t care', 'skip', 'ignore']
            if any(word in text_content.lower() for word in shame_words):
                confidence = max(confidence, 0.7)
                evidence.append("Shaming language detected")
        
        if pattern['id'] == 'fake_urgency':
            urgency_words = ['limited time', 'only left', 'expires soon', 'act now']
            if any(word in text_content.lower() for word in urgency_words):
                confidence = max(confidence, 0.8)
                evidence.append("Urgency language detected")
        
        if confidence > 0:
            detected_patterns.append({
                "pattern_id": pattern['id'],
                "pattern_type": pattern['name'],
                "confidence": confidence,
                "evidence": evidence
            })
    
    return detected_patterns

@server.tool()
def classify_pattern(pattern_id: str) -> Dict[str, Any]:
    """
    Classify a detected dark pattern.

    Args:
        pattern_id: The ID of the pattern to classify

    Returns:
        Dictionary with category, cognitive_bias, severity
    """
    for pattern in DARK_PATTERNS:
        if pattern['id'] == pattern_id:
            return {
                "category": pattern['name'],
                "cognitive_bias_exploited": pattern['cognitive_bias'],
                "severity_level": pattern['severity']
            }
    return {"error": f"Pattern ID '{pattern_id}' not found"}

@server.tool()
def explain_manipulation(pattern_id: str, user_type: str = "average user") -> Dict[str, Any]:
    """
    Explain why a pattern is manipulative.

    Args:
        pattern_id: The ID of the pattern
        user_type: Type of user (child, elderly, average user)

    Returns:
        Dictionary with explanation, psychological principle, harm potential
    """
    for pattern in DARK_PATTERNS:
        if pattern['id'] == pattern_id:
            base_explanation = f"This {pattern['name']} pattern manipulates users by {pattern['description'].lower()}."
            
            user_specific = {
                "child": "Children may not understand the implications and could be easily pressured.",
                "elderly": "Elderly users might feel more vulnerable to social pressure or urgency tactics.",
                "average user": "Average users may make decisions based on emotional responses rather than rational evaluation."
            }.get(user_type, "Users may be influenced without full awareness.")
            
            return {
                "plain_english_explanation": f"{base_explanation} {user_specific}",
                "psychological_principle_used": pattern['cognitive_bias'],
                "harm_potential": pattern['severity']
            }
    return {"error": f"Pattern ID '{pattern_id}' not found"}

@server.tool()
def risk_score(pattern_id: str, region: str) -> Dict[str, Any]:
    """
    Assess legal/compliance risk of a pattern.

    Args:
        pattern_id: The ID of the pattern
        region: Geographic region (EU, US, India)

    Returns:
        Dictionary with risk score, violated regulations, enforcement likelihood
    """
    regulations = {
        "EU": {"GDPR": ["Article 7 (Consent)", "Article 25 (Data protection by design)"]},
        "US": {"FTC Act": ["Section 5 (Unfair or deceptive acts)"], "CCPA": ["Section 1798.100 et seq."]},
        "India": {"DPDP Act": ["Section 4 (Consent)", "Section 5 (Purpose limitation)"]}
    }
    
    base_risk = {"High": 85, "Medium": 65, "Low": 35}
    
    for pattern in DARK_PATTERNS:
        if pattern['id'] == pattern_id:
            risk_score = base_risk.get(pattern['severity'], 50)
            
            # Adjust for region
            if region == "EU":
                risk_score += 10  # Stricter GDPR enforcement
            elif region == "US":
                risk_score += 5   # FTC active enforcement
            elif region == "India":
                risk_score -= 5   # Newer regulation
            
            violated_regs = regulations.get(region, {"General": ["Consumer protection laws"]})
            
            likelihood = "High" if risk_score > 70 else "Medium" if risk_score > 50 else "Low"
            
            return {
                "compliance_risk_score": min(risk_score, 100),
                "violated_regulation_references": violated_regs,
                "enforcement_likelihood": likelihood
            }
    
    return {"error": f"Pattern ID '{pattern_id}' not found"}

@server.tool()
def suggest_ethical_alternative(pattern_id: str) -> Dict[str, Any]:
    """
    Suggest ethical UI alternatives.

    Args:
        pattern_id: The ID of the pattern

    Returns:
        Dictionary with rewritten UI copy, redesigned flow, ethical justification
    """
    alternatives = {
        "confirmshaming": {
            "copy": "Accept Cookies / Decline Cookies",
            "flow": "Present accept and decline options with equal visual prominence and no shaming language.",
            "justification": "Respects user autonomy and provides genuine choice without emotional manipulation."
        },
        "forced_consent": {
            "copy": "I consent to optional features / I do not consent",
            "flow": "Use clear, accessible buttons for both consent and rejection with no pre-selection.",
            "justification": "Ensures informed consent and complies with privacy regulations requiring explicit opt-in."
        },
        "roach_motel": {
            "copy": "Start Free Trial / No Thanks",
            "flow": "Clearly explain cancellation process upfront and make it easy to cancel at any time.",
            "justification": "Builds trust through transparency and allows users to exit easily."
        },
        "hidden_costs": {
            "copy": "Total Price: $X.XX (includes all fees)",
            "flow": "Display all costs upfront in the product listing and checkout.",
            "justification": "Provides transparency and prevents surprise charges."
        },
        "sneak_into_basket": {
            "copy": "Add to Cart / Continue Shopping",
            "flow": "Only add items explicitly selected by the user.",
            "justification": "Respects user intent and prevents unauthorized additions."
        },
        "fake_urgency": {
            "copy": "Available while supplies last",
            "flow": "Use honest scarcity indicators based on actual inventory.",
            "justification": "Avoids creating false pressure and builds credibility."
        },
        "visual_manipulation": {
            "copy": "Accept / Reject",
            "flow": "Design buttons with equal size, color, and prominence.",
            "justification": "Ensures users can make decisions based on content, not deceptive design."
        },
        "default_bias_exploitation": {
            "copy": "Subscribe to newsletter? Yes / No",
            "flow": "Present options neutrally without pre-selection.",
            "justification": "Allows users to make conscious choices without bias toward defaults."
        },
        "nagging": {
            "copy": "Subscribe for updates (optional)",
            "flow": "Show subscription prompt once and respect user's choice.",
            "justification": "Reduces user annoyance and respects attention."
        }
    }
    
    for pattern in DARK_PATTERNS:
        if pattern['id'] == pattern_id:
            alt = alternatives.get(pattern_id, {
                "copy": "Clear, honest option",
                "flow": "Transparent user interaction",
                "justification": "Promotes ethical design principles"
            })
            return {
                "rewritten_ui_copy": alt["copy"],
                "redesigned_flow_description": alt["flow"],
                "ethical_justification": alt["justification"]
            }
    
    return {"error": f"Pattern ID '{pattern_id}' not found"}

# Run the server
if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    asyncio.run(server.run(stdio_server()))