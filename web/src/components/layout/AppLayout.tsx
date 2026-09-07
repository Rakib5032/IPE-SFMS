import {
  Outlet,
} from "react-router-dom";

import {
  useState,
} from "react";

import Sidebar
  from "./Sidebar";

import AppHeader
  from "./AppHeader";

import "./AppLayout.css";


function AppLayout() {

  const [
    sidebarOpen,
    setSidebarOpen,
  ] = useState(false);


  return (
    <div className="app-layout">


      {/* ==================================================
          DRAWER
          ================================================== */}

      <Sidebar
        open={sidebarOpen}
        onClose={() =>
          setSidebarOpen(false)
        }
      />


      {/* ==================================================
          MAIN APPLICATION
          ================================================== */}

      <div className="app-main">


        {/* HEADER */}

        <AppHeader
          onMenuClick={() =>
            setSidebarOpen(true)
          }
        />


        {/* PAGE */}

        <main className="app-content">

          <Outlet />

        </main>

      </div>

    </div>
  );
}


export default AppLayout;