"""
Objective Ethics Framework (OEF) - Core Implementation
Based on Haley Harper's OEF Whitepaper

This is a starting structure for the main components.
Build incrementally, testing each component as you go.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EthicalTier(Enum):
    """The five ethical tiers from the OEF framework"""
    TIER_1_ROUTINE = 1      # Low stakes, minimal ambiguity
    TIER_2_STANDARD = 2     # Moderate stakes, clear trade-offs
    TIER_3_HIGH_STAKES = 3  # Irreversible impact, complex trade-offs
    TIER_4_AMBIGUOUS = 4    # Novel/uncertain, systemic consequences
    TIER_5_PROHIBITED = 5   # Violates core boundaries

class EthicalTenet(Enum):
    """Core ethical tenets from the framework"""
    NON_MALEFICENCE = "non_maleficence"      # Do no harm
    BENEFICENCE = "beneficence"              # Promote well-being
    JUSTICE = "justice"                      # Ensure fairness/equity
    INTELLECTUAL_HONESTY = "intellectual_honesty"  # Acknowledge uncertainty

class WellBeingDimension(Enum):
    """Four dimensions of well-being"""
    PHYSICAL_INTEGRITY = "physical_integrity"
    COGNITIVE_STABILITY = "cognitive_stability"  
    AUTONOMY = "autonomy"
    SYSTEMIC_HEALTH = "systemic_health"

@dataclass
class DecisionContext:
    """Context information for ethical evaluation"""
    decision_request: str
    stakeholders: List[str]
    urgency_level: int  # 1-10 scale
    reversibility_score: float  # 0-1, where 1 is fully reversible
    potential_harm_level: int  # 1-10 scale
    system_confidence: float  # 0-1 confidence in decision validity
    domain_specific_data: Dict[str, Any]
    timestamp: datetime

@dataclass
class EthicalEvaluation:
    """Results from ethical evaluation"""
    assigned_tier: EthicalTier
    justification: str
    confidence_score: float
    relevant_tenets: List[EthicalTenet]
    heuristics_triggered: List[str]
    metadata: Dict[str, Any]

class DecisionEvaluationProtocol:
    """
    DEP: Determines ethical significance and assigns tier
    """
    
    def __init__(self):
        self.heuristics = self._load_heuristics()
        self.tier_thresholds = self._initialize_thresholds()
    
    def _load_heuristics(self) -> Dict[str, callable]:
        """Load ethical heuristics for pattern matching"""
        return {
            "harm_reduction": self._harm_reduction_check,
            "reversibility_test": self._reversibility_check,
            "proportionality": self._proportionality_check,
            "consensus_needed": self._consensus_check,
        }
    
    def _initialize_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Initialize tier assignment thresholds"""
        return {
            "tier_2": {"harm_threshold": 3, "confidence_min": 0.8},
            "tier_3": {"harm_threshold": 6, "reversibility_min": 0.5},
            "tier_4": {"uncertainty_max": 0.4, "stakeholder_count": 10},
            "tier_5": {"prohibited_indicators": ["irreversible_severe_harm"]}
        }
    
    def evaluate_decision(self, context: DecisionContext) -> EthicalEvaluation:
        """Main evaluation method - assigns tier and routes decision"""
        
        # Step 1: Contextual scan
        logger.info(f"Evaluating decision: {context.decision_request[:50]}...")
        
        # Step 2: Heuristic pattern check
        triggered_heuristics = []
        for heuristic_name, heuristic_func in self.heuristics.items():
            if heuristic_func(context):
                triggered_heuristics.append(heuristic_name)
        
        # Step 3: Tier assignment
        assigned_tier = self._assign_tier(context, triggered_heuristics)
        
        # Step 4: Generate justification
        justification = self._generate_justification(context, assigned_tier, triggered_heuristics)
        
        # Step 5: Determine relevant tenets
        relevant_tenets = self._identify_relevant_tenets(context, triggered_heuristics)
        
        return EthicalEvaluation(
            assigned_tier=assigned_tier,
            justification=justification,
            confidence_score=context.system_confidence,
            relevant_tenets=relevant_tenets,
            heuristics_triggered=triggered_heuristics,
            metadata={
                "evaluation_timestamp": datetime.now(),
                "context_hash": hash(str(context)),
                "urgency": context.urgency_level
            }
        )
    
    def _assign_tier(self, context: DecisionContext, heuristics: List[str]) -> EthicalTier:
        """Assign ethical tier based on context and heuristics"""
        
        # Tier 5 check - prohibited actions
        if (context.potential_harm_level >= 9 and context.reversibility_score < 0.1):
            return EthicalTier.TIER_5_PROHIBITED
        
        # Tier 4 check - ambiguous/novel
        if (context.system_confidence < 0.4 or 
            len(context.stakeholders) > self.tier_thresholds["tier_4"]["stakeholder_count"]):
            return EthicalTier.TIER_4_AMBIGUOUS
        
        # Tier 3 check - high stakes/sensitive
        if (context.potential_harm_level >= self.tier_thresholds["tier_3"]["harm_threshold"] or
            context.reversibility_score < self.tier_thresholds["tier_3"]["reversibility_min"]):
            return EthicalTier.TIER_3_HIGH_STAKES
        
        # Tier 2 check - standard with ethical implications
        if (context.potential_harm_level >= self.tier_thresholds["tier_2"]["harm_threshold"] or
            len(heuristics) > 0):
            return EthicalTier.TIER_2_STANDARD
        
        # Default to Tier 1
        return EthicalTier.TIER_1_ROUTINE
    
    def _generate_justification(self, context: DecisionContext, tier: EthicalTier, heuristics: List[str]) -> str:
        """Generate human-readable justification for tier assignment"""
        base_reason = f"Assigned {tier.name} based on: "
        
        reasons = []
        if context.potential_harm_level > 5:
            reasons.append(f"high harm potential ({context.potential_harm_level}/10)")
        if context.reversibility_score < 0.5:
            reasons.append(f"low reversibility ({context.reversibility_score:.2f})")
        if context.system_confidence < 0.5:
            reasons.append(f"low confidence ({context.system_confidence:.2f})")
        if len(context.stakeholders) > 5:
            reasons.append(f"many stakeholders ({len(context.stakeholders)})")
        if heuristics:
            reasons.append(f"triggered heuristics: {', '.join(heuristics)}")
        
        return base_reason + "; ".join(reasons)
    
    def _identify_relevant_tenets(self, context: DecisionContext, heuristics: List[str]) -> List[EthicalTenet]:
        """Identify which ethical tenets are most relevant"""
        tenets = []
        
        if context.potential_harm_level > 0:
            tenets.append(EthicalTenet.NON_MALEFICENCE)
        
        if "consensus_needed" in heuristics:
            tenets.append(EthicalTenet.JUSTICE)
        
        if context.system_confidence < 0.7:
            tenets.append(EthicalTenet.INTELLECTUAL_HONESTY)
        
        # Default to beneficence if decision could help
        if len(tenets) == 0 or context.potential_harm_level < 3:
            tenets.append(EthicalTenet.BENEFICENCE)
            
        return tenets
    
    # Heuristic check methods
    def _harm_reduction_check(self, context: DecisionContext) -> bool:
        return context.potential_harm_level > 3
    
    def _reversibility_check(self, context: DecisionContext) -> bool:
        return context.reversibility_score < 0.7
    
    def _proportionality_check(self, context: DecisionContext) -> bool:
        # Simple proportionality check - more sophisticated logic needed
        return context.potential_harm_level > 5 and context.urgency_level < 3
    
    def _consensus_check(self, context: DecisionContext) -> bool:
        return len(context.stakeholders) > 3

