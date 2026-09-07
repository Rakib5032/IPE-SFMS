import { useAuth } from "../../hooks/useAuth";
import DashboardLayout from "../../layouts/DashboardLayout";

function Dashboard() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <DashboardLayout>
        <div className="dashboard-loading">
          Loading dashboard...
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="dashboard-page">

        {/* Welcome */}
        <section className="dashboard-welcome">
          <div>
            <p className="dashboard-eyebrow">
              SFMS • Dashboard
            </p>

            <h1>
              Welcome, {user?.full_name ?? "User"}
            </h1>

            {/* <p className="dashboard-subtitle">
              Here's an overview of your SFMS activities.
            </p> */}
          </div>

          <div className="dashboard-status">
            <span className="status-dot" />
            Active
          </div>
        </section>

        {/* User information
        <section className="dashboard-profile-card">

          <div className="profile-avatar">
            {user?.full_name
              ?.charAt(0)
              .toUpperCase() ?? "U"}
          </div>

          <div className="profile-info">
            <h2>
              {user?.full_name ?? "User"}
            </h2>

            <p>
            {user?.designation ?? "SFMS User"}
            </p>
          </div>

          <div className="profile-details">

            <div>
              <span>Employee ID</span>
              <strong>
                {user?.employee_id ?? "-"}
              </strong>
            </div>

            <div>
              <span>Username</span>
              <strong>
                {user?.username ?? "-"}
              </strong>
            </div>

            <div>
              <span>Email</span>
              <strong>
                {user?.email ?? "-"}
              </strong>
            </div>

            <div>
              <span>Role</span>
              <strong>
                {user?.role_id ?? "-"}
              </strong>
            </div>

          </div>
        </section> */}

        {/* Overview */}
        <section className="dashboard-section">

          <div className="section-heading">
            <div>
              <h2>Overview</h2>
              {/* <p>
                Your current SFMS activity at a glance.
              </p> */}
            </div>
          </div>

          <div className="dashboard-cards">

            <div className="dashboard-card">
              <div className="dashboard-card-icon">
                👥
              </div>

              <div>
                <span>Total Users</span>
                <strong>0</strong>
              </div>

              <small>
                System users
              </small>
            </div>

            <div className="dashboard-card">
              <div className="dashboard-card-icon">
                🏭
              </div>

              <div>
                <span>Production Lines</span>
                <strong>0</strong>
              </div>

              <small>
                Active production lines
              </small>
            </div>

            <div className="dashboard-card">
              <div className="dashboard-card-icon">
                📦
              </div>

              <div>
                <span>Today's Production</span>
                <strong>0</strong>
              </div>

              <small>
                Production completed
              </small>
            </div>

            <div className="dashboard-card">
              <div className="dashboard-card-icon">
                📈
              </div>

              <div>
                <span>Efficiency</span>
                <strong>0%</strong>
              </div>

              <small>
                Overall efficiency
              </small>
            </div>

          </div>
        </section>

        {/* Quick access */}
        <section className="dashboard-section">

          <div className="section-heading">
            <div>
              <h2>Quick Access</h2>
              <p>
                Frequently used SFMS modules.
              </p>
            </div>
          </div>

          <div className="quick-access-grid">

            <div className="quick-access-card">
              <span className="quick-access-icon">
                👥
              </span>

              <div>
                <strong>User Management</strong>
                <p>
                  Manage system users
                </p>
              </div>
            </div>

            <div className="quick-access-card">
              <span className="quick-access-icon">
                🏭
              </span>

              <div>
                <strong>Line Management</strong>
                <p>
                  Manage production lines
                </p>
              </div>
            </div>

            <div className="quick-access-card">
              <span className="quick-access-icon">
                ⚙️
              </span>

              <div>
                <strong>Production</strong>
                <p>
                  Monitor production
                </p>
              </div>
            </div>

            <div className="quick-access-card">
              <span className="quick-access-icon">
                📊
              </span>

              <div>
                <strong>Reports</strong>
                <p>
                  View production reports
                </p>
              </div>
            </div>

          </div>
        </section>

      </div>
    </DashboardLayout>
  );
}

export default Dashboard;