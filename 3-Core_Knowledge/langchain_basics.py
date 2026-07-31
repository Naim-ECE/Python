from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# for installation pip install -U langchain langchain-openai openai

# --- STEP 1: Setup LLM ---
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0  # 0 = deterministic, 1 = creative
)
# temperature: Controls randomness
# 0: Always picks most likely token (reliable)
# 1: More creative/random (maybe useful for exploration)

# --- STEP 2: Create a prompt template ---
prompt = PromptTemplate(
    input_variables=["mcp_log"],
    template="""
    Analyze this MCP server log entry for security threats.
    Log: {mcp_log}
    
    Response:
    - Threat Level: (Low/Medium/High)
    - Explanation:
    - Recommended Action:
    """
)

# --- STEP 3: Build chain ---
chain = prompt | llm  # This creates a chain that takes the prompt and passes it to the LLM

# --- STEP 4: Use it ---
mcp_log = "User agent attempted to access /admin endpoint without auth"
result = chain.run(mcp_log=mcp_log)
print(result)
# Output: Structured analysis of the log entry