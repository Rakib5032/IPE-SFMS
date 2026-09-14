import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Login from "../pages/auth/Login";
import Dashboard from "../pages/dashboard/Dashboard";
import Users from "../pages/users/Users";
import Organization from "../pages/organization/Organization";
import LineDetails from "../pages/lines/LineDetails";
import ComingSoon from "../pages/common/ComingSoon";
import Layouts from "../pages/layoutus/Layouts";

import ProtectedRoute from "./ProtectedRoute";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Login */}
        <Route
          path="/"
          element={<Login />}
        />

        {/* Dashboard */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        {/* Users */}
        <Route
          path="/users"
          element={
            <ProtectedRoute>
              <Users />
            </ProtectedRoute>
          }
        />

        {/* Organizations */}
        <Route
          path="/organizations"
          element={
            <ProtectedRoute>
              <Organization />
            </ProtectedRoute>
          }
        />

        {/* Line Details */}
        <Route
          path="/lines/:lineId"
          element={
            <ProtectedRoute>
              <LineDetails />
            </ProtectedRoute>
          }
        />

        {/* Layout Management */}
        <Route
          path="/layout"
          element={
            <ProtectedRoute>
              <Layouts />
            </ProtectedRoute>
          }
        />

        {/* Layout Details */}
        <Route
          path="/layout/:layoutId"
          element={
            <ProtectedRoute>
              <Layouts />
            </ProtectedRoute>
          }
        />

        {/* Coming Soon */}
        <Route
          path="/coming-soon"
          element={
            <ProtectedRoute>
              <ComingSoon />
            </ProtectedRoute>
          }
        />

        {/* Any page that has not been implemented yet */}
        <Route
          path="*"
          element={
            <ProtectedRoute>
              <ComingSoon />
            </ProtectedRoute>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;