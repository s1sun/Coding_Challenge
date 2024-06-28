## Merck_Coding_Challenge
- Author: Shaojun Sun
- Resume: "resume_software.doc"
- Below are my solution for the Merck_Coding_Challenge
### 1. Designing High-Throughput Chemistry and Biology Experiments
PyPlate is a Python package for designing high-throughput chemistry and biology experiments. Suppose that you need to screen conditions for 12 cross-coupling reactions of the form:

A<sub>i</sub> + B<sub>i</sub> → C<sub>i</sub>

where A<sub>i</sub> and B<sub>i</sub> are starting materials, C<sub>i</sub> is a product, and i runs from 1…12.  For each reaction, let A<sub>i</sub> be the limiting reagent (0.1 mmol), add 1.1 equivalents of B<sub>i</sub>, 10 mol% Pd(OAc)<sub>2</sub>, and 15 mol% of ligand. 

#### (a): Screening a Common set of Conditions
>We aim to screen a common set of 2 **temperatures** (60 °C and 80 °C), 4 **solvents** (toluene, glyme, TBME, and dichloroethane), and 3 **ligands** (XPhos, SPhos, and dppf). 

**Solution for Requirement (a)**

The pyplate software package is a Python tool designed to facilitate the design and implementation of high-throughput chemistry and biology experiments. To display the results correctly. The following packages must be installed in your environment. 
   - python 3.10 or later
   - pyplate-hte 1.16.0 or later
   - Jupyter Notebook

For detailed information about how to screen **temperatures, solvents, ligands, and Ai_mw vs Bi_mw**, please refer to the "PyPlate_answer_a.ipynb" file.

#### (b): Explaining Modification to PyPlate
>The goal is to explain how to modify PyPlate to incorporate a feature like **tags** containing customer-specific additional requirements.

**Solution for Requirement (b)**

To accommodate additional information based on customer-specific requirements, I introduced the concept of tags. Tags will be a list containing customer-required additional information, such as Ai_mw, Bi_mw, etc.

For detailed information on adding **tags** into class **Substance**, please refer to the "PyPlate_answer_b.ipynb" file.

### 2. Parsing Chromatography Instrument Data
This document outlines the steps to parse three folders containing artificially generated and encoded chromatography data. Each folder represents a different challenge:
- The "Pear Challenge": time vs. intensity data.
- The "Scale Challenge": time vs. wavelength vs. absorbance data.
- The "Sixtysix Challenge": time vs. mass vs. intensity data.

#### (a) pear challenge (easy): time vs. intensity data
**Solution for Requirement (a)**

**(i) Examine the Raw Data**

To begin, I used the `format-hex pear | more` command in Windows PowerShell to inspect the binary data. The findings are as follows: 
1. The binary data is divided into three sections: header, body and footer.
2. The header consists of 320 bytes with the repeating pattern "H   " 4 bytes.
3. The body contains 80,000 bytes, consisting of pairs (time, intensity), with each pair occupying 2 X 4 bytes.
4. The footer consists of 480 bytes with the repeating pattern "H   " 4 bytes.

The detailed information for the raw data listed in the table below:
| Location | Length(bytes) | Endianess | Format   | Value                |
| -------- | ------------- | --------- | -------- | ---------------------|
| 0        | 320           |           |          | header               |                       
| 320      | 80,000        | little    | I(int)   | body                 |
| 320      | 4             | little    | I(int)   | &nbsp;&nbsp;&nbsp;&nbsp;time      |
| 324      | 4             | little    | I(int)   | &nbsp;&nbsp;&nbsp;&nbsp;intensity |
| 80,320   | 480           |           |          | footer               |

**(ii) Determine How the Data Are Stored in Binary Form**

Up reviewing the "pear.csv" file, I observed that each line contains a pair of values (time, intensity), each value requiring 4 bytes. The header and footer, each with repeating "H   ", are 320 and 480 bytes respectively.

**(iii) Write a Python program to Convert the Binary Data into csv Form**

