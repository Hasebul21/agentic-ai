from db.raw import run_sql


def get_all_inventory():
    rows = run_sql(
        "SELECT id, quantity FROM inventory LIMIT 5"
    )
    return rows

def get_inventory_by_product_id(product_id: int):
    rows = run_sql(
        "SELECT id, quantity FROM inventory WHERE product_id = :product_id",
        {"product_id": 11}
        
    )
    return rows


if __name__ == "__main__":
    inventory = get_all_inventory()
    print(inventory)
    product_ = get_inventory_by_product_id(1)
    print(product_)