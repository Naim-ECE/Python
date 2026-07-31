from langgraph.graph import StateGraph, START, END
from typing import Literal, TypedDict, Annotated, Optional
import operator
import json

# --- DEFINE COMPREHENSIVE STATE ---
class MCPAnalysisState(TypedDict):
    # Core conversation tracking
    messages: Annotated[list, operator.add]  # Accumulates messages
    
    # MCP request/response data
    mcp_request: str  # Original request
    mcp_response: str  # Response from MCP server
    mcp_status_code: int  # HTTP status code (200, 404, 500, etc.)
    mcp_endpoint: str  # Which endpoint was called
    
    # Security analysis fields
    threat_level: Literal["HIGH", "MEDIUM", "LOW", "NONE"]  # Severity
    threat_score: float  # 0.0 to 1.0 confidence score
    threat_categories: list  # List of threat types detected
    anomalies: list  # List of anomalies found
    
    # Features for ML analysis
    features: dict  # Extracted features for AI model
    
    # Action tracking
    action_taken: str  # What action was performed
    action_required: bool  # Does the user need to intervene?
    
    # Metadata
    timestamp: str  # When the analysis happened
    analysis_duration: float  # How long analysis took

# --- NODE 1: EXTRACT FEATURES ---
def extract_features(state: MCPAnalysisState) -> MCPAnalysisState:
    """Extract numerical features from MCP response"""
    response = state.get("mcp_response", "")
    status = state.get("mcp_status_code", 0)
    
    # Extract features (in real code: use NumPy)
    features = {
        "response_length": len(response),
        "status_code": status,
        "error_count": response.lower().count("error"),
        "auth_mentions": response.lower().count("auth"),
        "admin_mentions": response.lower().count("admin"),
    }
    
    return {
        **state,
        "features": features,
        "messages": state.get("messages", []) + [
            {"role": "assistant", "content": f"Features extracted: {json.dumps(features)}"}
        ]
    }

# --- NODE 2: AI ANALYSIS ---
def analyze_with_ai(state: MCPAnalysisState) -> MCPAnalysisState:
    """Use AI to analyze features and detect threats"""
    # In real code: use transformers/PyTorch
    # This is simplified logic
    
    features = state.get("features", {})
    threat_score = 0.0
    threat_categories = []
    anomalies = []
    
    # Rule-based scoring (replace with actual AI)
    if features.get("status_code", 0) in [401, 403]:
        threat_score += 0.5
        threat_categories.append("Authentication Failure")
        anomalies.append("Unauthorized access attempt")
    
    if features.get("admin_mentions", 0) > 3:
        threat_score += 0.3
        threat_categories.append("Admin Path Probing")
        anomalies.append("Excessive admin endpoint access")
    
    if features.get("error_count", 0) > 5:
        threat_score += 0.2
        threat_categories.append("Error Flooding")
        anomalies.append("Multiple errors detected")
    
    # Determine threat level
    if threat_score >= 0.7:
        threat_level = "HIGH"
    elif threat_score >= 0.4:
        threat_level = "MEDIUM"
    elif threat_score > 0:
        threat_level = "LOW"
    else:
        threat_level = "NONE"
    
    return {
        **state,
        "threat_score": threat_score,
        "threat_level": threat_level,
        "threat_categories": threat_categories,
        "anomalies": anomalies,
        "messages": state.get("messages", []) + [
            {"role": "assistant", "content": f"Threat Score: {threat_score:.2f} (Level: {threat_level})"}
        ]
    }

# --- NODE 3: TAKE ACTION ---
def take_action(state: MCPAnalysisState) -> MCPAnalysisState:
    """Take security action based on threat level"""
    threat_level = state.get("threat_level", "NONE")
    action_taken = ""
    action_required = False
    
    if threat_level == "HIGH":
        action_taken = "🚨 IMMEDIATE BLOCK: Endpoint disabled, admin alerted"
        action_required = True
    elif threat_level == "MEDIUM":
        action_taken = "⚠️ LOGGED: Request logged for review"
        action_required = True
    elif threat_level == "LOW":
        action_taken = "ℹ️ MONITORED: Request allowed but monitored"
        action_required = False
    else:
        action_taken = "✅ ALLOWED: No threats detected"
        action_required = False
    
    return {
        **state,
        "action_taken": action_taken,
        "action_required": action_required,
        "messages": state.get("messages", []) + [
            {"role": "assistant", "content": f"Action: {action_taken}"}
        ]
    }

# --- CONDITIONAL ROUTING ---
def should_continue(state: MCPAnalysisState) -> Literal["remediate", "end"]:
    """Route based on threat level"""
    if state.get("threat_level") == "HIGH":
        return "remediate"
    elif state.get("threat_level") == "MEDIUM":
        return "remediate"  # Also remediate for MEDIUM
    else:
        return "end"

# --- BUILD GRAPH ---
def build_mcp_security_pipeline():
    builder = StateGraph(MCPAnalysisState)
    
    # Add nodes
    builder.add_node("extract_features", extract_features)
    builder.add_node("analyze", analyze_with_ai)
    builder.add_node("remediate", take_action)
    
    # Add edges
    builder.add_edge(START, "extract_features")
    builder.add_edge("extract_features", "analyze")
    
    # Conditional routing
    builder.add_conditional_edges(
        "analyze",
        should_continue,
        {
            "remediate": "remediate",
            "end": END
        }
    )
    builder.add_edge("remediate", END)
    
    return builder.compile()

# --- USE IT ---
if __name__ == "__main__":
    # Create pipeline
    pipeline = build_mcp_security_pipeline()
    
    # Example MCP response
    test_response = """
    Error 401: Unauthorized access attempt to /admin/settings
    IP: 192.168.1.100 attempted 15 admin endpoint requests
    """
    
    # Initial state
    initial = {
        "messages": [
            {"role": "user", "content": "Analyze MCP security response"}
        ],
        "mcp_request": "GET /admin/settings",
        "mcp_response": test_response,
        "mcp_status_code": 401,
        "mcp_endpoint": "/admin/settings",
        "threat_level": "",
        "threat_score": 0.0,
        "threat_categories": [],
        "anomalies": [],
        "features": {},
        "action_taken": "",
        "action_required": False,
        "timestamp": "2024-01-15T10:30:00",
        "analysis_duration": 0.0
    }
    
    # Run pipeline
    result = pipeline.invoke(initial)
    
    # Pretty print results
    print("\n" + "="*60)
    print("🛡️  MCP SECURITY ANALYSIS REPORT")
    print("="*60)
    print(f"🔍 Threat Level: {result['threat_level']}")
    print(f"📊 Threat Score: {result['threat_score']:.2f}")
    print(f"🏷️  Categories: {', '.join(result.get('threat_categories', []))}")
    print(f"⚠️  Anomalies: {', '.join(result.get('anomalies', []))}")
    print(f"⚡ Action: {result['action_taken']}")
    print(f"👤 User Action Required: {result.get('action_required', False)}")
    print("="*60)