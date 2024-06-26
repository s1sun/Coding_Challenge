## Merck_Coding_Challenge
My name is Shaojun Sun. My resume has been loaded as "resume_software.doc". For the Merck_Coding_Challenge, please check my answers below:
### 1. Designing High-Throughput Chemistry and Biology Experiments
PyPlate is a Python package for designing high-throughput chemistry and biology experiments. Suppose that you need to screen conditions for 12 cross-coupling reactions of the form:

Ai + Bi → Ci

where Ai and Bi are starting materials, Ci is a product, and i runs from 1…12.  For each reaction, let Ai be the limiting reagent (0.1 mmol), add 1.1 equivalents of Bi, 10 mol% Pd(OAc)2, and 15 mol% of ligand. 

#### (a) [optional]: Screening a Common set of Conditions
>We aim to screen a common set of 2 **temperatures** (60 °C and 80 °C), 4 **solvents** (toluene, glyme, TBME, and dichloroethane), and 3 **ligands** (XPhos, SPhos, and dppf). 

**Solution for Requirement (a)**

The pyplate software package is a Python tool designed to facilitate the design and implementation of high-throughput chemistry and biology experiments. To display the results correctly. The following packages must be installed in your environment. 
   - python 3.10 or later
   - pyplate-hte 1.16.0 or later
   - Jupyter Notebook

For detailed information about how to screen **temperatures, solvents, ligands, and Ai_mw vs Bi_mw**, please refer to the "PyPlate_answer_a.ipynb" file.

#### (b): Explaining Modification to PyPlate
>The goal is to explain how to modify PyPlate to incorporate a feature like **tags** containing customer-additional requirements.

**Solution for Requirement (b)**

To accommodate additional information based on customer-specific requirements, I introduce the concept of tags. Tags will be a list containing customer-required additional information, such as Ai_mw, Bi_mw, etc.

For detailed information about how to add **tags** into class **Substance**, please refer to the "PyPlate_answer_b.ipynb" file.

### 2. Parsing Chromatography Instrument Date
This document outlines the steps to parse three folders containing artificially generated and encoded chromatography data. Each folder represents a different challenge. The focus here is on the "Pear Challenge": time vs. intensity data, the "Scale Challenge": time vs. wavelength vs. absorbance data, and the "Sixtysix Challenge": time vs. mass vs. intensity data.

#### (a) pear challenge (easy): time vs. intensity data
**Solution for Requirement (a)**

**(i) Examine the Raw Data**

To begin, I used the command `format-hex pear | more` from Windows PowerShell to inspect the binary data. I discovered the following: 
1. The binary data is divided into three sections: header, body and footer.
2. Each value occupies 4 bytes
3. The header consists of 320 bytes with the "H   " repeating throughout.
4. The body contains 10,000 pairs of values, with each pair occupying 2 X 4 bytes.
5. The footer consists of 480 bytes with the "H   " repeating throughout.

The detailed information for the raw data listed in the table below:
| Name                           | Bytes    | Byte order       | Format   | 
| ------------------------------ | -------- | ---------------- | -------- |
| header                         | 320      |                  |          |
| body (10000 pairs)             | 80000    |                  |          |
| &nbsp;&nbsp;&nbsp;each pair (time, Intensity) | 8        |                  |          |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;time      | 4        | (<)little-endian | I(4)     |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;intensity | 4        | (<)little-endian | I(4)     |
| footer                         | 480      |                  |          |

**(ii) Determine How the Data Are Stored in Binary Form**

Up reviewing the "pear_original.csv" file, I observed that each line contains a pair of values (time, intensity), with each value requiring 4 bytes. The header and footer, each with repeating "H   ", are 320 and 480 bytes respectively.

**(iii) Write a Python program to Convert the Binary Data into csv Form (to parallel the provided csv)**

