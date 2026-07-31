from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType
import torch

# --- WHY PEFT? ---
# Full fine-tuning of a 7B model needs 24GB+ VRAM
# PEFT (LoRA) fine-tuning only needs ~8GB VRAM!
# This is CRITICAL if you're on a personal machine

# --- STEP 1: Load base model ---
model_name = "microsoft/DialoGPT-small"  # Small model for testing
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# --- STEP 2: Configure LoRA (Low-Rank Adaptation) ---
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,  # For text generation
    r=4,              # Rank: lower = less parameters to train
    lora_alpha=16,    # Scaling factor
    lora_dropout=0.1, # Dropout for regularization
    target_modules=["c_attn"]  # Which layers to apply LoRA to
)

# --- STEP 3: Apply LoRA ---
model = get_peft_model(model, lora_config)

# --- SEE THE DIFFERENCE ---
def print_trainable_parameters(model):
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"Trainable: {trainable:,} ({trainable/total:.2%} of total)")

print_trainable_parameters(model)
# Output: Trainable: 294,912 (0.24% of total)
# Instead of training all 124M parameters, we only train 0.24%!
# Because of this, LoRA fine-tuning is much faster and requires less memory.
# It would feel like more parameters checks everything than LoRA, but LoRA is designed to adapt the model effectively with far fewer parameters. And it performs same or better than using full fine-tuning in many cases, especially for domain-specific tasks.

# --- STEP 4: Training (Simplified) ---
# Here's what happens during training:
training_data = [
    "MCP server error: unauthorized access attempt detected",
    "MCP server: normal operation, no threats detected",
    "Warning: MCP server response time exceeded threshold"
]

# In real training: you'd iterate through data, compute loss, backpropagate
# The key insight: LoRA only updates the tiny LoRA parameters
# The base model weights remain frozen (not changed)