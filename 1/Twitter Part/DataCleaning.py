file = open("output.txt")
file_input = open("input.csv")
file_output = open("first_clean.txt","w")


# interface of clean data model
if __name__ == '__main__':

    input = []  # name of movies
    while 1:
        line = file_input.readline()
        input.append(line[0:-1])
        if not line:
            break
        pass
    file_input.close()


    errorTime = 0   # stored the frequency of not format data
    while 1:
        line = file.readline()
        if line.strip().split("`")[0] in input :        # if the data is not split by "`", it is illegal. delete it
            print(line)
            file_output.write(line)     # write the format data into first_clean.txt
        else:
            errorTime+=1
        if not line:
            break
        pass

    print(errorTime)        # frequency of error data
file_output.close()
file.close()






