from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg


app = FastAPI(
    title="FSQRN Analytics API",
    description="API for supplier quality and risk analytics",
    version="1.0.0"
)


# Allow the React frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DATABASE_URL = (
    "dbname=fsqrn_analytics "
    "user=postgres "
    "password=Your_psql_password "
    "host=localhost "
    "port=5432"
)


@app.get("/")
def root():
    return {
        "message": "FSQRN Analytics API is running"
    }


@app.get("/suppliers/risk")
def get_supplier_risk():

    with psycopg.connect(DATABASE_URL) as connection:

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    s.supplier_id,
                    d.supplier_name,
                    d.failure_rate,
                    d.serious_incidents,
                    d.total_incidents,
                    d.failure_score,
                    d.serious_incident_score,
                    d.incident_frequency_score,
                    d.total_risk_score,
                    d.risk_score,
                    d.risk_category
                FROM supplier_risk_dashboard d
                JOIN suppliers s
                    ON s.supplier_name = d.supplier_name
                ORDER BY d.risk_score DESC;
            """)

            rows = cursor.fetchall()


    results = []

    for row in rows:

        results.append({
            "supplier_id": row[0],
            "supplier_name": row[1],
            "failure_rate": float(row[2]) if row[2] is not None else None,
            "serious_incidents": row[3],
            "total_incidents": row[4],
            "failure_score": row[5],
            "serious_incident_score": row[6],
            "incident_frequency_score": row[7],
            "total_risk_score": row[8],
            "risk_score": float(row[9]) if row[9] is not None else None,
            "risk_category": row[10]
        })

    return results


@app.get("/dashboard/summary")
def get_dashboard_summary():

    with psycopg.connect(DATABASE_URL) as connection:

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    COUNT(*) AS total_suppliers,

                    COUNT(
                        CASE
                            WHEN risk_category = 'High'
                            THEN 1
                        END
                    ) AS high_risk_suppliers,

                    COUNT(
                        CASE
                            WHEN risk_category = 'Medium'
                            THEN 1
                        END
                    ) AS medium_risk_suppliers,

                    COUNT(
                        CASE
                            WHEN risk_category = 'Low'
                            THEN 1
                        END
                    ) AS low_risk_suppliers,

                    ROUND(
                        AVG(risk_score),
                        2
                    ) AS average_risk_score,

                    ROUND(
                        AVG(failure_rate),
                        2
                    ) AS average_failure_rate

                FROM supplier_risk_dashboard;
            """)

            row = cursor.fetchone()


    return {
        "total_suppliers": row[0],
        "high_risk_suppliers": row[1],
        "medium_risk_suppliers": row[2],
        "low_risk_suppliers": row[3],
        "average_risk_score": float(row[4]),
        "average_failure_rate": float(row[5])
    }
    

