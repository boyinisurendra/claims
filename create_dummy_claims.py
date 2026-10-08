from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
import random

# Dummy claim data - Mix of approved, flagged, and denied claims
claims = [
    # APPROVED claims (normal amounts, standard codes)
    {"name": "Alice Johnson", "provider": "Central Hospital", "amount": 450, "code": "99213", "diag": "Z00.00", "expected": "APPROVED"},
    {"name": "Carol White", "provider": "Valley Clinic", "amount": 3200, "code": "99212", "diag": "R07.9", "expected": "APPROVED"},
    {"name": "Emma Davis", "provider": "County Medical", "amount": 2800, "code": "99211", "diag": "Z12.11", "expected": "APPROVED"},
    {"name": "Iris Taylor", "provider": "Mountain Health", "amount": 3900, "code": "99212", "diag": "M25.5", "expected": "APPROVED"},

    # FLAGGED claims (high amounts or special codes)
    {"name": "Bob Smith", "provider": "City Medical", "amount": 8750, "code": "99214", "diag": "M79.3", "expected": "FLAGGED"},
    {"name": "David Brown", "provider": "State Hospital", "amount": 12000, "code": "99215", "diag": "E11.9", "expected": "FLAGGED"},
    {"name": "Frank Miller", "provider": "Downtown Clinic", "amount": 7200, "code": "99213", "diag": "I10", "expected": "FLAGGED"},
    {"name": "Grace Lee", "provider": "Harbor Hospital", "amount": 4500, "code": "99214", "diag": "J45.901", "expected": "FLAGGED"},

    # DENIED claims (very high amounts)
    {"name": "Henry Wilson", "provider": "Sunrise Medical", "amount": 16500, "code": "99215", "diag": "F41.1", "expected": "DENIED"},
    {"name": "Jack Anderson", "provider": "Riverside Hospital", "amount": 18200, "code": "99214", "diag": "K21.9", "expected": "DENIED"},
]

print("📋 Creating 10 dummy insurance claim PDFs...\n")

for i, claim in enumerate(claims, 1):
    pdf_name = f"Claim_Sample_{i:02d}.pdf"
    c = canvas.Canvas(pdf_name, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "INSURANCE CLAIM FORM")
    
    # Divider line
    c.setLineWidth(2)
    c.line(50, 740, 550, 740)
    
    # Claim details
    c.setFont("Helvetica-Bold", 11)
    y_pos = 710
    
    details = [
        f"Claim Number: CLM-2024-{1000+i:04d}",
        f"Patient Name: {claim['name']}",
        f"Provider Name: {claim['provider']}",
        f"Service Date: {(datetime.now() - timedelta(days=random.randint(1,30))).strftime('%m/%d/%Y')}",
        f"Claim Amount: ${claim['amount']:,.2f}",
        f"Procedure Code: {claim['code']}",
        f"Diagnosis Code: {claim['diag']}",
        f"Insurance Plan: {'Premium' if claim['amount'] > 8000 else 'Standard'} Health Plan",
        f"Provider ID: PRV-{random.randint(10000, 99999)}",
        f"Member ID: MEM-{random.randint(100000, 999999)}",
    ]
    
    c.setFont("Helvetica", 11)
    for detail in details:
        c.drawString(50, y_pos, detail)
        y_pos -= 25
    
    # Description section
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y_pos - 10, "Service Description:")
    
    c.setFont("Helvetica", 10)
    descriptions = [
        "✓ Patient visit for medical evaluation and consultation",
        "✓ Comprehensive physical examination performed",
        "✓ Laboratory tests and diagnostics completed",
        "✓ Treatment plan documented and approved",
    ]
    
    y_pos -= 30
    for desc in descriptions:
        c.drawString(70, y_pos, desc)
        y_pos -= 18
    
    # Footer
    c.setFont("Helvetica", 9)
    c.drawString(50, 50, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Test Data Only")
    
    c.save()
    expected = claim.get('expected', 'UNKNOWN')
    emoji = "✅" if expected == "APPROVED" else "⚠️" if expected == "FLAGGED" else "❌"
    print(f"{emoji} {i:2d}. Created: {pdf_name:30s} | Patient: {claim['name']:15s} | Amount: ${claim['amount']:>7,.0f} | Expected: {expected}")

print(f"\n🎉 All 10 PDFs created successfully!")
print(f"📁 Location: C:\\Users\\294241\\Desktop\\claim_review_assistant\\")
print(f"\n📊 Expected Results:")
print(f"   ✅ 4 claims should be APPROVED (amounts < $10,000)")
print(f"   ⚠️  4 claims should be FLAGGED (amounts $8,750-$12,000)")
print(f"   ❌ 2 claims should be DENIED (amounts > $15,000)")
print(f"\n📝 Now you can:")
print(f"   1. Go to http://localhost:5173")
print(f"   2. Click 'Upload Claim'")
print(f"   3. Upload any of these PDFs")
print(f"   4. View different outcomes in Review Dashboard!")
print(f"   5. Use filters to see: Pending, Approved, Denied")
