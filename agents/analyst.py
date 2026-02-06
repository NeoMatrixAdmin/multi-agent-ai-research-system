import json
from agno.agent import Agent
from core.llm import get_llm
from core.models import Claim


class AnalystAgent:
    def __init__(self):
        self.agent = Agent(
            model=get_llm(),
            instructions="""
You are a research analyst.

Given a list of sources, extract 5–8 factual claims.

Return STRICT JSON ONLY in this format:
[
  {
    "claim": "text",
    "source_ids": ["id1", "id2"],
    "confidence": 0.0
  }
]

No markdown. No explanations.
"""
        )

    def extract_claims(self, sources):
        source_map = {
            s.id: f"{s.title} ({s.url})"
            for s in sources
        }

        response = self.agent.run(
            f"SOURCES:\n{json.dumps(source_map, indent=2)}"
        )

        try:
            parsed = json.loads(response.content)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                "AnalystAgent returned invalid JSON"
            ) from e

        claims = []
        for item in parsed:
            claims.append(
                Claim(
                    text=item["claim"],
                    sources=item["source_ids"],
                    confidence=float(item["confidence"]),
                )
            )

        return claims
