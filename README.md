# DarkLens – Dark Pattern Detection MCP Server

A production-grade Model Context Protocol (MCP) server that enables AI agents to detect, classify, explain, and ethically redesign dark patterns in websites and UI flows.

## Overview

DarkLens analyzes UI elements, consent flows, pricing structures, and interaction friction to identify manipulative design patterns. It provides structured JSON outputs suitable for reasoning and compliance assessment.

## Features

- **Pattern Detection**: Rule-based + NLP heuristics for identifying 9+ dark pattern categories
- **Classification**: Categorizes patterns with cognitive bias analysis and severity levels
- **Ethical Explanations**: Plain-English explanations of manipulation tactics and harm potential
- **Compliance Assessment**: Risk scoring under GDPR, FTC, and DPDP regulations
- **Ethical Alternatives**: Suggests redesigned UI flows and copy

## Supported Dark Patterns

- Confirmshaming
- Forced Consent
- Roach Motel
- Hidden Costs
- Sneak Into Basket
- Fake Urgency
- Visual Manipulation
- Default Bias Exploitation
- Nagging / Repeated Interruptions
- **Social Proof Manipulation** (Enhanced with Kaggle dataset)

## Data Sources

The detection system is enhanced with real-world examples from the [Kaggle Dark Patterns Dataset](https://www.kaggle.com/datasets/dhamur/dark-patterns-user-interfaces), providing 2,000+ labeled examples of dark patterns across e-commerce and web interfaces.

## Installation

### Prerequisites

- Python 3.10 or higher
- `uv` package manager (recommended) or `pip`

### Install with uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone or navigate to the project directory
cd /path/to/DarkLens-MCP-Server

# Install dependencies
uv sync
```

### Install with pip

```bash
# Install dependencies
pip install -e .
```

## Project Structure

```
DarkLens-MCP-Server/
├── darklens_mcp_server/
│   └── server.py          # Main MCP server implementation
├── data/
│   └── dark_patterns.json # Pattern taxonomy database
├── demo/                  # Example usage scripts
├── pyproject.toml         # Project configuration
├── requirements.txt       # Alternative dependencies
├── README.md             # This file
└── uv.lock               # Lock file for uv
```

## Server Components

### Resources
- `dark_patterns://taxonomy`: Complete dark patterns taxonomy
- `ui_text://{url}`: Extracted UI text elements from webpages

### Tools
- `detect_dark_patterns`: Analyze HTML/text/URL for dark patterns
- `classify_pattern`: Get detailed classification of a pattern
- `explain_manipulation`: Explain psychological manipulation
- `risk_score`: Assess legal/compliance risk
- `suggest_ethical_alternative`: Get ethical redesign suggestions

### Prompts
- `audit_website`: Comprehensive website audit template
- `explain_ui_to_user`: UI explanation for non-technical users
- `compliance_report`: UX ethics compliance report template
- `rewrite_cta`: Ethical CTA rewrite template
- `assess_gdpr_risk`: GDPR risk assessment template

## Usage

### Running the MCP Server

```bash
# With uv
uv run darklens_mcp_server

# With Python
python -m darklens_mcp_server.server
```

The server communicates via stdio for MCP protocol.

### MCP Client Integration

Connect using any MCP-compatible client.

#### Example Tool Call

```json
{
  "method": "tools/call",
  "params": {
    "name": "detect_dark_patterns",
    "arguments": {
      "input_type": "url",
      "content": "https://example.com"
    }
  }
}
```

#### Example Response

```json
{
  "result": [
    {
      "pattern_id": "confirmshaming",
      "pattern_type": "Confirmshaming",
      "confidence": 0.9,
      "evidence": ["No thanks, I don't want to save money"]
    }
  ]
}
```

## API Reference

### detect_dark_patterns
**Input:**
- `input_type`: "html" | "text" | "url"
- `content`: String content to analyze

**Output:** Array of detected patterns with ID, type, confidence, and evidence.

### classify_pattern
**Input:** `pattern_id`: String
**Output:** Category, cognitive bias, severity level.

### explain_manipulation
**Input:** `pattern_id`: String, `user_type`: "child" | "elderly" | "average user"
**Output:** Plain explanation, psychological principle, harm potential.

### risk_score
**Input:** `pattern_id`: String, `region`: "EU" | "US" | "India"
**Output:** Risk score (0-100), violated regulations, enforcement likelihood.

### suggest_ethical_alternative
**Input:** `pattern_id`: String
**Output:** Rewritten UI copy, redesigned flow, ethical justification.

## Ethical Considerations

This tool is designed to promote ethical UX design and regulatory compliance. Use responsibly to:

- Audit websites for manipulative patterns
- Educate designers on ethical alternatives
- Ensure compliance with privacy and consumer protection laws
- Improve user trust and experience

**Disclaimer:** This tool provides analysis based on established dark pattern research but should not be considered legal advice. Always consult with legal experts for compliance matters.

## Contributing

Contributions welcome! Please ensure code follows the established patterns and includes appropriate tests.

## License

[MIT License](LICENSE)

### Resources

Resources provide read-only access to data. They are like GET endpoints in REST APIs.

#### Static Resources

```python
@mcp.resource("users://list")
def get_users_list() -> str:
    """Get a list of all users."""
    return json.dumps(SAMPLE_USERS, indent=2)
```

#### Dynamic Resources with Parameters

```python
@mcp.resource("users://{user_id}")
def get_user_by_id(user_id: str) -> str:
    """Get a specific user by ID."""
    # Implementation...
```

#### External API Resources

```python
@mcp.resource("api://external/{endpoint}")
async def get_external_api_data(endpoint: str) -> str:
    """Fetch data from an external API endpoint."""
    # Implementation...
```

### Tools

Tools are executable functions that can perform computations, API calls, or other actions. They may require user approval before execution.

#### Synchronous Tools

```python
@mcp.tool()
def calculate_sum(numbers: List[float]) -> float:
    """Calculate the sum of a list of numbers."""
    return sum(numbers)
```

#### Asynchronous Tools

```python
@mcp.tool()
async def fetch_user_posts(user_id: int) -> str:
    """Fetch posts for a specific user from external API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/posts?userId={user_id}")
        return json.dumps(response.json(), indent=2)
```

#### Tools with Complex Logic

```python
@mcp.tool()
def analyze_text(text: str) -> Dict[str, Any]:
    """Analyze text and return statistics."""
    words = text.split()
    return {
        "word_count": len(words),
        "character_count": len(text),
        # ... more analysis
    }
```

### Prompts

Prompts are reusable templates that help LLMs interact effectively with your server. They define expected inputs and interaction patterns.

#### Simple Prompts

```python
@mcp.prompt()
def summarize_content(content: str, max_length: int = 100) -> str:
    """Create a prompt to summarize content."""
    return f"Please summarize the following content in {max_length} words or less:\n\n{content}"
```

#### Complex Prompts

```python
@mcp.prompt()
def create_study_plan(subject: str, hours_per_week: int, weeks: int) -> str:
    """Create a study plan prompt."""
    return f"""Create a detailed study plan for learning {subject}.

Available time: {hours_per_week} hours per week
Duration: {weeks} weeks

Please include:
1. Weekly breakdown of topics
2. Daily study schedule
3. Recommended resources
4. Assessment milestones
5. Tips for effective learning"""
```

## Running the Server

### Using uv

```bash
uv run darklens-server
```

### Using Python directly

```bash
python -m darklens_mcp_server.server
```

### Using the script

```bash
darklens-server
```

The server will start and listen for MCP protocol messages over stdio.

## Testing the Server

### Using MCP Inspector

The easiest way to test your MCP server is using the MCP Inspector:

```bash
# Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

# Run the inspector with your server
mcp-inspector uv run darklens-server
```

This will open a web interface where you can interact with your server's resources, tools, and prompts.

### Manual Testing with Client

You can also create a simple test client:

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def test_server():
    async with stdio_client(
        StdioServerParameters(command="uv", args=["run", "darklens-server"])
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List resources
            resources = await session.list_resources()
            print("Available resources:", [r.uri for r in resources.resources])

            # List tools
            tools = await session.list_tools()
            print("Available tools:", [t.name for t in tools.tools])

            # List prompts
            prompts = await session.list_prompts()
            print("Available prompts:", [p.name for p in prompts.prompts])

            # Test a resource
            resource_content = await session.read_resource("users://list")
            print("Users resource content:", resource_content.contents[0].text)

            # Test a tool
            result = await session.call_tool("calculate_sum", {"numbers": [1, 2, 3, 4, 5]})
            print("Sum tool result:", result.content[0].text)

            # Test a prompt
            prompt_result = await session.get_prompt("summarize_content", {
                "content": "This is a sample text to summarize.",
                "max_length": 50
            })
            print("Prompt result:", prompt_result.messages[0].content)

asyncio.run(test_server())
```

## Integration with Claude Desktop

To use this server with Claude Desktop:

1. **Configure Claude Desktop**:
   - Open `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Add your server configuration:

```json
{
  "mcpServers": {
    "darklens": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/DarkLens-MCP-Server",
        "run",
        "darklens-server"
      ]
    }
  }
}
```

2. **Restart Claude Desktop**

3. **Test in Claude**:
   - Ask Claude to "list available resources" or "use the calculate_sum tool"
   - Try prompts like "create a study plan for learning Python with 10 hours per week for 8 weeks"

## Available Resources

- `users://list` - List all sample users
- `users://{user_id}` - Get specific user by ID
- `posts://list` - List all sample posts
- `api://external/{endpoint}` - Fetch data from JSONPlaceholder API

## Available Tools

- `calculate_sum` - Sum a list of numbers
- `find_max` - Find maximum value in a list
- `reverse_string` - Reverse a string
- `fetch_user_posts` - Fetch posts for a user from external API
- `analyze_text` - Analyze text statistics

## Available Prompts

- `summarize_content` - Create a summarization prompt
- `analyze_sentiment` - Create a sentiment analysis prompt
- `generate_code` - Create a code generation prompt
- `create_study_plan` - Create a study plan prompt

## Best Practices

### Resources
- Keep resource functions lightweight - avoid heavy computation
- Use appropriate MIME types for different content types
- Handle errors gracefully and return meaningful error messages
- Use URI templates for dynamic resources

### Tools
- Include clear docstrings with parameter descriptions
- Validate input parameters
- Handle errors appropriately
- Use async functions for I/O operations
- Keep tool names descriptive and consistent

### Prompts
- Make prompts flexible with optional parameters
- Include clear instructions for the LLM
- Structure prompts for consistent output
- Use descriptive names and descriptions

### General
- Use logging instead of print statements (MCP uses stdio for communication)
- Test your server thoroughly before deployment
- Handle edge cases and invalid inputs
- Follow Python type hints for better tooling support

## Troubleshooting

### Server won't start
- Check Python version (must be 3.10+)
- Verify all dependencies are installed
- Check for syntax errors in your code

### Tools/resources not appearing
- Ensure decorators are applied correctly (`@mcp.tool()`, not `@mcp.tool`)
- Check that functions have proper type hints
- Verify server initialization

### Claude Desktop integration issues
- Check the path to your server in the config file
- Ensure the server starts without errors
- Restart Claude Desktop after config changes
- Check Claude Desktop logs for errors

### Common Errors
- **"print() breaks MCP"**: Never use `print()` in production - it corrupts the JSON-RPC protocol
- **"Async function required"**: Use `async def` for functions that perform I/O
- **"Invalid URI"**: Ensure resource URIs follow proper format

## Next Steps

- Explore the [MCP documentation](https://modelcontextprotocol.io) for advanced features
- Check out the [Python SDK examples](https://github.com/modelcontextprotocol/python-sdk/tree/main/examples)
- Learn about [building MCP clients](https://modelcontextprotocol.io/docs/develop/build-client)
- Discover [other MCP servers](https://github.com/modelcontextprotocol/awesome-mcp-servers)

## License

This project is provided as an educational example. Feel free to modify and extend it for your own MCP server implementations.