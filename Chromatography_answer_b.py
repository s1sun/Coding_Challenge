import chromatography
import pandas as pd
import struct
import sys
import platform
    
def parse_scale_binary_head(f, nbytes, metalocs):
    """
    Parses the header of the binary file to extract metadata.

    Args:
        f (file object): File object for the binary file.
        nbytes (int): Number of bytes to read at a time.
        metalocs (list of int): List of positions in the file where header information is located.

    Returns:
        list: A list of header values extracted from the binary file.
    """
    heads = []
    for i in range(len(metalocs)):
        f.seek(metalocs[i])
        read_bytes = f.read(nbytes)
        if not read_bytes:
            exit(1)
        head = struct.unpack('>h', read_bytes)[0]
        heads.append(head)
    return heads

def parse_scale_binary(binary_file_path):
    """
    Parses a binary file containing 'scale' format data.

    Args:
        binary_file_path (str): Path to the binary file.

    Returns:
        tuple: A tuple containing the title (list of strings) and the decoded values (list of lists).
    """
    decoded_values = []
    heads = []         
    with open(binary_file_path, 'rb') as f:
        nbytes = 2
        metalocs = [128, 256, 258, 260, 384]
        heads = parse_scale_binary_head(f, nbytes, metalocs)
        wavelengths = list(range(heads[1], heads[2]+1, heads[3]))
        f.seek(512)
        HH_bytes = f.read(nbytes)
        nbytes = 4
        lines = 0
        while lines < heads[4] and HH_bytes == b'HH':
            # Read 4 bytes for time (float)
            time_bytes = f.read(nbytes)
            time = struct.unpack('<f', time_bytes)[0]
            
            time = int(10000*time + 0.5)/10000
            #time = round(time, 4)
            pre, decimals = str(time).split('.')
            while len(decimals)<4:
                decimals += '0'
            time = pre + "." + decimals
            
            
            # Read subsequent bytes for absorbance values
            absorbances = []
            for _ in range(len(wavelengths)):
                absorbance_bytes = f.read(nbytes)
                absorbance = struct.unpack('>i', absorbance_bytes)[0]//heads[0]
                absorbances.append(absorbance)
            decoded_values.append([time] + absorbances)
            lines += 1
            
            HH_bytes = f.read(2)
            if not HH_bytes or HH_bytes != b'HH':
                break
    
    # Define the title header
    title = ["Time (min)"] + wavelengths
    return title, decoded_values

### Chromatography_answer_b.py

# This script parses binary data files in the 'scale' format, validates the parsing with sample data, 
# and generates test results on additional datasets.

# ---------- main ---------- #
if __name__ == '__main__':
    # 1. Validate the program with sample data
    binary_file_path = 'scale/sample/scale'
    original_file_path = 'scale/sample/scale.csv'
    csv_out_path = 'scale/sample/scale_out.csv'
    
    # Parse the binary file to get the decoded data and title
    title, decoded_values = parse_scale_binary(binary_file_path)
    
    # save the title and data to a csv file
    line_end = '\n'
    if platform.system() == 'Windows':
        line_end = '\r\n'
    chromatography.write_to_csv(csv_out_path, title, decoded_values, line_end)
    
    # Compare the generated CSV with the sample/scale.csv file
    df1 = pd.read_csv(csv_out_path)
    df2 = pd.read_csv(original_file_path)
    diff = df1.compare(df2)
    
    if not diff.empty:
        print('Differences between df1 and df2:', diff)
        sys.exit(1)
    
    
    # 2. Generate test results on datasets for problems 1, 2, and 3
    binary_fpaths = ['scale/problem1/scale','scale/problem2/scale','scale/problem3/scale']
    # line_end = '\n'
    for binary_fpath in binary_fpaths:
        # Parse and save each binary file as a CSV file
        title, decoded_values = parse_scale_binary(binary_fpath)
        csv_opath = binary_fpath + '.csv'
        chromatography.write_to_csv(csv_opath, title, decoded_values, line_end)
    
    print('Parsing completed, the csv file has been saved to the same folder as the binary data.')
    sys.exit(0)
