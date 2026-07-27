name = "MCP"
port = 8000
is_secure = True
config = {"host": "localhost", "port": port, "secure": is_secure} # Dictionary (like JS object)

def analysis_mcp(data) :
    """Docstring - like Javadoc"""
    return f"Analyzing: {data}"

print(analysis_mcp(2))
print(analysis_mcp.__doc__) # accessing the docstring of the function
