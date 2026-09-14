import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import DashboardLayout from "../../layouts/DashboardLayout";
import { getLine } from "../../services/lineService";
import api from "../../services/api";

import "./LineDetails.css";

interface Line {
  id: number;
  line_number: number;
  name: string;
  organization_unit_id: number;
  is_active: boolean;
}

interface LineStatus {
  id: number;
  line_id: number;
  status: string;
  reason?: string | null;
  started_at: string;
  ended_at?: string | null;
}

interface Layout {
  id: number;
  line_id: number;
  buyer: string;
  style?: string | null;
  job?: string | null;
  smv: number;
  required_machine_count?: number | null;
  total_machines: number;
  status: string;
  started_at: string;
  completed_at?: string | null;
  duration_minutes?: number | null;
  is_active?: boolean | null;
  notes?: string | null;
}

function LineDetails() {
  const { lineId } = useParams<{ lineId: string }>();
  const navigate = useNavigate();

  const [line, setLine] = useState<Line | null>(null);
  const [status, setStatus] = useState<LineStatus | null>(null);
  const [layout, setLayout] = useState<Layout | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!lineId) {
      setError("Line ID is missing.");
      setLoading(false);
      return;
    }

    async function loadLineDetails() {
      try {
        setLoading(true);
        setError("");

        const id = Number(lineId);

        if (!Number.isInteger(id) || id <= 0) {
          setError("Invalid line ID.");
          return;
        }

        const lineResult = await getLine(id);
        setLine(lineResult);

        const [statusResult, layoutResult] = await Promise.all([
          api.get<LineStatus | null>(
            `/line-status/${id}`,
          ),
          api.get<Layout | null>(
            `/layouts/line/${id}/active`,
          ),
        ]);

        setStatus(statusResult.data);
        setLayout(layoutResult.data);
      } catch (err: any) {
        setError(
          err.response?.data?.detail ??
            "Failed to load line details.",
        );
      } finally {
        setLoading(false);
      }
    }

    loadLineDetails();
  }, [lineId]);

  function formatDate(value?: string | null) {
    if (!value) return "—";

    return new Date(value).toLocaleString();
  }

  function getStatusClass(value?: string | null) {
    switch (value) {
      case "RUNNING":
        return "status-running";

      case "LAYOUT":
        return "status-layout";

      case "OFF":
        return "status-off";

      default:
        return "status-unknown";
    }
  }

  function getStatusLabel(value?: string | null) {
    switch (value) {
      case "RUNNING":
        return "Running";

      case "LAYOUT":
        return "Layout Change";

      case "OFF":
        return "Off";

      default:
        return "No Status";
    }
  }

  function getStatusDescription(value?: string | null) {
    switch (value) {
      case "RUNNING":
        return "Production line is currently operational.";

      case "LAYOUT":
        return "The line is currently undergoing layout activity.";

      case "OFF":
        return "The production line is currently stopped.";

      default:
        return "No current operational status is available.";
    }
  }

  if (loading) {
    return (
      <DashboardLayout>
        <div className="line-details-page">
          <div className="line-details-loading">
            Loading line details...
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="line-details-page">

        {/* ======================================================
            HEADER
        ====================================================== */}

        <header className="line-details-header">

          <button
            type="button"
            className="line-back-button"
            onClick={() => navigate("/organizations")}
          >
            <span aria-hidden="true">←</span>
            Back to Organizations
          </button>

          {line && (
            <div className="line-title-row">

              <div>
                <p className="line-eyebrow">
                  SFMS • Production Line
                </p>

                <h1>
                  Line {line.line_number}
                </h1>

                <p className="line-subtitle">
                  {line.name}
                </p>
              </div>

              <div>
                <span
                  className={
                    line.is_active
                      ? "line-active-badge"
                      : "line-inactive-badge"
                  }
                >
                  {line.is_active
                    ? "Active Line"
                    : "Inactive Line"}
                </span>
              </div>

            </div>
          )}

        </header>


        {/* ======================================================
            ERROR
        ====================================================== */}

        {error && (
          <div
            className="line-details-error"
            role="alert"
          >
            <span aria-hidden="true">⚠</span>
            <span>{error}</span>
          </div>
        )}


        {line && !error && (
          <>

            {/* ==================================================
                QUICK SUMMARY
            ================================================== */}

            <section className="line-summary-grid">

              <div className="line-summary-card">
                <span>Line Number</span>

                <strong>
                  {line.line_number}
                </strong>
              </div>


              <div className="line-summary-card">
                <span>Line Name</span>

                <strong>
                  {line.name}
                </strong>
              </div>


              <div className="line-summary-card">
                <span>Current Status</span>

                <strong
                  className={getStatusClass(
                    status?.status,
                  )}
                >
                  {getStatusLabel(status?.status)}
                </strong>
              </div>


              <div className="line-summary-card">
                <span>Active Layout</span>

                <strong>
                  {layout ? "Assigned" : "None"}
                </strong>
              </div>

            </section>


            {/* ==================================================
                LIVE STATUS
            ================================================== */}

            <section className="line-details-section">

              <div className="line-section-heading">
                <div>
                  <p className="line-section-label">
                    LIVE INFORMATION
                  </p>

                  <h2>
                    Current Line Status
                  </h2>
                </div>
              </div>


              {status ? (

                <div className="line-status-panel">

                  <div className="line-status-main">

                    <span
                      className={`line-status-indicator ${getStatusClass(
                        status.status,
                      )}`}
                      aria-hidden="true"
                    />

                    <div>

                      <strong
                        className={getStatusClass(
                          status.status,
                        )}
                      >
                        {getStatusLabel(
                          status.status,
                        )}
                      </strong>

                      <p>
                        {getStatusDescription(
                          status.status,
                        )}
                      </p>

                      <p>
                        Started{" "}
                        {formatDate(
                          status.started_at,
                        )}
                      </p>

                    </div>

                  </div>


                  {status.reason && (
                    <div className="line-status-reason">

                      <span>
                        Current Reason
                      </span>

                      <p>
                        {status.reason}
                      </p>

                    </div>
                  )}

                </div>

              ) : (

                <div className="line-empty-state">

                  <strong>
                    No current status
                  </strong>

                  <span>
                    No operational status has been
                    recorded for this line.
                  </span>

                </div>

              )}

            </section>


            {/* ==================================================
                ACTIVE LAYOUT
            ================================================== */}

            <section className="line-details-section">

              <div className="line-section-heading">

                <div>
                  <p className="line-section-label">
                    PRODUCTION
                  </p>

                  <h2>
                    Active Layout
                  </h2>
                </div>

              </div>


              {layout ? (

                <div className="layout-summary-card">

                  {/* Layout Header */}

                  <div className="layout-summary-top">

                    <div>
                      <span>
                        Buyer
                      </span>

                      <strong>
                        {layout.buyer}
                      </strong>
                    </div>


                    <span
                      className={`layout-status-badge ${getStatusClass(
                        layout.status,
                      )}`}
                    >
                      {getStatusLabel(
                        layout.status,
                      )}
                    </span>

                  </div>


                  {/* Layout Information */}

                  <div className="layout-summary-grid">

                    <div>
                      <span>
                        Style
                      </span>

                      <strong>
                        {layout.style ?? "—"}
                      </strong>
                    </div>


                    <div>
                      <span>
                        Job
                      </span>

                      <strong>
                        {layout.job ?? "—"}
                      </strong>
                    </div>


                    <div>
                      <span>
                        SMV
                      </span>

                      <strong>
                        {layout.smv}
                      </strong>
                    </div>


                    <div>
                      <span>
                        Total Machines
                      </span>

                      <strong>
                        {layout.total_machines}
                      </strong>
                    </div>


                    <div>
                      <span>
                        Required Machines
                      </span>

                      <strong>
                        {layout.required_machine_count ??
                          "—"}
                      </strong>
                    </div>


                    <div>
                      <span>
                        Started
                      </span>

                      <strong>
                        {formatDate(
                          layout.started_at,
                        )}
                      </strong>
                    </div>

                  </div>


                  {/* Notes */}

                  {layout.notes && (
                    <div className="layout-notes">

                      <span>
                        Notes
                      </span>

                      <p>
                        {layout.notes}
                      </p>

                    </div>
                  )}


                  {/* Action */}

                  <div className="layout-actions">

                    <button
                      type="button"
                      onClick={() =>
                        navigate(
                          `/layout/${layout.id}`,
                        )
                      }
                    >
                      View Layout
                      <span aria-hidden="true">
                        →
                      </span>
                    </button>

                  </div>

                </div>

              ) : (

                <div className="line-empty-state">

                  <strong>
                    No active layout
                  </strong>

                  <span>
                    No active production layout is
                    currently assigned to this line.
                  </span>

                </div>

              )}

            </section>

          </>
        )}

      </div>
    </DashboardLayout>
  );
}

export default LineDetails;