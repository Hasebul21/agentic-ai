from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from tools import tools

load_dotenv()

class Response(BaseModel):
    class CountryAudit(BaseModel):
        country: str = Field(description="Country name")
        total_purchases: int = Field(description="Total number of order items purchased by customers in this country")

    class CountryWiseSupplierAudit(BaseModel):
        country: str = Field(description="Country name")
        total_supplier: int = Field(description="Total number of order items for products supplied by suppliers in this country")

    class OrderStatusAudit(BaseModel):
        status: str = Field(description="Order status")
        total_orders: int = Field(description="Total number of orders with this status")

    summary: str
    country_audit: list[CountryAudit] = Field(
        description="Country-wise breakdown of total customer purchases, from get_purchases_by_customer_country"
    )

    country_wise_supplier_audit: list[CountryWiseSupplierAudit] = Field(
        description="Country-wise breakdown of total order items by supplier country, from get_order_items_by_supplier_country"
    )

    order_status_audit: list[OrderStatusAudit] = Field(
        description="Breakdown of total orders by status, from get_order_count_by_status"
    )
    tools_used: list[str] = Field(
        default_factory=list,
        description="Names of the tools used to gather the data for this report",
    )
    
user_prompt_content = """
    I am preparing an annual report for the company. 
    I need a detailed report that includes information 
    about products, suppliers, orders, and customers. 
    Please provide me with a comprehensive summary of the annual report, 
    including key insights and statistics. Additionally, I would like to see a breakdown of customers by country, suppliers by country, and orders by status. Please ensure that the data is accurate and up-to-date.
"""

system_prompt_content = """
    You are a audit manager assistant for a company.
    You will use accurate tools to query the database
    and provide the user valid answer what he asked for.
    For country-wise or status-wise totals and counts, always use the dedicated
    aggregation tools (get_purchases_by_customer_country, get_order_items_by_supplier_country,
    get_order_count_by_status) which return exact database-computed totals.
    Never count or sum rows yourself from raw/detailed data - always rely on the
    aggregation tool results for numeric totals.
    Dont Hellucinate or make up any answer. If you dont know the answer,
    say "I dont know".
"""

llm1 = ChatGroq(model="qwen/qwen3-32b")
llm2 = ChatOpenAI(model="gpt-4o-mini")
llm3 = ChatOpenRouter(
    model="google/gemini-2.5-flash",
    temperature=0.8,
)

prompt = {
    "messages": [
        {
            "role": "user", 
            "content": user_prompt_content
        }
      ]
    }

agent = create_agent(
    model=llm3,
    tools=tools,
    system_prompt=system_prompt_content,
    response_format=Response,
)

def render_report(report: Response) -> None:
    console = Console()

    country_table = Table(title="Customer Purchases by Country")
    country_table.add_column("Country")
    country_table.add_column("Total Purchases", justify="right")
    for row in report.country_audit:
        country_table.add_row(row.country, str(row.total_purchases))
    console.print(country_table)

    supplier_table = Table(title="Suppliers by Country")
    supplier_table.add_column("Country")
    supplier_table.add_column("Total Suppliers", justify="right")
    for row in report.country_wise_supplier_audit:
        supplier_table.add_row(row.country, str(row.total_supplier))
    console.print(supplier_table)

    status_table = Table(title="Orders by Status")
    status_table.add_column("Status")
    status_table.add_column("Total Orders", justify="right")
    for row in report.order_status_audit:
        status_table.add_row(row.status, str(row.total_orders))
    console.print(status_table)

    console.print(Panel(", ".join(report.tools_used) or "None", title="Tools Used", expand=False))


response = agent.invoke(prompt)
render_report(response["structured_response"])
