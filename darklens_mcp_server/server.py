"""DarkLens MCP Server - Dark Pattern Detection Server."""

import asyncio
import json
import re
from typing import Any, Dict, List

import httpx
import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("DarkLens MCP Server")

# Load dark patterns data
with open('/Users/manavaryasingh/DarkLens-MCP-Server/data/dark_patterns.json', 'r') as f:
    DARK_PATTERNS_DATA = json.load(f)

DARK_PATTERNS = DARK_PATTERNS_DATA['patterns']

# Resources
# @mcp.resource("dark_patterns://taxonomy")
# def get_dark_patterns_taxonomy() -> str:
#     """Get the complete dark patterns taxonomy."""
#     return json.dumps(DARK_PATTERNS, indent=2)

# @mcp.resource("ui_text://{url}")
# async def extract_ui_text(url: str) -> str:
#     """Extract UI text elements from a webpage."""
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url, timeout=10)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, 'html.parser')
#             
#             # Extract buttons, links, headings
#             elements = {
#                 "buttons": [btn.get_text(strip=True) for btn in soup.find_all('button') if btn.get_text(strip=True)],
#                 "links": [a.get_text(strip=True) for a in soup.find_all('a') if a.get_text(strip=True)],
#                 "headings": [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3']) if h.get_text(strip=True)],
#                 "modals": [div.get_text(strip=True) for div in soup.find_all('div', class_=re.compile(r'modal|popup|dialog')) if div.get_text(strip=True)]
#             }
#             
#             return json.dumps(elements, indent=2)
#     except Exception as e:
#         return json.dumps({"error": f"Failed to extract UI text: {str(e)}"}, indent=2)

# Tools
@mcp.tool()
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
            urgency_words = ['limited time', 'only left', 'expires soon', 'act now', 'hurry', 'flash sale']
            if any(word in text_content.lower() for word in urgency_words):
                confidence = max(confidence, 0.8)
                evidence.append("Urgency language detected")
        
        if pattern['id'] == 'social_proof':
            social_words = ['people have', 'purchased', 'added to cart', 'viewing this', 'just bought']
            if any(word in text_content.lower() for word in social_words):
                confidence = max(confidence, 0.6)
                evidence.append("Social proof language detected")
        
        if confidence > 0:
            detected_patterns.append({
                "pattern_id": pattern['id'],
                "pattern_type": pattern['name'],
                "confidence": confidence,
                "evidence": evidence
            })
    
    return detected_patterns

@mcp.tool()
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

@mcp.tool()
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

@mcp.tool()
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

