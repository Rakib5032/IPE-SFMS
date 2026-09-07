function DGMDashboard() {
  return (
    <div className="role-dashboard">
      <div className="dashboard-welcome">
        <h1>DGM Dashboard</h1>
        <p>Overall operational and production overview.</p>
      </div>

      <div className="dashboard-cards">
        <div className="dashboard-card">
          <span>Total Production</span>
          <strong>0</strong>
        </div>

        <div className="dashboard-card">
          <span>Line Efficiency</span>
          <strong>0%</strong>
        </div>

        <div className="dashboard-card">
          <span>Active Lines</span>
          <strong>0</strong>
        </div>

        <div className="dashboard-card">
          <span>Departments</span>
          <strong>0</strong>
        </div>
      </div>
    </div>
  );
}

export default DGMDashboard;