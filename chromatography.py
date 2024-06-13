import struct

def canconcate_items(row, delim):
    mystr = ""
    if len(row) > 0:
        mystr = str(row[0])
    for i in range(1, len(row)):
        mystr += delim + str(row[i])
    return mystr

def write_to_csv_WOCR(csv_file, title, data): # over different platforms
    with open(csv_file, 'w', newline='') as f:
        str_title = canconcate_items(title, ',')
        f.write(str_title)
        for row in data:
            str_line = canconcate_items(row, ',')
            f.write("\n" + str_line)

def parse_pear_binary(binary_file_path, csv_file_path):
    # load binary data
    binary_data = b''
    with open(binary_file_path, 'rb') as file:
        binary_data = file.read()
    
    decoded_values = []
    
    # analyze head and tail
    # num_values = len(binary_data) // 8
    num_heads = 320
    num_tails = 480
    
    # parse pear values format: each pear values is 2X4 bytes long and stored in little-endian format
    for i in range(num_heads, len(binary_data)-num_tails, 8):
        pair = struct.unpack_from('<II', binary_data, i)
        decoded_values.append([int(pair[0]), int(pair[1])])
    
    # write pear values into files
    title = ["Time (ms)", "Intensity"]
    write_to_csv_WOCR(csv_file_path, title, decoded_values)

    
def parse_scale_binary_head(f, nbytes, head_bytes):
    passed_bytes = 0
    read_bytes = f.read(nbytes)
    passed_bytes += nbytes
    heads = []
    if not read_bytes:
        exit(0)
    while passed_bytes < head_bytes:
        if read_bytes != b'\x00\x00':
            #print(read_bytes)
            head = struct.unpack('>h', read_bytes)[0]
            #print(head)
            heads.append(head)
        read_bytes = f.read(nbytes)
        passed_bytes += nbytes
    return heads, f

def parse_scale_binary(binary_file_path, csv_file_path):
    # Define the structure format for each data point
    # Assuming each time point is followed by absorbance values for multiple wavelengths
    # The exact format needs to be adjusted based on the actual binary encoding structure
    # Placeholder for reading the binary file and extracting data
    decoded_valus = []
    heads = []         
    with open(binary_file_path, 'rb') as f:
        nbytes = 2
        heads, f = parse_scale_binary_head(f, nbytes, 512)
        wavelengths = list(range(heads[1], heads[2]+1, heads[3]))
        HH_bytes = f.read(nbytes)
        nbytes = 4
        lines = 0
        while lines < heads[4] and HH_bytes == b'HH':
            # Read 4 bytes for time (double precision float)
            time_bytes = f.read(nbytes)
            time = struct.unpack('<f', time_bytes)[0]
            time = round(time, 4)
            # keep 4 decimal
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
            decoded_valus.append([time] + absorbances)
            lines += 1
            
            HH_bytes = f.read(2)
            if not HH_bytes or HH_bytes != b'HH':
                break
    
    # Write the decoded data to a CSV file
    title = ["Time (min)"] + wavelengths
    write_to_csv_WOCR(csv_file_path, title, decoded_valus)
