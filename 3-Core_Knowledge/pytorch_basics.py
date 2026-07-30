import torch

# --- TENSOR CREATION (Similar to NumPy) ---
# From Python list
tensor = torch.tensor([[1, 2], [3, 4]])
print(tensor)
# tensor([[1, 2],
#         [3, 4]])

# Special tensors
zeros = torch.zeros(3, 4)      # 3x4 zeros
ones = torch.ones(2, 3)        # 2x3 ones
random = torch.randn(3, 3)     # 3x3 random (normal distribution)

# --- TENSOR PROPERTIES ---
print(tensor.shape)      # torch.Size([2, 2]) → 2 rows, 2 cols
print(tensor.dtype)      # torch.int64 (default integer type)
print(tensor.device)     # cpu (or cuda:0 if on GPU)

# --- MOVING TO GPU (Critical for ML) ---
if torch.cuda.is_available():
    tensor_gpu = tensor.to('cuda')  # Move tensor to GPU
    print("Running on GPU!")
else:
    print("Running on CPU")

# --- TENSOR OPERATIONS (Like NumPy) ---
a = torch.tensor([1, 2, 3])
b = torch.tensor([4, 5, 6])

# Element-wise operations
print(a + b)        # tensor([5, 7, 9])
print(a * b)        # tensor([4, 10, 18]) → element-wise multiplication
print(torch.dot(a, b))  # tensor(32) → dot product (1*4 + 2*5 + 3*6)

# Matrix multiplication (critical for neural networks)
matrix1 = torch.tensor([[1, 2], [3, 4]])
matrix2 = torch.tensor([[5, 6], [7, 8]])
result = torch.matmul(matrix1, matrix2)
print(result)
# tensor([[19, 22],
#         [43, 50]])

# --- AUTOMATIC DIFFERENTIATION (THE MAGIC) ---
# This is why PyTorch is used for training neural networks
x = torch.tensor(2.0, requires_grad=True)  # Track operations
y = x ** 2 + 3 * x + 1  # y = x² + 3x + 1
y.backward()  # Compute derivative dy/dx
print(x.grad)  # tensor(7.0) → derivative is 2x + 3 = 7 at x=2

# Why this matters: Neural networks learn by computing gradients
# and updating weights. PyTorch does this automatically!