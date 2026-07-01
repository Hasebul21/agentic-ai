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


def detailed_report(_: str = "") -> list:
    rows = run_sql(
        """
        SELECT p.name as product_name, p.price as product_price,
        s."name" as supplier_name, s.country as supplier_country,
        oi.quantity as ordered_quantity, oi.unit_price as ordered_price, ord.total_amount as ordered_total_amount,
        ord.status as current_status, c.country as customer_country
        FROM products p
        JOIN suppliers s ON s.id = p.supplier_id
        JOIN order_items oi ON oi.product_id = p.id
        JOIN orders as ord ON ord.id = oi.order_id
        JOIN customers as c ON c.id = ord.customer_id
        """
    )
    return rows


def get_purchases_by_customer_country(_: str = "") -> list:
    rows = run_sql(
        """
        SELECT c.country as country, COUNT(*) as total_purchases
        FROM order_items oi
        JOIN orders ord ON ord.id = oi.order_id
        JOIN customers c ON c.id = ord.customer_id
        GROUP BY c.country
        ORDER BY c.country
        """
    )
    return rows


def get_order_items_by_supplier_country(_: str = "") -> list:
    rows = run_sql(
        """
        SELECT s.country as country, COUNT(*) as total_order_items
        FROM order_items oi
        JOIN products p ON p.id = oi.product_id
        JOIN suppliers s ON s.id = p.supplier_id
        GROUP BY s.country
        ORDER BY s.country
        """
    )
    return rows


def get_order_count_by_status(_: str = "") -> list:
    rows = run_sql(
        """
        SELECT status, COUNT(*) as total_orders
        FROM orders
        GROUP BY status
        ORDER BY status
        """
    )
    return rows

annual_report = Tool(
    name="annual_report",
    func=detailed_report,
    description="Generate a detailed annual report including product, supplier, order, and customer information.",
)
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

purchases_by_customer_country_tool = Tool(
    name="get_purchases_by_customer_country",
    func=get_purchases_by_customer_country,
    description="Get the exact total number of order items (purchases) grouped by customer country. Use this for country-wise customer purchase totals instead of counting rows manually.",
)

order_items_by_supplier_country_tool = Tool(
    name="get_order_items_by_supplier_country",
    func=get_order_items_by_supplier_country,
    description="Get the exact total number of order items grouped by supplier country. Use this for country-wise supplier audit totals instead of counting rows manually.",
)

order_count_by_status_tool = Tool(
    name="get_order_count_by_status",
    func=get_order_count_by_status,
    description="Get the exact total number of orders grouped by order status. Use this for the order status audit instead of counting rows manually.",
)


tools = [
    top_inventory_tool,
    find_customer_by_country_tool,
    annual_report,
    purchases_by_customer_country_tool,
    order_items_by_supplier_country_tool,
    order_count_by_status_tool,
]

if __name__ == "__main__":
    res = detailed_report()
    print(res)
