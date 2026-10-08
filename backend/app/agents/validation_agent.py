class ValidationAgent:
    def __init__(self):
        # Define business rules
        self.min_claim_amount = 100
        self.max_claim_amount = 10000
        self.flag_amount = 5000  # Flag for review if exceeds this

        # Valid procedure codes
        self.valid_procedure_codes = ["99211", "99212", "99213", "99214", "99215"]

        # Valid diagnosis codes
        self.valid_diagnosis_codes = ["Z00.00", "R07.9", "Z12.11", "I10", "M79.3", "J45.901", "E11.9", "F41.1", "M25.5"]

        # Valid insurance plans
        self.valid_insurance_plans = ["Standard Health Plan", "Premium Health Plan", "Basic Coverage", "Plus Coverage"]

    def validate_claim(self, extracted_data: dict) -> dict:
        """Validate claim against insurance policies and business rules."""

        required_fields = [
            "claim_number", "patient_name", "provider_name",
            "service_date", "claim_amount", "diagnosis_codes"
        ]

        missing_fields = [
            field for field in required_fields
            if not extracted_data.get(field)
        ]

        is_valid = True
        policy_violations = []
        field_validation = {}

        # ==================== AMOUNT VALIDATION ====================
        claim_amount = extracted_data.get("claim_amount", 0)

        if claim_amount < self.min_claim_amount:
            is_valid = False
            policy_violations.append(f"Claim amount ${claim_amount} is below minimum of ${self.min_claim_amount}")
            field_validation["claim_amount"] = {"valid": False, "reason": "Below minimum"}
        elif claim_amount > self.max_claim_amount:
            is_valid = False
            policy_violations.append(f"Claim amount ${claim_amount} exceeds maximum of ${self.max_claim_amount}")
            field_validation["claim_amount"] = {"valid": False, "reason": "Exceeds maximum"}
        elif claim_amount > self.flag_amount:
            policy_violations.append(f"High claim amount ${claim_amount} - requires manual review")
            field_validation["claim_amount"] = {"valid": True, "reason": "High amount - needs review"}
        else:
            field_validation["claim_amount"] = {"valid": True, "reason": "Within acceptable range"}

        # ==================== DIAGNOSIS CODE VALIDATION ====================
        diagnosis_codes = extracted_data.get("diagnosis_codes", [])

        for code in diagnosis_codes:
            if code not in self.valid_diagnosis_codes:
                policy_violations.append(f"Diagnosis code '{code}' is not in approved list")
                is_valid = False

        if diagnosis_codes:
            field_validation["diagnosis_codes"] = {"valid": len([c for c in diagnosis_codes if c in self.valid_diagnosis_codes]) > 0}
        else:
            is_valid = False
            field_validation["diagnosis_codes"] = {"valid": False}

        # ==================== PROCEDURE CODE VALIDATION ====================
        procedure_codes = extracted_data.get("procedure_codes", [])

        for code in procedure_codes:
            if code not in self.valid_procedure_codes:
                policy_violations.append(f"Procedure code '{code}' is not approved")
                is_valid = False

        if procedure_codes:
            field_validation["procedure_codes"] = {"valid": len([c for c in procedure_codes if c in self.valid_procedure_codes]) > 0}
        else:
            is_valid = False
            field_validation["procedure_codes"] = {"valid": False}

        # ==================== INSURANCE PLAN VALIDATION ====================
        insurance_plan = extracted_data.get("insurance_plan", "")

        if insurance_plan and insurance_plan not in self.valid_insurance_plans:
            policy_violations.append(f"Insurance plan '{insurance_plan}' is not valid")
            is_valid = False
            field_validation["insurance_plan"] = {"valid": False}
        else:
            field_validation["insurance_plan"] = {"valid": True}

        # ==================== PROVIDER VALIDATION ====================
        provider_name = extracted_data.get("provider_name", "")

        if not provider_name:
            is_valid = False
            policy_violations.append("Provider name is required")
            field_validation["provider_name"] = {"valid": False}
        else:
            field_validation["provider_name"] = {"valid": True}

        # ==================== PATIENT VALIDATION ====================
        patient_name = extracted_data.get("patient_name", "")

        if not patient_name:
            is_valid = False
            policy_violations.append("Patient name is required")
            field_validation["patient_name"] = {"valid": False}
        else:
            field_validation["patient_name"] = {"valid": True}

        return {
            "is_valid": is_valid and len(missing_fields) == 0,
            "missing_fields": missing_fields,
            "field_validation": field_validation,
            "policy_violations": policy_violations,
            "notes": f"Found {len(policy_violations)} validation issue(s)" if policy_violations else "All validations passed"
        }