To convert the binary data into a CSV format similar to **"pear.csv"**, I wrote the following Python script:
   1. **Read the Binary File**: Open the binary file in read mode.
   2. **Parse the Header**: Skip the first 320 bytes (header).
   3. **Extract Time and Intensity Values**: Read the next 80,000 bytes (body) as pairs of 2 X 4-byte values, interpreting them as little-endian integers.
   4. **Parse the Footer**: Skip the last 480 bytes (footer).
   5. **Save to CSV**: Write the extracted time and intensity values to a CSV file.
   6. **Compare the CSV to original "pear.csv"**: Verify the generated **"pear_out.csv"** with the original **"pear.csv"** and display the comparison results with no differences.

For the complete Python Script, please refer to **"Chromatography_answer_a.py"** file.

#### (b) scale challenge (intermediate): time vs. wavelength vs. absorbance data
**Solution for Requirement (b)**

**(i) Examine the Raw Data**

I used the "format-hex scale | more" command in Windows PowerShell and found the following:
1. The binary data is divided into two sections: header and body.
2. The header section contains 512 bytes, there are 5 components at specific locations:
   * Location 128: factor.
   * Location 256: start of wavelength in the list.
   * Location 258: end of wavelength in the list.
   * Location 260: increment in wavelength in the list.
   * Location 384: number of rows.
3. The body section contains the number of row specified in the header, with each row starting with "HH".
4. Each row in body section starts with the 2 bytes (b'HH'), followed by 4 bytes for time, and then 4 bytes for absorbances per wavelength.

The detailed information for the raw data listed in the table below:
| location | Length(bytes) | Endianess | Format   | Value                             |
| -------- | ------------- | --------- | -------- | --------------------------------- |
| 0        | 512           |           |          | header                            |
| 128      | 2             | big       | h(int)   | &nbsp;&nbsp;&nbsp;&nbsp;factor               |
| 256      | 2             | big       | h(int)   | &nbsp;&nbsp;&nbsp;&nbsp;wavelength_start     |
| 258      | 2             | big       | h(int)   | &nbsp;&nbsp;&nbsp;&nbsp;wavelength_end       |
| 260      | 2             | big       | h(int)   | &nbsp;&nbsp;&nbsp;&nbsp;wavelength_increment |
| 384      | 2             | big       | h(int)   | &nbsp;&nbsp;&nbsp;&nbsp;row_number           |
| 512      |               |           |          | body                              |
| 512      | 2             | big       | cc       | &nbsp;&nbsp;&nbsp;&nbsp;row_mark             |
| 514      | 4             | little    | f(float) | &nbsp;&nbsp;&nbsp;&nbsp;time                 |
| 518      | 4             | big       | xi(int)  | &nbsp;&nbsp;&nbsp;&nbsp;absorbances          |

Note: The number of wavelengths can be determined by (wavelength_end - wavelength_start)/wavelength_increment + 1

**(ii) Determine how the data are stored in binary form**

Reviewing the corresponding **"scare.csv"**, it contains 11,527 lines. The header title lists wavelengths ranging from 190 to 360, each increasing by 10. This matches the observations from the binary data header.

**(iii) write a Python program that converts the binary data into csv form**

To convert the binary data into a CSV format similar to **"scale.csv"**, I wrote a Python script.
   1. **Read the Binary File**: Open the binary file in read mode.
   2. **Parse the Header**: Read 5 components from the header section by location information. They are **Factor, wavelength_start, wavelength_end, wavelength_increment, and row_number**.
   3. **Extract Time and absorbances Values**: Read the body bytes started at 512 with each row starting with "HH" 2 big-endian characters, following by a 4 bytes little-endian float for time, and then the remaining multiple 4 bytes big-endian integers for absorbances.
   4. **Save to CSV**: Write the extracted time, wavelength, and absorbances data to a CSV file.
   5. **Compare the CSV to "scale.csv"**: Verify the generated **"scale_out.csv"** with the original **"scale.csv"** and display the comparison results with no differences.
      
For the complete Python Script, please refer to **"Chromatography_answer_b.py"** file.

#### (c) sixtysix (hard): time vs. mass vs. intensity data
**Solution for Requirement (c)**

**(i) Examine the raw data**

The binary file **"sixtysix.A"** contains 54,320 bytes, which is ten times the number of lines in the "sixtysix.csv" file. It is divided into 5,432 segments, each 10 bytes long, containing 3 values. 
1. The first value: 4 bytes representing the data location in **"sixtysix.B"**.
2. The second value: 4 bytes representing the time (calculated by dividing by 60,000 and rounding the result).
3. The Third value: 2 bytes representing the number of non-zero values in the current row defined by the second 'time' value.

