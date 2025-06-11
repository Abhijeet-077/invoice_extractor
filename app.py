import streamlit as st
import tempfile
import os
from parser import extract_invoice_data
from excel import save_to_excel, save_to_csv

st.set_page_config(page_title="Invoice Extractor", layout="centered")
st.title("🧾 Invoice PDF to Excel/CSV Extractor")

uploaded_files = st.file_uploader(
    "Upload one or more Invoice PDF files", 
    type=["pdf"], 
    accept_multiple_files=True
)

if uploaded_files:
    all_data = []

    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        st.write(f"Processing: {uploaded_file.name}")
        meta_data = extract_invoice_data(tmp_path)
        all_data.append(meta_data)

        os.remove(tmp_path)

    with st.spinner("Saving to Excel and CSV..."):
        temp_dir = tempfile.gettempdir()

        # Save only metadata now
        excel_path = os.path.join(temp_dir, "invoice_data.xlsx")
        save_to_excel(all_data, [], excel_path)  # Pass empty list for line_items

        save_to_csv(all_data, [], temp_dir)
        summary_csv = os.path.join(temp_dir, "summary.csv")

    with open(excel_path, "rb") as f:
        st.download_button("📥 Download Excel File", f, "invoice_data.xlsx")

    with open(summary_csv, "rb") as f:
        st.download_button("📥 Download Summary CSV", f, "summary.csv", mime="text/csv")
