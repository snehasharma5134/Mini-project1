import io
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

styles = getSampleStyleSheet()

with open("bill_manifest.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total bill definitions in manifest: {len(rows)}")

for idx, row in enumerate(rows):
    # Clean keys
    clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
    filename = clean_row.get("filename")
    cat = clean_row.get("category", "Bill")
    btype = clean_row.get("bill_type", "Utility")
    provider = clean_row.get("provider", "Utility Provider")
    bdate = clean_row.get("bill_date", "2025-01-01")
    ddate = clean_row.get("due_date", "2025-01-20")

    filepath = f"data/raw_pdfs/bills/{filename}"
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []

    title_style = ParagraphStyle('BTitle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor('#065F46'), spaceAfter=8)
    story.append(Paragraph(f'{btype.upper()} UTILITY STATEMENT & BILL', title_style))
    story.append(Paragraph(f'<b>Service Provider:</b> {provider}<br/>Billing Division & Customer Accounts<br/>Contact Support: support@{provider.lower().replace(" ", "")}.com', styles['Normal']))
    story.append(Spacer(1, 10))

    meta = [
        [Paragraph(f'<b>Account Number:</b> ACC-UTL-{idx+1000}', styles['Normal']), Paragraph(f'<b>Bill ID:</b> {filename.replace(".pdf","").upper()}', styles['Normal'])],
        [Paragraph(f'<b>Service Type:</b> {btype}', styles['Normal']), Paragraph(f'<b>Bill Date:</b> {bdate}', styles['Normal'])],
        [Paragraph(f'<b>Due Date:</b> <font color="red"><b>{ddate}</b></font>', styles['Normal']), Paragraph('<b>Payment Terms:</b> Immediate Settlement', styles['Normal'])]
    ]
    meta_table = Table(meta, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')), ('PADDING', (0,0), (-1,-1), 5)]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    subtotal = (idx % 120 + 35) * 1.85
    tax = round(subtotal * 0.08, 2)
    total = round(subtotal + tax, 2)

    charge_rows = [
        ['Description / Service Cycle', 'Billing Units', 'Amount ($)'],
        [f'{btype} Monthly Service Allocation', f'{idx % 50 + 20} units', f'{subtotal:,.2f}'],
        ['Regulatory Infrastructure & Grid Fee', 'Fixed charge', '12.50'],
        ['State & Municipal Utility Tax (8%)', 'Tax', f'{tax:,.2f}'],
        ['TOTAL AMOUNT PAYABLE', f'Due by {ddate}', f'${total+12.50:,.2f}']
    ]
    t = Table(charge_rows, colWidths=[270, 150, 120])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#065F46')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#A7F3D0')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#D1FAE5')),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    story.append(Paragraph('<b>Notice:</b> Please settle payment on or before the due date to prevent disconnection.', styles['Italic']))
    doc.build(story)

print(f"Successfully generated all {len(rows)} real bill PDF documents!")
