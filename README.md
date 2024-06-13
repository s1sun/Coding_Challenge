## Merck_Coding_Challenge
My name is Sean Sun. Please check the answers below for the Merck_Coding_Challenge.
### 1. Answer for the first challenge (a) [optional]: please refer to PyPlate_answer_a.ipynb file
### 2. Answer for the first challenge (b) : please refer to PyPlate_answer_b.ipynb file
### 3. Answer for the second challenge (a) pear challenge (easy): time vs. intensity data:
(i) examine the raw data

I used the command "format-hex pear | more" from Wondows PowerShell and found 
1. each value has 4 bytes
2. the head contains 320 bytes
3. the tail contains 480 bytes
   
(ii) determine how the data are stored in binary form

Check the corresponding pear_original.csv, each line has one pair values (time, intensity) with 2X4 bytes. The head contains 320 bytes, and the tail contains 480 bytes.

(iii) write a Python program that converts the binary data into csv form (to parallel the provided csv)

For the python script, please refer to Chromatography_answer_a.py and chromatography.py files.
### 4. Answer for the second challenge (b) scale challenge (intermediate): time vs. wavelength vs. absorbance data
(i) examine the raw data

I used the command "format-hex scale | more" from Wondows PowerShell and found 
1. There are two sections, head and body.
2. The head contains 512 bytes.
3. The body contains 1160430 bytes with start bytes "HH" and the "HH" bytes repeat 12345 times.
4. tried to parse the head and found 5 values, they are 20, 190, 400, 10, and 12345
5. 20 represents the factor; 190 represents the start of wavelengths; 400 stands for the last wavelengths; 10 stands for increasing value for next wavelength; 12345 stands for data length
   
(ii) determine how the data are stored in binary form

Check the corresponding scare_original.csv, it contains 12345 lines and the head title contains a list [190, 200, 210,...,400] each item increasing 10. The finding is consistence with the observed above.

(iii) write a Python program that converts the binary data into csv form (to parallel the provided csv)

For the python script, please refer to Chromatography_answer_b.py and chromatography.py files.
### 5. Answer for the second challenge (c) [optional]: please refer to Chromatography_answer_c.py file
