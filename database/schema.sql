CREATE TABLE suppliers (
    supplier_id VARCHAR(10) PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    region VARCHAR(20) NOT NULL,
    supplier_type VARCHAR(50) NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL
);


CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    supplier_id VARCHAR(10) NOT NULL,
    allergen VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,

    CONSTRAINT fk_product_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
);


CREATE TABLE inspections (
    inspection_id VARCHAR(10) PRIMARY KEY,
    supplier_id VARCHAR(10) NOT NULL,
    inspection_date DATE NOT NULL,
    inspection_type VARCHAR(50) NOT NULL,
    compliance_score NUMERIC(5,2) NOT NULL,
    result VARCHAR(20) NOT NULL,
    major_findings INTEGER NOT NULL,

    CONSTRAINT fk_inspection_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
);


CREATE TABLE quality_incidents (
    incident_id VARCHAR(10) PRIMARY KEY,
    product_id VARCHAR(10) NOT NULL,
    supplier_id VARCHAR(10) NOT NULL,
    incident_date DATE NOT NULL,
    incident_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    description TEXT,
    status VARCHAR(30) NOT NULL,

    CONSTRAINT fk_incident_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_incident_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
);


CREATE TABLE corrective_actions (
    action_id VARCHAR(10) PRIMARY KEY,
    incident_id VARCHAR(10) NOT NULL,
    supplier_id VARCHAR(10) NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    date_opened DATE NOT NULL,
    due_date DATE NOT NULL,
    date_closed DATE,
    status VARCHAR(20) NOT NULL,

    CONSTRAINT fk_action_incident
        FOREIGN KEY (incident_id)
        REFERENCES quality_incidents(incident_id),

    CONSTRAINT fk_action_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
);