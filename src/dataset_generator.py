# Dataset Generator for Invoices, Bills, and Receipts
import os
import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

VENDOR_NAMES = [
    'TechCorp Solutions Inc.', 'Apex Logistics Global', 'Nexus Cloud Services',
    'Pioneer Manufacturing Ltd.', 'Summit Creative Agency', 'Vanguard Industrial Supply',
    'Horizon Media Partners', 'Starlight Software Systems'
]
CLIENT_NAMES = [
    'Acme Enterprises', 'Global Logistics Co.', 'Quantum Financial Group',
    'BlueWave Technologies', 'Metro Retail Systems', 'Evergreen Health Systems',
    'Beacon Media Labs'
]
ITEMS = [
    ('Cloud Hosting Subscription (Annual)', 1200.00),
    ('UI/UX Design Consultation', 850.00),
    ('Custom Software Module Development', 3400.00),
    ('Network Security Audit Services', 1500.00),
    ('Hardware Maintenance and Support', 620.00),
    ('Database Migration and Optimization', 1950.00),
    ('Quarterly Tech Retainer Fee', 2500.00),
    ('API Integration & Webhook Setup', 980.00)
]

UTILITY_PROVIDERS = [
    ('Pacific Gas & Electric Utility', 'Electricity'),
    ('City Municipal Water Authority', 'Water & Sewer'),
    ('Metro Broadband Fiber Telecom', 'High-Speed Internet'),
    ('National Mobile Cellular Network', 'Corporate Wireless Phone'),
    ('Continental Commercial Energy', 'Natural Gas Service')
]

RESTAURANTS_SHOPS = [
    'Blue Fin Seafood & Grill', 'The Daily Brew Coffee Roasters', 'Urban Bistro & Kitchen',
    'Cornerstone Supermarket & Deli', 'Summit Stationers & Supplies', 'Green Leaf Fresh Market',
    'Star Express Fuel & Convenience'
]
RETAIL_ITEMS = [
    ('Organic Fairtrade Espresso', 4.50),
    ('Avocado Artisan Toast', 12.00),
    ('A4 Printer Paper Pack (500 sheets)', 8.99),
    ('Wireless Optical Mouse', 24.50),
    ('Fresh Salad Bowl with Quinoa', 14.25),
    ('USB-C Fast Charging Cable', 18.00),
    ('Sparkling Mineral Water', 3.25),
    ('Gourmet Chicken Sandwich', 11.50)
]

styles = getSampleStyleSheet()

def generate_invoice(filepath, seed_val):
    random.seed(seed_val)
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    vendor = random.choice(VENDOR_NAMES)
    client = random.choice(CLIENT_NAMES)
    inv_num = f'INV-2026-{random.randint(10000, 99999)}'
    po_num = f'PO-{random.randint(4000, 8999)}'
    date = (datetime(2026, 1, 1) + timedelta(days=random.randint(0, 250))).strftime('%B %d, %Y')
    due_date = (datetime(2026, 1, 1) + timedelta(days=random.randint(251, 300))).strftime('%B %d, %Y')
    
    title_style = ParagraphStyle('InvTitle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#1E3A8A'), spaceAfter=8)
    story.append(Paragraph('TAX INVOICE', title_style))
    story.append(Paragraph(f'<b>Vendor / Issuer:</b> {vendor}<br/>100 Industrial Parkway, Suite {random.randint(100, 900)}<br/>Tax ID / VAT: US-{random.randint(10000000, 99999999)}', styles['Normal']))
    story.append(Spacer(1, 12))
    
    meta_data = [
        [Paragraph(f'<b>Invoice Number:</b> {inv_num}', styles['Normal']), Paragraph(f'<b>Invoice Date:</b> {date}', styles['Normal'])],
        [Paragraph(f'<b>PO Number:</b> {po_num}', styles['Normal']), Paragraph(f'<b>Payment Due Date:</b> {due_date}', styles['Normal'])],
        [Paragraph(f'<b>Bill To Client:</b> {client}', styles['Normal']), Paragraph('<b>Payment Terms:</b> Net 30 Days', styles['Normal'])]
    ]
    meta_table = Table(meta_data, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')), ('PADDING', (0,0), (-1,-1), 6)]))
    story.append(meta_table)
    story.append(Spacer(1, 16))
    
    chosen_items = random.sample(ITEMS, k=random.randint(2, 4))
    table_data = [['Description', 'Qty', 'Unit Price ($)', 'Amount ($)']]
    subtotal = 0.0
    for desc, price in chosen_items:
        qty = random.randint(1, 3)
        amt = qty * price
        subtotal += amt
        table_data.append([desc, str(qty), f'{price:,.2f}', f'{amt:,.2f}'])
    tax = subtotal * 0.0825
    total = subtotal + tax
    
    table_data.append(['', '', 'Subtotal:', f'{subtotal:,.2f}'])
    table_data.append(['', '', 'Sales Tax (8.25%):', f'{tax:,.2f}'])
    table_data.append(['', '', 'Total Balance Due:', f'{total:,.2f}'])
    
    t = Table(table_data, colWidths=[260, 50, 110, 120])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTNAME', (2, -3), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E2E8F0')),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    story.append(Paragraph('<b>Remittance Instructions:</b> Please wire payment to First National Bank, Routing: 021000089, Account: 4981729019.<br/>Thank you for your business!', styles['Italic']))
    doc.build(story)

