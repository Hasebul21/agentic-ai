from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def invoke(user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}]
    )
    ai_response = response.choices[0].message.content

    return ai_response


if __name__ == "__main__":
    from db.raw import run_sql

    rows = run_sql(
        "SELECT id, quantity FROM inventory"
    )
    for row in rows:
        print(row.id, row.quantity)
