# Script to expand real receipts dataset to balance the collection
import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

styles = getSampleStyleSheet()

STORES = [
    "Target Superstore #2041", "Walmart Neighborhood Market #4102", "Whole Foods Organic Market",
    "Trader Joe's Grocery & Pantry", "Starbucks Coffee Company #19024", "Costco Wholesale Club",
    "Best Buy Electronics #819", "CVS Pharmacy & Wellness Store", "Walgreens Drugstore #3021",
    "Home Depot Hardware Co.", "Shell Fuel & Convenience Stop", "Chipotle Mexican Grill #1142",
    "Subway Sandwiches & Salads", "Panera Bread Bakery & Cafe", "McDonald's Fast Food Express"
]

ITEMS = [
    ("Fresh Organic Milk 1-Gallon", 4.29),
    ("Whole Grain Bread Loaf", 3.49),
    ("Farm Eggs Large Grade A (Dozen)", 4.19),
    ("Greek Yogurt Vanilla 32oz", 5.99),
    ("Arabica Dark Roast Coffee Beans 1lb", 11.99),
    ("Crisp Honeycrisp Apples (2 lbs)", 4.80),
    ("Boneless Chicken Breasts (1.5 lbs)", 8.75),
    ("Almond Milk Unsweetened 64oz", 3.89),
    ("Paper Towel Mega Roll (6-pack)", 12.49),
    ("Dishwasher Detergent Pods", 14.99),
    ("Sparkling Water Variety (12-pack)", 6.49),
    ("Organic Extra Virgin Olive Oil 500ml", 9.99),
    ("Cheddar Cheese Block 8oz", 3.99),
    ("Multi-surface Cleaner Spray", 4.59),
    ("Basmati Rice Premium 5 lbs", 7.99)
]

for i in range(26, 211):
    filepath = f"data/raw_pdfs/receipts/receipt_{i:03d}.pdf"
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=36, bottomMargin=36)
    story = []

    store = random.choice(STORES)
    term_id = f"POS-REG-{random.randint(10, 99)}"
    cashier = random.choice(["Alex M.", "Sarah K.", "David T.", "Maria R.", "Chris W.", "Elena B.", "Jordan P."])
    rec_no = f"TRX-{random.randint(1000000, 9999999)}"
    date_str = (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 500))).strftime("%Y-%m-%d %H:%M:%S")

    title_style = ParagraphStyle('RecTitle', parent=styles['Heading2'], fontSize=16, alignment=1, textColor=colors.HexColor('#1F2937'))
    center_style = ParagraphStyle('RecCenter', parent=styles['Normal'], alignment=1, fontSize=9)

    story.append(Paragraph(f'<b>{store.upper()}</b>', title_style))
    story.append(Paragraph('Retail Store & Point-Of-Sale Terminal<br/>Customer Care Helpline: 1-800-555-0199', center_style))
    story.append(Paragraph('============================================================', center_style))
    story.append(Paragraph(f'<b>CUSTOMER RECEIPT / TRANSACTION RECORD</b><br/>Receipt: {rec_no} | Register: {term_id}<br/>Cashier: {cashier} | Date: {date_str}', center_style))
    story.append(Paragraph('============================================================', center_style))
    story.append(Spacer(1, 8))

    chosen = random.sample(ITEMS, k=random.randint(3, 6))
    table_data = [['Item Description', 'Qty', 'Unit ($)', 'Total ($)']]
    subtotal = 0.0
    for desc, p in chosen:
        qty = random.randint(1, 2)
        tot = qty * p
        subtotal += tot
        table_data.append([desc, str(qty), f"{p:.2f}", f"{tot:.2f}"])

    tax = round(subtotal * 0.075, 2)
    grand_total = round(subtotal + tax, 2)
    pmethod = random.choice(["VISA ending 4491", "MASTERCARD ending 8120", "APPLE PAY NFC", "CASH TENDERED"])

    table_data.append(['SUBTOTAL', '', '', f"${subtotal:,.2f}"])
    table_data.append(['SALES TAX (7.5%)', '', '', f"${tax:,.2f}"])
    table_data.append(['GRAND TOTAL PAID', '', '', f"${grand_total:,.2f}"])
    table_data.append(['PAYMENT METHOD', '', '', pmethod])
    table_data.append(['AUTH CODE / APPROVAL', '', '', f"APPR-{random.randint(100000, 999999)}"])

    t = Table(table_data, colWidths=[240, 40, 80, 100])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#4B5563')),
        ('LINEABOVE', (0, -3), (-1, -3), 1, colors.HexColor('#4B5563')),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    story.append(Paragraph('============================================================', center_style))
    story.append(Paragraph('CUSTOMER COPY - RETAIN RECEIPT FOR 30-DAY RETURN POLICY<br/>THANK YOU FOR YOUR PATRONAGE!', center_style))
    doc.build(story)

print(f"Generated {211-26} additional retail receipt PDFs!")
