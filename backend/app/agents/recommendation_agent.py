class RecommendationAgent:
    def __init__(self):
        pass

    def generate_recommendation(
        self,
        extracted_data: dict,
        validation_results: dict
    ) -> dict:
        """Generate approval/denial recommendation based on validation results."""

        is_valid = validation_results.get("is_valid", False)
        missing_fields = validation_results.get("missing_fields", [])
        policy_violations = validation_results.get("policy_violations", [])
        claim_amount = extracted_data.get("claim_amount", 0)

        # ==================== RULE 1: Missing Required Fields ====================
        if missing_fields:
            decision = "flagged"
            confidence = 0.70
            reason = f"Missing required fields: {', '.join(missing_fields)}. Cannot process without complete information."
            return self._format_response(decision, confidence, reason, missing_fields)

        # ==================== RULE 2: Policy Violations ====================
        if policy_violations:
            violation_summary = " | ".join(policy_violations[:3])  # Show first 3
            decision = "flagged"
            confidence = 0.75
            reason = f"Policy violations found: {violation_summary}. Manual review required."
            return self._format_response(decision, confidence, reason, missing_fields)

        # ==================== RULE 3: Claim Amount Too High (Auto-Deny) ====================
        if claim_amount > 10000:
            decision = "denied"
            confidence = 0.90
            reason = f"Claim amount ${claim_amount:,.2f} exceeds maximum coverage limit of $10,000. DENIED. Please resubmit with corrected amount or pre-authorization."
            return self._format_response(decision, confidence, reason, missing_fields)

        # ==================== RULE 4: Claim Amount Too Low (Auto-Deny) ====================
        if claim_amount < 100:
            decision = "denied"
            confidence = 0.85
            reason = f"Claim amount ${claim_amount:,.2f} is below minimum claim amount of $100. DENIED."
            return self._format_response(decision, confidence, reason, missing_fields)

        # ==================== RULE 5: High Amount (Flag for Review) ====================
        if claim_amount > 5000:
            decision = "flagged"
            confidence = 0.80
            reason = f"High claim amount (${claim_amount:,.2f}) exceeds review threshold of $5,000. Requires manual verification before approval."
            return self._format_response(decision, confidence, reason, missing_fields)

        # ==================== RULE 6: All Validations Passed ====================
        if is_valid:
            decision = "approved"
            confidence = 0.95
            reason = f"Claim for ${claim_amount:,.2f} is complete and valid. All validations passed. APPROVED for immediate processing."
            return self._format_response(decision, confidence, reason, missing_fields)

        # ==================== RULE 7: Fallback (Should Not Reach) ====================
        decision = "flagged"
        confidence = 0.70
        reason = "Claim requires manual review for final determination."
        return self._format_response(decision, confidence, reason, missing_fields)

    def _format_response(self, decision, confidence, reason, missing_fields):
        """Format the recommendation response."""
        return {
            "recommendation": decision,
            "confidence": confidence,
            "reason": reason,
            "required_fields_missing": missing_fields,
            "policy_violations": [],
            "recommended_action": f"Status: {decision.upper()} - {reason}"
        }
