from core.models import ResearchState, ResearchArtifact


class ResearchMemory:
    def __init__(self, query: str):
        self.state = ResearchState(query=query)

    def add_artifact(self, step: str, content: dict):
        self.state.artifacts.append(
            ResearchArtifact(step=step, content=content)
        )

    def add_plan(self, steps: list[str]):
        self.state.plan = steps

    def add_source(self, source):
        self.state.sources[source.id] = source

    def add_claim(self, claim):
        self.state.claims.append(claim)
