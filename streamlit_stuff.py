import streamlit as st
import numpy as np

# Function to convert string input to numpy array
def string_to_matrix(input_str):
    try:
        # Splitting the input string by semicolons to get rows and then commas to get individual elements
        matrix = np.array([list(map(float, row.split(','))) for row in input_str.split(';')])
        return matrix
    except ValueError:
        st.error("Please enter a valid matrix.")
        return None

# Function to perform row reduction and display each step
def row_reduce(matrix):
    steps = ["Original Matrix:\n" + str(matrix)]
    m, n = matrix.shape
    row = 0
    for col in range(n):
        if row >= m:
            break
        pivot = matrix[row, col]
        if pivot == 0:
            for i in range(row+1, m):
                if matrix[i, col] != 0:
                    matrix[[row, i]] = matrix[[i, row]]  # Swap rows
                    steps.append(f"Swapped row {row+1} and row {i+1}:\n" + str(matrix))
                    pivot = matrix[row, col]
                    break
        if pivot == 0:
            continue
        if pivot != 1:
            matrix[row] = matrix[row] / pivot  # Scale to make pivot = 1
            steps.append(f"Scaled row {row+1} to make pivot 1:\n" + str(matrix))
        for i in range(m):
            if i != row and matrix[i, col] != 0:
                factor = matrix[i, col]
                matrix[i] -= factor * matrix[row]  # Eliminate column below pivot
                steps.append(f"Eliminated column {col+1} in row {i+1} using row {row+1}:\n" + str(matrix))
        row += 1
    return steps

# Streamlit UI
st.title('Matrix Calculations Step-by-Step')

# User inputs for matrices
matrix_input = st.text_area("Enter your matrix (row by row, separated by ';', and each element separated by ','):", "1,2;3,4")
operation = st.selectbox('Select Operation', ['Row Reduction'])

matrix = string_to_matrix(matrix_input)

if matrix is not None:
    # Perform and display calculations based on the operation
    if operation == 'Row Reduction':
        steps = row_reduce(matrix.copy())  # Using .copy() to avoid modifying the original matrix
        for step in steps:
            st.text(step)
