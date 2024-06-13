def parse_pear_binary(binary_file_path, csv_file_path):
    # load binary data
    binary_data = b''
    with open(binary_file_path, 'rb') as file:
        binary_data = file.read()
    
    decoded_values = []
    
    # analyze head and tail
    num_heads = 320
    num_tails = 480
    
    # parse pear values format: each pear values is 2X4 bytes long and stored in little-endian format
    for i in range(num_heads, len(binary_data)-num_tails, 8):
        pair = struct.unpack_from('<II', binary_data, i)
        decoded_values.append([int(pair[0]), int(pair[1])])
    
    # write pear values into files
    with open(csv_file_path, 'w', newline='\n') as fw:
        fw.write('Time (ms),Intensity')
        for pair in decoded_values:
            fw.write("\n%d,%d" % (pair[0], pair[1]))

# ---------- main ---------- #
if __name__ == '__main__':
    binary_file_path = 'pear/pear'
    csv_file_path = 'pear/pear.csv'
    parse_pear_binary(binary_file_path, csv_file_path)
