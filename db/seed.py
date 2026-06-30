"""
Populate the database with sample ecommerce/inventory data.
Run: PYTHONPATH=. .venv/bin/python db/seed.py
Clears existing data and re-seeds fresh each run.
"""
import random
from datetime import datetime, timedelta
from db.database import SessionLocal, engine, Base
from db.models import Category, Supplier, Product, Inventory, Customer, Order, OrderItem

Base.metadata.create_all(engine)

db = SessionLocal()

# Clear existing data in dependency order
db.query(OrderItem).delete()
db.query(Order).delete()
db.query(Inventory).delete()
db.query(Product).delete()
db.query(Customer).delete()
db.query(Supplier).delete()
db.query(Category).delete()
db.commit()

# ── Categories ────────────────────────────────────────────────
categories = [
    Category(name="Electronics", description="Gadgets and devices"),
    Category(name="Clothing", description="Apparel and accessories"),
    Category(name="Books", description="Physical and digital books"),
    Category(name="Home & Kitchen", description="Household items"),
    Category(name="Sports", description="Sports and outdoor equipment"),
    Category(name="Beauty", description="Skincare and personal care"),
    Category(name="Toys", description="Children's toys and games"),
]
db.add_all(categories)
db.commit()

# ── Suppliers ─────────────────────────────────────────────────
suppliers = [
    Supplier(name="TechSource Ltd",   email="tech@source.com",       country="USA"),
    Supplier(name="FashionHub",       email="info@fashionhub.com",   country="Italy"),
    Supplier(name="BookWorld",        email="orders@bookworld.com",  country="UK"),
    Supplier(name="HomeGoods Co",     email="supply@homegoods.com",  country="Germany"),
    Supplier(name="SportsPro",        email="contact@sportspro.com", country="Australia"),
    Supplier(name="GlowBeauty",       email="hello@glowbeauty.com",  country="South Korea"),
    Supplier(name="ToyFactory",       email="info@toyfactory.com",   country="China"),
]
db.add_all(suppliers)
db.commit()

# ── Products + Inventory ──────────────────────────────────────
# (name, sku, price, category, supplier, stock_qty, reorder_level)
products_data = [
    # Electronics
    ("Wireless Headphones",    "ELEC-001", 79.99,  "Electronics",   "TechSource Ltd",  45,  10),
    ("Bluetooth Speaker",      "ELEC-002", 49.99,  "Electronics",   "TechSource Ltd",   5,  10),
    ("Laptop Stand",           "ELEC-003", 29.99,  "Electronics",   "TechSource Ltd",   0,   5),
    ("USB-C Hub 7-Port",       "ELEC-004", 39.99,  "Electronics",   "TechSource Ltd",  60,  15),
    ("Mechanical Keyboard",    "ELEC-005", 119.99, "Electronics",   "TechSource Ltd",  22,  10),
    ("Webcam 4K",              "ELEC-006", 89.99,  "Electronics",   "TechSource Ltd",   3,   8),
    # Clothing
    ("Running Shoes",          "CLO-001",  89.99,  "Clothing",      "FashionHub",      30,   8),
    ("Winter Jacket",          "CLO-002", 149.99,  "Clothing",      "FashionHub",      12,   5),
    ("Cotton T-Shirt",         "CLO-003",  19.99,  "Clothing",      "FashionHub",      80,  20),
    ("Slim Fit Jeans",         "CLO-004",  59.99,  "Clothing",      "FashionHub",      35,  10),
    ("Sports Socks (5-pack)",  "CLO-005",  14.99,  "Clothing",      "FashionHub",       0,  15),
    # Books
    ("Python Crash Course",    "BOOK-001", 39.99,  "Books",         "BookWorld",      100,  20),
    ("Clean Code",             "BOOK-002", 44.99,  "Books",         "BookWorld",        0,  10),
    ("Designing Data Systems", "BOOK-003", 54.99,  "Books",         "BookWorld",       40,  10),
    ("Atomic Habits",          "BOOK-004", 29.99,  "Books",         "BookWorld",       55,  15),
    ("Deep Work",              "BOOK-005", 24.99,  "Books",         "BookWorld",       20,  10),
    # Home & Kitchen
    ("Coffee Maker",           "HOME-001", 59.99,  "Home & Kitchen","HomeGoods Co",    20,   5),
    ("Air Purifier",           "HOME-002", 129.99, "Home & Kitchen","HomeGoods Co",     8,   3),
    ("Blender Pro",            "HOME-003", 79.99,  "Home & Kitchen","HomeGoods Co",    15,   5),
    ("Stainless Steel Pans",   "HOME-004", 89.99,  "Home & Kitchen","HomeGoods Co",     0,   5),
    # Sports
    ("Yoga Mat",               "SPORT-001", 34.99, "Sports",        "SportsPro",        7,   8),
    ("Resistance Bands",       "SPORT-002", 19.99, "Sports",        "SportsPro",       50,  15),
    ("Dumbbells 10kg",         "SPORT-003", 44.99, "Sports",        "SportsPro",       18,   5),
    ("Jump Rope",              "SPORT-004",  9.99, "Sports",        "SportsPro",       90,  20),
    # Beauty
    ("Vitamin C Serum",        "BEAU-001",  29.99, "Beauty",        "GlowBeauty",      60,  15),
    ("Moisturizer SPF50",      "BEAU-002",  24.99, "Beauty",        "GlowBeauty",       4,  10),
    ("Face Wash Gel",          "BEAU-003",  14.99, "Beauty",        "GlowBeauty",      35,  12),
    # Toys
    ("LEGO City Set",          "TOY-001",   69.99, "Toys",          "ToyFactory",      25,   8),
    ("Remote Control Car",     "TOY-002",   49.99, "Toys",          "ToyFactory",       0,   5),
    ("Board Game - Strategy",  "TOY-003",   39.99, "Toys",          "ToyFactory",      30,  10),
]

