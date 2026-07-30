import numpy as np

# --- CREATING ARRAYS ---
# Python list → NumPy array
data = [1, 2, 3, 4, 5]
arr = np.array(data)
print(arr)  # [1 2 3 4 5]

# Why this matters: NumPy arrays are homogenous (all same type)
# This allows C-level optimizations instead of Python-level loops

# --- SHAPE & DIMENSIONS ---
# 1D array (vector)
vector = np.array([1, 2, 3])
print(vector.shape)  # (3,) → One dimension with 3 elements

# 2D array (matrix) - Like a spreadsheet
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])
print(matrix.shape)  # (2, 3) → 2 rows, 3 columns

# 3D array (tensor) - Like a cube of data
tensor = np.array([[[1, 2], [3, 4]],
                   [[5, 6], [7, 8]]])
print(tensor.shape)  # (2, 2, 2) → 2 layers, 2 rows, 2 columns

# --- SPECIAL ARRAYS (Common in ML) ---
zeros = np.zeros((3, 4))  # 3x4 matrix of zeros
ones = np.ones((2, 3))    # 2x3 matrix of ones
random = np.random.randn(3, 3)  # 3x3 random numbers (normal distribution)
identity = np.eye(3)      # 3x3 identity matrix

# --- BROADCASTING (NumPy's Magic) ---
# This is critical: operations work on arrays of different sizes
arr1 = np.array([1, 2, 3])
arr2 = np.array([[1], [2], [3]])

# arr1 (1x3) + arr2 (3x1) → NumPy "broadcasts" to make them (3x3)
result = arr1 + arr2
print(result)
# Output:
# [[2 3 4]
#  [3 4 5]
#  [4 5 6]]

# Why this matters: Without broadcasting, you'd need nested loops!
# This is how PyTorch tensors work too

# --- SLICING (Like Python lists but more powerful) ---
matrix = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12]])

# Get first 2 rows, columns 1-2
subset = matrix[:2, 1:3]  # [rows, columns]
print(subset)
# [[2 3]
#  [6 7]]

# Boolean indexing - filter based on condition
mask = matrix > 5  # Creates boolean mask
filtered = matrix[mask]  # Returns only elements > 5
print(filtered)  # [6 7 8 9 10 11 12]

# --- AGGREGATION FUNCTIONS ---
data = np.array([1, 2, 3, 4, 5])
print(np.mean(data))    # 3.0
print(np.std(data))     # 1.41 (standard deviation)
print(np.sum(data))     # 15
print(np.max(data))     # 5

# Axis operations (critical for ML)
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])
# axis=0 → column-wise (vertically)
print(np.sum(matrix, axis=0))  # [5, 7, 9] (sum each column)
# axis=1 → row-wise (horizontally)
print(np.sum(matrix, axis=1))  # [6, 15] (sum each row)

response_times = np.array([12.5, 15.3, 11.2, 45.8, 13.1, 14.2])

# Detect anomalies (values > 3 standard deviations from mean)
mean = np.mean(response_times)
std = np.std(response_times)
threshold = mean + 3 * std

anomalies = response_times[response_times > threshold]
print(f"Anomalous response times: {anomalies}")
# This would catch the 45.8ms spike as an anomaly

# Normalize data (common in ML preprocessing)
normalized = (response_times - mean) / std
print(f"Normalized: {normalized}")
