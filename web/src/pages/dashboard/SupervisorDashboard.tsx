function SupervisorDashboard() {
  return (
    <div className="role-dashboard">
      <div className="dashboard-welcome">
        <h1>Supervisor Dashboard</h1>
        <p>Your assigned line and production overview.</p>
      </div>

      <div className="dashboard-cards">
        <div className="dashboard-card">
          <span>Assigned Lines</span>
          <strong>0</strong>
        </div>

        <div className="dashboard-card">
          <span>Today's Target</span>
          <strong>0</strong>
        </div>

        <div className="dashboard-card">
          <span>Production</span>
          <strong>0</strong>
        </div>

        <div className="dashboard-card">
          <span>Efficiency</span>
          <strong>0%</strong>
        </div>
      </div>
    </div>
  );
}

export default SupervisorDashboard;