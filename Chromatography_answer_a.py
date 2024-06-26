import chromatography
import pandas as pd
import struct
import sys

def parse_pear_binary(binary_file_path):
    """
    Parses a binary file containing 'pear' format data.

    Args:
        binary_file_path (str): Path to the binary file.

    Returns:
        tuple: A tuple containing the title (list of strings) and the decoded values (list of lists).
    """
    # Load binary data
    binary_data = b''
    with open(binary_file_path, 'rb') as file:
        binary_data = file.read()
    
    # Define the number of bytes for head and tail
    num_heads = 320
    num_tails = 480
    
    # Parse pear values: each pear of values is 2X4 bytes long and stored in little-endian format
    decoded_values = []
    for i in range(num_heads, len(binary_data)-num_tails, 8):
        pair = struct.unpack_from('<II', binary_data, i)
        decoded_values.append([int(pair[0]), int(pair[1])])
    
    # Define the title header
    title = ['Time (ms)', 'Intensity']

    return title, decoded_values

### Chromatography_answer_a.py

# This script parses binary data files in the 'pear' format, validates the parsing with sample data, 
# and generates test results on additional datasets.

# ---------- main ---------- #
if __name__ == '__main__':
    # 1. Validate the program with sample data
    binary_file_path = 'pear/sample/pear'
    original_file_path = 'pear/sample/pear.csv'
    csv_out_path = 'pear/sample/pear_out.csv'
    
    # Parse the binary file to get the decoded data and title
    title, decoded_values = parse_pear_binary(binary_file_path)
    
    # save the title and data to a csv file
    line_end = '\r\n'
    chromatography.write_to_csv(csv_out_path, title, decoded_values, line_end)
    
    # Compare the generated CSV with the sample/pear.csv file
    df1 = pd.read_csv(csv_out_path)
    df2 = pd.read_csv(original_file_path)
    diff = df1.compare(df2)
    
    if not diff.empty:
        print('Differences between df1 and df2:', diff)
        sys.exit(1)
    
    
    # 2. Generate test results on datasets for problems 1, 2, and 3
    binary_fpaths = ['pear/problem1/pear','pear/problem2/pear','pear/problem3/pear']
    # line_end = '\n'
    for binary_fpath in binary_fpaths:
        # Parse and save each binary file as a CSV file
        title, decoded_values = parse_pear_binary(binary_fpath)
        csv_opath = binary_fpath + '.csv'
        chromatography.write_to_csv(csv_opath, title, decoded_values, line_end)
    
    print('Parsing completed, the csv file has been saved to the same folder as the binary data.')
    sys.exit(0)
