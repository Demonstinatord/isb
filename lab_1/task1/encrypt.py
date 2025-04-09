import argparse
from const import *

def get_args() -> argparse.Namespace:
    """
    Reads arguments from terminal
    :return: Arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword",
                        type=str, help="Path to the keyword text that will change the original text")
    parser.add_argument("--input",
                            type=str, help="Path to the original text")
    parser.add_argument("--output",
                            type=str, help="Path to the decrypted text")
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


def delimiter_check(symbol: str, delimiters: list)->bool:
    """
        This function checks if the given character is a delimiter.
        :arguments: symbol
        :return: bool
    """

    not_delimiter = True
    for j in delimiters:
        if (symbol == j):
            not_delimiter = False
    return not_delimiter


def get_symbol_code(symbol: str, alphabet: str)->int:
    """
    This function return number of symbol in alphabet
    :param symbol:
    :param alphabet:
    :return number of symbol:
    """
    for i in range (0, len(alphabet)):
        if symbol==alphabet[i]:
            return (i)
    raise ValueError("symbol is not from that alphabet")

def text_encrypter(text: str, key: str, alphabet: str, delimiters: list)->str:
    """
        This function creates ciphertext using a modified Caesar cipher.
        :arguments: original text, key
        :return: ciphertext
    """
    changed_text = ""
    for i in range(len(text)):
        if (delimiter_check(text[i], delimiters)):
            changed_text += alphabet[(get_symbol_code(text[i],alphabet)+get_symbol_code(key[i%len(key)],alphabet))%len(alphabet)]
        else:
            changed_text += text[i]
    return(changed_text)


def main():
    args=get_args()
    key = file_reader(args.keyword)
    text=file_reader(args.input)
    print(text)
    changed_text=text_encrypter(text,key,ALPHABET,DELIMITERS)
    print(changed_text)
    file_writer(args.output, changed_text)


if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"Something went wrong: {e}")