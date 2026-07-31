from langgraph.graph import StateGraph, START, END
from typing import Literal, TypedDict, Annotated
import operator

# --- STEP 1: DEFINE THE STATE FIRST ---
# This MUST be defined before any function that uses it as a type hint

class MCPAnalysisState(TypedDict):
    """State that flows through the LangGraph pipeline"""
    # messages: accumulates conversation history
    messages: Annotated[list, operator.add]
    
    # mcp_response: the raw response from MCP server
    mcp_response: str
    
    # threat_level: analysis result (HIGH/MEDIUM/LOW)
    threat_level: str
    
    # action_taken: what action was performed
    action_taken: str
    
    # Optional: additional fields you might need
    mcp_request: str
    features: list  # for numerical features
    threat_score: float

# --- STEP 2: DEFINE NODES (Functions that process state) ---
# Now you can use MCPAnalysisState as a type hint

def analyze_with_ai(state: MCPAnalysisState) -> MCPAnalysisState:
    """Analyze the MCP response and determine threat level"""
    # In real implementation: use transformers/PyTorch
    # For now, simple logic
    
    response = state.get("mcp_response", "")
    
    # Simple threat detection (replace with real AI)
    if "admin" in response.lower() and "unauthorized" in response.lower():
        threat = "HIGH"
    elif "error" in response.lower():
        threat = "MEDIUM"
    else:
        threat = "LOW"
    
    # Return updated state
    return {
        **state,  # Keep all existing state fields
        "threat_level": threat,
        "messages": state.get("messages", []) + [
            {"role": "assistant", "content": f"Threat level set to: {threat}"}
        ]
    }

def take_action(state: MCPAnalysisState) -> MCPAnalysisState:
    """Take remediation action based on threat level"""
    threat = state.get("threat_level", "LOW")
    
    if threat == "HIGH":
        action = "🚨 BLOCKED: Admin endpoint access denied"
    elif threat == "MEDIUM":
        action = "⚠️ LOGGED: Suspicious activity recorded"
    else:
        action = "✅ ALLOWED: Normal operation"
    
    return {
        **state,
        "action_taken": action,
        "messages": state.get("messages", []) + [
            {"role": "assistant", "content": f"Action taken: {action}"}
        ]
    }

# --- STEP 3: CONDITIONAL ROUTING FUNCTION ---
def should_continue(state: MCPAnalysisState) -> Literal["remediate", "end"]:
    """Decide whether to continue analysis or stop"""
    # If high threat, go to remediation
    if state.get("threat_level") == "HIGH":
        return "remediate"  # Go to remediation node
    else:
        return "end"  # Stop analysis

# --- STEP 4: BUILD THE GRAPH ---
builder = StateGraph(MCPAnalysisState)
builder.add_node("analyze", analyze_with_ai)
builder.add_node("remediate", take_action)

# Add edges
builder.add_edge(START, "analyze")

# Conditional edge: after analyze, decide what to do
builder.add_conditional_edges(
    "analyze",
    should_continue,  # Function that decides where to go
    {
        "remediate": "remediate",  # If returns "remediate" → go to remediate
        "end": END  # If returns "end" → stop
    }
)
builder.add_edge("remediate", END)

# Compile the graph
graph = builder.compile()

# --- STEP 5: RUN THE GRAPH ---
if __name__ == "__main__":
    # Initial state
    initial_state = {
        "messages": [{"role": "user", "content": "Analyze MCP server response"}],
        "mcp_response": "Error: Unauthorized access to /admin endpoint",
        "threat_level": "",
        "action_taken": "",
        "mcp_request": "GET /admin",
        "features": [],
        "threat_score": 0.0
    }
    
    # Run the graph
    result = graph.invoke(initial_state)
    
    # Print results
    print("\n" + "="*50)
    print("🛡️ MCP SECURITY ANALYSIS RESULT")
    print("="*50)
    print(f"🔍 Threat Level: {result.get('threat_level')}")
    print(f"⚡ Action Taken: {result.get('action_taken')}")
    print(f"📝 Messages:")
    for msg in result.get('messages', []):
        print(f"   {msg['role']}: {msg['content']}")
    print("="*50)