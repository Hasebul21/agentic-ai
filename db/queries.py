"""
Query examples — Easy / Medium / Complex
Run: python db/queries.py
"""
from sqlalchemy import func, desc, case, and_, or_
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Product, Category, Supplier, Inventory, Customer, Order, OrderItem


def get_db() -> Session:
    return SessionLocal()


# ══════════════════════════════════════════════════════════════
# EASY
# ══════════════════════════════════════════════════════════════

def easy_1_all_products(db: Session):
    """Get all active products."""
    return db.query(Product).filter(Product.is_active == True).all()


def easy_2_products_by_category(db: Session, category_name: str):
    """Get products in a specific category."""
    return (
        db.query(Product)
        .join(Category)
        .filter(Category.name == category_name)
        .all()
    )


def easy_3_low_stock(db: Session):
    """Products where stock is at or below reorder level."""
    return (
        db.query(Product, Inventory)
        .join(Inventory)
        .filter(Inventory.quantity <= Inventory.reorder_level)
        .all()
    )


def easy_4_orders_by_status(db: Session, status: str):
    """Get all orders with a given status."""
    return db.query(Order).filter(Order.status == status).all()


def easy_5_customer_orders(db: Session, customer_id: int):
    """Get all orders for a customer."""
    return db.query(Order).filter(Order.customer_id == customer_id).all()


# ══════════════════════════════════════════════════════════════
# MEDIUM
# ══════════════════════════════════════════════════════════════

