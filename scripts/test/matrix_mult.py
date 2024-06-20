def matrix_multiply_blockwise_from_file(file_A, file_B, file_C, block_size=100):
    print(f"block_size: {block_size}")
    def read_block(filename, start_row, start_col, num_rows, num_cols):
        block = []
        with open(filename, 'r') as file:
            for _ in range(start_row):
                file.readline()
            for _ in range(num_rows):
                row = file.readline().split()[start_col:start_col+num_cols]
                block.append([int(x) for x in row])
        return block

    rows_A = cols_A = rows_B = cols_B = 100

    with open(file_C, 'w') as file:
        for i in range(0, rows_A, block_size):
            print(f"Processing row block starting at row {i}")
            for j in range(0, cols_B, block_size):
                result_block = [[0]*block_size for _ in range(block_size)]
                for k in range(0, cols_A, block_size):
                    A_block = read_block(file_A, i, k, block_size, block_size)
                    B_block = read_block(file_B, k, j, block_size, block_size)
                    for ii in range(block_size):
                        for jj in range(block_size):
                            for kk in range(block_size):
                                result_block[ii][jj] += A_block[ii][kk] * B_block[kk][jj]
                for row in result_block:
                    file.write(' '.join(map(str, row)) + '\n')

matrix_multiply_blockwise_from_file('matrix_A.txt', 'matrix_B.txt', 'result_matrix.txt', block_size=10)
