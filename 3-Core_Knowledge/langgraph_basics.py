from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolExecutor
from typing import TypedDict, Annotated
import operator

# --- DEFINE STATE (What information flows through the graph) ---
class MCPAnalysisState(TypedDict):
    # Annotated with operator.add means messages accumulate (not overwritten)
    messages: Annotated[list, operator.add]
    mcp_response: str
    threat_level: str
    action_taken: str

# --- DEFINE NODES (Each step is a function) ---
def query_mcp_server(state: MCPAnalysisState):
    """
    Node 1: Query the MCP server
    This simulates sending a request to an MCP server
    """
    # In reality: you'd use requests/websockets to query real MCP server
    print("🔍 Querying MCP server...")
    
    # Simulate MCP response
    mcp_data = {
        "status": "active",
        "endpoints": ["/api", "/auth", "/admin"],
        "security_headers": ["X-Frame-Options", "Content-Security-Policy"]
    }
    
    # Update state
    return {
        "mcp_response": str(mcp_data),
        "messages": [{"role": "assistant", "content": f"Retrieved MCP data: {mcp_data}"}]
    }

def analyze_with_ai(state: MCPAnalysisState):
    """
    Node 2: Analyze the MCP response using an AI model
    """
    print("🧠 Analyzing with AI...")
    
    # Mock AI analysis (in reality: use transformers or LangChain)
    if "/admin" in state["mcp_response"]:
        threat = "HIGH"
        action = "Block admin endpoint access"
    else:
        threat = "LOW"
        action = "Allow normal operation"
    
    return {
        "threat_level": threat,
        "action_taken": action,
        "messages": [{"role": "assistant", "content": f"Analysis complete: {threat} threat level"}]
    }

def take_action(state: MCPAnalysisState):
    """
    Node 3: Take action based on analysis
    """
    print(f"⚡ Taking action: {state['action_taken']}")
    
    # In reality: implement security measures
    if state["threat_level"] == "HIGH":
        # Block endpoint, alert admin, etc.
        return {
            "messages": [{"role": "assistant", "content": "🚨 Security measure implemented!"}]
        }
    else:
        return {
            "messages": [{"role": "assistant", "content": "✅ No action needed"}]
        }

# --- BUILD THE GRAPH ---
# Why use a graph? It gives you:
# 1. Clear visualization of the flow
# 2. Easy debugging (can inspect each step)
# 3. Cyclical workflows possible (can loop back)
# 4. Human-in-the-loop capabilities

# Initialize graph with state
builder = StateGraph(MCPAnalysisState)

# Add nodes (steps)
builder.add_node("query_mcp", query_mcp_server)
builder.add_node("analyze", analyze_with_ai)
builder.add_node("take_action", take_action)

# Add edges (transitions)
builder.add_edge(START, "query_mcp")  # Start → query
builder.add_edge("query_mcp", "analyze")  # query → analyze
builder.add_edge("analyze", "take_action")  # analyze → action
builder.add_edge("take_action", END)  # action → End

# --- COMPILE AND RUN ---
# Compile: Turns the graph into a runnable object
graph = builder.compile()

# Invoke: Run the graph
result = graph.invoke({
    "messages": [{"role": "user", "content": "Analyze MCP server security"}],
    "mcp_response": "",  # Initially empty, filled by nodes
    "threat_level": "",
    "action_taken": ""
})

print("\n--- FINAL RESULT ---")
print(f"Threat Level: {result['threat_level']}")
print(f"Action: {result['action_taken']}")
print("Messages:", result['messages'])