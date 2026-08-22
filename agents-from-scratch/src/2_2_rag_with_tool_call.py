"""
Q: Wrap a RAG retrieval step as a LangChain tool, bind it to the LLM, and let
the model decide whether to call it based on the question — handle the
tool-call loop (LLM emits tool call -> execute -> feed result back -> final
answer) and show one query that should trigger retrieval and one that shouldn't.
"""

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import uuid
from langchain.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')
embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

# Get documents
current_dir = Path(__file__).resolve().parent.parent
document_path = current_dir / "docs" / "crow_and_fox.txt"
with open(document_path, 'r', encoding='utf-8') as document:
    docs = document.read()  
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500, chunk_overlap=100)
texts = splitter.create_documents([docs])

# Vector Store
vector_store = Chroma(
    collection_name='Crow_and_Fox_Story',
    collection_metadata={
        'description': "The story about crow and fox"
    },
    embedding_function=embeddings
)
vector_store.add_documents(ids=[str(uuid.uuid4()) for _ in range(len(texts))], documents=texts)
retriever = vector_store.as_retriever(search_type='mmr', search_kwargs={'k':3, "fetch_k":10})

@tool("RAG_tool")
def rag_tool(query:str):
    """RAG context from crow and fox story"""
    retrieved_content = retriever.invoke(query)
    content = "\n\n".join([doc.page_content for doc in retrieved_content])
    return content

llm_with_tools = llm.bind_tools([rag_tool])

def answer(query: str) -> str:
    messages = [
        SystemMessage(
            content="""Answer the user's question.
            Use the RAG tool when the question requires information
            from the Crow and Fox story.
            For general conversation, answer directly."""
        ),
        HumanMessage(content=query)
    ]

    result = llm_with_tools.invoke(messages)
    if result.tool_calls:
        messages.append(result)
        for tool_call in result.tool_calls:
            tool_result = rag_tool.invoke(tool_call)
            messages.append(tool_result)
        result = llm_with_tools.invoke(messages)

    return result.content

if __name__ == "__main__":
    print(answer('How did Fox deceive the crow?'))
    print(answer('Hi, how are you?'))


    