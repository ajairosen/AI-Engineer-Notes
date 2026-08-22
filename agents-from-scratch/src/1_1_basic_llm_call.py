"""
Q: Write the minimal LangChain code to send a single prompt to a chat model
and print the response.
"""

from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model='gpt-4o-mini')

def main():
    
    result = llm.invoke('Whats 2+ 3?')
    return result.content

if __name__ == "__main__":
    result = main()
    print(result)