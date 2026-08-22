"""
Q: Build a single ReAct-style agent that can loop -- reason, decide to call a
tool, observe the result, and repeat until it has a final answer -- using
LangGraph (rather than manually managing the tool-call loop). Give it the
Tavily search tool so it can answer questions needing current/external info.
"""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain.tools import tool
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')
tavily_tool = TavilySearch(max_results=5)

@tool
def web_search_tool(query: str) -> str:
    """Performs web search for current information"""
    result = tavily_tool.invoke(query)
    return "\n\n".join([res['content'] for res in result['results']])

tools = [web_search_tool]

agent = create_agent(
    model=llm, tools=tools,
    system_prompt="""You are an expert at doing web search.
    Use web_search_tool whenever the query is related to current information
    or the query demands a web search."""
)

def run(query: str):
    inputs = {'messages': [HumanMessage(content=query)]}
    for chunk in agent.stream(inputs, stream_mode='updates'):
        print(chunk)

if __name__ == "__main__":
    run('Whats the current weather in Chennai?')