def medium_1_total_revenue_per_category(db: Session):
    """Total revenue grouped by category."""
    return (
        db.query(Category.name, func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"))
        .join(Product, Product.category_id == Category.id)
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(Order.status != "cancelled")
        .group_by(Category.name)
        .order_by(desc("revenue"))
        .all()
    )


def medium_2_top_customers(db: Session, limit: int = 5):
    """Top customers by total spend."""
    return (
        db.query(Customer.name, Customer.email, func.sum(Order.total_amount).label("total_spent"))
        .join(Order)
        .filter(Order.status.in_(["shipped", "delivered"]))
        .group_by(Customer.id, Customer.name, Customer.email)
        .order_by(desc("total_spent"))
        .limit(limit)
        .all()
    )


def medium_3_product_sales_count(db: Session):
    """Number of units sold per product."""
    return (
        db.query(Product.name, Product.sku, func.sum(OrderItem.quantity).label("units_sold"))
        .join(OrderItem)
        .join(Order)
        .filter(Order.status != "cancelled")
        .group_by(Product.id, Product.name, Product.sku)
        .order_by(desc("units_sold"))
        .all()
    )


def medium_4_out_of_stock_products(db: Session):
    """Products with zero stock."""
    return (
        db.query(Product.name, Product.sku, Category.name.label("category"), Inventory.quantity)
        .join(Category)
        .join(Inventory)
        .filter(Inventory.quantity == 0)
        .all()
    )


def medium_5_orders_per_month(db: Session):
    """Count orders per month."""
    return (
        db.query(
            func.date_trunc("month", Order.created_at).label("month"),
            func.count(Order.id).label("order_count"),
            func.sum(Order.total_amount).label("total_revenue"),
        )
        .group_by("month")
        .order_by("month")
        .all()
    )


# ══════════════════════════════════════════════════════════════
# COMPLEX
# ══════════════════════════════════════════════════════════════

def complex_1_customer_rfm(db: Session):
    """
    RFM Analysis — Recency, Frequency, Monetary value per customer.
    Useful for customer segmentation.
    """
    return (
        db.query(
            Customer.name,
            Customer.email,
            func.max(Order.created_at).label("last_order_date"),
            func.count(Order.id).label("frequency"),
            func.sum(Order.total_amount).label("monetary"),
        )
        .join(Order)
        .filter(Order.status != "cancelled")
        .group_by(Customer.id, Customer.name, Customer.email)
        .order_by(desc("monetary"))
        .all()
    )


def complex_2_supplier_performance(db: Session):
    """
    Supplier performance — how much revenue each supplier's products generate,
    and how many of their products are low on stock.
    """
    low_stock = (
        db.query(Product.supplier_id, func.count(Product.id).label("low_stock_count"))
        .join(Inventory)
        .filter(Inventory.quantity <= Inventory.reorder_level)
        .group_by(Product.supplier_id)
        .subquery()
    )

    return (
        db.query(
            Supplier.name.label("supplier"),
            func.count(Product.id).label("total_products"),
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("total_revenue"),
            low_stock.c.low_stock_count,
        )
        .join(Product, Product.supplier_id == Supplier.id)
        .join(OrderItem, OrderItem.product_id == Product.id)
        .outerjoin(low_stock, low_stock.c.supplier_id == Supplier.id)
        .group_by(Supplier.id, Supplier.name, low_stock.c.low_stock_count)
        .order_by(desc("total_revenue"))
        .all()
    )


def complex_3_repeat_vs_one_time_customers(db: Session):
    """
    Split customers into repeat buyers vs one-time buyers
    and compute average order value for each group.
    """
    order_counts = (
        db.query(Customer.id, func.count(Order.id).label("order_count"))
        .join(Order)
        .group_by(Customer.id)
        .subquery()
    )

    return (
        db.query(
            case((order_counts.c.order_count > 1, "repeat"), else_="one-time").label("customer_type"),
            func.count(order_counts.c.id).label("customer_count"),
            func.avg(order_counts.c.order_count).label("avg_orders"),
        )
        .group_by("customer_type")
        .all()
    )


def complex_4_product_never_ordered(db: Session):
    """Products that have never been ordered (potential dead stock)."""
    ordered_ids = db.query(OrderItem.product_id).distinct().subquery()
    return (
        db.query(Product.name, Product.sku, Category.name.label("category"), Inventory.quantity)
        .join(Category)
        .join(Inventory)
        .filter(Product.id.not_in(ordered_ids))
        .all()
    )


def complex_5_category_growth(db: Session):
    """
    Month-over-month revenue growth per category.
    Uses a self-join via subquery to compare current vs previous month.
    """
    monthly = (
        db.query(
            Category.name.label("category"),
            func.date_trunc("month", Order.created_at).label("month"),
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"),
        )
        .join(Product, Product.category_id == Category.id)
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(Order.status != "cancelled")
        .group_by(Category.name, "month")
        .order_by(Category.name, "month")
        .all()
    )
    return monthly


# ══════════════════════════════════════════════════════════════
# Runner
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    db = get_db()

    print("\n── EASY 1: Active products ──────────────────────────")
    for p in easy_1_all_products(db)[:3]:
        print(f"  {p.sku} | {p.name} | ${p.price}")

    print("\n── EASY 3: Low stock ────────────────────────────────")
    for p, inv in easy_3_low_stock(db):
        print(f"  {p.name}: {inv.quantity} units (reorder at {inv.reorder_level})")

    print("\n── MEDIUM 1: Revenue by category ────────────────────")
    for cat, rev in medium_1_total_revenue_per_category(db):
        print(f"  {cat}: ${rev:.2f}")

    print("\n── MEDIUM 2: Top 5 customers ────────────────────────")
    for name, email, spent in medium_2_top_customers(db):
        print(f"  {name} ({email}): ${spent:.2f}")

    print("\n── COMPLEX 1: RFM Analysis ──────────────────────────")
    for name, email, last, freq, money in complex_1_customer_rfm(db):
        print(f"  {name} | orders={freq} | spent=${money:.2f} | last={last}")

    print("\n── COMPLEX 4: Products never ordered ────────────────")
    for name, sku, cat, qty in complex_4_product_never_ordered(db):
        print(f"  {name} ({sku}) | {cat} | stock={qty}")

    db.close()
