import streamlit as st
from finasistant_app.agents.agent import assistant_workflow
from langchain_core.messages import (
    HumanMessage,
    BaseMessage,
)
from finasistant_app.config.settings import settings


st.title(settings.assistant_title)


if "messages" not in st.session_state:
    st.session_state.messages = []
if "langgraph_messages" not in st.session_state:
    st.session_state.langgraph_messages = []

for message in st.session_state.messages:
    with st.chat_message(message["type"]):
        st.write(message)

if prompt := st.chat_input("What is up?"):
    with st.spinner("Thinking..."):
        st.session_state.langgraph_messages.append(HumanMessage(content=prompt))
        for event in assistant_workflow.stream(
            input={"messages": st.session_state.langgraph_messages},
            stream_mode="values",
        ):
            message: BaseMessage = event["messages"][-1]
            with st.chat_message(message.type):
                st.write(message.dict())
                st.session_state.messages.append(
                    {"type": message.type, "content": message.dict()}
                )
                if not isinstance(message, HumanMessage):
                    st.session_state.langgraph_messages.append(message)

# Query examples:
# Hello can you show me last 5 years of MSFT data monthly
