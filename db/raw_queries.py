from sqlalchemy import text
from db.database import engine


def run(sql: str, params: dict = {}):
    with engine.connect() as conn:
        result = conn.execute(text(sql), params)
        return result.fetchall()


if __name__ == "__main__":

    # ── Simple select ─────────────────────────────────────────
    rows = run("SELECT name, price FROM products LIMIT 5")
    for row in rows:
        print(row.name, row.price)

    # ── With WHERE filter ─────────────────────────────────────
    rows = run(
        "SELECT name, price FROM products WHERE price > :min_price",
        {"min_price": 50}
    )
    for row in rows:
        print(row.name, row.price)

    # ── JOIN ──────────────────────────────────────────────────
    rows = run("""
        SELECT p.name, p.price, c.name AS category
        FROM products p
        JOIN categories c ON c.id = p.category_id
        ORDER BY p.price DESC
        LIMIT 5
    """)
    for row in rows:
        print(row.name, row.price, row.category)

    # ── Aggregation ───────────────────────────────────────────
    rows = run("""
        SELECT c.name AS category, SUM(oi.quantity * oi.unit_price) AS revenue
        FROM categories c
        JOIN products p ON p.category_id = c.id
        JOIN order_items oi ON oi.product_id = p.id
        JOIN orders o ON o.id = oi.order_id
        WHERE o.status != 'cancelled'
        GROUP BY c.name
        ORDER BY revenue DESC
    """)
    for row in rows:
        print(row.category, round(float(row.revenue), 2))
