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


def frequency_test(text: str)->float:
    """
    This function checks frequency of "1"
    :param text: Sequence of interest

    :return: P_value
    """
    su = 0
    n=len(text)
    for i in range(0, n):
        if text[i] == "1":
            su += 1
        if text[i] == "0":
            su -= 1
    su=abs(su)
    su/=math.sqrt(n)
    p_value = math.erfc(su/math.sqrt(2))

    return p_value


def consecutive_test(text: str)->float:
    """
        This function checks frequency of changes "1" to "0" and vise versa
        :param text: Sequence of interest
        :return: p_value
        """
    n = len(text)
    su = 0
    for i in range(0, n):
        if text[i] == "1":
            su += 1
    su = su/len(text)
    if not (abs(su-0.5)<2/math.sqrt(n)):
        return 0.0
    count=0
    for i in range(0, len(text)-1):
        if text[i]==text[i+1]:
            count+=1

    numerator = abs(count-2*n*su*(1-su))
    denominator = (2*math.sqrt(2*n)*su*(1-su))
    p_value=math.erfc(numerator/denominator)

    return p_value


def longest_sequence_test(text: str)->float:
    """

    This function checks frequency of blocks with different length of "1" string 
        :param text: Sequence of interest

        :return: p_value
    """
    n = len(text)
    v=[0, 0, 0, 0]
    for i in range(0, n, 8):
        max_count=0
        count = 0
        for j in range(0,8):
            if text[i+j] == "1":
                count += 1
                if count>max_count:
                    max_count=count
            else: count=0
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
        hi_sq+=math.pow((v[i] - 16 * PI_CONST[i]),2) / 16 * PI_CONST[i]
    p_value=mpmath.gammainc(1.5, hi_sq / 2)

    return p_value


def main():
    output_text=""
    for i in range(0,len(SEQUENCES)):
        print(f"P_values of {GENERATOR_NAMES[i]}:\n")
        text=file_reader(SEQUENCES[i])
        ft = frequency_test(text)
        ct = consecutive_test(text)
        lt = longest_sequence_test(text)
        print(f"{ft}\n{ct}\n{lt}\n")
        if (ft>=P
                and ct >=P
                and lt)>=P:
            print(f"\n{GENERATOR_NAMES[i]} generator is reliable\n")
            output_text+=(f"{GENERATOR_NAMES[i]} generator is "
                          f"reliable\nP1:{ft}\nP2:{ct}\nP3:{lt}\n")
        else:
            print(f"\n{GENERATOR_NAMES[i]} generator is not reliable\n")
            output_text+=(f"{GENERATOR_NAMES[i]} generator is "
                          f"not reliable\nP1:{ft}\nP2:{ct}\nP3:{lt}\n")
    file_writer("report.txt", output_text)


if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"Something went wrong: {e}")
