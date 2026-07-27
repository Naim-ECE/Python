# Read
with open('read.txt', 'r') as file:
    data = file.read()

print(data)

# Write
with open('write.txt', 'w') as file:
    file.write("Scan complete")
