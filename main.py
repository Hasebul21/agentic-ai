from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools import tools

load_dotenv()

class Answer(BaseModel):
    summary: str
    results: list
    tools_used: list
    
user_prompt_content = """
    can you give me the name of 
    the customers who are from Bangladesh and USA
    i just need name
"""

system_prompt_content = """
    You are a database manager assistant for a company.
    You will use accurate tools to query the database 
    and provide the user valid answer what he asked for.
    Dont Hellucinate or make up any answer. If you dont know the answer, 
    say "I dont know".
"""

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = {
    "messages": [
        {
            "role": "user", 
            "content": user_prompt_content
        }
      ]
    }

agent = create_agent(
    model="gpt-4o-mini",
    tools=tools,
    system_prompt=system_prompt_content,
    response_format=Answer,
)

response = agent.invoke(prompt)
print(response["structured_response"])
