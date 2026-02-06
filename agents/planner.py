from agno.agent import Agent
from core.llm import get_llm


class PlannerAgent:
    def __init__(self):
        self.agent = Agent(
            model=get_llm(),
            instructions="""
You are a research planner.

Rules:
- Break the task into 4–6 concrete research steps
- EACH line must start with a dash (-)
- No paragraphs
- No explanations
- Output ONLY the bullet list

Example:
- Automation impact by sector
- Job creation in AI-related roles
- Wage polarization across regions
- Policy and reskilling responses
""",
            retries=3,
            delay_between_retries=2,
            exponential_backoff=True,
        )

    def create_plan(self, query: str) -> list[str]:
        original_query = query

        for attempt in range(3):
            response = self.agent.run(query)

            steps = [
                line.strip("- ").strip()
                for line in response.content.splitlines()
                if line.strip().startswith("-")
            ]

            if len(steps) >= 3:
                return steps

            # Re-prompt with explicit correction
            query = (
                "Your previous response did not follow the required format.\n\n"
                "Return ONLY a bullet list where every line starts with '-'.\n\n"
                f"Task: {original_query}"
            )

        raise RuntimeError("PlannerAgent failed to generate a valid research plan")
