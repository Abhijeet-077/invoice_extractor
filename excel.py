import pandas as pd

def save_to_excel(meta_data_list, line_items_list, filename):
    writer = pd.ExcelWriter(filename, engine='openpyxl')

    df_summary = pd.DataFrame(meta_data_list)
    df_summary.to_excel(writer, index=False, sheet_name='Summary')

    df_items = pd.DataFrame(line_items_list)
    df_items.to_excel(writer, index=False, sheet_name='LineItems')

    writer.close()
    print(f"Saved extracted data to {filename}")

def save_to_csv(meta_data_list, line_items_list, output_folder):
    df_summary = pd.DataFrame(meta_data_list)
    df_items = pd.DataFrame(line_items_list)

    summary_path = f"{output_folder}/summary.csv"
    items_path = f"{output_folder}/line_items.csv"

    df_summary.to_csv(summary_path, index=False)
    df_items.to_csv(items_path, index=False)

    print(f"Saved summary to {summary_path}")
    print(f"Saved line items to {items_path}")
