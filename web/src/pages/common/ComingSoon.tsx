import { useNavigate } from "react-router-dom";
import "./ComingSoon.css";

function ComingSoon() {
  const navigate = useNavigate();

  return (
    <div className="coming-soon-page">
      <div className="coming-soon-card">

        {/* Cartoon Animation */}
        <div className="cartoon-scene">

          {/* Ground */}
          <div className="scene-ground" />

          {/* Clouds */}
          <div className="scene-cloud cloud-1" />
          <div className="scene-cloud cloud-2" />

          {/* Toolbox */}
          <div className="toolbox">
            <div className="toolbox-handle" />
            <div className="toolbox-body">
              <span />
              <span />
            </div>
          </div>

          {/* Hammer */}
          <div className="hammer">
            <div className="hammer-head" />
            <div className="hammer-handle" />
          </div>

          {/* Worker */}
          <div className="worker">

            {/* Head */}
            <div className="worker-head">
              <div className="worker-hair" />

              {/* Helmet */}
              <div className="worker-helmet">
                <span />
              </div>

              <div className="worker-eye eye-left" />
              <div className="worker-eye eye-right" />

              <div className="worker-mouth" />
            </div>

            {/* Body */}
            <div className="worker-body">
              <div className="worker-shirt-line" />
            </div>

            {/* Arms */}
            <div className="worker-arm arm-left" />
            <div className="worker-arm arm-right" />

            {/* Legs */}
            <div className="worker-leg leg-left" />
            <div className="worker-leg leg-right" />

            {/* Shoes */}
            <div className="worker-shoe shoe-left" />
            <div className="worker-shoe shoe-right" />
          </div>

          {/* Sign */}
          <div className="construction-sign">
            <div className="sign-board">
              <span>COMING</span>
              <span>SOON</span>
            </div>

            <div className="sign-post post-left" />
            <div className="sign-post post-right" />
          </div>

          {/* Small funny gear */}
          <div className="floating-gear gear-1">⚙</div>
          <div className="floating-gear gear-2">⚙</div>

          {/* Impact lines */}
          <div className="impact impact-1" />
          <div className="impact impact-2" />
          <div className="impact impact-3" />

        </div>

        {/* Status */}
        <div className="coming-soon-status">
          <span className="status-dot" />
          In Development
        </div>

        {/* Title */}
        <h1 className="coming-soon-title">
          Coming Soon
        </h1>

        {/* Description */}
        <p className="coming-soon-description">
          This section of the Sewing Floor Management
          System is currently under development.
          It will be available in a future release.
        </p>

        {/* Button */}
        <button
          type="button"
          className="coming-soon-button"
          onClick={() => navigate("/dashboard")}
        >
          <span className="button-arrow">
            ←
          </span>

          Go to Dashboard
        </button>

      </div>
    </div>
  );
}

export default ComingSoon;