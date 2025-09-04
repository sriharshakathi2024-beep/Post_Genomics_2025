#2.1
def matrix_multiply(A, B):
    
    result = [[0]*len(B[0]) for _ in range(len(A))]
    
    for i in range(len(A)):           # rows of A
        for j in range(len(B[0])):    # columns of B
            for k in range(len(B)):   
                result[i][j] += A[i][k] * B[k][j]
    return result

# Example
A = [[2,0],
     [1,1],
     [3,0]]

B = [[2,1,6],
     [1,0,0]]

print(matrix_multiply(A, B))


#2.2
import numpy as np
import time

def element_wise_multiply(A, B):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Matrices must have the same dimensions for element-wise multiplication.")
    
    result = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]
    
    for i in range(len(A)):
        for j in range(len(A[0])):
            result[i][j] = A[i][j] * B[i][j]
    
    return result


n = 1000
A = np.random.randint(0, 10, size=(n, n)).tolist()
B = np.random.randint(0, 10, size=(n, n)).tolist()

# --- Custom function ---
start_time_defined = time.perf_counter()
output_defined = element_wise_multiply(A, B)
end_time_defined = time.perf_counter()
defined_time = end_time_defined - start_time_defined

print(f"Time taken by custom function: {defined_time:.6f} seconds")

# --- NumPy ---
A_np = np.array(A)
B_np = np.array(B)

start_time_numpy = time.perf_counter()
output_numpy = np.multiply(A_np, B_np)
end_time_numpy = time.perf_counter()
numpy_time = end_time_numpy - start_time_numpy

print(f"Time taken by NumPy function: {numpy_time:.6f} seconds")

if defined_time > numpy_time:
    print("\n NumPy is faster.")
else:
    print("\n Custom function is faster (try increasing n).")




