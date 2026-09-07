import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

interface HeaderProps {
  onMenuClick: () => void;
  onLogout: () => void;
}

const roleNames: Record<number, string> = {
  1: "Administrator",
  2: "Deputy General Manager",
  3: "Central Manager",
  4: "Group Manager",
  5: "Floor IE",
  6: "Supervisor",
  8: "Deputy Production Manager",
  9: "Assistant Production Manager",
  10: "In-Charge",
};

function Header({ onMenuClick, onLogout }: HeaderProps) {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [accountOpen, setAccountOpen] = useState(false);
  const accountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function closeOnOutsideClick(event: MouseEvent) {
      if (
        accountRef.current &&
        !accountRef.current.contains(event.target as Node)
      ) {
        setAccountOpen(false);
      }
    }

    function closeOnEscape(event: KeyboardEvent) {
      if (event.key === "Escape") setAccountOpen(false);
    }

    document.addEventListener("mousedown", closeOnOutsideClick);
    document.addEventListener("keydown", closeOnEscape);

    return () => {
      document.removeEventListener("mousedown", closeOnOutsideClick);
      document.removeEventListener("keydown", closeOnEscape);
    };
  }, []);

  const fullName = user?.full_name ?? "User";
  const designation = user?.designation ?? "Employee";
  const roleName = roleNames[user?.role_id ?? 0] ?? "User";
  const initial = fullName.trim().charAt(0).toUpperCase() || "U";

  function goTo(path: string) {
    setAccountOpen(false);
    navigate(path);
  }

  return (
    <header className="app-header">
      <div className="app-header-left">
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

        <button
          type="button"
          className="app-brand"
          onClick={() => navigate("/dashboard")}
          aria-label="Go to SFMS dashboard"
        >
          <span className="app-brand-name">SFMS</span>
          <span className="app-brand-subtitle">
            Sewing Floor Management System
          </span>
        </button>
      </div>

      <div className="app-header-right">
        <button
          type="button"
          className="notification-button"
          aria-label="Notifications"
          title="Notifications"
        >
          <span aria-hidden="true">🔔</span>
        </button>

        <div className="account-menu" ref={accountRef}>
          <button
            type="button"
            className={`account-trigger ${
              accountOpen ? "account-trigger-open" : ""
            }`}
            onClick={() => setAccountOpen((open) => !open)}
            aria-expanded={accountOpen}
            aria-haspopup="menu"
          >
            <span className="account-avatar">{initial}</span>

            <span className="account-summary">
              <strong>{fullName}</strong>
              <span>{designation}</span>
            </span>

            <span className="account-chevron" aria-hidden="true">
              ▾
            </span>
          </button>

          {accountOpen && (
            <div className="account-dropdown" role="menu">
              <div className="account-dropdown-header">
                <div className="account-dropdown-avatar">{initial}</div>
                <div>
                  <strong>{fullName}</strong>
                  <span>{roleName}</span>
                </div>
              </div>

              <div className="account-dropdown-divider" />

              <button
                type="button"
                className="account-dropdown-item"
                onClick={() => goTo("/profile")}
                role="menuitem"
              >
                <span aria-hidden="true">◉</span>
                <span>Profile</span>
              </button>

              <button
                type="button"
                className="account-dropdown-item"
                onClick={() => goTo("/settings")}
                role="menuitem"
              >
                <span aria-hidden="true">⚙</span>
                <span>Settings</span>
              </button>

              <div className="account-dropdown-divider" />

              <button
                type="button"
                className="account-dropdown-item account-logout-item"
                onClick={() => {
                  setAccountOpen(false);
                  onLogout();
                }}
                role="menuitem"
              >
                <span aria-hidden="true">↪</span>
                <span>Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

export default Header;
