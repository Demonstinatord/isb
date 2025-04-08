import argparse
import json
from const import *


def freq_calculate(input_text: str)->dict:
    char_count = {}
    total_chars=len(input_text)
    for char in input_text:
        if char!="\n":
            if char in char_count:
                char_count[char] += 1
            else:
                char_count[char] = 1
            char_count[char] = char_count.get(char, 0) + 1
    freq = {char: count / total_chars for char, count in char_count.items()}
    sorted_freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))
    for char in sorted_freq:
        print(char,":",sorted_freq[char])
    return sorted_freq





def get_args() -> argparse.Namespace:
    """
    Reads arguments from terminal
    :return: Arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-input", "--input_file",
                            type=str, help="Path to the encrypted text")
    parser.add_argument("-output", "--output_file",
                            type=str, help="Path to the decrypted text")
    parser.add_argument( "--keyword",
                        type=str, help="Keyword that will change the original text")
    parser.add_argument("--str_to_change",
                        type=str, help="String that will be changed in the original text")
    arguments = parser.parse_args()
    return arguments


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


def text_changer(original_text: str, symbols_to_change: str, keyword: str)->str:
    """
        This function creates a text using symbols from ciphertext or symbols from keyword string.
        :arguments: original text(original ciphertext), symbols_to_change(symbols needed to change), keyword(string of wildcards)
        :return: changed text
    """
    changed_text = ""
    for i in range(0, len(original_text)):
        for j in range(len(symbols_to_change)):
            if symbols_to_change[j]==original_text[i]:
                changed_text += keyword[j]
                break
        else:
            changed_text += original_text[i]
    return changed_text


def keyword_writer(wildcards: str, symbols_to_change: str, file:str)->None:
    """
    That function creates json version of substitution key
    :param wildcards:
    :param symbols_to_change:
    :param file:
    :return:
    """
    keyword = {wildcards[i]: symbols_to_change[i] for i in range(len(wildcards))}
    sorted_keyword = dict(sorted(keyword.items()))
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(sorted_keyword, f, ensure_ascii=False)

def main():
    args=get_args()
    input_f=args.input_file
    text=file_reader(input_f)
    changed_text=text_changer(text,args.str_to_change,args.keyword)
    changed_text=changed_text.upper()
    freq=freq_calculate(text)

    print(changed_text)
    temp_text=""
    for char in freq:
        temp_text += (char + " : " + f"{freq[char]:.4f}" + '\n')
    file_writer(args.output_file, changed_text)
    file_writer(Freq_analys,temp_text)
    keyword_writer(args.keyword,args.str_to_change,Keyword,)

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"Something went wrong: {e}")
