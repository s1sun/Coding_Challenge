import chromatography

### Chromatography_answer_c.py
# ---------- main ---------- #
if __name__ == '__main__':
    binary_file_A = 'sixtysix/sixtysix.A'
    binary_file_B = 'sixtysix/sixtysix.B'
    csv_file_path = 'sixtysix/sixtysix.csv'
    
    # Call the chromatography functions to parse and save as CSV
    parse_sixtysix_binary(binary_file_A, binary_file_B, csv_file_path)
