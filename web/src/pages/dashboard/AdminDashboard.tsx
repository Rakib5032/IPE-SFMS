function AdminDashboard() {
  return (
    <div className="role-dashboard">
      <div className="dashboard-welcome">
        <h1>Admin Dashboard</h1>
        <p>System-wide overview and administration.</p>
      </div>

      <div className="dashboard-cards">
        <div className="dashboard-card">
          <span>Total Users</span>
          <strong>0</strong>
        </div>

        <div className="dashboard-card">
          <span>Total Lines</span>
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

export default AdminDashboard;