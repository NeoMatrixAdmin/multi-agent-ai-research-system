from agno.agent import Agent
from core.llm import get_llm

class WriterAgent:
    def __init__(self):
        self.agent = Agent(
            model=get_llm(),
            markdown=True,
            instructions="""
Write a professional investigative report.

Structure:
- Headline
- Executive Summary
- Key Findings
- Impact Analysis
- Future Outlook

Ground every section in verified claims.
"""
        )

    def write(self, state):
        claims_text = "\n".join(
            f"- {c.text} (confidence: {c.confidence})"
            for c in state.claims
        )

        response = self.agent.run(
            f"""
QUERY: {state.query}

VERIFIED CLAIMS:
{claims_text}
"""
        )

        return {
            "markdown": response.content,
            "claims": [c.__dict__ for c in state.claims],
        }
