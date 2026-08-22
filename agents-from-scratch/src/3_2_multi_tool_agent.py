"""
Q: Give one agent two tools -- a RAG tool (crow-and-fox retriever) and Tavily
web search -- and see whether it picks the right tool per query: RAG for the
story, web search for current info, neither for general questions.
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage
load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')
embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
tavily_tool = TavilySearch(max_results=5)

txt_file_path = r'C:\Users\visha\agentic-AI\notes_using_claude\agents-from-scratch\docs\crow_and_fox.txt'
with open(txt_file_path, encoding='utf-8', mode='r') as txt_file:
    txt_contents = txt_file.read()
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
documents = splitter.create_documents([txt_contents])

vector_store = Chroma(
    collection_name='fox_crow_story',
    embedding_function=embeddings
)

vector_store.add_documents(
    documents=documents
)

retriever = vector_store.as_retriever(
    search_type = 'mmr', search_kwargs={'k':2, 'fetch_k':5}
)

@tool
def rag_tool(query:str):
    "Retrieves data about crow and fox story"
    retrieved_documents = retriever.invoke(query)
    content = "\n\n".join([doc.page_content for doc in retrieved_documents])
    return content


@tool
def web_search_tool(query:str):
    "Performs web search for the given query"
    results = tavily_tool.invoke(query)
    return "\n\n".join([res['content'] for res in results['results']])

tools = [rag_tool, web_search_tool]

system_prompt = """
You are a helpful and smart assistant with access to a RAG tool and a web search tool.
Use the RAG tool when the user asks something about the Crow and Fox story.
Use the web search tool when the user asks about something current, recent, or needs information from the internet.
For simple questions, greetings, or anything you can answer on your own, don't use any tool.
Choose the appropriate tool only when needed, and use the information from the tool to answer the user's question naturally.
"""


#-----------------------#
agent = create_agent(model=llm,
                     tools=tools,
                     system_prompt=system_prompt)



def run(query:str):
    print(f"--------{query.upper()}---------")
    inputs = {'messages':HumanMessage(content=query)}
    for chunk in agent.stream(inputs, stream_mode="updates"):
        for node, update in chunk.items():
            # Tool was used
            if node == "tools":
                print("Tool used:", end=" ")
                for message in update["messages"]:
                    print(message.name)
            # Final model response
            if node == "model":
                for message in update["messages"]:
                    if message.content:
                        print("Answer:", message.content)
                        
if __name__ == "__main__":
    queries = [
            'Whats the weather in chennai?',
            'Why did fox decieve the crow',
            'Who is Graham bell'
            ]
    for query in queries:
        run(query=query)