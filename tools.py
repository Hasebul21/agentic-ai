from db.raw import run_sql
from langchain_core.tools import Tool

def get_all_inventory(_: str = "") -> list:
    rows = run_sql("""
                   SELECT name, quantity FROM inventory
                   JOIN products ON inventory.product_id = products.id
                   WHERE products.is_active = true
                   ORDER BY quantity desc
                   LIMIT 5""")
    return rows


def get_inventory_by_product_id(product_id: int):
    rows = run_sql(
        "SELECT id, quantity FROM inventory WHERE product_id = :product_id",
        {"product_id": 11},
    )
    return rows


def get_product_by_price_and_status(price: int, isActive: bool) -> list:
    rows = run_sql(
        """ SELECT * FROM products WHERE 
        price < :price AND is_active =:isActive
        ORDER BY price desc """,
        {"price": price, "isActive": isActive},
    )
    return rows


def get_customer_by_country(country: str):
    rows = run_sql(
        "SELECT * FROM customers WHERE country =:country", {"country": country}
    )
    return rows

top_inventory_tool = Tool(
    name="get_top_inventory",
    func=get_all_inventory,
    description="Get the top 5 items from the inventory with the highest quantity.",
)

find_customer_by_country_tool = Tool(
    name="find_customer_by_country",
    func=get_customer_by_country,
    description="Get all customers from a specific country.",
)

tools = [top_inventory_tool, find_customer_by_country_tool]

if __name__ == "__main__":
    res = get_all_inventory()
    print(res)
