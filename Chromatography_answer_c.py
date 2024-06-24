import chromatography
import pandas as pd

### Chromatography_answer_c.py
# ---------- main ---------- #
if __name__ == '__main__':
    binary_file_A = 'sixtysix/sixtysix.A'
    binary_file_B = 'sixtysix/sixtysix.B'
    csv_file_path = 'sixtysix/sixtysix.csv'
    original_file_path = 'sixtysix/original.csv'
    
    # Call the chromatography functions to parse and save as CSV
    parse_sixtysix_binary(binary_file_A, binary_file_B, csv_file_path)

    # Compare the generated CSV with sixtysix_original.csv
    df1 = pd.read_csv(csv_file_path)
    df2 = pd.read_csv(original_file_path)
    diff = df1.compare(df2)
    print("Differences between df1 and df2:")
    print(diff)
