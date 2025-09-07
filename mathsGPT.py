import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv

# Load environment variables (optional, if using .env file)
load_dotenv()

# ---------------- Streamlit UI ----------------
st.set_page_config(
    page_title="MathsGPT",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("🧠 MathsGPT - Ask Anything, Solve Everything")

# Get API key
groq_api_key = st.sidebar.text_input("🔑 Enter your Groq API Key:", type="password")
if not groq_api_key:
    st.info("Please provide your Groq API key to continue.")
    st.stop()

# ---------------- LLM Setup ----------------
# Use a smaller model for faster responses (you can switch back to 70B if needed)
llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)

# ---------------- Tools ----------------
wiki_tool = Tool(
    name="Wikipedia",
    func=WikipediaAPIWrapper().run,
    description="Use this for general knowledge or current events."
)

# Prompt for math reasoning
prompt = PromptTemplate(
    template="""
You are a brilliant math teacher. Solve the math problem step by step using logical reasoning.

🔢 Always:
1. Identify like terms and group them.
2. Move terms to one side to isolate variables.
3. Simplify each step with clear, simple explanation.
4. Provide the final boxed answer at the end.

📌 Problem:
{question}

✍ Detailed Solution:
""",
    input_variables=["question"]
)

reasoning_chain = prompt | llm

reasoning_tool = Tool(
    name="MathReasoning",
    func=lambda q: reasoning_chain.invoke({"question": q}).content.strip(),
    description="Useful for solving math problems with step-by-step reasoning."
)

# Agent (for non-math queries)
agent = initialize_agent(
    tools=[wiki_tool, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True,
)

# ---------------- Session History ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me any math or general question."}]

# Display past messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------- User Input ----------------
question = st.chat_input("Enter your question:")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.spinner("Thinking..."):
        try:
            # Expanded math keywords
            math_keywords = [
                "age", "solve", "years", "equation", "times", "+", "-", "*", "/", "find",
                "add", "sum", "difference", "product", "number", "value", "math"
            ]

            if any(word in question.lower() for word in math_keywords):
                # Directly solve math with reasoning
                response = reasoning_chain.invoke({"question": question}).content.strip()
            else:
                # Use agent (Wikipedia/general queries)
                resp = agent.invoke({"input": question})
                response = resp.get("output", str(resp)) if isinstance(resp, dict) else str(resp)

        except Exception as e:
            response = f"⚠ Sorry, an error occurred: {str(e)}"

    st.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