class EthicalActionPathway:
    """
    EAP: Generates and selects ethically justified actions
    """
    
    def __init__(self):
        self.action_filters = self._initialize_filters()
    
    def _initialize_filters(self) -> Dict[str, callable]:
        """Initialize action filtering functions"""
        return {
            "harm_threshold": lambda action, context: action.get("harm_score", 0) <= 5,
            "reversibility_min": lambda action, context: action.get("reversibility", 1) >= 0.3,
            "confidence_check": lambda action, context: action.get("confidence", 0) >= 0.5
        }
    
    def process_decision(self, context: DecisionContext, evaluation: EthicalEvaluation) -> Dict[str, Any]:
        """Main EAP processing method"""
        
        if evaluation.assigned_tier == EthicalTier.TIER_1_ROUTINE:
            return {"action": "proceed_normally", "justification": "Routine decision, no ethical concerns"}
        
        if evaluation.assigned_tier == EthicalTier.TIER_5_PROHIBITED:
            return {"action": "block_decision", "justification": "Decision violates ethical boundaries"}
        
        # For tiers 2-4, generate and evaluate options
        options = self._generate_options(context, evaluation)
        filtered_options = self._apply_filters(options, context)
        selected_action = self._select_action(filtered_options, evaluation)
        
        return {
            "action": selected_action,
            "justification": self._justify_selection(selected_action, evaluation),
            "alternatives_considered": len(options),
            "options_after_filtering": len(filtered_options)
        }
    
    def _generate_options(self, context: DecisionContext, evaluation: EthicalEvaluation) -> List[Dict[str, Any]]:
        """Generate possible actions - placeholder for now"""
        # This would integrate with actual decision-making systems
        base_options = [
            {
                "id": "proceed",
                "description": "Proceed with original decision",
                "harm_score": context.potential_harm_level,
                "reversibility": context.reversibility_score,
                "confidence": context.system_confidence
            },
            {
                "id": "modified_proceed", 
                "description": "Proceed with safeguards",
                "harm_score": max(0, context.potential_harm_level - 2),
                "reversibility": min(1.0, context.reversibility_score + 0.2),
                "confidence": context.system_confidence
            },
            {
                "id": "defer",
                "description": "Defer decision for more information",
                "harm_score": 1,
                "reversibility": 1.0,
                "confidence": 0.9
            }
        ]
        
        return base_options
    
    def _apply_filters(self, options: List[Dict[str, Any]], context: DecisionContext) -> List[Dict[str, Any]]:
        """Filter options based on ethical criteria"""
        filtered = []
        for option in options:
            passes_all_filters = True
            for filter_name, filter_func in self.action_filters.items():
                if not filter_func(option, context):
                    passes_all_filters = False
                    break
            if passes_all_filters:
                filtered.append(option)
        return filtered
    
    def _select_action(self, options: List[Dict[str, Any]], evaluation: EthicalEvaluation) -> Dict[str, Any]:
        """Select best action from filtered options"""
        if not options:
            return {"id": "no_action", "description": "No ethically acceptable options found"}
        
        # Simple scoring - would be more sophisticated in practice
        best_option = None
        best_score = -1
        
        for option in options:
            score = (
                (10 - option.get("harm_score", 5)) * 0.4 +  # Lower harm is better
                option.get("reversibility", 0.5) * 0.3 +     # Higher reversibility is better  
                option.get("confidence", 0.5) * 0.3          # Higher confidence is better
            )
            
            if score > best_score:
                best_score = score
                best_option = option
        
        return best_option
    
    def _justify_selection(self, action: Dict[str, Any], evaluation: EthicalEvaluation) -> str:
        """Generate justification for selected action"""
        return f"Selected '{action['description']}' based on {evaluation.assigned_tier.name} evaluation. " \
               f"Balances harm minimization with practical feasibility."