The binary file **"sixtysix.B"** contains multiple mass and intensity segments, each 6 bytes. Each segment consists of: 
1. The first value: 2 bytes representing mass
2. The second value: 4 bytes representing intensity.

The **"fsixtysix.C"** contains the following: 
- The file starts with "1F 8B", indicating gzip compresseion.

Before dealing with two binary files **"sixtysix.A"** and **"sixtysix.B"**, the file **"sixtysix.C"** can be analyzed by decompressing it using the following python script:
```
import gzip

# load binary data from sixtysix_C file
binary_file_C = 'sixtysix/sixtysix.C'
binary_data_C = b''
with open(binary_file_C, 'rb') as fileC:
   binary_data_C = fileC.read()

# Check the first two bytes for the gzip magic number
if binary_data_C[:2] == b'\x1F\x8B':
   print('binary_file_C is a gzip file')
   # Decompress the gzip data
   decompressed_data = gzip.decompress(binary_data_C)
   print(decompressed_data)
else:
   print('binary_file_C is not a gzip file')
```
The python script outputs the result **"There Is Nothing Useful In This File"** repeating.

The detailed information for the "sixtysix.A" binary data is listed in the table below:
| location | Length(bytes) | Endianess | Format   | Value                          |
| -------- | ------------- | --------- | -------- | ------------------------------ |
| 0        | 4             | big       | I(int)   | location in B file             |
| 4        | 4             | big       | I(int)   | time                           |
| 8        | 2             | big       | H(int)   | number of mass at current time |

Each row occupies 10 bytes with 3 values mentioned above, The "sixtysix.A" file consists of multiple rows.

The detailed information for the "sixtysix.B" binary data listed in the table below:
| location | Length(bytes) | Endianess | Format   | Name      |
| -------- | ------------- | --------- | -------- | --------- |
| 0        | 2             | little    | H(int)   | mass      |
| 4        | 4             | little    | I(int)   | intensity |

Each row occupy 6 bytes with 2 values mentione above, The "sixtysix.B" consists of multiple rows.

**(ii) Determine how the data are stored in binary form**

Reviewing the corresponding original "sixtysix.csv," it contains 5,432 lines. The number of lines in the csv file matches the number of segments in the binary A file. The "Time (min)" information is derived from the second value of each segment in A file, and the corresponding pair values (mass and intensity) location mentioned in first value can be drived from B. The number of mass intensity at the same time mentioned in third value of each segment can be extracted from the B file at start location determined by the first value of the segment in the A file.

**(iii) write a Python program that converts the binary data into csv form (to parallel the provided csv)**

To convert the binary data into a CSV format similar to **"sixtysix_original.csv"**, I wrote a Python script. The script reads the binary file, processes the A and B files, and extracts the time, mass, and intensity values:
   1. **Read the Binary Files**: Open the sixtysix.A and sixtysix.B binary files in read mode.
   2. **Parse the sixtysix.A**: Read 10 bytes per segment, totaling 5432 segments from sixtysix.A binary file, extracting **location in B file, time, and number of pair (mass, intensity)**.
   3. **Parse the sixtysix.B**: Read 6 bytes per segment, totaling 50575 pairs from sixtysix.B binary file, extracting **mass, intensity**.
   4. **Assemble dataframe from parsed sixtysix.A and sixtysix.B**: Create a zero values dataframe with 5432(equal to number segments in A) rows and 49(equal to number of mass in B) columns, indexed by time, and populate with mass and intensity values extracted from "sixtysix.B".
   5. **Save to CSV**: Write the extracted time vs. mass vs. intensity data to a CSV file.
   6. **Compare the CSV to "sixtysix.csv"**: Verify the generated **"sixtysix_out.csv"** with the original **"sixtysit.csv"** and display the comparison results with no differences.(Note: there may be slight differences in the rounding of float values to specific decimal places across different platforms in python)

Note: Due to python round function precision limitation. The float value for time from different platforms exists a tiny diffence. It will be allowed.
      
For the complete Python Script, please refer to **"Chromatography_answer_c.py"** file.

All test results for encoding binary files are stored in their respective problem folders, alongside the binary data files.
