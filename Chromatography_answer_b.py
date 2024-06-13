import chromatography

### Chromatography_answer_b.py
# ---------- main ---------- #
if __name__ == '__main__':
    binary_file_path = 'scale/scale'
    csv_file_path = 'scale/scale.csv'
    
    # Call the chromatography functions to parse and save as CSV
    chromatography.parse_scale_binary(binary_file_path, csv_file_path)