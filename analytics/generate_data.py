import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path


NUM_SUPPLIERS = 50
NUM_PRODUCTS = 150
NUM_INSPECTIONS = 500
NUM_INCIDENTS = 250


RAW_DATA = Path("data/raw")
RAW_DATA.mkdir(parents=True, exist_ok=True)


countries = [
    "United Kingdom",
    "Germany",
    "France",
    "Italy",
    "Netherlands",
    "Spain",
    "South Africa",
    "Poland",
]


supplier_types = [
    "Dairy",
    "Produce",
    "Coffee",
    "Bakery",
    "Packaging",
    "Beverages",
    "Food",
]


risk_levels = [
    "Low",
    "Medium",
    "High"
]


suppliers = []

for i in range(1, NUM_SUPPLIERS + 1):

    supplier_id = f"SUP{i:03d}"

    suppliers.append({
        "supplier_id": supplier_id,
        "supplier_name": f"Supplier Company {i}",
        "country": random.choice(countries),
        "region": random.choice(["UK", "EMEA"]),
        "supplier_type": random.choice(supplier_types),
        "risk_level": random.choice(risk_levels),
        "status": random.choice([
            "Active",
            "Active",
            "Active",
            "Inactive"
        ])
    })


suppliers_df = pd.DataFrame(suppliers)


product_categories = [
    "Coffee",
    "Dairy",
    "Bakery",
    "Food",
    "Beverage",
    "Syrup",
    "Produce",
]


allergens = [
    "Milk",
    "Nuts",
    "Soy",
    "Wheat",
    "Egg",
    "None",
]


products = []

for i in range(1, NUM_PRODUCTS + 1):

    products.append({
        "product_id": f"PROD{i:03d}",
        "product_name": f"Product {i}",
        "category": random.choice(product_categories),
        "supplier_id": random.choice(
            suppliers_df["supplier_id"].tolist()
        ),
        "allergen": random.choice(allergens),
        "status": random.choice([
            "Active",
            "Active",
            "Active",
            "Inactive"
        ])
    })


products_df = pd.DataFrame(products)


start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 9, 20)


def random_date():

    days_between = (end_date - start_date).days

    random_days = random.randint(
        0,
        days_between
    )

    return start_date + timedelta(
        days=random_days
    )


inspection_types = [
    "Food Safety",
    "Quality",
    "Supplier Audit",
    "Hygiene",
    "Regulatory"
]


inspections = []

for i in range(1, NUM_INSPECTIONS + 1):

    score = random.randint(60, 100)

    inspections.append({
        "inspection_id": f"INS{i:04d}",
        "supplier_id": random.choice(
            suppliers_df["supplier_id"].tolist()
        ),
        "inspection_date": random_date(),
        "inspection_type": random.choice(
            inspection_types
        ),
        "compliance_score": score,
        "result": "Pass" if score >= 80 else "Fail",
        "major_findings": random.randint(0, 5)
    })


inspections_df = pd.DataFrame(inspections)


incidents = []

for i in range(1, NUM_INCIDENTS + 1):

    product = random.choice(
        products_df.to_dict("records")
    )

    incidents.append({
        "incident_id": f"INC{i:04d}",
        "product_id": product["product_id"],
        "supplier_id": product["supplier_id"],
        "incident_date": random_date(),
        "incident_type": random.choice([
            "Contamination",
            "Temperature Breach",
            "Packaging Defect",
            "Foreign Material",
            "Allergen Issue",
            "Labelling Error",
            "Product Quality"
        ]),
        "severity": random.choice([
            "Low",
            "Medium",
            "High",
            "Critical"
        ]),
        "description": "Synthetic quality incident",
        "status": random.choice([
            "Open",
            "Under Investigation",
            "Closed"
        ])
    })


incidents_df = pd.DataFrame(incidents)


action_types = [
    "Supplier Investigation",
    "Root Cause Analysis",
    "Staff Training",
    "Process Improvement",
    "Product Hold",
    "Additional Inspection"
]


corrective_actions = []

for i, incident in incidents_df.iterrows():

    opened = incident["incident_date"]

    due = opened + timedelta(
        days=random.randint(7, 30)
    )

    status = random.choice([
        "Open",
        "In Progress",
        "Closed"
    ])

    if status == "Closed":

        closed = due - timedelta(
            days=random.randint(0, 10)
        )

        if closed < opened:
            closed = opened

    else:

        closed = None

    corrective_actions.append({
        "action_id": f"CA{i + 1:04d}",
        "incident_id": incident["incident_id"],
        "supplier_id": incident["supplier_id"],
        "action_type": random.choice(action_types),
        "date_opened": opened,
        "due_date": due,
        "date_closed": closed,
        "status": status
    })


corrective_actions_df = pd.DataFrame(
    corrective_actions
)


suppliers_df.to_csv(
    RAW_DATA / "suppliers.csv",
    index=False
)

products_df.to_csv(
    RAW_DATA / "products.csv",
    index=False
)

inspections_df.to_csv(
    RAW_DATA / "inspections.csv",
    index=False
)

incidents_df.to_csv(
    RAW_DATA / "quality_incidents.csv",
    index=False
)

corrective_actions_df.to_csv(
    RAW_DATA / "corrective_actions.csv",
    index=False
)


print("FSQRN synthetic data generated successfully!")
print(f"Suppliers: {len(suppliers_df)}")
print(f"Products: {len(products_df)}")
print(f"Inspections: {len(inspections_df)}")
print(f"Quality incidents: {len(incidents_df)}")
print(f"Corrective actions: {len(corrective_actions_df)}")