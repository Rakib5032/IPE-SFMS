import { useNavigate } from "react-router-dom";

function UserManagement() {
  const navigate = useNavigate();

  return (
    <main className="user-management-page">

      <div className="user-management-header">
        <div>
          <div className="dashboard-eyebrow">
            SFMS • Users
          </div>

          <h1>
            User Management
          </h1>

          <p>
            Manage employees and system users.
          </p>
        </div>
      </div>


      <div className="user-management-grid">

        {/* ==================================================
            UPDATE USER
            ================================================== */}

        <button
          type="button"
          className="user-management-card"
          onClick={() =>
            navigate("/users/update")
          }
        >

          <div className="user-management-icon">
            ✎
          </div>

          <div>
            <h2>
              Update User
            </h2>

            <p>
              Search for an existing user
              and update their information.
            </p>
          </div>

          <span className="user-management-arrow">
            →
          </span>

        </button>


        {/* ==================================================
            CREATE USER
            ================================================== */}

        <button
          type="button"
          className="user-management-card"
          onClick={() =>
            navigate("/users/create")
          }
        >

          <div className="user-management-icon create">
            +
          </div>

          <div>
            <h2>
              Create User
            </h2>

            <p>
              Create a new employee account
              and assign their role.
            </p>
          </div>

          <span className="user-management-arrow">
            →
          </span>

        </button>

      </div>

    </main>
  );
}

export default UserManagement;