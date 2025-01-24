

def main():
    ms = generate_magic_string(20)
    ones = count_ones(ms)
    print(ms)
    print("1221121221221121122")
    print(ms == "1221121221221121122")
    print(ones)
    pass

def generate_magic_string(n) -> str:
    string = "122"
    position = 2
    while len(string) < n:
        next_value = str(3 - int(string[-1:]))
        if string[position] == "1":
            string = string + next_value
            position += 1
        elif string[position] == "2":
            string = string + next_value + next_value
            position += 1
    return string[:n-1]
    
def count_ones(string):
    return string.count("1")
    
if __name__ == "__main__":
    main()
    input("Processing done. Press Enter to close...") 