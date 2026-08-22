"""
Q: Force the LLM to return data matching a schema instead of free text --
define a Pydantic model and use LangChain's structured-output binding so
.invoke() returns a validated instance of the model, not a raw AIMessage.
"""

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

class Sentiment(BaseModel):
    sentiment: Optional[str] = Field(
        description='One of: postive, negative, neutral'
    )
    confidence : Optional[float] = Field(
        ge=0,
        le=1,
        description="Confidence score between 0 and 1"
    )

class Extraction(BaseModel):
    
    name : Optional[str] = Field(
        description="Name of the user"
        )
    date : Optional[str] = Field(
        description="Date mentioned by the user. Strictly format date as YYYY-MM-DD"
        )
    amount : Optional[int|float] = Field(
        description='Amount mentioned by the user. return integer or float value'
        )
    sentiment_with_confidence : Optional[Sentiment] = Field(
        description='Extract sentiment and confidence from users text'
        )
    
llm_with_structure_output = llm.with_structured_output(Extraction)

def run(query:str):
    return llm_with_structure_output.invoke([HumanMessage(content=query)])


if __name__ == "__main__":
    query = """His name is David Miller. Born on 14-03-1990.
    He invested $50000 last year and is really happy with the returns."""
    print(run(query=query))