cat_map = {c.name: c for c in categories}
sup_map = {s.name: s for s in suppliers}

products = []
for name, sku, price, cat, sup, qty, reorder in products_data:
    p = Product(name=name, sku=sku, price=price,
                category=cat_map[cat], supplier=sup_map[sup])
    db.add(p)
    db.flush()
    db.add(Inventory(product=p, quantity=qty, reorder_level=reorder))
    products.append(p)
db.commit()

# ── Customers ─────────────────────────────────────────────────
customers_data = [
    ("Alice Rahman",    "alice@example.com",   "Bangladesh"),
    ("Bob Smith",       "bob@example.com",     "USA"),
    ("Clara Müller",    "clara@example.com",   "Germany"),
    ("David Chen",      "david@example.com",   "China"),
    ("Eva López",       "eva@example.com",     "Spain"),
    ("Farhan Hossain",  "farhan@example.com",  "Bangladesh"),
    ("Grace Kim",       "grace@example.com",   "South Korea"),
    ("Henry Walker",    "henry@example.com",   "UK"),
    ("Iris Tanaka",     "iris@example.com",    "Japan"),
    ("James Okafor",    "james@example.com",   "Nigeria"),
    ("Karen Singh",     "karen@example.com",   "India"),
    ("Leo Rossi",       "leo@example.com",     "Italy"),
    ("Maria Santos",    "maria@example.com",   "Brazil"),
    ("Noor Al-Rashid",  "noor@example.com",    "UAE"),
    ("Oscar Petrov",    "oscar@example.com",   "Russia"),
]
customers = [Customer(name=n, email=e, country=c) for n, e, c in customers_data]
db.add_all(customers)
db.commit()

# ── Orders + Order Items (spread over last 6 months) ──────────
statuses = ["delivered", "delivered", "delivered", "shipped", "pending", "cancelled"]

def random_past_date(days_back: int = 180) -> datetime:
    return datetime.now() - timedelta(days=random.randint(0, days_back))

for customer in customers:
    num_orders = random.randint(1, 5)
    for _ in range(num_orders):
        items_sample = random.sample(products, random.randint(1, 4))
        status = random.choice(statuses)
        order = Order(customer=customer, status=status)
        db.add(order)
        db.flush()
        total = 0
        for product in items_sample:
            qty = random.randint(1, 5)
            item = OrderItem(
                order=order,
                product=product,
                quantity=qty,
                unit_price=float(product.price),
            )
            db.add(item)
            total += qty * float(product.price)
        order.total_amount = round(total, 2)
        order.created_at = random_past_date()

db.commit()
db.close()

print("Done — seeded:")
print(f"  {len(categories)} categories")
print(f"  {len(suppliers)} suppliers")
print(f"  {len(products_data)} products")
print(f"  {len(customers)} customers")
print("  orders seeded for each customer (1–5 each)")
