from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
import json

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3-32b",
    reasoning_format = "hidden"
)

parser = JsonOutputParser()

template = PromptTemplate(
    template='Tell me the net worth, address, education, background of {username} \n {format_instructions}',
    input_variables = ['username'],
    partial_variables = {'format_instructions' : parser.get_format_instructions()},
    validate_template = True

)


print(template.invoke({'username': 'Mark Zuckerberg'}))

chain = template | llm | parser

response = chain.invoke({'username': 'Mark Zuckerberg'})

# Plain indented output — no colors, just clean structure
print(json.dumps(response, indent=2, ensure_ascii=False))



