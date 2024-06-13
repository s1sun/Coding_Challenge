## Merck_Coding_Challenge
My name is Sean Sun. Please check the answers below for the Merck_Coding_Challenge.
### 1. Answer for the first challenge (a) [optional]: please refer to PyPlate_answer_a.ipynb file
### 2. Answer for the first challenge (b) : please refer to PyPlate_answer_b.ipynb file
### 3. Answer for the second challenge (a) pear challenge (easy): time vs. intensity data:
(i) examine the raw data

I used the command "format-hex pear | more" from Wondows PowerShell and discovered
1. each value is 4 bytes
2. the head consists of 320 bytes
3. the footer consists 480 bytes
   
(ii) determine how the data are stored in binary form

Up reviewing the "pear_original.csv" file, each line contains a pair of values (time, intensity), each requiring 4 bytes. The header is 320 bytes, and the footer is 480 bytes.

(iii) write a Python program that converts the binary data into csv form (to parallel the provided csv)

To see the python script, please refer to "Chromatography_answer_a.py" and "chromatography.py" files.
### 4. Answer for the second challenge (b) scale challenge (intermediate): time vs. wavelength vs. absorbance data
(i) examine the raw data

I used the command "format-hex scale | more" in Wondows PowerShell and found the following
1. The binary data is divided into two sections: head and body.
2. The head section contains 512 bytes.
3. The body section contains 1160430 bytes, beginning with "HH". The "HH" bytes repeat 12345 times.
4. Parsing the head revealed 5 values: 20, 190, 400, 10, and 12345.
   * 20 represents the factor;
   * 190 represents the start of wavelengths;
   * 400 represents the end of wavelengths;
   * 10 represents the increment for next wavelength;
   * 12345 represents the data length
   
(ii) determine how the data are stored in binary form

Reviewing the corresponding "scare_original.csv", it contains 12345 lines. The head title lists wavelengths [190, 200, 210,...,400] each increasing by 10. This matches the observations from the head of binary data.

(iii) write a Python program that converts the binary data into csv form (to parallel the provided csv)

To see the python script, please refer to "Chromatography_answer_b.py" and "chromatography.py" files.
### 5. Answer for the second challenge (c) sixtysix (hard – optional, for bonus points): time vs. mass vs. intensity data
I am working on it
