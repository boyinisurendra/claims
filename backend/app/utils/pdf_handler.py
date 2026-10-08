import os
from pathlib import Path
from ..config import settings


class PDFHandler:
    def __init__(self):
        pass

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        return "Mock PDF text extracted"

    def extract_structured_data(self, text: str) -> dict:
        return {
            "claim_number": "CLM-2024-001",
            "patient_name": "John Doe",
            "provider_name": "City Hospital",
            "service_date": "2024-01-15",
            "claim_amount": 5000.0,
            "procedure_codes": ["99213"],
            "diagnosis_codes": ["Z00.00"],
            "insurance_plan": "Standard Plan",
        }

    def _extract_claim_number(self, text: str) -> str:
        return "CLM-2024-001"

    def _extract_patient_name(self, text: str) -> str:
        return "John Doe"

    def _extract_provider_name(self, text: str) -> str:
        return "City Hospital"

    def _extract_date(self, text: str, date_type: str) -> str:
        return "2024-01-15"

    def _extract_amount(self, text: str) -> float:
        return 5000.0

    def _extract_procedure_codes(self, text: str) -> list:
        return ["99213"]

    def _extract_diagnosis_codes(self, text: str) -> list:
        return ["Z00.00"]

    def _extract_insurance_plan(self, text: str) -> str:
        return "Standard Plan"


def save_upload(file, upload_dir: str = None) -> str:
    if upload_dir is None:
        upload_dir = settings.upload_dir

    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path
