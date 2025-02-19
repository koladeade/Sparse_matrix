import re

class SparseMatrix:
    def __init__(self, num_rows=0, num_cols=0):
        self.matrix = {}
        self.num_rows = num_rows
        self.num_cols = num_cols

    def load_from_file(self, file_path):
        """Load matrix data from a file."""
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                self.num_rows = int(re.search(r'\d+', lines[0]).group())
                self.num_cols = int(re.search(r'\d+', lines[1]).group())

                for line in lines[2:]:
                    match = re.match(r'\((\d+),\s*(\d+),\s*(-?\d+)\)', line)
                    if match:
                        row, col, value = map(int, match.groups())
                        self.matrix[(row, col)] = value
        except Exception as e:
            raise ValueError(f'Error loading matrix from file {file_path}: {e}')

    def get_element(self, row, col):
        """Return the element at the specified position, or 0 if not found."""
        return self.matrix.get((row, col), 0)

    def set_element(self, row, col, value):
        """Set the value of the element at the specified position."""
        if value == 0:
            self.matrix.pop((row, col), None)
        else:
            self.matrix[(row, col)] = value

    def transpose(self):
        """Transpose the sparse matrix."""
        transposed = SparseMatrix(self.num_cols, self.num_rows)
        for (row, col), value in self.matrix.items():
            transposed.matrix[(col, row)] = value
        return transposed

    def __add__(self, other):
        """Add two sparse matrices."""
        result = SparseMatrix(max(self.num_rows, other.num_rows), max(self.num_cols, other.num_cols))

        # Adding elements from both matrices
        for (row, col), value in self.matrix.items():
            result.matrix[(row, col)] = result.get_element(row, col) + value
        for (row, col), value in other.matrix.items():
            result.matrix[(row, col)] = result.get_element(row, col) + value
        
        return result

    def __sub__(self, other):
        """Subtract one sparse matrix from another."""
        result = SparseMatrix(max(self.num_rows, other.num_rows), max(self.num_cols, other.num_cols))

        # Subtracting elements from both matrices
        for (row, col), value in self.matrix.items():
            result.matrix[(row, col)] = result.get_element(row, col) + value
        for (row, col), value in other.matrix.items():
            result.matrix[(row, col)] = result.get_element(row, col) - value
        
        return result

    def __mul__(self, other):
        if self.num_cols != other.num_rows:
            raise ValueError('Matrices cannot be multiplied due to dimension mismatch.')

        result = SparseMatrix(self.num_rows, other.num_cols)

        # Multiplying matrices element by element
        for (row, col), value in self.matrix.items():
            for k in range(other.num_cols):
                result.matrix[(row, k)] = result.get_element(row, k) + value * other.get_element(col, k)

        return result

    def save_to_file(self, file_path):
        """Save the matrix to a file."""
        try:
            with open(file_path, 'w') as file:
                file.write(f"rows={self.num_rows}\n")
                file.write(f"cols={self.num_cols}\n")
                for (row, col), value in sorted(self.matrix.items()):
                    file.write(f"({row}, {col}, {value})\n")
        except Exception as e:
            raise ValueError(f'Error saving matrix to file {file_path}: {e}')


def get_matrix_operation():
    """Get the matrix operation from the user."""
    operation = input("Select an option: 1. Add, 2. Subtract, 3. Multiply: ").strip().lower()
    if operation in ['1', 'add']:
        return 'add'
    elif operation in ['2', 'subtract']:
        return 'subtract'
    elif operation in ['3', 'multiply']:
        return 'multiply'
    else:
        print('Invalid operation')
        return None


def main():
    file1 = 'easy_sample_03_2.txt'
    file2 = 'easy_sample_03_3.txt'

    matrix1 = SparseMatrix()
    matrix1.load_from_file(file1)
    matrix2 = SparseMatrix()
    matrix2.load_from_file(file2)

    print(f'Matrix 1: {matrix1.num_rows}x{matrix1.num_cols}')
    print(f'Matrix 2: {matrix2.num_rows}x{matrix2.num_cols}')

    operation = get_matrix_operation()
    if operation is None:
        return

    output_file = "result_matrix.txt"

    try:
        if operation == 'add':
            result = matrix1 + matrix2
        elif operation == 'subtract':
            result = matrix1 - matrix2
        elif operation == 'multiply':
            # Transpose Matrix 2 if needed for multiplication
            matrix2_transposed = matrix2.transpose()
            result = matrix1 * matrix2_transposed
    except ValueError as e:
        print(f"Error: {e}")
        return

    result.save_to_file(output_file)
    print(f'Result saved to {output_file}')


if __name__ == "__main__":
    main()
