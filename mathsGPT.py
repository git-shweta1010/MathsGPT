import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.callbacks.streamlit import StreamlitCallbackHandler
from dotenv import load_dotenv

load_dotenv()

# Streamlit UI setup
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

# Load LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)

# Tools
wiki_tool = Tool(
    name="Wikipedia",
    func=WikipediaAPIWrapper().run,
    description="Use this for questions related to current events or general knowledge."
)

# Math reasoning using prompt | llm pattern
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

✍️ Detailed Solution:
"""
,

)

reasoning_chain = prompt | llm

reasoning_tool = Tool(
    name="MathReasoning",
    func=lambda q: reasoning_chain.invoke({"question": q}).content.strip().split("additional_kwargs")[0],
    description="Useful for solving math problems with reasoning (including equations)."
)

# Agent initialization (still uses the agent for multi-tool logic)
agent = initialize_agent(
    tools=[wiki_tool, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True,
)

# Session history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me any math or general question."}]

# Display past messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
question = st.chat_input("Enter your question:")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.spinner("Thinking..."):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        try:
            # Recommended replacement for .run()
            response = agent.invoke({"input": question}, config={"callbacks": [st_cb]})
            if isinstance(response, dict):
                response = response.get("output", "No response.")
        except Exception as e:
            response = "Sorry, something went wrong while processing your question."
            st.error(str(e))

    st.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


