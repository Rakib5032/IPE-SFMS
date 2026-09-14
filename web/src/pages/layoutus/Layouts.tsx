import { FormEvent, useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import DashboardLayout from "../../layouts/DashboardLayout";
import { getLines } from "../../services/lineService";
import {
  completeLayout,
  createLayout,
  createLayoutMachine,
  getLayout,
  getLayoutMachines,
  getLineLayouts,
  updateLayout,
  updateLayoutMachine,
} from "../../services/layoutService";
import { hasPermission } from "../../config/permissions";
import { useAuth } from "../../hooks/useAuth";

import type { Line } from "../../types/line";
import type {
  Layout,
  LayoutMachine,
} from "../../types/layout";

import "./Layouts.css";

const MACHINE_STATUSES = [
  "PENDING",
  "RUNNING",
  "COMPLETED",
  "OFF",
] as const;

function formatDate(value?: string | null) {
  if (!value) return "—";
  return new Date(value).toLocaleString();
}

function statusClass(status?: string | null) {
  return (status || "UNKNOWN").toLowerCase();
}

function emptyMachineStatus(total: number) {
  const result: Record<string, string> = {};
  for (let i = 1; i <= total; i += 1) {
    result[String(i)] = "PENDING";
  }
  return result;
}

function Layouts() {
  const { layoutId } = useParams<{ layoutId?: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();

  const canManage = hasPermission(user?.role_id, "MANAGE_LAYOUT");

  const [lines, setLines] = useState<Line[]>([]);
  const [layoutsByLine, setLayoutsByLine] = useState<Record<number, Layout[]>>(
    {},
  );
  const [selectedLineId, setSelectedLineId] = useState<number | "">("");

  const [layout, setLayout] = useState<Layout | null>(null);
  const [machines, setMachines] = useState<LayoutMachine[]>([]);

  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    line_id: "",
    buyer: "",
    style: "",
    job: "",
    smv: "",
    required_machine_count: "",
    total_machines: "0",
    notes: "",
  });

  const [machineForm, setMachineForm] = useState({
    machine_number: "",
    machine_name: "",
    status: "PENDING",
    reason: "",
  });

  const selectedLine = useMemo(
    () => lines.find((line) => line.id === selectedLineId),
    [lines, selectedLineId],
  );

  async function loadOverview() {
    try {
      setLoading(true);
      setError("");

      const lineData = await getLines();
      setLines(lineData);

      const entries = await Promise.all(
        lineData.map(async (line) => {
          try {
            return [line.id, await getLineLayouts(line.id)] as const;
          } catch {
            return [line.id, []] as const;
          }
        }),
      );

      setLayoutsByLine(Object.fromEntries(entries));
    } catch (err: any) {
      setError(err.response?.data?.detail ?? "Failed to load layouts.");
    } finally {
      setLoading(false);
    }
  }

  async function loadDetail(id: number) {
    try {
      setDetailLoading(true);
      setError("");
      const [layoutData, machineData] = await Promise.all([
        getLayout(id),
        getLayoutMachines(id),
      ]);

      setLayout(layoutData);
      setMachines(machineData);
    } catch (err: any) {
      setError(err.response?.data?.detail ?? "Failed to load layout.");
      setLayout(null);
    } finally {
      setDetailLoading(false);
    }
  }

  useEffect(() => {
    if (layoutId) {
      const id = Number(layoutId);
      if (Number.isInteger(id) && id > 0) {
        loadDetail(id);
      } else {
        setError("Invalid layout ID.");
      }
      return;
    }

    loadOverview();
  }, [layoutId]);

  function openCreate(lineId?: number) {
    setMessage("");
    setError("");
    setLayout(null);

    const id = lineId ?? (selectedLineId === "" ? "" : selectedLineId);

    setForm({
      line_id: id === "" ? "" : String(id),
      buyer: "",
      style: "",
      job: "",
      smv: "",
      required_machine_count: "",
      total_machines: "0",
      notes: "",
    });

    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function openEdit(item: Layout) {
    setLayout(item);
    setForm({
      line_id: String(item.line_id),
      buyer: item.buyer,
      style: item.style ?? "",
      job: item.job ?? "",
      smv: String(item.smv),
      required_machine_count:
        item.required_machine_count == null
          ? ""
          : String(item.required_machine_count),
      total_machines: String(item.total_machines),
      notes: item.notes ?? "",
    });
    setMessage("");
    setError("");
  }

  async function handleCreate(event: FormEvent) {
    event.preventDefault();

    const lineId = Number(form.line_id);
    const total = Number(form.total_machines);
    const smv = Number(form.smv);

    if (!Number.isInteger(lineId) || lineId <= 0) {
      setError("Select a line.");
      return;
    }
    if (!form.buyer.trim()) {
      setError("Buyer is required.");
      return;
    }
    if (!Number.isFinite(smv) || smv <= 0) {
      setError("SMV must be greater than 0.");
      return;
    }
    if (!Number.isInteger(total) || total < 0) {
      setError("Total machines must be a valid number.");
      return;
    }

    try {
      setSaving(true);
      setError("");

      const created = await createLayout({
        line_id: lineId,
        buyer: form.buyer.trim(),
        style: form.style.trim() || null,
        job: form.job.trim() || null,
        smv,
        required_machine_count:
          form.required_machine_count === ""
            ? null
            : Number(form.required_machine_count),
        total_machines: total,
        machine_status: emptyMachineStatus(total),
        status: "RUNNING",
        notes: form.notes.trim() || null,
      });

      setMessage("Layout created successfully.");
      navigate(`/layout/${created.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail ?? "Failed to create layout.");
    } finally {
      setSaving(false);
    }
  }

  async function handleUpdate(event: FormEvent) {
    event.preventDefault();
    if (!layout) return;

    try {
      setSaving(true);
      setError("");

      const updated = await updateLayout(layout.id, {
        buyer: form.buyer.trim(),
        style: form.style.trim() || null,
        job: form.job.trim() || null,
        smv: Number(form.smv),
        required_machine_count:
          form.required_machine_count === ""
            ? null
            : Number(form.required_machine_count),
        total_machines: Number(form.total_machines),
        notes: form.notes.trim() || null,
      });

      setLayout(updated);
      setMessage("Layout updated successfully.");
      await loadDetail(updated.id);
    } catch (err: any) {
      setError(err.response?.data?.detail ?? "Failed to update layout.");
    } finally {
      setSaving(false);
    }
  }

  async function handleComplete() {
    if (!layout || !layout.is_active) return;
    if (!window.confirm("Complete this layout and close the active session?")) {
      return;
    }

    try {
      setSaving(true);
      setError("");
      const completed = await completeLayout(layout.id);
      setLayout(completed);
      setMessage("Layout completed.");
      await loadDetail(completed.id);
    } catch (err: any) {
      setError(err.response?.data?.detail ?? "Failed to complete layout.");
    } finally {
      setSaving(false);
    }
  }

  async function handleAddMachine(event: FormEvent) {
    event.preventDefault();
    if (!layout) return;

    const number = Number(machineForm.machine_number);
    if (!Number.isInteger(number) || number <= 0) {
      setError("Machine number must be a positive integer.");
      return;
    }

    try {
      setSaving(true);
      setError("");

      await createLayoutMachine({
        layout_id: layout.id,
        machine_number: number,
        machine_name: machineForm.machine_name.trim() || null,
        status: machineForm.status,
        reason: machineForm.reason.trim() || null,
      });

      setMachineForm({
        machine_number: "",
        machine_name: "",
        status: "PENDING",
        reason: "",
      });

      setMessage("Machine added.");
      await loadDetail(layout.id);
    } catch (err: any) {
      setError(err.response?.data?.detail ?? "Failed to add machine.");
    } finally {
      setSaving(false);
    }
  }

  async function handleMachineStatus(
    machine: LayoutMachine,
    status: string,
  ) {
    try {
      setSaving(true);
      setError("");

      await updateLayoutMachine(machine.id, { status });
      await loadDetail(machine.layout_id);
    } catch (err: any) {
      setError(
        err.response?.data?.detail ?? "Failed to update machine status.",
      );
    } finally {
      setSaving(false);
    }
  }

  if (layoutId) {
    return (
      <DashboardLayout>
        <div className="layouts-page">
          <button
            className="layout-back"
            type="button"
            onClick={() => navigate("/layout")}
          >
            ← Back to Layouts
          </button>

          {detailLoading && <div className="layout-card">Loading layout...</div>}

          {!detailLoading && layout && (
            <>
              <header className="layout-header">
                <div>
                  <p className="layout-eyebrow">SFMS • Layout</p>
                  <h1>Layout #{layout.id}</h1>
                  <p>
                    Line {layout.line_id} · {layout.buyer}
                    {layout.style ? ` · ${layout.style}` : ""}
                  </p>
                </div>
                <span className={`layout-status ${statusClass(layout.status)}`}>
                  {layout.status}
                </span>
              </header>

              {message && <div className="layout-message">{message}</div>}
              {error && <div className="layout-error">{error}</div>}

              <section className="layout-card layout-summary">
                <div><span>Buyer</span><strong>{layout.buyer}</strong></div>
                <div><span>Style</span><strong>{layout.style || "—"}</strong></div>
                <div><span>Job</span><strong>{layout.job || "—"}</strong></div>
                <div><span>SMV</span><strong>{layout.smv}</strong></div>
                <div><span>Required Machines</span><strong>{layout.required_machine_count ?? "—"}</strong></div>
                <div><span>Total Machines</span><strong>{layout.total_machines}</strong></div>
                <div><span>Started</span><strong>{formatDate(layout.started_at)}</strong></div>
                <div><span>Completed</span><strong>{formatDate(layout.completed_at)}</strong></div>
                <div><span>Duration</span><strong>{layout.duration_minutes == null ? "Running" : `${layout.duration_minutes} min`}</strong></div>
              </section>

              {canManage && layout.is_active && (
                <section className="layout-card">
                  <div className="layout-section-heading">
                    <div>
                      <p className="layout-eyebrow">Management</p>
                      <h2>Edit active layout</h2>
                    </div>
                    <button
                      type="button"
                      className="danger-button"
                      disabled={saving}
                      onClick={handleComplete}
                    >
                      Complete Layout
                    </button>
                  </div>

                  <form className="layout-form" onSubmit={handleUpdate}>
                    <label>Buyer<input value={form.buyer} onChange={e => setForm({...form, buyer:e.target.value})} required /></label>
                    <label>Style<input value={form.style} onChange={e => setForm({...form, style:e.target.value})} /></label>
                    <label>Job<input value={form.job} onChange={e => setForm({...form, job:e.target.value})} /></label>
                    <label>SMV<input type="number" step="0.01" min="0.01" value={form.smv} onChange={e => setForm({...form, smv:e.target.value})} required /></label>
                    <label>Required machines<input type="number" min="0" value={form.required_machine_count} onChange={e => setForm({...form, required_machine_count:e.target.value})} /></label>
                    <label>Total machines<input type="number" min="0" value={form.total_machines} onChange={e => setForm({...form, total_machines:e.target.value})} required /></label>
                    <label className="full">Notes<textarea value={form.notes} onChange={e => setForm({...form, notes:e.target.value})} /></label>
                    <div className="full form-actions"><button disabled={saving} type="submit" className="primary-button">{saving ? "Saving..." : "Save Changes"}</button></div>
                  </form>
                </section>
              )}

              <section className="layout-card">
                <div className="layout-section-heading">
                  <div>
                    <p className="layout-eyebrow">Machines</p>
                    <h2>Layout machines</h2>
                  </div>
                </div>

                {canManage && (
                  <form className="machine-form" onSubmit={handleAddMachine}>
                    <input
                      type="number"
                      min="1"
                      placeholder="Machine #"
                      value={machineForm.machine_number}
                      onChange={e => setMachineForm({...machineForm, machine_number:e.target.value})}
                      required
                    />
                    <input
                      placeholder="Machine name"
                      value={machineForm.machine_name}
                      onChange={e => setMachineForm({...machineForm, machine_name:e.target.value})}
                    />
                    <select value={machineForm.status} onChange={e => setMachineForm({...machineForm, status:e.target.value})}>
                      {MACHINE_STATUSES.map(s => <option key={s}>{s}</option>)}
                    </select>
                    <input
                      placeholder="Reason"
                      value={machineForm.reason}
                      onChange={e => setMachineForm({...machineForm, reason:e.target.value})}
                    />
                    <button className="primary-button" disabled={saving} type="submit">Add Machine</button>
                  </form>
                )}

                {machines.length === 0 ? (
                  <div className="layout-empty">No machine records have been added to this layout.</div>
                ) : (
                  <div className="machine-table-wrap">
                    <table className="machine-table">
                      <thead><tr><th>#</th><th>Name</th><th>Status</th><th>Reason</th><th>Started</th><th>Completed</th></tr></thead>
                      <tbody>
                        {machines.map(machine => (
                          <tr key={machine.id}>
                            <td>{machine.machine_number}</td>
                            <td>{machine.machine_name || "—"}</td>
                            <td>
                              {canManage ? (
                                <select
                                  value={machine.status}
                                  disabled={saving}
                                  onChange={e => handleMachineStatus(machine, e.target.value)}
                                >
                                  {MACHINE_STATUSES.map(s => <option key={s}>{s}</option>)}
                                </select>
                              ) : (
                                <span className={`machine-status ${statusClass(machine.status)}`}>{machine.status}</span>
                              )}
                            </td>
                            <td>{machine.reason || "—"}</td>
                            <td>{formatDate(machine.started_at)}</td>
                            <td>{formatDate(machine.completed_at)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </section>
            </>
          )}

          {!detailLoading && !layout && (
            <div className="layout-error">{error || "Layout not found."}</div>
          )}
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="layouts-page">
        <header className="layout-header">
          <div>
            <p className="layout-eyebrow">SFMS • Operations</p>
            <h1>Layout Management</h1>
            <p>Create, monitor and complete production layouts by line.</p>
          </div>
          {canManage && (
            <button
              className="primary-button"
              type="button"
              onClick={() => openCreate()}
            >
              + New Layout
            </button>
          )}
        </header>

        {message && <div className="layout-message">{message}</div>}
        {error && <div className="layout-error">{error}</div>}

        {canManage && (
          <section className="layout-card">
            <div className="layout-section-heading">
              <div>
                <p className="layout-eyebrow">New production session</p>
                <h2>Create Layout</h2>
              </div>
            </div>

            <form className="layout-form" onSubmit={handleCreate}>
              <label>Line
                <select value={form.line_id} onChange={e => setForm({...form, line_id:e.target.value})} required>
                  <option value="">Select line</option>
                  {lines.map(line => (
                    <option key={line.id} value={line.id}>
                      Line {line.line_number} — {line.name}
                    </option>
                  ))}
                </select>
              </label>
              <label>Buyer<input value={form.buyer} onChange={e => setForm({...form, buyer:e.target.value})} required /></label>
              <label>Style<input value={form.style} onChange={e => setForm({...form, style:e.target.value})} /></label>
              <label>Job<input value={form.job} onChange={e => setForm({...form, job:e.target.value})} /></label>
              <label>SMV<input type="number" step="0.01" min="0.01" value={form.smv} onChange={e => setForm({...form, smv:e.target.value})} required /></label>
              <label>Required machines<input type="number" min="0" value={form.required_machine_count} onChange={e => setForm({...form, required_machine_count:e.target.value})} /></label>
              <label>Total machines<input type="number" min="0" value={form.total_machines} onChange={e => setForm({...form, total_machines:e.target.value})} required /></label>
              <label className="full">Notes<textarea value={form.notes} onChange={e => setForm({...form, notes:e.target.value})} /></label>
              <div className="full form-actions"><button disabled={saving} type="submit" className="primary-button">{saving ? "Creating..." : "Create Layout"}</button></div>
            </form>
          </section>
        )}

        <section className="layout-grid">
          {loading ? (
            <div className="layout-card">Loading lines and layouts...</div>
          ) : lines.length === 0 ? (
            <div className="layout-card layout-empty">No lines are available for your account.</div>
          ) : (
            lines.map(line => {
              const items = layoutsByLine[line.id] ?? [];
              const active = items.find(item => item.is_active);

              return (
                <article className="layout-card line-layout-card" key={line.id}>
                  <div className="line-card-heading">
                    <div>
                      <p className="layout-eyebrow">Production Line</p>
                      <h2>Line {line.line_number}</h2>
                      <span>{line.name}</span>
                    </div>
                    {canManage && (
                      <button type="button" className="secondary-button" onClick={() => openCreate(line.id)}>
                        New Layout
                      </button>
                    )}
                  </div>

                  {active ? (
                    <div className="active-layout">
                      <div className="active-layout-top">
                        <span className={`layout-status ${statusClass(active.status)}`}>{active.status}</span>
                        <span>Started {formatDate(active.started_at)}</span>
                      </div>
                      <h3>{active.buyer}</h3>
                      <p>{active.style || "No style"} {active.job ? `· Job ${active.job}` : ""}</p>
                      <div className="layout-mini-grid">
                        <div><span>SMV</span><strong>{active.smv}</strong></div>
                        <div><span>Machines</span><strong>{active.total_machines}</strong></div>
                        <div><span>Required</span><strong>{active.required_machine_count ?? "—"}</strong></div>
                      </div>
                      <button type="button" className="primary-button full-width" onClick={() => navigate(`/layout/${active.id}`)}>
                        View Layout
                      </button>
                    </div>
                  ) : (
                    <div className="layout-empty">No active layout for this line.</div>
                  )}

                  <div className="history-heading">Layout history</div>
                  {items.length === 0 ? (
                    <p className="muted">No layout sessions yet.</p>
                  ) : (
                    <div className="history-list">
                      {items.slice(0, 5).map(item => (
                        <button
                          type="button"
                          className="history-row"
                          key={item.id}
                          onClick={() => navigate(`/layout/${item.id}`)}
                        >
                          <span>#{item.id} · {item.buyer}</span>
                          <span>{item.status}</span>
                        </button>
                      ))}
                    </div>
                  )}
                </article>
              );
            })
          )}
        </section>
      </div>
    </DashboardLayout>
  );
}

export default Layouts;
