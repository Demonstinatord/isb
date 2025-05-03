import random
def main():
    rand_arr=[]
    seq=""
    for i in range(0,128):
        rand_arr.append(random.randint(0,1))
    random.shuffle(rand_arr)
    for j in rand_arr:
        seq+=str(j)
    print(seq)
    file = open("sequence_python.txt", "w")
    file.write(seq)
    file.close()
if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"Something went wrong: {e}")