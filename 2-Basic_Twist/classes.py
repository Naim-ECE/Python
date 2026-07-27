class MCPScanner:
    def __init__(self, target): # constructor method
        self.target = target
    
    def scan(self):
        return f"Scanning {self.target}"

# Creating the object
scanner = MCPScanner("192.168.1.1")
# ^^^^^^^           ^^^^^^^^^^^^^^^^
# variable          constructor call

# Calling the method
result = scanner.scan()
print(result)
#        ^^^^^^^ ^^^^^
#        object  method call