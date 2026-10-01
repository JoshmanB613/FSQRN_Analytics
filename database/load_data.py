import pandas as pd
import psycopg
from pathlib import Path


# -----------------------------
# Database connection
# -----------------------------

DB_NAME = "fsqrn_analytics"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432


# -----------------------------
# File locations
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"


# -----------------------------
# Connect to PostgreSQL
# -----------------------------

password = input("Enter PostgreSQL password: ")


connection = psycopg.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=password,
    host=DB_HOST,
    port=DB_PORT
)


print("Connected to PostgreSQL!")


# -----------------------------
# Load CSV files
# -----------------------------

suppliers_df = pd.read_csv(
    RAW_DATA / "suppliers.csv"
)

products_df = pd.read_csv(
    RAW_DATA / "products.csv"
)

inspections_df = pd.read_csv(
    RAW_DATA / "inspections.csv"
)

incidents_df = pd.read_csv(
    RAW_DATA / "quality_incidents.csv"
)

corrective_actions_df = pd.read_csv(
    RAW_DATA / "corrective_actions.csv"
)


# -----------------------------
# Insert data
# -----------------------------

with connection.cursor() as cursor:

    # Suppliers
    for _, row in suppliers_df.iterrows():

        cursor.execute(
            """
            INSERT INTO suppliers (
                supplier_id,
                supplier_name,
                country,
                region,
                supplier_type,
                risk_level,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["supplier_id"],
                row["supplier_name"],
                row["country"],
                row["region"],
                row["supplier_type"],
                row["risk_level"],
                row["status"]
            )
        )


    # Products
    for _, row in products_df.iterrows():

        cursor.execute(
            """
            INSERT INTO products (
                product_id,
                product_name,
                category,
                supplier_id,
                allergen,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                row["product_id"],
                row["product_name"],
                row["category"],
                row["supplier_id"],
                row["allergen"],
                row["status"]
            )
        )


    # Inspections
    for _, row in inspections_df.iterrows():

        cursor.execute(
            """
            INSERT INTO inspections (
                inspection_id,
                supplier_id,
                inspection_date,
                inspection_type,
                compliance_score,
                result,
                major_findings
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["inspection_id"],
                row["supplier_id"],
                row["inspection_date"],
                row["inspection_type"],
                row["compliance_score"],
                row["result"],
                row["major_findings"]
            )
        )


    # Quality incidents
    for _, row in incidents_df.iterrows():

        cursor.execute(
            """
            INSERT INTO quality_incidents (
                incident_id,
                product_id,
                supplier_id,
                incident_date,
                incident_type,
                severity,
                description,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["incident_id"],
                row["product_id"],
                row["supplier_id"],
                row["incident_date"],
                row["incident_type"],
                row["severity"],
                row["description"],
                row["status"]
            )
        )


    # Corrective actions
    for _, row in corrective_actions_df.iterrows():

        date_closed = (
            row["date_closed"]
            if pd.notna(row["date_closed"])
            else None
        )

        cursor.execute(
            """
            INSERT INTO corrective_actions (
                action_id,
                incident_id,
                supplier_id,
                action_type,
                date_opened,
                due_date,
                date_closed,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["action_id"],
                row["incident_id"],
                row["supplier_id"],
                row["action_type"],
                row["date_opened"],
                row["due_date"],
                date_closed,
                row["status"]
            )
        )


# -----------------------------
# Save changes
# -----------------------------

connection.commit()


print()
print("=" * 50)
print("DATA LOADING COMPLETE")
print("=" * 50)

print(f"Suppliers loaded: {len(suppliers_df)}")
print(f"Products loaded: {len(products_df)}")
print(f"Inspections loaded: {len(inspections_df)}")
print(f"Quality incidents loaded: {len(incidents_df)}")
print(f"Corrective actions loaded: {len(corrective_actions_df)}")


connection.close()

print()
print("PostgreSQL connection closed.")