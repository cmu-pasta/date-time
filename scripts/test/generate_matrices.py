import random

def generate_matrix(rows, cols):
    return [[random.randint(0, 100) for _ in range(cols)] for _ in range(rows)]

rows_A = 1000
cols_A = 1000
rows_B = cols_A
cols_B = 1000

A = generate_matrix(rows_A, cols_A)
B = generate_matrix(rows_B, cols_B)

def write_matrix_to_file(matrix, filename):
    with open(filename, 'w') as file:
        for row in matrix:
            file.write(' '.join(map(str, row)) + '\n')

write_matrix_to_file(A, 'matrix_A.txt')
write_matrix_to_file(B, 'matrix_B.txt')
