import numpy as np
import pandas as pd
import sys, getopt
import cooler


def main(argv):

    input_file = ''
    output_file = ''
    resolution = 0
    chromosome = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:r:c:")

    except getopt.GetoptError:
        print('cool_to_sparse.py -i <input_file> -o <output_file> -r <resolution> -c <chromosome>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <input_file> -o <output_file> -r <resolution> -c <chromosome>')
            sys.exit()
        elif opt in (["-i"]):
            input_file = arg
        elif opt in (["-o"]):
            output_file = arg
        elif opt in (["-r"]):
            resolution = int(arg)
        elif opt in (["-c"]):
            chromosome = int(arg)

    contact_matrix = np.loadtxt(input_file, dtype=str, skiprows=1)

    error = ''
    sparse_matrix = []
    if contact_matrix[0][0].isnumeric():
        for i in range(len(contact_matrix)):
            if int(contact_matrix[i][0]) == chromosome and int(contact_matrix[i][3]) == chromosome:
                sparse_matrix.append([contact_matrix[i][1]/resolution, contact_matrix[i][4]/resolution, contact_matrix[i][6]])
    else:
        for i in range(len(contact_matrix)):
            if contact_matrix[i][0] == 'chr' + str(chromosome) and contact_matrix[i][3] == 'chr' + str(chromosome):
                sparse_matrix.append([int(contact_matrix[i][1])/resolution, int(contact_matrix[i][4])/resolution, contact_matrix[i][6]])
                
    if error == '':
        with open(output_file, 'w') as f:
            for row in sparse_matrix:
                f.write(str(int(row[0])) + " " + str(int(row[1])) + " " + str(row[2]) + "\n")
    else:
        print(error)

if __name__ == "__main__":
    main(sys.argv[1:])