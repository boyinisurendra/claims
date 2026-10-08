from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

pdf_file = "sample_claim.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)

c.setFont("Helvetica-Bold", 16)
c.drawString(50, 750, "INSURANCE CLAIM FORM")

c.setFont("Helvetica", 12)
c.drawString(50, 700, "Claim Number: CLM-2024-005678")
c.drawString(50, 680, "Patient Name: Jane Smith")
c.drawString(50, 660, "Provider Name: County Hospital")
c.drawString(50, 640, "Service Date: 01/20/2024")
c.drawString(50, 620, "Claim Amount: $3,500.00")
c.drawString(50, 600, "Procedure Code: 99213")
c.drawString(50, 580, "Diagnosis Code: Z00.00")
c.drawString(50, 560, "Insurance Plan: Premium Health Plan")

c.save()
print(f"PDF created: {pdf_file}")
