import {
  useLocation,
  useNavigate,
} from "react-router-dom";

interface AppHeaderProps {
  onMenuClick: () => void;
}

const pageTitles: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/users": "User Management",
  "/organizations": "Organization Management",
  "/lines": "Lines",
  "/layout": "Layout",
  "/production": "Production",
  "/reports": "Reports",
  "/profile": "Profile",
  "/settings": "Settings",
};

function AppHeader({
  onMenuClick,
}: AppHeaderProps) {

  const location = useLocation();
  const navigate = useNavigate();

  const pageTitle =
    pageTitles[location.pathname] || "SFMS";

  const isDashboard =
    location.pathname === "/dashboard";

  return (
    <header className="app-header">

      {/* ==================================================
          LEFT SIDE
          ================================================== */}

      <div className="app-header-left">

        {/* DRAWER BUTTON */}

        <button
          type="button"
          className="app-menu-button"
          onClick={onMenuClick}
          aria-label="Open navigation menu"
          title="Open navigation menu"
        >
          <span />
          <span />
          <span />
        </button>


        {/* PAGE TITLE */}

        <div className="app-header-title">

          <h1>
            {pageTitle}
          </h1>

          <span>
            Sewing Floor Management System
          </span>

        </div>

      </div>


      {/* ==================================================
          BACK TO DASHBOARD
          ================================================== */}

      {!isDashboard && (
        <button
          type="button"
          className="header-back-button"
          onClick={() =>
            navigate("/dashboard")
          }
        >
          <span>
            ←
          </span>

          <span>
            Back to Dashboard
          </span>
        </button>
      )}

    </header>
  );
}

export default AppHeader;