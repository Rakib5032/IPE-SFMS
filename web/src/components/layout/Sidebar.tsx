import { NavLink } from "react-router-dom";

import { useAuth } from "../../hooks/useAuth";
import { hasPermission } from "../../config/permissions";

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

interface MenuItem {
  label: string;
  path: string;
  permission: Parameters<typeof hasPermission>[1];
}


/* ============================================================
   OPERATIONS
   ============================================================ */

const operationItems: MenuItem[] = [
  {
    label: "Lines",
    path: "/lines",
    permission: "VIEW_LINES",
  },
  {
    label: "Layout",
    path: "/layout",
    permission: "VIEW_LAYOUT",
  },
  {
    label: "Production",
    path: "/production",
    permission: "VIEW_PRODUCTION",
  },
];


/* ============================================================
   MANAGEMENT
   ============================================================ */

const managementItems: MenuItem[] = [
  {
    label: "Users",
    path: "/users",
    permission: "MANAGE_USERS",
  },
  {
    label: "Organizations",
    path: "/organizations",
    permission: "VIEW_ORGANIZATIONS",
  },
];


/* ============================================================
   REPORTING
   ============================================================ */

const reportingItems: MenuItem[] = [
  {
    label: "Reports",
    path: "/reports",
    permission: "VIEW_REPORTS",
  },
];


/* ============================================================
   SIDEBAR
   ============================================================ */

function Sidebar({
  open,
  onClose,
}: SidebarProps) {

  const { user } = useAuth();

  const roleId = user?.role_id;

  /*
   * ADMIN role ID
   *
   * Users are restricted to Administrator.
   * Organizations are controlled by VIEW_ORGANIZATIONS
   * permission and therefore can be visible to other
   * authorized roles.
   */
  const isAdmin = roleId === 1;


  /* ==========================================================
     PERMISSION CHECK
     ========================================================== */

  const canView = (
    permission: MenuItem["permission"],
  ): boolean => {

    return hasPermission(
      roleId,
      permission,
    );
  };


  /* ==========================================================
     OPERATIONS
     ========================================================== */

  const visibleOperationItems =
    operationItems.filter(
      (item) =>
        canView(item.permission),
    );


  /* ==========================================================
     MANAGEMENT
     ========================================================== */

  const visibleManagementItems =
    managementItems.filter(
      (item) => {

        /*
         * Users
         *
         * ADMIN only
         */
        if (item.label === "Users") {
          return (
            isAdmin &&
            canView(item.permission)
          );
        }


        /*
         * Organizations
         *
         * Controlled by VIEW_ORGANIZATIONS
         * permission.
         */
        if (item.label === "Organizations") {
          return canView(item.permission);
        }


        return canView(
          item.permission,
        );
      },
    );


  /* ==========================================================
     REPORTING
     ========================================================== */

  const visibleReportingItems =
    reportingItems.filter(
      (item) =>
        canView(item.permission),
    );


  /* ==========================================================
     USER INITIAL
     ========================================================== */

  const userInitial =
    user?.full_name
      ?.charAt(0)
      ?.toUpperCase() || "U";


  /* ==========================================================
     RENDER
     ========================================================== */

  return (
    <>

      {/* ======================================================
          SIDEBAR OVERLAY
          ====================================================== */}

      {open && (
        <div
          className="sidebar-overlay"
          onClick={onClose}
          aria-hidden="true"
        />
      )}


      {/* ======================================================
          SIDEBAR
          ====================================================== */}

      <aside
        className={`sidebar ${
          open
            ? "sidebar-open"
            : ""
        }`}
        aria-label="Application menu"
      >


        {/* ====================================================
            HEADER
            ==================================================== */}

        <div className="sidebar-header">

          <div className="sidebar-brand">

            <h2>
              SFMS
            </h2>

            <span>
              Sewing Floor Management
            </span>

          </div>


          {/* CLOSE BUTTON */}

          <button
            type="button"
            className="sidebar-close"
            onClick={onClose}
            aria-label="Close menu"
          >
            ×
          </button>

        </div>


        {/* ====================================================
            NAVIGATION
            ==================================================== */}

        <nav className="sidebar-nav">


          {/* ==================================================
              DASHBOARD
              ================================================== */}

          <NavLink
            to="/dashboard"
            onClick={onClose}
            className="sidebar-main-link"
          >

            <span className="sidebar-icon">
              ⌂
            </span>

            <span>
              Dashboard
            </span>

          </NavLink>


          {/* ==================================================
              OPERATIONS
              ================================================== */}

          {visibleOperationItems.length > 0 && (

            <div className="sidebar-section">

              <div className="sidebar-section-title">
                OPERATIONS
              </div>


              {visibleOperationItems.map(
                (item) => (

                  <NavLink
                    key={item.path}
                    to={item.path}
                    onClick={onClose}
                  >

                    <span className="sidebar-icon">

                      {item.label === "Lines" &&
                        "▦"}

                      {item.label === "Layout" &&
                        "▤"}

                      {item.label === "Production" &&
                        "◈"}

                    </span>

                    <span>
                      {item.label}
                    </span>

                  </NavLink>

                ),
              )}

            </div>

          )}


          {/* ==================================================
              MANAGEMENT
              ================================================== */}

          {visibleManagementItems.length > 0 && (

            <div className="sidebar-section">

              <div className="sidebar-section-title">
                MANAGEMENT
              </div>


              {visibleManagementItems.map(
                (item) => (

                  <NavLink
                    key={item.path}
                    to={item.path}
                    onClick={onClose}
                  >

                    <span className="sidebar-icon">

                      {item.label === "Users" &&
                        "♙"}

                      {item.label === "Organizations" &&
                        "▥"}

                    </span>

                    <span>
                      {item.label}
                    </span>

                  </NavLink>

                ),
              )}

            </div>

          )}


          {/* ==================================================
              REPORTING
              ================================================== */}

          {visibleReportingItems.length > 0 && (

            <div className="sidebar-section">

              <div className="sidebar-section-title">
                REPORTING
              </div>


              {visibleReportingItems.map(
                (item) => (

                  <NavLink
                    key={item.path}
                    to={item.path}
                    onClick={onClose}
                  >

                    <span className="sidebar-icon">
                      ▥
                    </span>

                    <span>
                      {item.label}
                    </span>

                  </NavLink>

                ),
              )}

            </div>

          )}

        </nav>


        {/* ====================================================
            BOTTOM USER AREA
            ==================================================== */}

        <div className="sidebar-bottom">


          {/* ==================================================
              PROFILE
              ================================================== */}

          <NavLink
            to="/profile"
            onClick={onClose}
            className="sidebar-profile"
          >

            <div className="sidebar-avatar">
              {userInitial}
            </div>


            <div className="sidebar-user-info">

              <strong>
                {user?.full_name ||
                  "User"}
              </strong>

              <span>
                {user?.designation ||
                  "Employee"}
              </span>

            </div>

          </NavLink>


          {/* ==================================================
              SETTINGS
              ================================================== */}

          <NavLink
            to="/settings"
            onClick={onClose}
            className="sidebar-bottom-link"
          >

            <span className="sidebar-icon">
              ⚙
            </span>

            <span>
              Settings
            </span>

          </NavLink>

        </div>

      </aside>

    </>
  );
}


export default Sidebar;