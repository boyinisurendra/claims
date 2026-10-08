from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta

# Test cases with different validation scenarios
test_claims = [
    # ✅ APPROVED - Valid amounts ($100-$5000), valid codes
    {
        "name": "01_APPROVED_Valid_Amount",
        "patient": "John Smith",
        "provider": "City Hospital",
        "amount": 3500,
        "procedure": "99213",
        "diagnosis": "Z00.00",
        "plan": "Standard Health Plan",
        "expected": "APPROVED ✅"
    },
    {
        "name": "02_APPROVED_Min_Amount",
        "patient": "Sarah Johnson",
        "provider": "Valley Clinic",
        "amount": 150,
        "procedure": "99211",
        "diagnosis": "R07.9",
        "plan": "Premium Health Plan",
        "expected": "APPROVED ✅"
    },
    {
        "name": "03_APPROVED_Max_Valid",
        "patient": "Michael Brown",
        "provider": "Downtown Clinic",
        "amount": 4900,
        "procedure": "99214",
        "diagnosis": "M79.3",
        "plan": "Basic Coverage",
        "expected": "APPROVED ✅"
    },

    # ⚠️ FLAGGED - High amounts ($5000+), valid codes
    {
        "name": "04_FLAGGED_High_Amount",
        "patient": "Emily Davis",
        "provider": "Harbor Hospital",
        "amount": 6500,
        "procedure": "99215",
        "diagnosis": "E11.9",
        "plan": "Plus Coverage",
        "expected": "FLAGGED ⚠️"
    },
    {
        "name": "05_FLAGGED_Flag_Threshold",
        "patient": "Robert Wilson",
        "provider": "Sunrise Medical",
        "amount": 5001,
        "procedure": "99213",
        "diagnosis": "Z12.11",
        "plan": "Standard Health Plan",
        "expected": "FLAGGED ⚠️"
    },

    # ❌ DENIED - Invalid amounts, valid codes
    {
        "name": "06_DENIED_Below_Min",
        "patient": "Grace Lee",
        "provider": "Mountain Health",
        "amount": 50,
        "procedure": "99212",
        "diagnosis": "I10",
        "plan": "Premium Health Plan",
        "expected": "DENIED ❌"
    },
    {
        "name": "07_DENIED_Above_Max",
        "patient": "Henry Taylor",
        "provider": "Riverside Hospital",
        "amount": 12500,
        "procedure": "99214",
        "diagnosis": "F41.1",
        "plan": "Basic Coverage",
        "expected": "DENIED ❌"
    },
    {
        "name": "08_DENIED_Way_Above_Max",
        "patient": "Iris Anderson",
        "provider": "Metro Health",
        "amount": 25000,
        "procedure": "99215",
        "diagnosis": "M25.5",
        "plan": "Plus Coverage",
        "expected": "DENIED ❌"
    },

    # ❌ FLAGGED - Invalid diagnosis/procedure codes
    {
        "name": "09_FLAGGED_Invalid_Diagnosis",
        "patient": "Jack Martinez",
        "provider": "Coastal Medical",
        "amount": 3000,
        "procedure": "99213",
        "diagnosis": "INVALID99",
        "plan": "Standard Health Plan",
        "expected": "FLAGGED ⚠️"
    },
    {
        "name": "10_FLAGGED_Invalid_Procedure",
        "patient": "Karen White",
        "provider": "Central Hospital",
        "amount": 2500,
        "procedure": "99999",
        "diagnosis": "Z00.00",
        "plan": "Premium Health Plan",
        "expected": "FLAGGED ⚠️"
    },
]

print("📋 Creating validation test PDFs...\n")

for i, claim in enumerate(test_claims, 1):
    pdf_name = f"Test_{claim['name']}.pdf"
    c = canvas.Canvas(pdf_name, pagesize=letter)

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "INSURANCE CLAIM FORM")

    # Divider line
    c.setLineWidth(2)
    c.line(50, 740, 550, 740)

    # Expected result box
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0.95, 0.95, 0.95)
    c.rect(50, 710, 500, 20, fill=1)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(60, 715, f"Expected Result: {claim['expected']}")

    # Claim details
    c.setFont("Helvetica-Bold", 11)
    y_pos = 685

    claim_number = f"CLM-TEST-{i:04d}"

    details = [
        f"Claim Number: {claim_number}",
        f"Patient Name: {claim['patient']}",
        f"Provider Name: {claim['provider']}",
        f"Service Date: {(datetime.now() - timedelta(days=5)).strftime('%m/%d/%Y')}",
        f"Claim Amount: ${claim['amount']:,.2f}",
        f"Procedure Code: {claim['procedure']}",
        f"Diagnosis Code: {claim['diagnosis']}",
        f"Insurance Plan: {claim['plan']}",
        f"Provider ID: PRV-{10000+i:05d}",
        f"Member ID: MEM-{100000+i:06d}",
    ]

    c.setFont("Helvetica", 11)
    for detail in details:
        c.drawString(50, y_pos, detail)
        y_pos -= 22

    # Footer with test purpose
    c.setFont("Helvetica", 9)
    c.drawString(50, 50, f"Test Case: {claim['name']} | Amount: ${claim['amount']} | Diagnosis: {claim['diagnosis']}")

    c.save()
    print(f"✅ {i:2d}. {pdf_name:45s} → {claim['expected']}")

print(f"\n🎉 All 10 test PDFs created!")
print(f"📊 Expected Results:")
print(f"   ✅ 3 should be APPROVED (amounts $150-$4,900)")
print(f"   ⚠️  2 should be FLAGGED (amounts $5,001+)")
print(f"   ❌ 3 should be DENIED (invalid amounts)")
print(f"   ⚠️  2 should be FLAGGED (invalid codes)")
print(f"\n📝 Now upload each PDF to test all validation scenarios!")
