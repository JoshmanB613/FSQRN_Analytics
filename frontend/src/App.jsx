import { useEffect, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from "recharts";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [summary, setSummary] = useState(null);
  const [suppliers, setSuppliers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Search and filter
  const [searchTerm, setSearchTerm] = useState("");
  const [riskFilter, setRiskFilter] = useState("All");

  const [activePage, setActivePage] = useState("Dashboard");
  const [inspections, setInspections] = useState([]);

  const [incidents, setIncidents] = useState([]);
  const [correctiveActions, setCorrectiveActions] = useState([]);

  // Supplier details
  const [supplierDetails, setSupplierDetails] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [
  summaryResponse,
  suppliersResponse,
  inspectionsResponse
] = await Promise.all([
  fetch(`${API_URL}/dashboard/summary`),
  fetch(`${API_URL}/suppliers/risk`),
  fetch(`${API_URL}/inspections`)
]);

        if (
              !summaryResponse.ok ||
              !suppliersResponse.ok ||
              !inspectionsResponse.ok
            ) {
          throw new Error("Failed to fetch dashboard data");
        }

        const summaryData = await summaryResponse.json();
        const suppliersData = await suppliersResponse.json();
        const inspectionsData = await inspectionsResponse.json();

        setSummary(summaryData);
        setSuppliers(suppliersData);
        setInspections(inspectionsData);
      } catch (error) {
        console.error(error);
        setError("Could not connect to the FSQRN Analytics API.");
      } finally {
        setLoading(false);
      }
    }



    loadDashboard();
  }, []);

  async function handleSupplierClick(supplierId) {
    setDetailsLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/suppliers/${supplierId}`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch supplier details");
      }

      const data = await response.json();

      setSupplierDetails(data);

      // Scroll down to the supplier details
      setTimeout(() => {
        document
          .getElementById("supplier-details")
          ?.scrollIntoView({ behavior: "smooth" });
      }, 100);

    } catch (error) {
      console.error(error);
    } finally {
      setDetailsLoading(false);
    }
  }

  async function loadInspections() {
  try {
    const response = await fetch(`${API_URL}/inspections`);

    if (!response.ok) {
      throw new Error("Failed to fetch inspections");
    }

    const data = await response.json();

    setInspections(data);
  } catch (error) {
    console.error(error);
  }
}

async function loadIncidents() {
  try {
    const response = await fetch(`${API_URL}/incidents`);

    if (!response.ok) {
      throw new Error("Failed to fetch incidents");
    }

    const data = await response.json();

    setIncidents(data);
  } catch (error) {
    console.error(error);
  }
}

async function loadCorrectiveActions() {
  try {
    const response = await fetch(`${API_URL}/corrective-actions`);

    if (!response.ok) {
      throw new Error("Failed to fetch corrective actions");
    }

    const data = await response.json();

    setCorrectiveActions(data);
  } catch (error) {
    console.error(error);
  }
}

  if (loading) {
    return <div className="loading">Loading FSQRN Analytics...</div>;
  }

  if (error) {
    return (
      <div className="error">
        <h2>Connection Error</h2>
        <p>{error}</p>
        <p>Make sure FastAPI is running on port 8000.</p>
      </div>
    );
  }

  const riskData = [
    { name: "High Risk", value: summary.high_risk_suppliers },
    { name: "Medium Risk", value: summary.medium_risk_suppliers },
    { name: "Low Risk", value: summary.low_risk_suppliers }
  ];

  const inspectionResultData = [
  {
    name: "Pass",
    value: inspections.filter(
      (inspection) => inspection.result === "Pass"
    ).length
  },
  {
    name: "Fail",
    value: inspections.filter(
      (inspection) => inspection.result === "Fail"
    ).length
  }
];

  const failureRateData = [...suppliers]
    .sort((a, b) => b.failure_rate - a.failure_rate)
    .slice(0, 10);

  const filteredSuppliers = suppliers.filter((supplier) => {
    const matchesSearch = supplier.supplier_name
      .toLowerCase()
      .includes(searchTerm.toLowerCase());

    const matchesRisk =
      riskFilter === "All" ||
      supplier.risk_category === riskFilter;

    return matchesSearch && matchesRisk;
  });

  // Find calculated risk information for the selected supplier
  const selectedSupplierRisk = supplierDetails
    ? suppliers.find(
        (supplier) =>
          supplier.supplier_id === supplierDetails.supplier.supplier_id
      )
    : null;

  return (
    <div className="dashboard">

      <aside className="sidebar">
        <div className="logo">FSQRN</div>
        <p className="logo-subtitle">Analytics</p>

       <nav>
  <a
    href="#"
    className={activePage === "Dashboard" ? "active" : ""}
    onClick={(event) => {
      event.preventDefault();
      setActivePage("Dashboard");
    }}
  >
    Dashboard
  </a>

  <a
    href="#"
    className={activePage === "Suppliers" ? "active" : ""}
    onClick={(event) => {
      event.preventDefault();
      setActivePage("Suppliers");
    }}
  >
    Suppliers
  </a>

  <a
    href="#"
    className={activePage === "Inspections" ? "active" : ""}
    onClick={(event) => {
      event.preventDefault();
      setActivePage("Inspections");
      loadInspections();
    }}
  >
    Inspections
  </a>

  <a
    href="#"
    className={activePage === "Incidents" ? "active" : ""}
    onClick={(event) => {
      event.preventDefault();
      setActivePage("Incidents");
      loadIncidents();
    }}
  >
    Incidents
  </a>

  <a
    href="#"
    className={activePage === "Corrective Actions" ? "active" : ""}
    onClick={(event) => {
      event.preventDefault();
      setActivePage("Corrective Actions");
      loadCorrectiveActions();
    }}
  >
    Corrective Actions
  </a>
</nav>

      </aside>

      <main className="main-content">
        
        {activePage === "Inspections" && (
  <section>

    <header className="header">
      <div>
        <h1>Inspections</h1>
        <p>
          Supplier inspection records and compliance performance
        </p>
      </div>
    </header>

    <section className="panel">

      <div className="panel-header">
        <div>
          <h2>Inspection Records</h2>
          <p>
            {inspections.length} inspections recorded across suppliers
          </p>
        </div>
      </div>

      <div className="table-container">

        <table>

          <thead>
            <tr>
              <th>Inspection ID</th>
              <th>Supplier</th>
              <th>Date</th>
              <th>Type</th>
              <th>Compliance Score</th>
              <th>Result</th>
              <th>Major Findings</th>
            </tr>
          </thead>

          <tbody>

            {inspections.map((inspection) => (

              <tr key={inspection.inspection_id}>

                <td className="inspection-id">
                  {inspection.inspection_id}
                </td>

                <td className="supplier-name">
                  {inspection.supplier_name}
                </td>

                <td className="inspection-date">
                  {inspection.inspection_date}
                </td>

                <td className="inspection-type">
                  {inspection.inspection_type}
                </td>

                <td className="compliance-score">
                  {Number(inspection.compliance_score).toFixed(1)}%
                </td>

                <td>
                  <span
                    className={`result-badge ${
                      inspection.result.toLowerCase()
                    }`}
                  >
                    {inspection.result}
                  </span>
                </td>

                <td className="major-findings">
                  {inspection.major_findings}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </section>

  </section>
        )}

{activePage === "Dashboard" && (

        <section>
        <header className="header">
          <div>
            <h1>FSQRN Analytics Dashboard</h1>
            <p>
              Food Safety, Quality, Regulatory & Nutrition analytics
            </p>
          </div>
        </header>

        {/* SUMMARY CARDS */}

{summary && (
  <section className="summary-grid">

    <div className="card">
      <p>Total Suppliers</p>
      <h2>{summary.total_suppliers}</h2>
      <span>Suppliers monitored in the dataset</span>
    </div>

    <div className="card high">
      <p>High Risk</p>
      <h2>{summary.high_risk_suppliers}</h2>
      <span>Suppliers requiring closer monitoring</span>
    </div>

    <div className="card medium">
      <p>Medium Risk</p>
      <h2>{summary.medium_risk_suppliers}</h2>
      <span>Suppliers with moderate risk exposure</span>
    </div>

    <div className="card low">
      <p>Low Risk</p>
      <h2>{summary.low_risk_suppliers}</h2>
      <span>Suppliers with lower calculated risk</span>
    </div>

    <div className="card">
      <p>Average Risk Score</p>
      <h2>{summary.average_risk_score}</h2>
      <span>Average calculated supplier risk</span>
    </div>

    <div className="card">
      <p>Average Failure Rate</p>
      <h2>{summary.average_failure_rate}%</h2>
      <span>Average inspection failure rate</span>
    </div>

  </section>
)}

        {/* CHARTS */}

        <section className="analytics-grid">

          <div className="panel chart-panel">

            <div className="panel-header">
              <div>
                <h2>Supplier Risk Distribution</h2>
                <p>
                  Shows the proportion of suppliers classified as high, medium, or low risk based on the calculated supplier risk score.
                </p>
              </div>
            </div>

            <div className="chart-container">

              <ResponsiveContainer width="100%" height={300}>

                <PieChart>

                  <Pie
  data={riskData}
  dataKey="value"
  nameKey="name"
  cx="50%"
  cy="50%"
  outerRadius={100}
  label={({ name, value }) => {
    const total =
      summary.high_risk_suppliers +
      summary.medium_risk_suppliers +
      summary.low_risk_suppliers;

    return `${name}: ${((value / total) * 100).toFixed(0)}%`;
  }}
>
  <Cell fill="#ef4444" />
  <Cell fill="#facc15" />
  <Cell fill="#3b82f6" />
  </Pie>

                  <Tooltip
                    formatter={(value, name) => {
    const total =
      summary.high_risk_suppliers +
      summary.medium_risk_suppliers +
      summary.low_risk_suppliers;

    const percentage = ((value / total) * 100).toFixed(1);

    return [`${value} suppliers (${percentage}%)`, 
            `${name} suppliers`
          ];
  }}/>

                  <Legend />

                </PieChart>

              </ResponsiveContainer>

            </div>

          </div>


          <div className="panel chart-panel">

            <div className="panel-header">
              <div>
                <h2>Highest Supplier Failure Rates</h2>
                <p>
                  Top 10 suppliers by inspection failure rate
                </p>
              </div>
            </div>

            <div className="chart-container">

              <ResponsiveContainer width="100%" height={450}>

                <BarChart
                  data={failureRateData}
                  layout="vertical"
                  margin={{
                    top: 10,
                    right: 30,
                    left: 40,
                    bottom: 10
                  }}
                >

                  <CartesianGrid stroke="transparent" />

                  <XAxis
                    type="number"
                    domain={[0, 100]}
                    ticks={[0, 25, 50, 75, 100]}
                    tickFormatter={(value) => `${value}%`}
                    tick={{ fill: "#2563eb", fontWeight: 600 }}
                    stroke="#000000"
                  />

                  <YAxis
                    type="category"
                    dataKey="supplier_name"
                    width={140}
                    tick={{ fill: "#2563eb", fontWeight: 600 }}
                    stroke="#000000"
                  />

                  <Tooltip
                    formatter={(value) => [
                      `${Number(value).toFixed(1)}%`,
                      "Inspection Failure Rate"
                    ]}
                  />

                  <Bar
                  dataKey="failure_rate"
                  name="Failure Rate"
                  fill="#22c55e"
                  label={{
                    position: "right",
                    fill: "#2563eb",
                    fontWeight: 600,
                    formatter: (value) => `${value}%`
                        }}/>
                </BarChart>

              </ResponsiveContainer>

            </div>

          </div>

        </section>
        <div className="panel chart-panel">

  <div className="panel-header">
    <div>
      <h2>Inspection Results</h2>
      <p>
        Shows the number of inspections that passed or failed across all recorded supplier inspections.
      </p>
    </div>
  </div>

  <div className="chart-container">

    <ResponsiveContainer width="100%" height={300}>

      <BarChart
  data={inspectionResultData}
  margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
>

 <XAxis
  dataKey="name"
  stroke="#000000"
  tick={{ fill: "#2563eb" }}
/>

<YAxis
  stroke="#000000"
  tick={{ fill: "#2563eb" }}
/>

  <Tooltip
    formatter={(value) => [
      `${value} inspections`,
      "Count"
    ]}
  />

  <Legend />

  <Bar
  dataKey="value"
  name="Inspections"
  label={{ position: "top" }}
>
  <Cell fill="#22c55e" />
  <Cell fill="#ef4444" />
</Bar>
</BarChart>

    </ResponsiveContainer>

  </div>

</div>

          </section>

        )}

        {activePage === "Suppliers" && (
  <section>

    <header className="header">
      <div>
        <h1>Suppliers</h1>
        <p>
          Supplier risk and compliance performance
        </p>
      </div>
    </header>

    {/* SUPPLIER TABLE */}

    <section className="panel">

      <div className="panel-header">

        <div>
          <h2>Supplier Risk Analysis</h2>

          <p>
            Risk assessment based on inspection failures and incidents
          </p>
        </div>

        <span className="supplier-count">
          {filteredSuppliers.length} suppliers
        </span>

      </div>

      <div className="supplier-controls">

        <input
          type="text"
          placeholder="Search supplier..."
          value={searchTerm}
          onChange={(event) =>
            setSearchTerm(event.target.value)
          }
        />

        <select
          value={riskFilter}
          onChange={(event) =>
            setRiskFilter(event.target.value)
          }
        >
          <option value="All">All Risks</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>

      </div>

      <div className="table-container">

        <table>

          <thead>
            <tr>
              <th>Supplier</th>
              <th>Failure Rate</th>
              <th>Total Incidents</th>
              <th>Serious Incidents</th>
              <th>Risk Score</th>
              <th>Risk Category</th>
            </tr>
          </thead>

          <tbody>

            {filteredSuppliers.map((supplier) => (

              <tr key={supplier.supplier_id}>

                <td className="supplier-name">

                  <button
                    className="supplier-link"
                    onClick={() =>
                      handleSupplierClick(
                        supplier.supplier_id
                      )
                    }
                  >
                    {supplier.supplier_name}
                  </button>

                </td>

                <td className="failure-rate">
                  {Number(supplier.failure_rate).toFixed(1)}%
                </td>

                <td className="incident-count">
                  {supplier.total_incidents}
                </td>

                <td className="serious-incident-count">
                  {supplier.serious_incidents}
                </td>

                <td>
                  <td className="risk-score">
                    {Number(supplier.risk_score).toFixed(1)}
                  </td>
                </td>

                <td>

                  <span
                    className={`risk-badge ${supplier.risk_category.toLowerCase()}`}
                  >
                    {supplier.risk_category}
                  </span>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </section>

            {/* LOADING DETAILS */}

        {detailsLoading && (
          <div className="details-loading">
            Loading supplier details...
          </div>
        )}


        {/* SUPPLIER DETAILS */}

        {supplierDetails && !detailsLoading && (

          <section
            id="supplier-details"
            className="panel supplier-details"
          >

            <div className="panel-header">

              <div>
                <h2>
                  {supplierDetails.supplier.supplier_name}
                </h2>

                <p>
                  Detailed supplier performance and compliance information
                </p>
              </div>

              <button
                className="close-details"
                onClick={() => setSupplierDetails(null)}
              >
                Close
              </button>

            </div>


            {/* SUPPLIER INFORMATION */}

            <div className="details-section">

              <h3>Supplier Information</h3>

              <div className="details-grid">

                <div>
                  <span>Supplier ID</span>
                  <strong>
                    {supplierDetails.supplier.supplier_id}
                  </strong>
                </div>

                <div>
                  <span>Country</span>
                  <strong>
                    {supplierDetails.supplier.country}
                  </strong>
                </div>

                <div>
                  <span>Region</span>
                  <strong>
                    {supplierDetails.supplier.region}
                  </strong>
                </div>

                <div>
                  <span>Supplier Type</span>
                  <strong>
                    {supplierDetails.supplier.supplier_type}
                  </strong>
                </div>

                <div>
                  <span>Status</span>
                  <strong>
                    {supplierDetails.supplier.status}
                  </strong>
                </div>

                {selectedSupplierRisk && (
                  <>
                    <div>
                      <span>Risk Score</span>
                      <strong>
                        {Number(selectedSupplierRisk.risk_score).toFixed(1)}
                      </strong>
                    </div>

                  <div>
                    <span>Risk Category</span>
                    <strong
                          className={`supplier-risk-badge ${
                            selectedSupplierRisk.risk_category.toLowerCase()
                        }`}
                    >
                        {selectedSupplierRisk.risk_category}
                      </strong>
                    </div>

                    <div>
                      <span>Failure Rate</span>
                      <strong>
                        {Number(selectedSupplierRisk.failure_rate).toFixed(1)}%
                      </strong>
                    </div>
                  </>
                )}

              </div>

            </div>


            {/* INSPECTIONS */}

            <div className="details-section">

              <div className="details-section-header">

                <div>
                  <h3>Inspection History</h3>
                  <p>
                    {supplierDetails.inspections.length} inspections recorded
                  </p>
                </div>

              </div>


              <div className="table-container">

                <table>

                  <thead>

                    <tr>
                      <th>Date</th>
                      <th>Type</th>
                      <th>Score</th>
                      <th>Result</th>
                      <th>Major Findings</th>
                    </tr>

                  </thead>

                  <tbody>

                    {supplierDetails.inspections.map(
                      (inspection) => (

                        <tr key={inspection.inspection_id}>

                          <td>
                            {inspection.inspection_date}
                          </td>

                          <td>
                            {inspection.inspection_type}
                          </td>

                          <td className="compliance-score">
                            {Number(inspection.compliance_score).toFixed(1)}%
                          </td>

                          <td>

                            <span
                              className={`result-badge ${
                                inspection.result.toLowerCase()
                              }`}
                            >
                              {inspection.result}
                            </span>

                          </td>

                          <td>
                            {inspection.major_findings}
                          </td>

                        </tr>

                      )
                    )}

                  </tbody>

                </table>

              </div>

            </div>


            {/* QUALITY INCIDENTS */}

            <div className="details-section">

              <div className="details-section-header">

                <div>
                  <h3>Quality Incidents</h3>
                  <p>
                    {supplierDetails.incidents.length} incidents recorded
                  </p>
                </div>

              </div>


              <div className="table-container">

                <table>

                  <thead>

                    <tr>
                      <th>Date</th>
                      <th>Product</th>
                      <th>Incident Type</th>
                      <th>Severity</th>
                      <th>Status</th>
                    </tr>

                  </thead>


                  <tbody>

                    {supplierDetails.incidents.map(
                      (incident) => (

                        <tr key={incident.incident_id}>

                          <td>
                            {incident.incident_date}
                          </td>

                          <td>
                            {incident.product_name}
                          </td>

                          <td>
                            {incident.incident_type}
                          </td>

                          <td>

                            <span
                              className={`severity-badge ${incident.severity.toLowerCase()}`}
                            >
                              {incident.severity}
                            </span>

                          </td>

                          <td>
                            {incident.status}
                          </td>

                        </tr>

                      )
                    )}

                  </tbody>

                </table>

              </div>

            </div>


            {/* CORRECTIVE ACTIONS */}

            <div className="details-section">

              <div className="details-section-header">

                <div>
                  <h3>Corrective Actions</h3>
                  <p>
                    {supplierDetails.corrective_actions.length} actions recorded
                  </p>
                </div>

              </div>


              <div className="table-container">

                <table>

                  <thead>

                    <tr>
                      <th>Opened</th>
                      <th>Incident</th>
                      <th>Action Type</th>
                      <th>Due Date</th>
                      <th>Closed</th>
                      <th>Status</th>
                    </tr>

                  </thead>


                  <tbody>

                    {supplierDetails.corrective_actions.map(
                      (action) => (

                        <tr key={action.action_id}>

                          <td>
                            {action.date_opened}
                          </td>

                          <td>
                            {action.incident_id}
                          </td>

                          <td>
                            {action.action_type}
                          </td>

                          <td>
                            {action.due_date}
                          </td>

                          <td>
                            {action.date_closed ? (
                              action.date_closed
                            ) : (
                              <span className="not-closed">
                                Not Closed
                              </span>
                            )}
                          </td>

                          <td>
                            {action.status}
                          </td>

                        </tr>

                      )
                    )}

                  </tbody>

                </table>

              </div>

            </div>

          </section>

        )}

  </section>
)}

{activePage === "Incidents" && (
  <section>

    <header className="header">
      <div>
        <h1>Incidents</h1>
        <p>
          Quality incidents across suppliers and products
        </p>
      </div>
    </header>

    <section className="panel">

      <div className="panel-header">
        <div>
          <h2>Quality Incidents</h2>
          <p>
            {incidents.length} incidents recorded across suppliers and products
          </p>
        </div>
      </div>

      <div className="table-container">

        <table>

          <thead>
            <tr>
              <th>Incident ID</th>
              <th>Supplier</th>
              <th>Product</th>
              <th>Date</th>
              <th>Incident Type</th>
              <th>Severity</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>

            {incidents.map((incident) => (

              <tr key={incident.incident_id}>

                <td className="incident-id">
                  {incident.incident_id}
                </td>

                <td className="supplier-name">
                  {incident.supplier_name}
                </td>

                <td className="product-name">
                  {incident.product_name}
                </td>

                <td className="incident-date">
                  {incident.incident_date}
                </td>

                <td className="incident-type">
                  {incident.incident_type}
                </td>

                <td>
                  <span
                    className={`severity-badge ${
                      incident.severity.toLowerCase()
                    }`}
                  >
                    {incident.severity}
                  </span>
                </td>

                <td>
                  <span className="incident-status">
                    {incident.status}
                  </span>
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </section>

  </section>
)}

{activePage === "Corrective Actions" && (
  <section>

    <header className="header">
      <div>
        <h1>Corrective Actions</h1>
        <p>
          Tracking corrective actions raised from quality incidents
        </p>
      </div>
    </header>

    <section className="panel">

      <div className="panel-header">
        <div>
          <h2>Corrective Action Records</h2>
          <p>
            {correctiveActions.length} corrective actions recorded across quality incidents
          </p>
        </div>
      </div>

      <div className="table-container">

        <table>

          <thead>
            <tr>
              <th>Action ID</th>
              <th>Supplier</th>
              <th>Incident</th>
              <th>Action Type</th>
              <th>Date Opened</th>
              <th>Due Date</th>
              <th>Date Closed</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>

            {correctiveActions.map((action) => (

              <tr key={action.action_id}>

                <td className="action-id">
                  {action.action_id}
                </td>

                <td className="supplier-name">
                  {action.supplier_name}
                </td>

                <td className="incident-id">
                  {action.incident_id}
                </td>

                <td className="action-type">
                  {action.action_type}
                </td>

                <td className="action-date">
                  {action.date_opened}
                </td>

                <td className="action-date">
                  {action.due_date}
                </td>

                <td>
                  {action.date_closed ? (
                    action.date_closed
                  ) : (
                    <span className="not-closed">
                      Open
                    </span>
                  )}
                </td>

                <td>
                  <span className="corrective-action-status">
                    {action.status}
                  </span>
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </section>

  </section>
)}

      </main>

    </div>
  );
}

export default App;