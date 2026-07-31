import torch
import torch.nn as nn
import torch.optim as optim

# --- DEFINING A NEURAL NETWORK ---
class MCPSecurityClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        # nn.Module: Base class for all neural networks
        super(MCPSecurityClassifier, self).__init__()
        
        # Define layers (like building blocks)
        self.layer1 = nn.Linear(input_size, hidden_size)
        # Linear: y = xW^T + b (matrix multiplication + bias)
        # Input: batch_size × input_size
        # Output: batch_size × hidden_size
        
        self.layer2 = nn.Linear(hidden_size, hidden_size)
        self.output = nn.Linear(hidden_size, output_size)
        
        # Activation function (introduces non-linearity)
        self.relu = nn.ReLU()
        # ReLU: f(x) = max(0, x) → makes negative values 0
        
    def forward(self, x):
        # Forward pass: how data flows through the network
        x = self.relu(self.layer1(x))  # Input → Hidden1 → ReLU
        x = self.relu(self.layer2(x))  # Hidden1 → Hidden2 → ReLU
        x = self.output(x)             # Hidden2 → Output
        return x

# --- CREATING AND USING THE MODEL ---
model = MCPSecurityClassifier(
    input_size=10,    # 10 features (e.g., request length, port, etc.)
    hidden_size=20,   # Hidden layer size
    output_size=2     # 2 classes (safe/unsafe)
)

# Generate some dummy data (like MCP request features)
# In real scenario: features = [request_size, time, port, etc.]
sample_data = torch.randn(1, 10)  # 1 sample, 10 features
output = model(sample_data)       # Forward pass
print(output)  # tensor([[0.1, -0.2]]) → raw scores (logits)

# --- TRAINING LOOP (How models learn) ---
# Loss function: measures how wrong the model is
criterion = nn.CrossEntropyLoss()  # For classification tasks

# Optimizer: updates weights to minimize loss
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Learning rate

# Simplified training step
def train_step(input_data, true_label):
    # 1. Forward pass
    predictions = model(input_data)
    
    # 2. Calculate loss
    loss = criterion(predictions, true_label)
    
    # 3. Backward pass (compute gradients)
    optimizer.zero_grad()  # Reset gradients from previous step
    loss.backward()        # Compute new gradients
    
    # 4. Update weights
    optimizer.step()       # Apply gradients to weights
    
    return loss.item()     # Return loss value

# Why this matters: This is how the model learns to distinguish
# between safe and unsafe MCP server behaviors!