To convert the binary data into a CSV format similar to **"pear_original.csv"**, I wrote the following Python script:
   1. **Read the Binary File**: Open the binary file in read mode.
   2. **Parse the Header**: Skip the first 320 bytes (header).
   3. **Extract Time and Intensity Values**: Read the next 80,000 bytes (body) as pairs of 2X4-byte values, interpreting them as little-endian integers.
   4. **Parse the Footer**: Skip the last 480 bytes (footer).
   5. **Save to CSV**: Write the extracted time and intensity values to a CSV file.
   6. **Compare the CSV to "pear_original.csv"**: Verify the generated **"pear.csv"** with the **"pear_original.csv"** and display the comparison results with no differences.

For the complete Python Script, please refer to **"Chromatography_answer_a.py"** and **"chromatography.py"** files.

#### (b) scale challenge (intermediate): time vs. wavelength vs. absorbance data
**Solution for Requirement (b)**

**(i) Examine the Raw Data**

I used the command "format-hex scale | more" in Windows PowerShell and found the following:
1. The binary data is divided into two sections: header and body.
2. The header section contains 512 bytes.
3. The body section contains 1,160,430 bytes, beginning with "HH". The "HH" bytes repeat 12,345 times.
4. Parsing the header revealed 5 values: 20, 190, 400, 10, and 12,345.
   * 20 represents the factor.
   * 190 represents the start value of wavelength in list.
   * 400 represents the end value of wavelength in list.
   * 10 represents the increment value in wavelength in the list.
   * 12,345 represents the number of rows.
5. In the body section, there are 12,345 segments, each beginning with the bytes b'HH' and containing 94 bytes.

The detailed information for the raw data listed in the table below:
| Name                              | offset      | Byte order       | Format   | 
| --------------------------------- | ----------- | ---------------- | -------- |
| factor                            | 128         | (>)big-endian    | h(2)     |
| start wavelength in list          | 256         | (>)big-endian    | h(2)     |
| end wavelength in list            | 258         | (>)big-endian    | h(2)     |
| increment                         | 260         | (>)big-endian    | h(2)     |
| number of rows                    | 384         | (>)big-endian    | h(2)     |
| body start (12345 rows)           | 512         | (>)big-endian    | h(2)     |
| &nbsp;&nbsp;&nbsp;each row mark in body          |             | (>)big-endian    | cc(2)    |
| &nbsp;&nbsp;&nbsp;time in body                   |             | (<)little-endian | f(4)     |
| &nbsp;&nbsp;&nbsp;absorbances in 22 wavelengths  |             | (>)big-endian    | 22i(22X4)|

**(ii) Determine how the data are stored in binary form**

Reviewing the corresponding **"scare_original.csv"**, it contains 12,345 lines. The header title lists wavelengths ranging from 190 to 400, each increasing by 10. This matches the observations from the header of binary data.

**(iii) write a Python program that converts the binary data into csv form (to parallel the provided csv)**

To convert the binary data into a CSV format similar to **"scale_original.csv"**, I wrote a Python script.
   1. **Read the Binary File**: Open the binary file in read mode.
   2. **Parse the Header**: Read 5 components from the header section. They are **Factor, start_value, end_value, increment, and row_number**.
   3. **Extract Time and absorbances Values**: Read the next (12345 X 94) bytes (body) with each row containing 94 bytes. Each row is composed of 2 big-endian characters, following by a little-endian float, and then 22 big-endian integers.
   4. **Save to CSV**: Write the extracted time vs. wavelength vs. absorbances data to a CSV file.
   5. **Compare the CSV to "scale_original.csv"**: Verify the generated **"scale.csv"** with the **"scale_original.csv"** and display the comparison results with no differences.
      
For the complete Python Script, please refer to **"Chromatography_answer_b.py"** and **"chromatography.py"** files.

#### (c) sixtysix (hard – optional, for bonus points): time vs. mass vs. intensity data
**Solution for Requirement (c)**

**(i) Examine the raw data**

The binary file **"sixtysix.A"** contains 54,320 bytes, which is ten times the number of lines in the CSV file "sixtysix_original.csv". It is divided into 5,432 segments, each 10 bytes long, containing 3 values. 
1. The first value: 4 bytes representing bytes preceding the row.
2. The second value: 4 bytes representing time and can be calculated by dividing it by 60,001 and rounding the result.
3. Third value: 2 bytes representing the number of non-zero values in the current row defined by the second value.

