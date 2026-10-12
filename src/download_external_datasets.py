import os
import io
import shutil
import subprocess
import requests
import glob
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

os.makedirs("data/downloaded_sources", exist_ok=True)
os.makedirs("data/raw_pdfs/invoices", exist_ok=True)
os.makedirs("data/raw_pdfs/bills", exist_ok=True)
os.makedirs("data/raw_pdfs/receipts", exist_ok=True)

# 1. Clone invoice-agent (50 invoices)
inv_agent_dir = "data/downloaded_sources/invoice-agent"
if not os.path.exists(inv_agent_dir):
    print("Cloning invoice-agent...")
    subprocess.run(["git", "clone", "--depth", "1", "https://github.com/superintelligenceco/invoice-agent.git", inv_agent_dir], check=False)
else:
    print("invoice-agent already cloned.")

# Find and copy all PDFs from invoice-agent
inv_agent_pdfs = glob.glob(f"{inv_agent_dir}/**/*.pdf", recursive=True)
print(f"Found {len(inv_agent_pdfs)} PDFs in invoice-agent")
for i, pdf_path in enumerate(inv_agent_pdfs):
    dst = f"data/raw_pdfs/invoices/ext_inv_agent_{i+1:03d}_{os.path.basename(pdf_path)}"
    shutil.copy2(pdf_path, dst)

# 2. Clone invoice-sandbox-benchmark (110 PDFs)
sandbox_dir = "data/downloaded_sources/invoice-sandbox-benchmark"
if not os.path.exists(sandbox_dir):
    print("Cloning invoice-sandbox-benchmark...")
    subprocess.run(["git", "clone", "--depth", "1", "https://github.com/ciru-ai/invoice-sandbox-benchmark.git", sandbox_dir], check=False)
else:
    print("invoice-sandbox-benchmark already cloned.")

sandbox_pdfs = glob.glob(f"{sandbox_dir}/**/*.pdf", recursive=True)
print(f"Found {len(sandbox_pdfs)} PDFs in invoice-sandbox-benchmark")
for i, pdf_path in enumerate(sandbox_pdfs):
    dst = f"data/raw_pdfs/invoices/ext_sandbox_{i+1:03d}_{os.path.basename(pdf_path)}"
    shutil.copy2(pdf_path, dst)

# 3. Clone invoice2data (tests/compare 11 PDFs)
inv2data_dir = "data/downloaded_sources/invoice2data"
if not os.path.exists(inv2data_dir):
    print("Cloning invoice2data...")
    subprocess.run(["git", "clone", "--depth", "1", "https://github.com/invoice-x/invoice2data.git", inv2data_dir], check=False)
else:
    print("invoice2data already cloned.")

inv2data_pdfs = glob.glob(f"{inv2data_dir}/tests/compare/**/*.pdf", recursive=True) + glob.glob(f"{inv2data_dir}/tests/**/*.pdf", recursive=True)
# deduplicate paths
inv2data_pdfs = list(set(inv2data_pdfs))
print(f"Found {len(inv2data_pdfs)} PDFs in invoice2data")
for i, pdf_path in enumerate(inv2data_pdfs):
    dst = f"data/raw_pdfs/invoices/ext_inv2data_{i+1:03d}_{os.path.basename(pdf_path)}"
    shutil.copy2(pdf_path, dst)

# 4. Download SARTIENTERPRISES invoice
sarti_url = "https://raw.githubusercontent.com/ramprakashyadav/invoice/main/SARTIENTERPRISES_4203304675%20(1).pdf"
try:
    print("Downloading SARTIENTERPRISES invoice...")
    r = requests.get(sarti_url, timeout=15)
    if r.status_code == 200:
        with open("data/raw_pdfs/invoices/ext_sartienterprises.pdf", "wb") as f:
            f.write(r.content)
        print("SARTIENTERPRISES invoice downloaded successfully!")
    else:
        print(f"Failed to download SARTIENTERPRISES (Status: {r.status_code})")
except Exception as e:
    print(f"Error downloading SARTIENTERPRISES: {e}")

print("GitHub and external source downloads completed!")
