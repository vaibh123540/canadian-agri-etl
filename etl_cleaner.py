import pandas as pd
import csv
import re

# FILE CONFIGURATION
INPUT_FILE = '3210035901-eng.csv'  # The raw file from StatsCan
OUTPUT_FILE = 'cleaned_provincial_crops.csv' # The clean file for Tableau

def clean_data():
    print(f"Processing {INPUT_FILE}...")
    
    # 1. Read the raw text lines to handle the messy headers
    with open(INPUT_FILE, 'r') as f:
        lines = f.readlines()

    # The file structure is specific:
    # Row 9 (Index 8): Province Names (merged cells)
    # Row 11 (Index 10): Years (2020-2025 repeated)
    # Row 12+ (Index 11+): The actual data
    
    reader = csv.reader(lines)
    all_rows = list(reader)
    
    prov_row = all_rows[8]  # The row with "Quebec", "Ontario", etc.
    year_row = all_rows[10] # The row with "2020", "2021", etc.

    # 2. Map column indices to Province names
    # StatsCan puts the province name in the first column of the group, 
    # then leaves empty columns for the years belonging to that province.
    province_map = {} 
    current_province = None

    for i in range(1, len(prov_row)):
        val = prov_row[i].strip()
        if val:
            # Clean footnotes like "Ontario 10" -> "Ontario"
            clean_name = re.sub(r'\s\d+.*', '', val) 
            clean_name = re.sub(r'\(.*?\)', '', clean_name) # Remove (Terminated)
            current_province = clean_name.strip()
            province_map[i] = current_province

    # 3. Extract and Clean Data Rows
    clean_data = []
    
    # Iterate through data rows (starting at index 11)
    for row_idx in range(11, len(all_rows)):
        row = all_rows[row_idx]
        
        # Stop if we hit the footnotes at the bottom
        if not row or not row[0] or "Symbol legend" in row[0] or "Footnotes" in row[0]:
            break
            
        crop_name = row[0]
        # Remove footnote numbers from crop name
        crop_name = re.sub(r'\s\d+.*', '', crop_name).strip() 
        
        # For each province found in the header...
        for start_col, prov_name in province_map.items():
            # We assume 6 years of data (2020-2025) based on the file layout
            for i in range(6): 
                col_idx = start_col + i
                if col_idx >= len(row): break
                
                year = year_row[col_idx]
                val = row[col_idx]
                
                # CLEANING RULES:
                # 1. Remove commas (e.g. "1,000" -> "1000")
                # 2. Remove status letters (e.g. "100A" -> "100")
                # 3. Handle missing data ("..", "x", "F")
                
                val_clean = val.replace(',', '')
                val_clean = re.sub(r'[A-Za-z]', '', val_clean).strip()
                
                if val_clean in ['', '..', '...']:
                    continue # Skip empty data
                
                try:
                    num_val = float(val_clean)
                    clean_data.append({
                        'Province': prov_name,
                        'Crop': crop_name,
                        'Year': year,
                        'Production_MT': num_val
                    })
                except ValueError:
                    continue

    # 4. Save to CSV
    df = pd.DataFrame(clean_data)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Success! Cleaned data saved to {OUTPUT_FILE}")
    print(f"Total records: {len(df)}")

if __name__ == "__main__":
    clean_data()
