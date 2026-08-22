"""
Q: Build the smallest end-to-end RAG pipeline: load source text, split into
chunks, embed + store in a vector store, retrieve relevant chunks for a
query, and pass retrieved context + query to the LLM for an answer.
"""

# Dependencies
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import uuid

# Load Env variables
from dotenv import load_dotenv
load_dotenv()

# llm and embeddings
llm = ChatOpenAI(model='gpt-4o-mini')
embeddings = OpenAIEmbeddings(model='text-embedding-3-large')


# Get documents
current_dir = Path(__file__).resolve().parent.parent
document_path = current_dir / "docs" / "crow_and_fox.txt"
with open(document_path, 'r', encoding='utf-8') as document:
    docs = document.read()  
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500, chunk_overlap=100)
texts = splitter.create_documents([docs])
# print(texts)

# Vector Store
vector_store = Chroma(
    collection_name='sample-RAG',
    embedding_function=embeddings
)
vector_store.add_documents(ids=[str(uuid.uuid4()) for _ in range(len(texts))], documents=texts)

retriever = vector_store.as_retriever(search_type='mmr', search_kwargs={'k':3, "fetch_k":10})

def main():
    
    query = "What did the fox do?"
    
    retrieved_docs = retriever.invoke(query)
    content = "\n\n".join([doc.page_content.strip() for doc in retrieved_docs])
    
    prompt = f"""
    Answer for the query based on the content given:
    content : {content}
    question: {query}
    """
    
    result = llm.invoke(prompt)
    
    return result.content

if __name__ == "__main__":
    print(main())
    