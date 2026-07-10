"""Evaluate an LLM's answer to a question using an OpenRouter model as judge."""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

JUDGE_SYSTEM_PROMPT = """
You are a strict evaluator grading an LLM's answer to a user's question.
Score the answer from 1 (very poor) to 10 (excellent) based on two factors combined:
- Accuracy: is the answer factually correct and does it actually address the question?
- Performance: is it clear, complete, relevant, and well-structured?
Give a single overall mark that reflects both factors together, plus a short
justification for each. Be strict and honest - do not inflate scores.

Respond with ONLY a JSON object matching this exact shape, no other text:
{"score": <integer 1-10>, "accuracy_notes": "<string>", "performance_notes": "<string>"}
"""


class EvaluationResult(BaseModel):
    score: int = Field(ge=1, le=10, description="Single overall mark covering accuracy and performance")
    accuracy_notes: str = Field(description="Brief note on factual correctness relative to the question")
    performance_notes: str = Field(description="Brief note on clarity, completeness, and relevance")


def evaluate_response(question: str, response: str, model: str = "google/gemini-2.5-flash") -> EvaluationResult:
    """Grade an LLM response to a question, returning a single 1-10 mark."""
    completion = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": f"Question:\n{question}\n\nLLM Response:\n{response}"},
        ],
    )
    content = completion.choices[0].message.content
    if content is None:
        raise ValueError("Judge model returned an empty response")
    return EvaluationResult(**json.loads(content))


def render_evaluation(question: str, response: str, result: EvaluationResult) -> None:
    console = Console()
    console.print(Panel(question, title="Question", expand=False))
    console.print(Panel(response, title="LLM Response", expand=False))
    console.print(Panel(
        f"Score: {result.score}/10\n\n"
        f"Accuracy: {result.accuracy_notes}\n\n"
        f"Performance: {result.performance_notes}",
        title="Evaluation",
        expand=False,
    ))


if __name__ == "__main__":
    question = "What is the capital of France?"
    response = "The capital of France is Paris, a city known for the Eiffel Tower."

    result = evaluate_response(question, response)
    render_evaluation(question, response, result)
