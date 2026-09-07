function FloorDashboard() {
  return (
    <div className="role-dashboard">
      <div className="dashboard-welcome">
        <h1>Floor Dashboard</h1>
        <p>
          Monitor your floor, assigned lines, and production.
        </p>
      </div>

      <div className="dashboard-cards">
        <div className="dashboard-card">
          <span>Active Lines</span>
          <strong>0</strong>
        </div>

        <div className="dashboard-card">
          <span>Today's Target</span>
          <strong>0</strong>
        </div>

        <div className="dashboard-card">
          <span>Today's Production</span>
          <strong>0</strong>
        </div>

        <div className="dashboard-card">
          <span>Floor Efficiency</span>
          <strong>0%</strong>
        </div>
      </div>

      <div className="dashboard-section floor-dashboard-section">
        <h2>Line Status</h2>

        <div className="floor-line-status">
          <div className="dashboard-card">
            <span>Running</span>
            <strong>0</strong>
          </div>

          <div className="dashboard-card">
            <span>Stopped</span>
            <strong>0</strong>
          </div>

          <div className="dashboard-card">
            <span>Under Maintenance</span>
            <strong>0</strong>
          </div>
        </div>
      </div>
    </div>
  );
}

export default FloorDashboard;