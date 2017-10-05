

file = open("output.txt")

file_input = open("input.csv")

file_output = open("first_clean.txt","w")




if __name__ == '__main__':
    input = []
    # input = ["47 Meters Dow"]
    while 1:
        line = file_input.readline()
        input.append(line[0:-1])
        if not line:
            break
        pass
    file_input.close()
    print(input)

    while 1:
        line = file.readline()
        if line.strip().split("`")[0] in input :
            print(line)
            file_output.write(line)
        if not line:
            break
        pass




