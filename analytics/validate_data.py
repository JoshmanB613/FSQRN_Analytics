import pandas as pd
from pathlib import Path


RAW_DATA = Path("data/raw")


suppliers_df = pd.read_csv(RAW_DATA / "suppliers.csv")
products_df = pd.read_csv(RAW_DATA / "products.csv")
inspections_df = pd.read_csv(RAW_DATA / "inspections.csv")
incidents_df = pd.read_csv(RAW_DATA / "quality_incidents.csv")
corrective_actions_df = pd.read_csv(
    RAW_DATA / "corrective_actions.csv"
)


errors = []


def check_missing_values(df, name):

    missing = df.isnull().sum()

    for column, count in missing.items():

        if count > 0:
            errors.append(
                f"{name}: {column} has {count} missing values"
            )


def check_duplicates(df, column, name):

    duplicates = df[column].duplicated().sum()

    if duplicates > 0:
        errors.append(
            f"{name}: {duplicates} duplicate {column} values"
        )


def check_supplier_relationships():

    valid_suppliers = set(
        suppliers_df["supplier_id"]
    )

    invalid_products = products_df[
        ~products_df["supplier_id"].isin(valid_suppliers)
    ]

    if len(invalid_products) > 0:
        errors.append(
            f"Products: {len(invalid_products)} invalid supplier relationships"
        )

    invalid_inspections = inspections_df[
        ~inspections_df["supplier_id"].isin(valid_suppliers)
    ]

    if len(invalid_inspections) > 0:
        errors.append(
            f"Inspections: {len(invalid_inspections)} invalid supplier relationships"
        )


def check_incident_relationships():

    valid_products = set(
        products_df["product_id"]
    )

    invalid_products = incidents_df[
        ~incidents_df["product_id"].isin(valid_products)
    ]

    if len(invalid_products) > 0:
        errors.append(
            f"Quality Incidents: {len(invalid_products)} invalid product relationships"
        )

    product_supplier_map = dict(
        zip(
            products_df["product_id"],
            products_df["supplier_id"]
        )
    )

    for _, incident in incidents_df.iterrows():

        expected_supplier = product_supplier_map.get(
            incident["product_id"]
        )

        if expected_supplier != incident["supplier_id"]:

            errors.append(
                f"Quality Incident {incident['incident_id']}: "
                f"supplier does not match product supplier"
            )


def check_corrective_action_relationships():

    valid_incidents = set(
        incidents_df["incident_id"]
    )

    invalid_incidents = corrective_actions_df[
        ~corrective_actions_df["incident_id"].isin(valid_incidents)
    ]

    if len(invalid_incidents) > 0:
        errors.append(
            f"Corrective Actions: {len(invalid_incidents)} invalid incident relationships"
        )

    incident_supplier_map = dict(
        zip(
            incidents_df["incident_id"],
            incidents_df["supplier_id"]
        )
    )

    for _, action in corrective_actions_df.iterrows():

        expected_supplier = incident_supplier_map.get(
            action["incident_id"]
        )

        if expected_supplier != action["supplier_id"]:

            errors.append(
                f"Corrective Action {action['action_id']}: "
                f"supplier does not match incident supplier"
            )


def check_inspection_scores():

    invalid_scores = inspections_df[
        (inspections_df["compliance_score"] < 0) |
        (inspections_df["compliance_score"] > 100)
    ]

    if len(invalid_scores) > 0:
        errors.append(
            f"Inspections: {len(invalid_scores)} invalid compliance scores"
        )


def check_inspection_results():

    valid_results = {
        "Pass",
        "Fail"
    }

    invalid_results = inspections_df[
        ~inspections_df["result"].isin(valid_results)
    ]

    if len(invalid_results) > 0:
        errors.append(
            f"Inspections: {len(invalid_results)} invalid results"
        )


def check_status_values():

    supplier_statuses = {
        "Active",
        "Inactive"
    }

    invalid_supplier_status = suppliers_df[
        ~suppliers_df["status"].isin(supplier_statuses)
    ]

    if len(invalid_supplier_status) > 0:
        errors.append(
            f"Suppliers: {len(invalid_supplier_status)} invalid statuses"
        )

    incident_statuses = {
        "Open",
        "Under Investigation",
        "Closed"
    }

    invalid_incident_status = incidents_df[
        ~incidents_df["status"].isin(incident_statuses)
    ]

    if len(invalid_incident_status) > 0:
        errors.append(
            f"Quality Incidents: {len(invalid_incident_status)} invalid statuses"
        )

    action_statuses = {
        "Open",
        "In Progress",
        "Closed"
    }

    invalid_action_status = corrective_actions_df[
        ~corrective_actions_df["status"].isin(action_statuses)
    ]

    if len(invalid_action_status) > 0:
        errors.append(
            f"Corrective Actions: {len(invalid_action_status)} invalid statuses"
        )


def check_dates():

    inspections_df["inspection_date"] = pd.to_datetime(
        inspections_df["inspection_date"],
        errors="coerce"
    )

    incidents_df["incident_date"] = pd.to_datetime(
        incidents_df["incident_date"],
        errors="coerce"
    )

    corrective_actions_df["date_opened"] = pd.to_datetime(
        corrective_actions_df["date_opened"],
        errors="coerce"
    )

    corrective_actions_df["due_date"] = pd.to_datetime(
        corrective_actions_df["due_date"],
        errors="coerce"
    )

    corrective_actions_df["date_closed"] = pd.to_datetime(
        corrective_actions_df["date_closed"],
        errors="coerce"
    )

    if inspections_df["inspection_date"].isnull().any():
        errors.append(
            "Inspections: invalid inspection dates found"
        )

    if incidents_df["incident_date"].isnull().any():
        errors.append(
            "Quality Incidents: invalid incident dates found"
        )

    if corrective_actions_df["date_opened"].isnull().any():
        errors.append(
            "Corrective Actions: invalid opening dates found"
        )

    if corrective_actions_df["due_date"].isnull().any():
        errors.append(
            "Corrective Actions: invalid due dates found"
        )


check_missing_values(suppliers_df, "Suppliers")
check_missing_values(products_df, "Products")
check_missing_values(inspections_df, "Inspections")
check_missing_values(incidents_df, "Quality Incidents")
check_missing_values(
    corrective_actions_df,
    "Corrective Actions"
)


check_duplicates(
    suppliers_df,
    "supplier_id",
    "Suppliers"
)

check_duplicates(
    products_df,
    "product_id",
    "Products"
)

check_duplicates(
    inspections_df,
    "inspection_id",
    "Inspections"
)

check_duplicates(
    incidents_df,
    "incident_id",
    "Quality Incidents"
)

check_duplicates(
    corrective_actions_df,
    "action_id",
    "Corrective Actions"
)


check_supplier_relationships()
check_incident_relationships()
check_corrective_action_relationships()
check_inspection_scores()
check_inspection_results()
check_status_values()
check_dates()


print()
print("=" * 50)
print("FSQRN DATA VALIDATION REPORT")
print("=" * 50)

print()

print(f"Suppliers: {len(suppliers_df)}")
print(f"Products: {len(products_df)}")
print(f"Inspections: {len(inspections_df)}")
print(f"Quality Incidents: {len(incidents_df)}")
print(f"Corrective Actions: {len(corrective_actions_df)}")

print()

if len(errors) == 0:

    print("DATA VALIDATION PASSED")
    print("No data quality issues were found.")

else:

    print("DATA VALIDATION FAILED")
    print()
    print("Issues found:")

    for error in errors:
        print(f"- {error}")