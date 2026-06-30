from sqlalchemy import text
from db.database import engine


def run_sql(sql: str, params: dict = {}) -> list:
    with engine.connect() as conn:
        result = conn.execute(text(sql), params)
        return result.fetchall()
