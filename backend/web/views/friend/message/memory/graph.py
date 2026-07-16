import os
from typing import Annotated, Sequence

from langgraph.constants import START, END

from langgraph.graph.state import StateGraph

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from typing_extensions import TypedDict

from langchain_openai.chat_models.base import ChatOpenAI


class MemoryGraph:
    @staticmethod
    def create_app():
        llm=ChatOpenAI(
            model='deepseek-v4-pro',
            openai_api_key=os.getenv('API_KEY'),
            openai_api_base=os.getenv('API_BASE'),
        )
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]

        def model_call(state: AgentState)->AgentState:
            res=llm.invoke(state['messages'])
            return {'messages':[res]}
        graph=StateGraph(AgentState)
        graph.add_node('agent',model_call)
        graph.add_edge(START,'agent')
        graph.add_edge('agent',END)
        return graph.compile()