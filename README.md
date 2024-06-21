## Merck_Coding_Challenge
My name is Sean Sun. Please check the answers below for the Merck_Coding_Challenge.
### 1. Answer for the first challenge (a) [optional]: please refer to PyPlate_answer_a.ipynb file
### 2. Answer for the first challenge (b) : please refer to PyPlate_answer_b.ipynb file
### 3. Answer for the second challenge (a) pear challenge (easy): time vs. intensity data:
(i) examine the raw data

I used the command "format-hex pear | more" from Wondows PowerShell and discovered that the binary data is divided into three sections: head, body and footer.
1. Each value is 4 bytes
2. The header consists of 320 bytes with the "H   " repeating throughout.
3. The body contains 10000 pairs values, with each pair occupying 4 bytes.
4. the footer consists of 480 bytes with the "H   " repeating throughout.

The detailed information for the raw data listed in the table below:
| Name                           | Bytes    | Byte order       | Format   | 
| ------------------------------ | -------- | ---------------- | -------- |
| header                         | 320      |                  |          |
| body (10000 segments)          | 80000    |                  |          |
| each segment (time, Intensity) | 8        |                  |          |
| time                           | 4        | (<)little-endian | I(4)     |
| intensity                      | 4        | (<)little-endian | I(4)     |
| footer                         | 480      |                  |          |

(ii) determine how the data are stored in binary form

Up reviewing the "pear_original.csv" file, each line contains a pair of values (time, intensity), each value requiring 4 bytes. The header is 320 bytes, and the footer is 480 bytes.

(iii) write a Python program that converts the binary data into csv form (to parallel the provided csv)

To see the python script, please refer to "Chromatography_answer_a.py" and "chromatography.py" files.
### 4. Answer for the second challenge (b) scale challenge (intermediate): time vs. wavelength vs. absorbance data
(i) examine the raw data

I used the command "format-hex scale | more" in Wondows PowerShell and found the following
1. The binary data is divided into two sections: header and body.
2. The header section contains 512 bytes.
3. The body section contains 1160430 bytes, beginning with "HH". The "HH" bytes repeat 12345 times.
4. Parsing the header revealed 5 values: 20, 190, 400, 10, and 12345.
   * 20 represents the factor.
   * 190 represents the start of wavelengths.
   * 400 represents the end of wavelengths.
   * 10 represents the increment for next wavelength.
   * 12345 represents the data length.
5. In body section, there are 12345 segments, each beginning with the bytes b'HH' and containing 94 bytes.

The detailed information for the raw data listed in the table below:
| Name                    | offset      | Byte order       | Format   | 
| ----------------------- | ----------- | ---------------- | -------- |
| factor                  | 128         | (>)big-endian    | h(2)     |
| start of wavelengths    | 256         | (>)big-endian    | h(2)     |
| end of wavelengths      | 258         | (>)big-endian    | h(2)     |
| increment               | 260         | (>)big-endian    | h(2)     |
| data length             | 384         | (>)big-endian    | h(2)     |
| start of body           | 512         | (>)big-endian    | h(2)     |
| mark in body data       |             | (>)big-endian    | cc(2)    |
| time in body data       |             | (<)little-endian | f(4)     |
| wavelength in body data |             | (>)big-endian    | i(4)     |

(ii) determine how the data are stored in binary form

Reviewing the corresponding "scare_original.csv", it contains 12345 lines. The header title lists wavelengths [190, 200, 210,...,400] each increasing by 10. This matches the observations from the header of binary data.

(iii) write a Python program that converts the binary data into csv form (to parallel the provided csv)

To see the python script, please refer to "Chromatography_answer_b.py" and "chromatography.py" files.
### 5. Answer for the second challenge (c) sixtysix (hard – optional, for bonus points): time vs. mass vs. intensity data
(i) examine the raw data

The binary file "sixtysix.A" contains 54,320 bytes, which is ten times the number of lines in the CSV file "sixtysix_original.csv". It is divided into 5,432 segments, each 10 bytes long, containing 3 values. The first and second values occupy 4 bytes each, and the third value occupies 2 bytes. The first value indicates the number of bytes preceding the row. The second value represents time and can be calculated by dividing it by 60,001 and rounding the result. Third value represents the number of non-zero values in the current row defined by the second time value.

The binary file "sixtysix.B" contains 352,236 bytes. Each segment is 6 bytes long, resulting in a total of 58,706 segments. Referencing "sixtysix_original.csv," each segment in "sixtysix.B" consists of a pair of values: <mass (2 bytes), intensity (4 bytes)>.

The detailed information for the A binary data listed in the table below:
| Name                             | Bytes       | Byte order        | Format   | 
| -------------------------------- | ----------- | ----------------- | -------- |
| A file(5432 segments)            | 54320       |                   |          |
| Each segment in A file           | 10          |                   |          |
|    1.  f_value (bytes preceding  | 4           | (>)big-endian     | I(4)     |
|    2.  s_value (Time)            | 4           | (>)big-endian     | I(4)     |
|    3.  t_value (No mass types)   | 2           | (>)big-endian     | H(2)     |

The detailed information for the B binary data listed in the table below:
| Name                             | Bytes       | Byte order        | Format   | 
| -------------------------------- | ----------- | ----------------- | -------- |
| B file(58706 segment)            | 352236      |                   |          |
| Each segment in B file           | 6           |                   |          |
|    1.  f_value (mass type)       | 2           | (<))little-endian | H(2)     |
|    2.  s_value (intensity)       | 4           | (<))little-endian | I(4)     |


(ii) determine how the data are stored in binary form

Reviewing the corresponding "sixtysix_original.csv," it contains 5,432 lines. The "Time (min)" information is derived from the A file, and the number of lines in csv file matches the number of segments in the binary A file. The "Intensity" information is sourced from the B file.

(iii) write a Python program that converts the binary data into csv form (to parallel the provided csv)

To see the python script, please refer to "Chromatography_answer_c.py" and "chromatography.py" files.
