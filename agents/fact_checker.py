from core.verification import verify_claims

class FactCheckerAgent:
    def __init__(self, min_confidence=0.75, min_claims=3):
        self.min_confidence = min_confidence
        self.min_claims = min_claims

    def verify(self, draft, state):
        claims = state.claims

        if len(claims) < self.min_claims:
            return {
                "status": "failed",
                "reason": "Insufficient verified claims",
                "claims_found": len(claims),
                "draft": draft,
            }

        verified = [
            c for c in claims
            if c.confidence >= self.min_confidence and len(c.sources) >= 2
        ]

        if len(verified) < self.min_claims:
            return {
                "status": "revision_required",
                "verified_claims": len(verified),
                "draft": draft,
            }

        return {
            "status": "approved",
            "draft": draft,
        }
