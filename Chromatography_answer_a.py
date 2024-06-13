import chromatography

### Chromatography_answer_a.py
# ---------- main ---------- #
if __name__ == '__main__':
    binary_file_path = 'pear/pear'
    csv_file_path = 'pear/pear.csv'
    
    # Call the chromatography functions to parse and save as CSV
    chromatography.parse_pear_binary(binary_file_path, csv_file_path)