class RecursiveAlignmentPathway:
    """
    RAP: Long-term monitoring and system refinement
    """
    
    def __init__(self):
        self.decision_log = []
        self.patterns = {}
        
    def log_decision(self, context: DecisionContext, evaluation: EthicalEvaluation, action: Dict[str, Any]):
        """Log decision for pattern analysis"""
        log_entry = {
            "timestamp": datetime.now(),
            "context": context,
            "evaluation": evaluation,
            "action": action,
            "outcome": None  # To be filled in later
        }
        self.decision_log.append(log_entry)
        logger.info(f"Logged decision {len(self.decision_log)}: {action.get('id', 'unknown')}")
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """Analyze logged decisions for patterns and drift"""
        if len(self.decision_log) < 5:
            return {"status": "insufficient_data", "entries": len(self.decision_log)}
        
        # Simple pattern analysis - would be more sophisticated
        tier_distribution = {}
        for entry in self.decision_log:
            tier = entry["evaluation"].assigned_tier.name
            tier_distribution[tier] = tier_distribution.get(tier, 0) + 1
        
        return {
            "total_decisions": len(self.decision_log),
            "tier_distribution": tier_distribution,
            "analysis_timestamp": datetime.now()
        }
    
    def recommend_adjustments(self) -> List[str]:
        """Generate recommendations for system improvement"""
        patterns = self.analyze_patterns()
        recommendations = []
        
        if patterns.get("total_decisions", 0) < 10:
            recommendations.append("Continue monitoring - more data needed for reliable patterns")
            return recommendations
        
        # Example recommendation logic
        tier_dist = patterns.get("tier_distribution", {})
        if tier_dist.get("TIER_4_AMBIGUOUS", 0) > len(self.decision_log) * 0.3:
            recommendations.append("High rate of Tier 4 decisions suggests need for better heuristics or training data")
        
        if tier_dist.get("TIER_5_PROHIBITED", 0) > 0:
            recommendations.append("Prohibited decisions detected - review input filtering and validation")
        
        return recommendations

