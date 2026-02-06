from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime


@dataclass
class Source:
    id: str
    title: str
    url: str
    publisher: str
    published_date: str | None
    credibility_score: float
    tool: str


@dataclass
class Claim:
    text: str
    sources: List[str]
    confidence: float
    verified: bool = False


@dataclass
class ResearchArtifact:
    step: str
    content: Dict
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ResearchState:
    query: str
    plan: List[str] = field(default_factory=list)
    sources: Dict[str, Source] = field(default_factory=dict)
    claims: List[Claim] = field(default_factory=list)
    artifacts: List[ResearchArtifact] = field(default_factory=list)
