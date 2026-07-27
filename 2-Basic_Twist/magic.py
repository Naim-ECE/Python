# Instead of loops
squares = [x**2 for x in range(10)]  # [0,1,4,9,...]

# Dictionary comprehension
config = {f"port_{i}": 8000+i for i in range(3)} # "f" means format string. It will replace {i} with the value of i in each iteration.

print(squares)
print(config)