function ManagerDashboard() {
  return (
    <div className="role-dashboard">
      <div className="dashboard-welcome">
        <h1>Manager Dashboard</h1>
        <p>Department and production management overview.</p>
      </div>

      <div className="dashboard-cards">
        <div className="dashboard-card">
          <span>Today's Production</span>
          <strong>0</strong>
        </div>

        <div className="dashboard-card">
          <span>Target</span>
          <strong>0</strong>
        </div>

        <div className="dashboard-card">
          <span>Efficiency</span>
          <strong>0%</strong>
        </div>

        <div className="dashboard-card">
          <span>Active Lines</span>
          <strong>0</strong>
        </div>
      </div>
    </div>
  );
}

export default ManagerDashboard;