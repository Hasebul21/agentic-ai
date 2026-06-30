from db.raw import run_sql


def get_all_inventory():
    rows = run_sql(
        "SELECT id, quantity FROM inventory"
    )
    return rows




if __name__ == "__main__":
    get_all_inventory()
    