@mcp.tool()
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
        },
        "social_proof": {
            "copy": "Based on customer reviews",
            "flow": "Use genuine customer testimonials and reviews without artificial social pressure.",
            "justification": "Builds trust through authentic social validation rather than manufactured pressure."
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

# Prompts
@mcp.prompt()
def audit_website(url: str) -> str:
    """Generate a prompt for auditing a website for dark patterns."""
    return f"""Please analyze the website at {url} for dark patterns. Use the available tools to:

1. Extract UI text elements from the page
2. Detect any dark patterns present
3. For each detected pattern, classify it and explain the manipulation
4. Assess the legal risk under relevant regulations
5. Suggest ethical alternatives for any problematic patterns

Provide a comprehensive report of your findings."""

@mcp.prompt()
def explain_ui_to_user(ui_element: str) -> str:
    """Generate a prompt for explaining UI elements to non-technical users."""
    return f"""Explain this UI element in simple, plain English that a non-technical user can understand: "{ui_element}"

Consider:
- What does this element do?
- Are there any hidden implications or manipulations?
- How might different types of users (children, elderly, average users) interpret this?
- Is this design ethical and transparent?

Use the dark pattern detection tools if needed to analyze for manipulative elements."""

@mcp.prompt()
def compliance_report(patterns: List[str], region: str) -> str:
    """Generate a prompt for creating a UX ethics compliance report."""
    pattern_list = ", ".join(patterns)
    return f"""Create a comprehensive UX ethics compliance report for the following dark patterns: {pattern_list}

Focus on the {region} region and include:
- Risk assessment for each pattern
- Relevant regulations that may be violated
- Enforcement likelihood
- Recommended remediation steps
- Ethical design alternatives

Structure the report as a professional document suitable for stakeholders."""

@mcp.prompt()
def rewrite_cta(cta_text: str) -> str:
    """Generate a prompt for rewriting manipulative CTAs."""
    return f"""Rewrite this call-to-action text to remove manipulation and make it ethical: "{cta_text}"

Consider:
- Remove any shaming, urgency, or pressure tactics
- Make the language clear and honest
- Ensure it respects user autonomy
- Provide genuine value proposition

Use the ethical alternative suggestion tool to help with the rewrite."""

@mcp.prompt()
def assess_gdpr_risk(pattern_id: str) -> str:
    """Generate a prompt for assessing GDPR risk of a pattern."""
    return f"""Assess the GDPR compliance risk of the '{pattern_id}' dark pattern.

Consider:
- Which GDPR articles might be violated?
- What is the potential impact on user rights?
- Enforcement likelihood by supervisory authorities
- Recommended actions for compliance

Provide a detailed risk assessment with specific regulatory references."""

if __name__ == "__main__":
    mcp.run()


@mcp.tool()
async def fetch_user_posts(user_id: int) -> str:
    """Fetch posts for a specific user from external API.

    Args:
        user_id: The user ID to fetch posts for
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/posts?userId={user_id}")
            response.raise_for_status()
            posts = response.json()
            return json.dumps(posts, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to fetch posts: {str(e)}"}, indent=2)


@mcp.tool()
def analyze_text(text: str) -> Dict[str, Any]:
    """Analyze text and return statistics.

    Args:
        text: The text to analyze
    """
    words = text.split()
    sentences = text.split('.')
    return {
        "word_count": len(words),
        "sentence_count": len([s for s in sentences if s.strip()]),
        "character_count": len(text),
        "average_word_length": sum(len(word) for word in words) / len(words) if words else 0,
    }


# Prompts
@mcp.prompt()
def summarize_content(content: str, max_length: int = 100) -> str:
    """Create a prompt to summarize content.

    Args:
        content: The content to summarize
        max_length: Maximum length of the summary
    """
    return f"Please summarize the following content in {max_length} words or less:\n\n{content}"


@mcp.prompt()
def analyze_sentiment(text: str) -> str:
    """Create a prompt to analyze sentiment of text.

    Args:
        text: The text to analyze for sentiment
    """
    return f"Analyze the sentiment of the following text. Classify it as positive, negative, or neutral, and explain your reasoning:\n\n{text}"


@mcp.prompt()
def generate_code(language: str, task: str, requirements: str = "") -> str:
    """Create a prompt to generate code.

    Args:
        language: Programming language
        task: The coding task
        requirements: Additional requirements
    """
    prompt = f"Write {language} code to {task}."
    if requirements:
        prompt += f"\n\nRequirements:\n{requirements}"
    return prompt


@mcp.prompt()
def create_study_plan(subject: str, hours_per_week: int, weeks: int) -> str:
    """Create a study plan prompt.

    Args:
        subject: The subject to study
        hours_per_week: Hours available per week
        weeks: Number of weeks for the plan
    """
    return f"""Create a detailed study plan for learning {subject}.

Available time: {hours_per_week} hours per week
Duration: {weeks} weeks

Please include:
1. Weekly breakdown of topics
2. Daily study schedule
3. Recommended resources
4. Assessment milestones
5. Tips for effective learning"""


def main():
    """Main entry point for the MCP server."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("DarkLens MCP Server")
        print("Usage: python -m darklens_mcp_server.server")
        print("Or: darklens-server")
        return

    # Run the server with stdio transport
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()