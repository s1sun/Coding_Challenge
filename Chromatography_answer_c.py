import chromatography
import pandas as pd
import struct
import sys
import gzip
import platform

def is_binary_C_gzip(binary_file_C):
    """
    Check if the provided binary file is in gzip format.

    Args:
        binary_file_C (str): Path to the binary file to check.

    Returns:
        bool: True if the file is a gzip file, False otherwise.
    """
    # load binary data from the file
    binary_data_C = b''
    with open(binary_file_C, 'rb') as fileC:
        binary_data_C = fileC.read()
    
    # Check the first two bytes for the gzip magic number
    if binary_data_C[:2] == b'\x1F\x8B':
        print('binary_file_C is a gzip file')
        # Decompress the gzip data
        decompressed_data = gzip.decompress(binary_data_C)
        print(decompressed_data)
        return True
    else:
        return False
    

def parse_sixtysix_binary(binary_file_A, binary_file_B):
    """
    Parse binary data files in the 'sixtysix' format.

    Args:
        binary_file_A (str): Path to the binary file A.
        binary_file_B (str): Path to the binary file B.

    Returns:
        tuple: A tuple containing the title (list) and decoded values (list of lists).
    """
    # load binary data from file A
    binary_data_A = b''
    with open(binary_file_A, 'rb') as fileA:
        binary_data_A = fileA.read()
    # Load binary data from file B
    binary_data_B = b''
    with open(binary_file_B, 'rb') as fileB:
        binary_data_B = fileB.read()
    
    massset = set()
    decoded_valuesA = []
    decoded_valuesB = []
    times = []
    
    # parse binary data in file A format
    # Each swegment contains 10 bytes with big-endianess: 3 values (4 bytes, 4 bypes, 2 bytes)
    for i in range(0, len(binary_data_A), 10):
        segs = struct.unpack_from('>IIH', binary_data_A, i)
        decoded_valuesA.append(segs)
        time = int(segs[1]/6 + 0.5)/10000
        #time = round(segs[1]/60000, 4)
        # keep 4 decimal
        pre, decimals = str(time).split('.')
        while len(decimals)<4:
            decimals += '0'
        str_time = pre + "." + decimals
        times.append(str_time)
    
    # parse binary data in file B
    # Each segment contains 6 bytes with little-endianess: 2 values ( 2 bytes, 4 bytes)
    for i in range(0, len(binary_data_B), 6):
        pair = struct.unpack_from('<HI', binary_data_B, i)
        decoded_valuesB.append(pair)
        if pair[0] not in massset:
            massset.add(pair[0])
    
    # Assemble a zero dataframe with index=times and columns=sorted(massset)
    df = pd.DataFrame(0, index=times, columns=sorted(massset))

    # fill in time, mass, intensity into cell of the dataframe
    for i in range(len(times)):
        for j in range(decoded_valuesA[i][2]):
            pair = decoded_valuesB[decoded_valuesA[i][0]//6 + j]
            df.loc[times[i], pair[0]] =  pair[1]
    
    # set index as first column of the dataframe and then reset index
    df = df.rename_axis('Time (min)').reset_index() 

    # convert dataframe to list of list     
    decoded_values = df.values.tolist()
    
    # Define the title header
    title = df.columns
    return title, decoded_values

### Chromatography_answer_c.py

# This script parses binary data files in the 'sixtysix' format, validates the parsing with sample data, 
# and generates test results on additional datasets.

# ---------- main ---------- #
if __name__ == '__main__':
    # 1. Validate the program with sample data
    binary_file_A = 'sixtysix/sample/sixtysix.A'
    binary_file_B = 'sixtysix/sample/sixtysix.B'
    binary_file_C = 'sixtysix/sample/sixtysix.C'
    original_file_path = 'sixtysix/sample/sixtysix.csv'
    csv_out_path = 'sixtysix/sample/sixtysix_out.csv'
    
    if not is_binary_C_gzip(binary_file_C):
        print("sixtysix.C is not the expected gzip file, must exit.")
        sys.exit(1)
        
    # Parse the binary file to get the decoded data and title
    title, decoded_values = parse_sixtysix_binary(binary_file_A, binary_file_B)
    
    # save the title and data to a csv file with right line_end
    line_end = '\n'
    if platform.system() == 'Windows':
        line_end = '\r\n'
    chromatography.write_to_csv(csv_out_path, title, decoded_values, line_end)
    
    # Compare the generated CSV with the sample/sixtysix.csv file
    df1 = pd.read_csv(csv_out_path)
    df2 = pd.read_csv(original_file_path)
    diff = df1.compare(df2)
    
    if not diff.empty and diff.shape[1]>2:
        print('Differences between df1 and df2:', diff)
        sys.exit(1)
    
    
    # 2. Generate test results on datasets for problems 1, 2, and 3
    binary_fpaths = ['sixtysix/problem1/sixtysix','sixtysix/problem2/sixtysix','sixtysix/problem3/sixtysix']
    # line_end = '\n'
    for binary_fpath in binary_fpaths:
        # Parse and save encoded binary data as a CSV file
        binary_fpath_A = binary_fpath + '.A'
        binary_fpath_B = binary_fpath + '.B'
        binary_fpath_C = binary_fpath + '.C'
        if not is_binary_C_gzip(binary_fpath_C):
            sys.exit(1)
        title, decoded_values = parse_sixtysix_binary(binary_fpath_A, binary_fpath_B)
        csv_opath = binary_fpath + '.csv'
        chromatography.write_to_csv(csv_opath, title, decoded_values, line_end)
    
    print('Parsing completed, the csv file has been saved to the same folder as the binary data.')
    sys.exit(0)