@app.get("/suppliers/{supplier_id}")
def get_supplier_details(supplier_id: str):

    with psycopg.connect(DATABASE_URL) as connection:

        with connection.cursor() as cursor:

            # Get supplier information
            cursor.execute("""
                SELECT
                    supplier_id,
                    supplier_name,
                    country,
                    region,
                    supplier_type,
                    risk_level,
                    status
                FROM suppliers
                WHERE supplier_id = %s;
            """, (supplier_id,))

            supplier = cursor.fetchone()


            if supplier is None:
                return {
                    "error": "Supplier not found"
                }


            # Get inspections
            cursor.execute("""
                SELECT
                    inspection_id,
                    inspection_date,
                    inspection_type,
                    compliance_score,
                    result,
                    major_findings
                FROM inspections
                WHERE supplier_id = %s
                ORDER BY inspection_date DESC;
            """, (supplier_id,))

            inspections = cursor.fetchall()


            # Get quality incidents
            cursor.execute("""
                SELECT
                    qi.incident_id,
                    qi.incident_date,
                    qi.incident_type,
                    qi.severity,
                    qi.description,
                    qi.status,
                    p.product_name
                FROM quality_incidents qi
                JOIN products p
                    ON qi.product_id = p.product_id
                WHERE qi.supplier_id = %s
                ORDER BY qi.incident_date DESC;
            """, (supplier_id,))

            incidents = cursor.fetchall()


            # Get corrective actions
            cursor.execute("""
                SELECT
                    action_id,
                    incident_id,
                    action_type,
                    date_opened,
                    due_date,
                    date_closed,
                    status
                FROM corrective_actions
                WHERE supplier_id = %s
                ORDER BY date_opened DESC;
            """, (supplier_id,))

            corrective_actions = cursor.fetchall()


    return {

        "supplier": {
            "supplier_id": supplier[0],
            "supplier_name": supplier[1],
            "country": supplier[2],
            "region": supplier[3],
            "supplier_type": supplier[4],
            "risk_level": supplier[5],
            "status": supplier[6]
        },


        "inspections": [

            {
                "inspection_id": row[0],
                "inspection_date": str(row[1]),
                "inspection_type": row[2],
                "compliance_score": float(row[3]),
                "result": row[4],
                "major_findings": row[5]
            }

            for row in inspections

        ],


        "incidents": [

            {
                "incident_id": row[0],
                "incident_date": str(row[1]),
                "incident_type": row[2],
                "severity": row[3],
                "description": row[4],
                "status": row[5],
                "product_name": row[6]
            }

            for row in incidents

        ],


        "corrective_actions": [

            {
                "action_id": row[0],
                "incident_id": row[1],
                "action_type": row[2],
                "date_opened": str(row[3]),
                "due_date": str(row[4]),
                "date_closed": str(row[5]) if row[5] else None,
                "status": row[6]
            }

            for row in corrective_actions

        ]

    }
    
@app.get("/inspections")
def get_inspections():

    with psycopg.connect(DATABASE_URL) as connection:

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    i.inspection_id,
                    i.supplier_id,
                    s.supplier_name,
                    i.inspection_date,
                    i.inspection_type,
                    i.compliance_score,
                    i.result,
                    i.major_findings
                FROM inspections i
                JOIN suppliers s
                    ON i.supplier_id = s.supplier_id
                ORDER BY i.inspection_date DESC;
            """)

            rows = cursor.fetchall()

    results = []

    for row in rows:

        results.append({
            "inspection_id": row[0],
            "supplier_id": row[1],
            "supplier_name": row[2],
            "inspection_date": str(row[3]),
            "inspection_type": row[4],
            "compliance_score": float(row[5]),
            "result": row[6],
            "major_findings": row[7]
        })

    return results

@app.get("/incidents")
def get_incidents():

    with psycopg.connect(DATABASE_URL) as connection:

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    qi.incident_id,
                    qi.supplier_id,
                    s.supplier_name,
                    qi.product_id,
                    p.product_name,
                    qi.incident_date,
                    qi.incident_type,
                    qi.severity,
                    qi.description,
                    qi.status
                FROM quality_incidents qi
                JOIN suppliers s
                    ON qi.supplier_id = s.supplier_id
                JOIN products p
                    ON qi.product_id = p.product_id
                ORDER BY qi.incident_date DESC;
            """)

            rows = cursor.fetchall()

    results = []

    for row in rows:

        results.append({
            "incident_id": row[0],
            "supplier_id": row[1],
            "supplier_name": row[2],
            "product_id": row[3],
            "product_name": row[4],
            "incident_date": str(row[5]),
            "incident_type": row[6],
            "severity": row[7],
            "description": row[8],
            "status": row[9]
        })

    return results

@app.get("/corrective-actions")
def get_corrective_actions():

    with psycopg.connect(DATABASE_URL) as connection:

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    ca.action_id,
                    ca.supplier_id,
                    s.supplier_name,
                    ca.incident_id,
                    ca.action_type,
                    ca.date_opened,
                    ca.due_date,
                    ca.date_closed,
                    ca.status
                FROM corrective_actions ca
                JOIN suppliers s
                    ON ca.supplier_id = s.supplier_id
                ORDER BY ca.date_opened DESC;
            """)

            rows = cursor.fetchall()

    results = []

    for row in rows:

        results.append({
            "action_id": row[0],
            "supplier_id": row[1],
            "supplier_name": row[2],
            "incident_id": row[3],
            "action_type": row[4],
            "date_opened": str(row[5]),
            "due_date": str(row[6]),
            "date_closed": str(row[7]) if row[7] else None,
            "status": row[8]
        })

    return results
