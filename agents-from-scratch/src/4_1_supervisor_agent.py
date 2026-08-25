from langchain_openai import ChatOpenAI
from typing import Literal, TypedDict, Annotated
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

class Supervisor(BaseModel):
    next: Literal['rag', 'get_weather', 'base_llm'] = Field(
        description="""
        Return:
        rag: If the user is asking some question about crow and fox story
        get_weather: if the user is asking about weather information
        base_llm: if the user's question is generic with respect to llm's knowledge
        """ 
    )
    
llm_w_structured = llm.with_structured_output(Supervisor)


class State(TypedDict):
    messages : Annotated[list, add_messages]
    next : str
    
def supervisor_node(state:State):
    messages = state['messages']
    prompt = """
    Use any of the these following tool to get the job done
    rag: Users question is about fox and crow story.
    get_weather: Users question is about weather
    base_llm: Users question is about generic questions
    """
    response = llm_w_structured.invoke(
        [prompt] + messages
    )
    
    return {'next': response.next}

def rag_node(state:State):
    last_user_message = next(
        message
        for message in reversed(state['messages'])
        if isinstance(message, HumanMessage)
    )
    
        