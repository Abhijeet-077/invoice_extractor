from parser import extract_invoice_data
from excel import save_to_excel
import os

INPUT_FOLDER = "sample_invoices"
OUTPUT_FILE = "output.xlsx"

def process_invoices():
    all_data = []
    all_line_items = []

    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".pdf"):
            file_path = os.path.join(INPUT_FOLDER, filename)
            print(f"Processing: {file_path}")
            meta_data, line_items = extract_invoice_data(file_path)
            all_data.append(meta_data)
            for item in line_items:
                item["Invoice Number"] = meta_data.get("Invoice Number")
                all_line_items.append(item)

    save_to_excel(all_data, all_line_items, OUTPUT_FILE)

if __name__ == "__main__":
    process_invoices()
