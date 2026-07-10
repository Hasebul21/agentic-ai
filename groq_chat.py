from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

from evaluator import evaluate_response, render_evaluation

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3-32b",
)


template = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a {system_input} expert and keep the answer short and concise under 3 lines"),
        ("user", "Tell me about {user_input} in short and concise manner"),
    ]
)

prompts = template.format_messages(
    system_input="mathematics",
    user_input="circle area",
)

#print(prompts)

response = llm.invoke(prompts)
#print(response.content)


examples = [
    {"input": "Bangladesh", "output":"BDT"},
    {"input": "Algeria", "output":"DZD"},
    {"input": "Greece", "output":"EUR"}
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai" , "{output}")
    ]
)


few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

#print("Few shot prompt: ", few_shot_prompt.format())
prompts = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert and keep the answer short and concise under 3 lines"),
        few_shot_prompt,
        ("human", "Give me the output for {user_input}?"),
    ]
)

final_prompt = prompts.format_messages(
    user_input="HONDURAS"
)

#response = llm.invoke(final_prompt)
#print(response.content)

def outputParser():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert and keep the answer short and concise under 1 lines. "
            "Dont give me anything else except the answer. I dont want to see thinking, processing, or any other text. Just give me the answer."),
            ("human", "Give me a short and concise joke about {topic}?")
        ]
    )
    llm = ChatGroq(
        model="qwen/qwen3-32b",
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    question = "Give me a short and concise joke about programming?"
    result = chain.invoke({"topic": "programming"})
    print(result)

    evaluation = evaluate_response(question, result)
    render_evaluation(question, result, evaluation)

if __name__ == "__main__":
    outputParser()
