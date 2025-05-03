import math
import mpmath
import os
from pathlib import Path
from const import *


def file_reader(input_f:str)->str:
    """
            This function read some information from the file.
            :arguments: input_f(path to the file)
            :return: text
    """
    try:

        f = open(input_f, "r", encoding="utf-8")
        text = f.read()
        f.close()
        return text
    except: raise PermissionError("can't open file to read")


def file_writer(output: str,output_text: str):
    """
        This function writes some information into the file.
        :arguments: output(path to the file), output_text
    """
    try:
        f = open(f'{output}', "w", encoding="utf-8")
        f.write(output_text)
        f.close()

    except: raise PermissionError("can't open file to write")


def frequency_test(text: str, p: float)->bool:
    """
    This function checks frequency of "1"
    :param text: Sequence of interest
    :param p: Control value
    :return: True or false
    """
    su = 0
    n=len(text)
    for i in range(0, n):
        if text[i] == "1":
            su += 1
        else:
            su -= 1
    p_value = math.erfc(su/math.sqrt(2*n))
    print(p_value)
    return p_value >= p


def consecutive_test(text: str, p: float)->bool:
    """
        This function checks frequency of changes "1" to "0" and vise versa
        :param text: Sequence of interest
        :param p: Control value
        :return: True or false
        """
    n = len(text)
    su = 0
    for i in range(0, n):
        if text[i] == "1":
            su += 1
    su = su/len(text)
    if not (abs(su-0.5)<2/math.sqrt(n)):
        return False
    count=0
    for i in range(0, len(text)-1):
        if text[i]==text[i+1]:
            count+=1
    p_value=math.erfc(abs(count-2*n*su*(1-su))/(2*math.sqrt(2*n*su*(1-su))))
    print(p_value)
    return p_value >= p


def longest_sequence_test(text: str, p: float)->bool:
    """

    This function checks frequency of blocks with different length of "1" string 
        :param text: Sequence of interest
        :param p: Control value
        :return: True or false
    """
    n = len(text)
    v=[0, 0, 0, 0,]
    for i in range(0, n, 8):
        count = 0
        for j in range(0,8):
            if text[i+j] == "1":
                count += 1
        if count<=1:
            v[0]+=1
        if count==2:
            v[1]+=1
        if count==3:
            v[2]+=1
        if count>=4:
            v[3]+=1

    hi_sq = 0
    for i in range(0,4):
        hi_sq+=math.pow((v[i]-16*PI_CONST[i]),2)/16*PI_CONST[i]
    p_value=mpmath.gammainc(1.5,hi_sq/2)
    print(p_value)
    return p_value >= p


def main():
    output_text=""
    for i in range(0,len(SEQUENCES)):
        print(f"P_values of {GENERATOR_NAMES[i]}:\n")
        text=file_reader(SEQUENCES[i])
        if (frequency_test(text,P)
                and consecutive_test(text,P)
                and longest_sequence_test(text,P)):
            print(f"\n{GENERATOR_NAMES[i]} generator is reliable\n")
            output_text+=f"{GENERATOR_NAMES[i]} generator is reliable\n"
        else:
            print(f"\n{GENERATOR_NAMES[i]} generator is not reliable\n")
            output_text+=f"{GENERATOR_NAMES[i]} generator is not reliable\n"

    file_writer("report.txt", output_text)


if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"Something went wrong: {e}")