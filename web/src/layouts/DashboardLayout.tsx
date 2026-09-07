import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Header from "../components/layout/Header";
import Sidebar from "../components/layout/Sidebar";
import Footer from "../components/layout/Footer";

import { getRefreshToken, clearTokens } from "../utils/storage";
import { logout } from "../services/authService";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const navigate = useNavigate();

  async function handleLogout() {
    const refreshToken = getRefreshToken();

    try {
      if (refreshToken) await logout(refreshToken);
    } catch {
      // Continue logout even if the server request fails.
    } finally {
      clearTokens();
      navigate("/", { replace: true });
    }
  }

  return (
    <div className="app-shell">
      <Sidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <div className="app-main">
        <Header
          onMenuClick={() => setSidebarOpen(true)}
          onLogout={handleLogout}
        />

        <main className="app-content">{children}</main>

        <Footer />
      </div>
    </div>
  );
}

export default DashboardLayout;
