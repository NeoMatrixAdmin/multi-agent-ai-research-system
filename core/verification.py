def verify_claims(claims, min_confidence: float):
    verified = []
    rejected = []

    for claim in claims:
        if claim.confidence >= min_confidence and len(claim.sources) >= 2:
            claim.verified = True
            verified.append(claim)
        else:
            rejected.append(claim)

    return verified, rejected
