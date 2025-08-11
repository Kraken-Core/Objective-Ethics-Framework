
from typing import Dict, Any

class ReversibilityHeuristic:
    domain = "harm"

    def evaluate(self, context: Dict[str, Any]) -> float:
        reversibility = context.get("reversibility", 0.5)
        return 1.0 - reversibility

class ProportionalityHeuristic:
    domain = "harm"

    def evaluate(self, context: Dict[str, Any]) -> float:
        expected_benefit = context.get("expected_benefit", 0.5)
        expected_harm = context.get("expected_harm", 0.5)
        if expected_benefit + expected_harm == 0:
            return 1.0
        return expected_harm / (expected_benefit + expected_harm)

class UncertaintyHeuristic:
    domain = "epistemic"

    def evaluate(self, context: Dict[str, Any]) -> float:
        certainty = context.get("evidence_certainty", 0.5)
        return 1.0 - certainty

class EvidenceAdequacyHeuristic:
    domain = "epistemic"

    def evaluate(self, context: Dict[str, Any]) -> float:
        evidence_quality = context.get("evidence_quality", 0.5)
        evidence_quantity = context.get("evidence_quantity", 0.5)
        return 1.0 - ((evidence_quality + evidence_quantity) / 2)

class VolitionalMisalignmentHeuristic:
    domain = "risk"

    def evaluate(self, context: Dict[str, Any]) -> float:
        alignment = context.get("volitional_alignment", 0.5)
        autonomy = context.get("stakeholder_autonomy", True)
        if not autonomy:
            return 0.8
        return 1.0 - alignment

    def educability_flag(self, context: Dict[str, Any]) -> bool:
        alignment = context.get("volitional_alignment", 0.5)
        autonomy = context.get("stakeholder_autonomy", True)
        return autonomy and alignment < 0.5

class ReproducibilityPressureHeuristic:
    domain = "meta-epistemic"

    def evaluate(self, context: Dict[str, Any]) -> float:
        urgency = context.get("urgency", 0.5)
        scenario_count = context.get("scenario_count", 10)
        success_rate = context.get("success_rate", 0.7)
        if urgency >= 0.8:
            return 0.1
        if scenario_count > 10 and success_rate < 0.5:
            return 0.9
        elif scenario_count > 5 and success_rate < 0.6:
            return 0.6
        elif success_rate >= 0.8:
            return 0.1
        return 0.4

class TransparencyReadinessHeuristic:
    domain = "accountability"

    def evaluate(self, context: Dict[str, Any]) -> float:
        ethical_tier = context.get("ethical_tier", 3)
        impact_scope = context.get("impact_scope", "individual")
        score = 0.0
        if ethical_tier >= 4:
            score += 0.4
        if impact_scope == "group":
            score += 0.3
        elif impact_scope == "systemic":
            score += 0.5
        return min(score, 1.0)

def calculate_svi(context: Dict[str, Any]) -> float:
    cognitive = context.get("cognitive_capacity", 0.5)
    legal = 1.0 if not context.get("legal_agency", True) else 0.0
    advocacy = 1.0 - context.get("self_advocacy_ability", 0.5)
    return round((1.0 - cognitive + legal + advocacy) / 3.0, 2)

def legal_compliance_filter(context: Dict[str, Any]) -> str:
    legal = context.get("legality", "unclear")
    return legal

class EthicalDecisionEngine:
    def __init__(self):
        self.heuristics = [
            ReversibilityHeuristic(),
            ProportionalityHeuristic(),
            UncertaintyHeuristic(),
            EvidenceAdequacyHeuristic(),
            VolitionalMisalignmentHeuristic(),
            ReproducibilityPressureHeuristic(),
            TransparencyReadinessHeuristic()
        ]

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        scores = {}
        total = 0
        for heuristic in self.heuristics:
            score = heuristic.evaluate(context)
            scores[heuristic.__class__.__name__] = round(score, 3)
            total += score

        normalized_pressure = round(total / len(self.heuristics), 3)
        recommendation = (
            "Proceed" if normalized_pressure <= 0.33 else
            "Proceed with caution" if normalized_pressure <= 0.66 else
            "Defer or escalate"
        )

        result = {
            "heuristic_scores": scores,
            "normalized_pressure": normalized_pressure,
            "recommendation": recommendation,
            "educate": VolitionalMisalignmentHeuristic().educability_flag(context),
            "svi": calculate_svi(context),
            "legal": legal_compliance_filter(context)
        }
        return result
