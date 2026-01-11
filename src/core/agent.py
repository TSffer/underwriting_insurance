from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from src.core.tools.comparator import compare_policies
from src.core.tools.rag_tool import consult_policy


def get_agent_executor():
    """
    Inicializa y retorna el agente ejecutor usando LangGraph.
    """
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    tools = [compare_policies, consult_policy]

    agent_executor = create_react_agent(llm, tools)

    return agent_executor
