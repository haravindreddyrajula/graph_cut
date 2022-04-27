

def writefile(data):
    file1 = open("adj_matrix.txt", "a")  # append mode
    file1.write(str(data))
    file1.write("\n ------------------------------- \n")
    file1.close()


def writealgooutputfile(data):
    file1 = open("algo_output.txt", "a")  # append mode
    file1.write(str(data))
    file1.write("\n ------------------------------- \n")
    file1.close()

# def create_dir():
#     os.mkdir
