import chromatography
import pandas as pd

### Chromatography_answer_a.py
# ---------- main ---------- #
if __name__ == '__main__':
    binary_file_path = 'pear/pear'
    csv_file_path = 'pear/pear.csv'
    original_file_path = 'pear/pear_original.csv'
    
    # Call the chromatography functions to parse and save as CSV
    chromatography.parse_pear_binary(binary_file_path, csv_file_path)
    
    # Compare the generated CSV with pear_original.csv
    df1 = pd.read_csv(csv_file_path)
    df2 = pd.read_csv(original_file_path)
    diff = df1.compare(df2)
    print("Differences between df1 and df2:")
    print(diff)