class ObjectiveEthicsFramework:
    """
    Main OEF coordinator - orchestrates all components
    """
    
    def __init__(self):
        self.dep = DecisionEvaluationProtocol()
        self.eap = EthicalActionPathway() 
        self.rap = RecursiveAlignmentPathway()
        logger.info("OEF Framework initialized")
    
    def process_ethical_decision(self, decision_request: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry point for ethical decision processing"""
        
        # Create decision context
        context = DecisionContext(
            decision_request=decision_request,
            stakeholders=context_data.get("stakeholders", []),
            urgency_level=context_data.get("urgency_level", 5),
            reversibility_score=context_data.get("reversibility_score", 0.5),
            potential_harm_level=context_data.get("potential_harm_level", 3),
            system_confidence=context_data.get("system_confidence", 0.7),
            domain_specific_data=context_data.get("domain_data", {}),
            timestamp=datetime.now()
        )
        
        # Step 1: DEP evaluation
        evaluation = self.dep.evaluate_decision(context)
        logger.info(f"DEP assigned tier: {evaluation.assigned_tier.name}")
        
        # Step 2: EAP processing (for tiers 2-4)
        if evaluation.assigned_tier in [EthicalTier.TIER_2_STANDARD, 
                                      EthicalTier.TIER_3_HIGH_STAKES, 
                                      EthicalTier.TIER_4_AMBIGUOUS]:
            action_result = self.eap.process_decision(context, evaluation)
        else:
            # Tier 1 or 5 handled directly
            if evaluation.assigned_tier == EthicalTier.TIER_1_ROUTINE:
                action_result = {"action": "proceed", "justification": "Routine decision"}
            else:  # Tier 5
                action_result = {"action": "block", "justification": "Prohibited decision"}
        
        # Step 3: RAP logging
        self.rap.log_decision(context, evaluation, action_result)
        
        # Step 4: Determine routing based on tier
        routing_decision = self._determine_routing(evaluation.assigned_tier)
        
        return {
            "ethical_evaluation": {
                "tier": evaluation.assigned_tier.name,
                "justification": evaluation.justification,
                "confidence": evaluation.confidence_score,
                "tenets": [t.value for t in evaluation.relevant_tenets]
            },
            "recommended_action": action_result,
            "routing": routing_decision,
            "metadata": {
                "processing_timestamp": datetime.now(),
                "framework_version": "0.1.0"
            }
        }
    
    def _determine_routing(self, tier: EthicalTier) -> Dict[str, Any]:
        """Determine routing based on tier"""
        routing_map = {
            EthicalTier.TIER_1_ROUTINE: {"route": "direct_execution", "human_review": False},
            EthicalTier.TIER_2_STANDARD: {"route": "automatic_execution", "human_review": False},
            EthicalTier.TIER_3_HIGH_STAKES: {"route": "rap_monitoring", "human_review": False},
            EthicalTier.TIER_4_AMBIGUOUS: {"route": "human_review_required", "human_review": True},
            EthicalTier.TIER_5_PROHIBITED: {"route": "blocked_and_flagged", "human_review": True}
        }
        return routing_map.get(tier, {"route": "unknown", "human_review": True})
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and recommendations"""
        patterns = self.rap.analyze_patterns()
        recommendations = self.rap.recommend_adjustments()
        
        return {
            "framework_status": "operational",
            "decisions_processed": len(self.rap.decision_log),
            "pattern_analysis": patterns,
            "recommendations": recommendations,
            "last_updated": datetime.now()
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize the framework
    oef = ObjectiveEthicsFramework()
    
    # Example decision 1: Routine decision
    result1 = oef.process_ethical_decision(
        decision_request="Schedule a routine software update",
        context_data={
            "stakeholders": ["users", "IT_team"],
            "urgency_level": 3,
            "reversibility_score": 0.9,
            "potential_harm_level": 1,
            "system_confidence": 0.95
        }
    )
    
    print("Example 1 - Routine Decision:")
    print(json.dumps(result1, indent=2, default=str))
    print("\n" + "="*50 + "\n")
    
    # Example decision 2: High-stakes decision
    result2 = oef.process_ethical_decision(
        decision_request="Implement new AI hiring algorithm",
        context_data={
            "stakeholders": ["job_applicants", "HR_team", "company", "regulators"],
            "urgency_level": 4,
            "reversibility_score": 0.3,
            "potential_harm_level": 7,
            "system_confidence": 0.6
        }
    )
    
    print("Example 2 - High-Stakes Decision:")
    print(json.dumps(result2, indent=2, default=str))
    print("\n" + "="*50 + "\n")
    
    # Check system status
    status = oef.get_system_status()
    print("System Status:")
    print(json.dumps(status, indent=2, default=str))