The binary file **"sixtysix.B"** contains 352,236 bytes divided into 58,706 segments of 6 bytes each. Referencing "sixtysix_original.csv," each segment in "sixtysix.B" consists of a pair of values: 
1. The first value: 2 bytes, representing mass
2. The second value: 4 bytes, representing intensity.

I used the command **"format-hex sixtysix.C"** in Windows PowerShell and found the following: 
- The file starts with "1F 8B", which is the magic number for gzip compressed files. This indicates that the data is compressed using gzip

Before dealing with binary files, the "sixtysix.C" will be first analyzed by decompressing it using the floowing python script:
```
import gzip

# load binary data from sixtysix_C file
binary_file_C = 'sixtysix/sixtysix.C'
binary_data_C = b''
with open(binary_file_C, 'rb') as fileC:
   binary_data_C = fileC.read()

# Decompress the gzip data
decompressed_data_C = gzip.decompress(binary_data_C)

# Print the decompressed data
print(decompressed_data_C)
```
The python script outputs the result **"There Is Nothing Useful In This File"** repeating.

The detailed information for the "sixtysix.A" binary data is listed in the table below:
| Name                             | Bytes       | Byte order        | Format   | 
| -------------------------------- | ----------- | ----------------- | -------- |
| A file(5432 segments)            | 54320       |                   |          |
| Each segment in A file           | 10          |                   |          |
| &nbsp;&nbsp;&nbsp;1.  f_value (bytes preceding) | 4           | (>)big-endian     | I(4)     |
| &nbsp;&nbsp;&nbsp;2.  s_value (Time)            | 4           | (>)big-endian     | I(4)     |
| &nbsp;&nbsp;&nbsp;3.  t_value (number of mass)  | 2           | (>)big-endian     | H(2)     |

The detailed information for the "sixtysix.B" binary data listed in the table below:
| Name                             | Bytes       | Byte order        | Format   | 
| -------------------------------- | ----------- | ----------------- | -------- |
| B file(58706 segments)           | 352236      |                   |          |
| Each segment in B file           | 6           |                   |          |
| &nbsp;&nbsp;&nbsp;1.  f_value (mass)            | 2           | (<))little-endian | H(2)     |
| &nbsp;&nbsp;&nbsp;2.  s_value (intensity)       | 4           | (<))little-endian | I(4)     |


**(ii) Determine how the data are stored in binary form**

Reviewing the corresponding "sixtysix_original.csv," it contains 5,432 lines. The "Time (min)" information is derived from the A file, and the number of lines in csv file matches the number of segments in the binary A file. The "Intensity" information with corresponding mass is sourced from the B file.

**(iii) write a Python program that converts the binary data into csv form (to parallel the provided csv)**

To convert the binary data into a CSV format similar to **"sixtysix_original.csv"**, I wrote a Python script. The script reads the binary file, processes the A and B files, and extracts the time, mass, and intensity values:
   1. **Read the Binary Files**: Open the sixtysix.A and sixtysix.B binary files in read mode.
   2. **Parse the sixtysix.A**: Read 10 bytes per segment with total 5432 segments from sixtysix.A binary file, extracting **bytes_proceding, time, and number_of_mass**.
   3. **Parse the sixtysix.B**: Read 6 bytes per segment with total 58706 pairs from sixtysix.B binary file, extracting **mass, intensity**.
   4. **Assemble dataframe from parsed sixtysix.A and sixtysix.B**: create a zero values dataframe with 5432(equal to number segments in A) rows and 48(equal to number of mass in B) columns, and index by time, and populate with mass and intensity values extracted from "sixtysix.B".
   5. **Save to CSV**: Write the extracted time vs. mass vs. intensity data to a CSV file.
   6. **Compare the CSV to "sixtysix_original.csv"**: Verify the generated **"sixtysix.csv"** with the **"sixtysit_original.csv"** and display the comparison results with no differences.
      
For the complete Python Script, please refer to **"Chromatography_answer_c.py"** and **"chromatography.py"** files.

