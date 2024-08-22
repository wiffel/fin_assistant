from typing import Annotated
from typing_extensions import TypedDict
from finasistant_app.llm import get_default_anthropic_model
from langgraph.graph import StateGraph, START, END
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from finasistant_app.tools.alphavantage_tools_csv import (
    tools as alphavantage_tools,
)
from finasistant_app.tools.code_writing_tools import tools as code_writing_tools


class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = get_default_anthropic_model()
llm_with_alphavantage_tools = llm.bind_tools(alphavantage_tools)


def financial_alphavantage_assistant(state: State):
    template = (
        "You are a helpful assistant. That consults users on data analysis and helps to retrieve nessesry data from alphavantage API."
        "If a CSV file info is returned - you need to briefly inform user that data was fetched and ready for further analysys by given file"
        "and provide dataset_description as is returned from the tool in ``` quotes. Do not ask user any follow-up questions."
    )
    system_prompt_message = SystemMessagePromptTemplate.from_template(template)
    prompt = ChatPromptTemplate.from_messages(
        [
            system_prompt_message,
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    llm = prompt | llm_with_alphavantage_tools
    response = llm.invoke({"messages": state["messages"]})
    return {"data_context": response.content, "messages": response}


def write_streamlit_page_expert(state: State):
    system_prompt_message = SystemMessagePromptTemplate.from_template(
        (
            "You are an expert Streamlit developer. Your task is to create a Streamlit page that visualizes data to fulfil user query using plotly library."
            "\nUse a tool you were provided to save code."
            "\nYou MUST pass your code to save_streamlit_page_code tool, into python_code parameter."
            "\nTry to make page as interactive as possible."
            "\nUse data context provided by previous tool call to write a Streamlit page."
        )
    )
    prompt = ChatPromptTemplate.from_messages(
        [system_prompt_message, MessagesPlaceholder(variable_name="messages")]
    )
    llm = prompt | llm_with_alphavantage_tools
    response = llm.invoke(
        {"messages": state["messages"]}
    )
    return {"messages": response}


graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("consult_user", financial_alphavantage_assistant)
graph_builder.add_node("write_streamlit_page", write_streamlit_page_expert)
graph_builder.add_node("fetch_data_with_alphavantage_tools", ToolNode(alphavantage_tools))
graph_builder.add_node("write_streamlit_page_tools", ToolNode(code_writing_tools))

# Tie nodes with edges
graph_builder.add_edge(START, "consult_user")
graph_builder.add_conditional_edges(
    "consult_user",
    tools_condition,
    {"__end__": "__end__", "tools": "fetch_data_with_alphavantage_tools"},
)
graph_builder.add_edge("fetch_data_with_alphavantage_tools", "write_streamlit_page")
graph_builder.add_edge("write_streamlit_page", "write_streamlit_page_tools")
graph_builder.add_edge("write_streamlit_page_tools", END)

assistant_workflow = graph_builder.compile()
