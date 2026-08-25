"""
Q: Handle follow-up questions in RAG -- a question like "how did he do it?"
doesn't carry enough standalone meaning for retrieval. Keep a running chat
history and make sure the retrieval query for a follow-up gets resolved into
a standalone question (e.g. via an explicit rewrite step, or -- as done here
-- by giving a tool-calling agent full conversation memory so it writes a
self-contained query itself when it decides to call the RAG tool).
"""

# Dependencies
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.tools import tool
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage
load_dotenv()

# LLM and embedding model
llm = ChatOpenAI(model='gpt-4o-mini')
embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

# Read the file content
txt_file_path = r'C:\Users\visha\agentic-AI\notes_using_claude\agents-from-scratch\docs\crow_and_fox.txt'
with open(txt_file_path, encoding='utf-8', mode='r') as txt_file:
    txt_file_contents = txt_file.read()

# Chunking documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 100
)
documents = splitter.create_documents([txt_file_contents])

# Vector store creation and ingestion
vector_store = Chroma(
    collection_name='fox_and_crow_story',
    embedding_function=embeddings
)

vector_store.add_documents(documents)

# retriever setup
retriever = vector_store.as_retriever(
    search_type='mmr', search_kwargs={'k':2, 'fetch_k':6}
)

@tool
def rag_tool(query:str):
    """Tool used to retrieve data from crow and fox story"""
    retrieved_contents = retriever.invoke(query)
    contents = "\n\n".join([doc.page_content for doc in retrieved_contents])
    return contents

tools = [rag_tool]
llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages : Annotated[list, add_messages]
    
def chatbot(state:State):
    messages = state['messages']
    prompt = """
    You are an smart AI assistant helpful in chossing rightfull tool
    Strictly use RAG tool for question related to crow and fox story.
    For generic question use your knowledge to answer the questions
    """
    result = llm_with_tools.invoke(
        [
            SystemMessage(content=prompt), *messages
        ]
    )
    return {
        "messages" : [result]
    }
    
graph = StateGraph(State)

graph.add_node('chatbot', chatbot)
graph.add_node('tool_node', ToolNode(tools))

graph.add_edge(START, 'chatbot')
graph.add_conditional_edges(
    'chatbot',
    tools_condition,
    {'tools':'tool_node', "__end__":END}
)
graph.add_edge('tool_node', 'chatbot')

app = graph.compile(checkpointer=MemorySaver())

def run(thread_id):
    query = str(input("Query: "))
    while query != 'OVER':
        for event in app.stream(
            {'messages':[
                HumanMessage(content=query)
            ]}, stream_mode='values', 
            config={'configurable': {'thread_id':f"{thread_id}"}}
        ):
            event['messages'][-1].pretty_print()
        query = str(input("Query: "))
        
if __name__ == "__main__":
    run("1")