import argparse
import os
import json
def freq_calculate(input_text: str)->dict:
    char_count = {}
    total_chars=len(input_text)
    for char in input_text:
        if indent_check(char):
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


def indent_check(symbol):
    return symbol!="\n"


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
    parser.add_argument("-reference", "--reference_frequency",
                        type=str, help="Path to the JSON file with reference frequencies")
    parser.add_argument( "--keyword",
                        type=str, help="Keyword that will change the original text")
    parser.add_argument("--str_to_change",
                        type=str, help="String that will be changed in the original text")
    arguments = parser.parse_args()
    return arguments


def file_reader(input_f):
    f = open(input_f, "r", encoding="utf-8")
    text = f.read()
    f.close()
    return text
def file_writer(output,output_text):
    try:
        f = open(f'{output}', "w", encoding="utf-8")
        if type(output)=='dict':
            for char in output:
                f.write(char, ":", output[char])

        else:
            f.write(output_text)
        f.close()

    except: raise PermissionError("can't open file to write")


def text_changer(original_text, str_to_change, keyword ):


    changed_text = ""
    for i in range(0, len(original_text)):
        for j in range(len(str_to_change)):
            if str_to_change[j]==original_text[i]:
                changed_text += keyword[j]
                break
        else:
            changed_text += original_text[i]


    return changed_text

def delimiter_check(symbol):
    delimiters=["\n"]
    not_delimiter = True
    for j in delimiters:
        if (symbol == j):
            not_delimiter = False

    return not_delimiter


def main():
    args=get_args()
    input_f=args.input_file
    text=file_reader(input_f)
    print(args.keyword[0])
    changed_text=text_changer(text,args.str_to_change,args.keyword)
    changed_text=changed_text.upper()
    freq=freq_calculate(text)

    print(changed_text)

    file_writer(args.output_file, changed_text)

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"Something went wrong: {e}")