def generate_bill(filepath, seed_val):
    random.seed(seed_val)
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    provider, service_type = random.choice(UTILITY_PROVIDERS)
    account_num = f'ACC-{random.randint(1000000, 9999999)}'
    bill_num = f'BILL-{random.randint(50000, 99999)}'
    meter_num = f'MTR-{random.randint(1000, 9999)}'
    cycle_start = (datetime(2026, 1, 1) + timedelta(days=random.randint(0, 180))).strftime('%m/%d/%Y')
    cycle_end = (datetime(2026, 1, 1) + timedelta(days=random.randint(181, 210))).strftime('%m/%d/%Y')
    due_date = (datetime(2026, 1, 1) + timedelta(days=random.randint(211, 230))).strftime('%m/%d/%Y')
    
    title_style = ParagraphStyle('BillTitle', parent=styles['Heading1'], fontSize=22, textColor=colors.HexColor('#065F46'), spaceAfter=8)
    story.append(Paragraph('UTILITY STATEMENT & BILL', title_style))
    story.append(Paragraph(f'<b>Service Provider:</b> {provider}<br/>Department of Customer Billing & Grid Operations<br/>Customer Care Hotline: 1-800-{random.randint(100,999)}-{random.randint(1000,9999)}', styles['Normal']))
    story.append(Spacer(1, 12))
    
    meta_data = [
        [Paragraph(f'<b>Account Number:</b> {account_num}', styles['Normal']), Paragraph(f'<b>Bill Statement ID:</b> {bill_num}', styles['Normal'])],
        [Paragraph(f'<b>Service Type:</b> {service_type}', styles['Normal']), Paragraph(f'<b>Meter Identifier:</b> {meter_num}', styles['Normal'])],
        [Paragraph(f'<b>Billing Cycle:</b> {cycle_start} to {cycle_end}', styles['Normal']), Paragraph(f'<b>Due Date:</b> <font color="red"><b>{due_date}</b></font>', styles['Normal'])]
    ]
    meta_table = Table(meta_data, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')), ('PADDING', (0,0), (-1,-1), 6)]))
    story.append(meta_table)
    story.append(Spacer(1, 16))
    
    prev_balance = round(random.uniform(0.0, 50.0), 2)
    units_used = random.randint(120, 850)
    rate_per_unit = round(random.uniform(0.12, 0.35), 4)
    energy_charge = round(units_used * rate_per_unit, 2)
    grid_fee = 18.50
    regulatory_tax = round((energy_charge + grid_fee) * 0.05, 2)
    total_due = prev_balance + energy_charge + grid_fee + regulatory_tax
    
    table_data = [
        ['Billing Breakdown Item', 'Consumption / Details', 'Charge ($)'],
        ['Previous Outstanding Balance', 'Payments applied prior to cutoff', f'{prev_balance:,.2f}'],
        [f'Current {service_type} Usage', f'{units_used} Units @ ${rate_per_unit}/unit', f'{energy_charge:,.2f}'],
        ['Standard Infrastructure & Grid Delivery Charge', 'Base Monthly Connection', f'{grid_fee:,.2f}'],
        ['Municipal & State Regulatory Surcharge', 'Statutory fee 5%', f'{regulatory_tax:,.2f}'],
        ['TOTAL AMOUNT DUE', f'Please pay by {due_date}', f'${total_due:,.2f}']
    ]
    
    t = Table(table_data, colWidths=[240, 200, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#065F46')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#A7F3D0')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#D1FAE5')),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    story.append(Paragraph('<b>Late Payment Notice:</b> A late charge penalty of 1.5% will apply if this bill is not settled by the due date. Auto-pay customers will be charged automatically.', styles['Normal']))
    doc.build(story)

def generate_receipt(filepath, seed_val):
    random.seed(seed_val)
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=36, bottomMargin=36)
    story = []
    
    store = random.choice(RESTAURANTS_SHOPS)
    term_id = f'POS-TERM-{random.randint(10, 99)}'
    cashier = random.choice(['Alex M.', 'Sarah K.', 'David T.', 'Maria R.', 'Chris W.'])
    receipt_no = f'REC#{random.randint(100000, 999999)}'
    time_str = f'{random.randint(8, 22):02d}:{random.randint(10, 59):02d}:{random.randint(10, 59):02d}'
    date_str = (datetime(2026, 1, 1) + timedelta(days=random.randint(0, 270))).strftime('%Y-%m-%d')
    
    title_style = ParagraphStyle('RecTitle', parent=styles['Heading2'], fontSize=18, alignment=1, textColor=colors.HexColor('#1F2937'))
    center_style = ParagraphStyle('RecCenter', parent=styles['Normal'], alignment=1, fontSize=10)
    
    story.append(Paragraph(f'<b>{store.upper()}</b>', title_style))
    story.append(Paragraph('420 Market Street, Downtown District<br/>Tel: (555) 019-2834', center_style))
    story.append(Paragraph('------------------------------------------------------------', center_style))
    story.append(Paragraph(f'<b>RECEIPT / TRANSACTION RECORD</b><br/>Receipt: {receipt_no} | Register: {term_id}<br/>Cashier: {cashier} | Date: {date_str} {time_str}', center_style))
    story.append(Paragraph('------------------------------------------------------------', center_style))
    story.append(Spacer(1, 10))
    
    chosen = random.sample(RETAIL_ITEMS, k=random.randint(2, 4))
    table_data = [['Item Description', 'Qty', 'Price ($)']]
    subtotal = 0.0
    for desc, p in chosen:
        qty = random.randint(1, 2)
        total_p = qty * p
        subtotal += total_p
        table_data.append([desc, str(qty), f'{total_p:,.2f}'])
    
    tax = round(subtotal * 0.08, 2)
    grand_total = subtotal + tax
    payment_method = random.choice(['VISA CARD ending 4491', 'MASTERCARD ending 8120', 'CASH TENDERED', 'APPLE PAY MOBILE'])
    
    table_data.append(['SUBTOTAL', '', f'{subtotal:,.2f}'])
    table_data.append(['TAX (8%)', '', f'{tax:,.2f}'])
    table_data.append(['TOTAL AMOUNT PAID', '', f'${grand_total:,.2f}'])
    table_data.append(['PAYMENT METHOD', '', payment_method])
    table_data.append(['AUTH CODE / APPROVAL', '', f'APPR-{random.randint(100000, 999999)}'])
    
    t = Table(table_data, colWidths=[260, 50, 140])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#4B5563')),
        ('LINEABOVE', (0, -3), (-1, -3), 1, colors.HexColor('#4B5563')),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))
    story.append(Paragraph('------------------------------------------------------------', center_style))
    story.append(Paragraph('CUSTOMER COPY - ALL SALES ARE FINAL WITHIN 14 DAYS<br/>THANK YOU FOR SHOPPING WITH US!', center_style))
    doc.build(story)

def run():
    print('Generating Training and Validation Documents...')
    for i in range(1, 26):
        generate_invoice(f'data/raw_pdfs/invoices/invoice_{i:02d}.pdf', seed_val=100 + i)
        generate_bill(f'data/raw_pdfs/bills/bill_{i:02d}.pdf', seed_val=200 + i)
        generate_receipt(f'data/raw_pdfs/receipts/receipt_{i:02d}.pdf', seed_val=300 + i)
    
    print('Generating Unseen Test Evaluation Documents...')
    for i in range(1, 6):
        generate_invoice(f'data/test_pdfs/test_invoice_{i:02d}.pdf', seed_val=700 + i)
        generate_bill(f'data/test_pdfs/test_bill_{i:02d}.pdf', seed_val=800 + i)
        generate_receipt(f'data/test_pdfs/test_receipt_{i:02d}.pdf', seed_val=900 + i)
    print('Successfully generated 75 training PDFs and 15 unseen test PDFs!')

if __name__ == '__main__':
    run()
