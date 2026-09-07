import {
  useNavigate,
} from "react-router-dom";

import "./BackToDashboard.css";

function BackToDashboard() {

  const navigate =
    useNavigate();


  return (
    <button
      type="button"
      className="back-dashboard-button"
      onClick={() =>
        navigate("/dashboard")
      }
    >
      <span className="back-dashboard-icon">
        ←
      </span>

      <span>
        Back to Dashboard
      </span>

    </button>
  );
}


export default BackToDashboard;