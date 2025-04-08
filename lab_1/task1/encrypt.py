
def delimiter_check(symbol):
    delimiters=[",",".",":",";"," ","\n","-","+"]
    not_delimiter = True
    for j in delimiters:
        if (symbol == j):
            not_delimiter = False

    return not_delimiter

def main():
    f = open('original_text.txt',"r",encoding="utf-8")
    text = f.read()
    f.close()
    key = "ВОЛОГДББ"
    print(text)
    delimiters=[",",".",":",";"," ","\n","-","+"]
    count=0
    changed_text=""
    for i in range(0,len(text)):
        if(delimiter_check(text[i])):
            changed_text+=chr((ord(text[i])+ord(key[i % len(key)]))%32+1040)
        else:
            changed_text+=text[i]
    print(changed_text)
    f = open('changed_text.txt', "w", encoding="utf-8")
    f.write(changed_text)
    f.close()
if __name__=="__main__":
    main()