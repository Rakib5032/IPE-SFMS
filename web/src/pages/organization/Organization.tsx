import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import type { FormEvent } from "react";

import {
  createLine,
  createOrganizationUnit,
  getOrganizationUnits,
  getUnitLines,
  updateLine,
  updateOrganizationUnit,
} from "../../services/organizationService";

import type {
  Line,
  OrganizationUnit,
} from "../../types/organization";

import DashboardLayout from "../../layouts/DashboardLayout";

import "./Organization.css";


type UnitForm = {
  name: string;
  code: string;
  unit_type: "GROUP" | "UNIT";
  parent_id: number | null;
};


type LineForm = {
  line_number: string;
  name: string;
};


function Organization() {

  const navigate = useNavigate();

  const [organizations, setOrganizations] =
    useState<OrganizationUnit[]>([]);

  const [lines, setLines] =
    useState<Record<number, Line[]>>({});

  const [expandedGroups, setExpandedGroups] =
    useState<number[]>([]);

  const [expandedUnits, setExpandedUnits] =
    useState<number[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState("");

  const [message, setMessage] =
    useState("");

  const [showUnitForm, setShowUnitForm] =
    useState(false);

  const [editingUnit, setEditingUnit] =
    useState<OrganizationUnit | null>(null);

  const [showLineForm, setShowLineForm] =
    useState(false);

  const [editingLine, setEditingLine] =
    useState<Line | null>(null);

  const [selectedUnitId, setSelectedUnitId] =
    useState<number | null>(null);

  const [unitForm, setUnitForm] =
    useState<UnitForm>({
      name: "",
      code: "",
      unit_type: "GROUP",
      parent_id: null,
    });

  const [lineForm, setLineForm] =
    useState<LineForm>({
      line_number: "",
      name: "",
    });


  // ==========================================================
  // LOAD ORGANIZATION
  // ==========================================================

  async function loadOrganizations() {

    try {

      setLoading(true);
      setError("");

      const result =
        await getOrganizationUnits();

      setOrganizations(result);

    } catch (err: any) {

      setError(
        err.response?.data?.detail ??
        "Failed to load organization structure.",
      );

    } finally {

      setLoading(false);

    }

  }


  useEffect(() => {
    loadOrganizations();
  }, []);


  // ==========================================================
  // GROUPS
  // ==========================================================

  const groups = useMemo(
    () =>
      organizations
        .filter(
          (item) =>
            item.unit_type === "GROUP",
        )
        .sort(
          (a, b) =>
            a.code.localeCompare(b.code),
        ),
    [organizations],
  );


  function getGroupUnits(
    groupId: number,
  ) {

    return organizations
      .filter(
        (item) =>
          item.unit_type === "UNIT" &&
          item.parent_id === groupId,
      )
      .sort(
        (a, b) =>
          a.code.localeCompare(b.code),
      );

  }


  // ==========================================================
  // EXPAND GROUP
  // ==========================================================

  function toggleGroup(
    groupId: number,
  ) {

    setExpandedGroups(
      (previous) =>
        previous.includes(groupId)
          ? previous.filter(
              (id) => id !== groupId,
            )
          : [...previous, groupId],
    );

  }


  // ==========================================================
  // EXPAND UNIT / LOAD LINES
  // ==========================================================

  async function toggleUnit(
    unitId: number,
  ) {

    const alreadyExpanded =
      expandedUnits.includes(unitId);

    if (alreadyExpanded) {

      setExpandedUnits(
        (previous) =>
          previous.filter(
            (id) => id !== unitId,
          ),
      );

      return;

    }


    setExpandedUnits(
      (previous) => [
        ...previous,
        unitId,
      ],
    );


    if (!lines[unitId]) {

      try {

        const result =
          await getUnitLines(unitId);

        setLines(
          (previous) => ({
            ...previous,
            [unitId]: result,
          }),
        );

      } catch (err: any) {

        setError(
          err.response?.data?.detail ??
          "Failed to load lines.",
        );

      }

    }

  }


  // ==========================================================
  // CLEAR MESSAGES
  // ==========================================================

  function clearMessages() {

    setError("");
    setMessage("");

  }


  // ==========================================================
  // ADD GROUP
  // ==========================================================

  function openAddGroup() {

    clearMessages();

    setEditingUnit(null);

    setUnitForm({
      name: "",
      code: "",
      unit_type: "GROUP",
      parent_id: null,
    });

    setShowUnitForm(true);

  }


  // ==========================================================
  // ADD UNIT
  // ==========================================================

  function openAddUnit(
    groupId: number,
  ) {

    clearMessages();

    setEditingUnit(null);

    setUnitForm({
      name: "",
      code: "",
      unit_type: "UNIT",
      parent_id: groupId,
    });

    setShowUnitForm(true);

  }


  // ==========================================================
  // EDIT ORGANIZATION
  // ==========================================================

  function openEditUnit(
    organization: OrganizationUnit,
  ) {

    clearMessages();

    setEditingUnit(
      organization,
    );

    setUnitForm({
      name: organization.name,
      code: organization.code,
      unit_type: organization.unit_type,
      parent_id: organization.parent_id,
    });

    setShowUnitForm(true);

  }


  // ==========================================================
  // SAVE ORGANIZATION
  // ==========================================================

  async function handleUnitSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {

    event.preventDefault();

    clearMessages();

    if (!unitForm.name.trim()) {

      setError(
        "Organization name is required.",
      );

      return;

    }


    if (!unitForm.code.trim()) {

      setError(
        "Organization code is required.",
      );

      return;

    }


    try {

      setSaving(true);

      if (editingUnit) {

        await updateOrganizationUnit(
          editingUnit.id,
          {
            name: unitForm.name.trim(),
            code: unitForm.code.trim(),
            unit_type:
              unitForm.unit_type,
            parent_id:
              unitForm.parent_id,
          },
        );

        setMessage(
          "Organization updated successfully.",
        );

      } else {

        await createOrganizationUnit({
          name: unitForm.name.trim(),
          code: unitForm.code.trim(),
          unit_type:
            unitForm.unit_type,
          parent_id:
            unitForm.parent_id,
          is_active: true,
        });

        setMessage(
          "Organization created successfully.",
        );

      }

      setShowUnitForm(false);

      await loadOrganizations();

    } catch (err: any) {

      setError(
        err.response?.data?.detail ??
        "Failed to save organization.",
      );

    } finally {

      setSaving(false);

    }

  }


  // ==========================================================
  // TOGGLE ORGANIZATION
  // ==========================================================

  async function toggleOrganization(
    organization: OrganizationUnit,
  ) {

    clearMessages();

    try {

      setSaving(true);

      await updateOrganizationUnit(
        organization.id,
        {
          is_active:
            !organization.is_active,
        },
      );

      setMessage(
        `${organization.name} is now ${
          organization.is_active
            ? "inactive"
            : "active"
        }.`,
      );

      await loadOrganizations();

    } catch (err: any) {

      setError(
        err.response?.data?.detail ??
        "Failed to update organization status.",
      );

    } finally {

      setSaving(false);

    }

  }


  // ==========================================================
  // ADD LINE
  // ==========================================================

  function openAddLine(
    unitId: number,
  ) {

    clearMessages();

    setSelectedUnitId(unitId);

    setEditingLine(null);

    setLineForm({
      line_number: "",
      name: "",
    });

    setShowLineForm(true);

  }


  // ==========================================================
  // EDIT LINE
  // ==========================================================

  function openEditLine(
    line: Line,
  ) {

    clearMessages();

    setSelectedUnitId(
      line.organization_unit_id,
    );

    setEditingLine(line);

    setLineForm({
      line_number:
        String(line.line_number),
      name: line.name,
    });

    setShowLineForm(true);

  }


  // ==========================================================
  // SAVE LINE
  // ==========================================================

  async function handleLineSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {

    event.preventDefault();

    clearMessages();

    const lineNumber =
      Number(lineForm.line_number);


    if (
      !Number.isInteger(lineNumber) ||
      lineNumber <= 0
    ) {

      setError(
        "Line number must be a positive integer.",
      );

      return;

    }


    if (!lineForm.name.trim()) {

      setError(
        "Line name is required.",
      );

      return;

    }


    try {

      setSaving(true);

      if (editingLine) {

        await updateLine(
          editingLine.id,
          {
            line_number: lineNumber,
            name:
              lineForm.name.trim(),
          },
        );

        setMessage(
          "Line updated successfully.",
        );

      } else {

        if (!selectedUnitId) {

          setError(
            "Please select a unit.",
          );

          return;

        }


        await createLine(
          selectedUnitId,
          {
            line_number: lineNumber,
            name:
              lineForm.name.trim(),
            organization_unit_id:
              selectedUnitId,
            is_active: true,
          },
        );

        setMessage(
          "Line created successfully.",
        );

      }


      setShowLineForm(false);


      if (selectedUnitId) {

        const result =
          await getUnitLines(
            selectedUnitId,
          );

        setLines(
          (previous) => ({
            ...previous,
            [selectedUnitId]:
              result,
          }),
        );

      }

    } catch (err: any) {

      setError(
        err.response?.data?.detail ??
        "Failed to save line.",
      );

    } finally {

      setSaving(false);

    }

  }


  // ==========================================================
  // TOGGLE LINE
  // ==========================================================

  async function toggleLine(
    line: Line,
  ) {

    clearMessages();

    try {

      setSaving(true);

      await updateLine(
        line.id,
        {
          is_active:
            !line.is_active,
        },
      );

      setMessage(
        `${line.name} is now ${
          line.is_active
            ? "inactive"
            : "active"
        }.`,
      );


      const result =
        await getUnitLines(
          line.organization_unit_id,
        );

      setLines(
        (previous) => ({
          ...previous,
          [line.organization_unit_id]:
            result,
        }),
      );

    } catch (err: any) {

      setError(
        err.response?.data?.detail ??
        "Failed to update line status.",
      );

    } finally {

      setSaving(false);

    }

  }


  // ==========================================================
  // LOADING
  // ==========================================================

  if (loading) {

    return (
      <DashboardLayout>

        <div className="organization-page">

          <div className="organization-loading">
            Loading organization structure...
          </div>

        </div>

      </DashboardLayout>
    );

  }


  // ==========================================================
  // RENDER
  // ==========================================================

  return (
    <DashboardLayout>

      <div className="organization-page">

        <button
          type="button"
          className="secondary-button organization-back-button"
          onClick={() =>
            navigate("/dashboard")
          }
        >
          ← Back to Dashboard
        </button>


        <div className="organization-header">

          <div>

            <div className="organization-eyebrow">
              SFMS • Administration
            </div>

            <h1>
              Organization Management
            </h1>

            <p>
              Manage groups, units and production
              lines from one place.
            </p>

          </div>


          <button
            type="button"
            className="organization-primary-button"
            onClick={openAddGroup}
          >
            + Add Group
          </button>

        </div>


        {message && (
          <div className="organization-message">
            ✓ {message}
          </div>
        )}


        {error && (
          <div className="organization-error">
            {error}
          </div>
        )}


        <div className="organization-summary">

          <div className="organization-summary-card">

            <span>
              Groups
            </span>

            <strong>
              {groups.length}
            </strong>

          </div>


          <div className="organization-summary-card">

            <span>
              Units
            </span>

            <strong>
              {
                organizations.filter(
                  (item) =>
                    item.unit_type === "UNIT",
                ).length
              }
            </strong>

          </div>


          <div className="organization-summary-card">

            <span>
              Lines Loaded
            </span>

            <strong>
              {
                Object.values(lines)
                  .flat()
                  .length
              }
            </strong>

          </div>


          <div className="organization-summary-card">

            <span>
              Active Units
            </span>

            <strong>
              {
                organizations.filter(
                  (item) =>
                    item.is_active,
                ).length
              }
            </strong>

          </div>

        </div>


        <div className="organization-tree">

          {groups.map((group) => {

            const groupUnits =
              getGroupUnits(group.id);

            const groupExpanded =
              expandedGroups.includes(
                group.id,
              );


            return (

              <section
                className={`organization-group ${
                  !group.is_active
                    ? "inactive"
                    : ""
                }`}
                key={group.id}
              >

                <div className="organization-group-header">

                  <button
                    type="button"
                    className="tree-expand-button"
                    onClick={() =>
                      toggleGroup(
                        group.id,
                      )
                    }
                  >
                    {groupExpanded
                      ? "⌄"
                      : "›"}
                  </button>


                  <div className="organization-group-icon">
                    G
                  </div>


                  <div className="organization-node-info">

                    <strong>
                      {group.name}
                    </strong>

                    <span>
                      Code {group.code}
                    </span>

                  </div>


                  <span className="organization-badge">
                    GROUP
                  </span>


                  {!group.is_active && (
                    <span className="inactive-badge">
                      INACTIVE
                    </span>
                  )}


                  <div className="organization-node-actions">

                    <button
                      type="button"
                      onClick={() =>
                        openEditUnit(
                          group,
                        )
                      }
                    >
                      Edit
                    </button>


                    <button
                      type="button"
                      onClick={() =>
                        openAddUnit(
                          group.id,
                        )
                      }
                    >
                      + Unit
                    </button>


                    <button
                      type="button"
                      className={
                        group.is_active
                          ? "danger-action"
                          : "success-action"
                      }
                      onClick={() =>
                        toggleOrganization(
                          group,
                        )
                      }
                    >
                      {group.is_active
                        ? "Deactivate"
                        : "Activate"}
                    </button>

                  </div>

                </div>


                {groupExpanded && (

                  <div className="organization-children">

                    {groupUnits.length === 0 && (

                      <div className="organization-empty">
                        No units in this group.
                      </div>

                    )}


                    {groupUnits.map(
                      (unit) => {

                        const unitLines =
                          lines[unit.id] ??
                          [];

                        const unitExpanded =
                          expandedUnits.includes(
                            unit.id,
                          );


                        return (

                          <div
                            className={`organization-unit ${
                              !unit.is_active
                                ? "inactive"
                                : ""
                            }`}
                            key={unit.id}
                          >

                            <div className="organization-unit-header">

                              <button
                                type="button"
                                className="tree-expand-button"
                                onClick={() =>
                                  toggleUnit(
                                    unit.id,
                                  )
                                }
                              >
                                {unitExpanded
                                  ? "⌄"
                                  : "›"}
                              </button>


                              <div className="organization-unit-icon">
                                U
                              </div>


                              <div className="organization-node-info">

                                <strong>
                                  {unit.name}
                                </strong>

                                <span>
                                  Code {unit.code}
                                </span>

                              </div>


                              <span className="organization-badge unit">
                                UNIT
                              </span>


                              {!unit.is_active && (
                                <span className="inactive-badge">
                                  INACTIVE
                                </span>
                              )}


                              <div className="organization-node-actions">

                                <button
                                  type="button"
                                  onClick={() =>
                                    openEditUnit(
                                      unit,
                                    )
                                  }
                                >
                                  Edit
                                </button>


                                <button
                                  type="button"
                                  onClick={() =>
                                    openAddLine(
                                      unit.id,
                                    )
                                  }
                                >
                                  + Line
                                </button>


                                <button
                                  type="button"
                                  className={
                                    unit.is_active
                                      ? "danger-action"
                                      : "success-action"
                                  }
                                  onClick={() =>
                                    toggleOrganization(
                                      unit,
                                    )
                                  }
                                >
                                  {unit.is_active
                                    ? "Deactivate"
                                    : "Activate"}
                                </button>

                              </div>

                            </div>


                            {unitExpanded && (

                              <div className="line-list">

                                {unitLines.length === 0 ? (

                                  <div className="organization-empty">
                                    No lines found.
                                  </div>

                                ) : (

                                  unitLines.map(
                                    (line) => (

                                      <div
                                        className={`line-row ${
                                          !line.is_active
                                            ? "inactive"
                                            : ""
                                        }`}
                                        key={line.id}
                                      >

                                        <div className="line-number">
                                          {line.line_number}
                                        </div>


                                        <div className="line-name">
                                          {line.name}
                                        </div>


                                        {!line.is_active && (
                                          <span className="inactive-badge">
                                            INACTIVE
                                          </span>
                                        )}


                                        <div className="line-actions">

                                          {/* VIEW LINE */}
                                          <button
                                            type="button"
                                            className="line-view-button"
                                            onClick={() =>
                                              navigate(
                                                `/lines/${line.id}`,
                                              )
                                            }
                                          >
                                            View
                                          </button>


                                          {/* EDIT LINE */}
                                          <button
                                            type="button"
                                            onClick={() =>
                                              openEditLine(
                                                line,
                                              )
                                            }
                                          >
                                            Edit
                                          </button>


                                          {/* ACTIVATE / DEACTIVATE */}
                                          <button
                                            type="button"
                                            className={
                                              line.is_active
                                                ? "danger-action"
                                                : "success-action"
                                            }
                                            onClick={() =>
                                              toggleLine(
                                                line,
                                              )
                                            }
                                          >
                                            {line.is_active
                                              ? "Deactivate"
                                              : "Activate"}
                                          </button>

                                        </div>

                                      </div>

                                    ),
                                  )

                                )}

                              </div>

                            )}

                          </div>

                        );

                      },
                    )}

                  </div>

                )}

              </section>

            );

          })}

        </div>


        {/* ======================================================
            ORGANIZATION MODAL
            ====================================================== */}

        {showUnitForm && (

          <div
            className="organization-modal-overlay"
            onClick={() =>
              setShowUnitForm(false)
            }
          >

            <div
              className="organization-modal"
              onClick={(event) =>
                event.stopPropagation()
              }
            >

              <div className="organization-modal-header">

                <div>

                  <span>
                    {editingUnit
                      ? "Edit organization"
                      : "New organization"}
                  </span>

                  <h2>
                    {editingUnit
                      ? "Update"
                      : "Create"}
                  </h2>

                </div>


                <button
                  type="button"
                  onClick={() =>
                    setShowUnitForm(false)
                  }
                >
                  ×
                </button>

              </div>


              <form
                onSubmit={
                  handleUnitSubmit
                }
                className="organization-form"
              >

                <label>
                  Name

                  <input
                    value={
                      unitForm.name
                    }
                    onChange={(event) =>
                      setUnitForm(
                        (previous) => ({
                          ...previous,
                          name:
                            event.target.value,
                        }),
                      )
                    }
                    placeholder="Group1 / Unit1"
                  />

                </label>


                <label>
                  Code

                  <input
                    value={
                      unitForm.code
                    }
                    onChange={(event) =>
                      setUnitForm(
                        (previous) => ({
                          ...previous,
                          code:
                            event.target.value,
                        }),
                      )
                    }
                    placeholder="100 / 101"
                  />

                </label>


                <label>
                  Type

                  <select
                    value={
                      unitForm.unit_type
                    }
                    onChange={(event) =>
                      setUnitForm(
                        (previous) => ({
                          ...previous,
                          unit_type:
                            event.target.value as
                              | "GROUP"
                              | "UNIT",
                          parent_id:
                            event.target.value ===
                            "GROUP"
                              ? null
                              : previous.parent_id,
                        }),
                      )
                    }
                    disabled={
                      editingUnit !== null
                    }
                  >

                    <option value="GROUP">
                      Group
                    </option>

                    <option value="UNIT">
                      Unit
                    </option>

                  </select>

                </label>


                {unitForm.unit_type ===
                  "UNIT" && (

                  <label>
                    Parent Group

                    <select
                      value={
                        unitForm.parent_id ??
                        ""
                      }
                      onChange={(event) =>
                        setUnitForm(
                          (previous) => ({
                            ...previous,
                            parent_id:
                              event.target.value
                                ? Number(
                                    event.target.value,
                                  )
                                : null,
                          }),
                        )
                      }
                    >

                      <option value="">
                        Select group
                      </option>


                      {groups.map(
                        (group) => (

                          <option
                            key={group.id}
                            value={group.id}
                          >
                            {group.name} —{" "}
                            {group.code}
                          </option>

                        ),
                      )}

                    </select>

                  </label>

                )}


                <div className="organization-form-actions">

                  <button
                    type="button"
                    className="secondary-button"
                    onClick={() =>
                      setShowUnitForm(
                        false,
                      )
                    }
                  >
                    Cancel
                  </button>


                  <button
                    type="submit"
                    className="organization-primary-button"
                    disabled={saving}
                  >
                    {saving
                      ? "Saving..."
                      : editingUnit
                        ? "Save Changes"
                        : "Create"}
                  </button>

                </div>

              </form>

            </div>

          </div>

        )}


        {/* ======================================================
            LINE MODAL
            ====================================================== */}

        {showLineForm && (

          <div
            className="organization-modal-overlay"
            onClick={() =>
              setShowLineForm(false)
            }
          >

            <div
              className="organization-modal"
              onClick={(event) =>
                event.stopPropagation()
              }
            >

              <div className="organization-modal-header">

                <div>

                  <span>
                    {editingLine
                      ? "Edit production line"
                      : "New production line"}
                  </span>

                  <h2>
                    {editingLine
                      ? "Update Line"
                      : "Add Line"}
                  </h2>

                </div>


                <button
                  type="button"
                  onClick={() =>
                    setShowLineForm(false)
                  }
                >
                  ×
                </button>

              </div>


              <form
                onSubmit={
                  handleLineSubmit
                }
                className="organization-form"
              >

                <label>
                  Line Number

                  <input
                    type="number"
                    min="1"
                    value={
                      lineForm.line_number
                    }
                    onChange={(event) =>
                      setLineForm(
                        (previous) => ({
                          ...previous,
                          line_number:
                            event.target.value,
                        }),
                      )
                    }
                    placeholder="e.g. 126"
                  />

                </label>


                <label>
                  Line Name

                  <input
                    value={
                      lineForm.name
                    }
                    onChange={(event) =>
                      setLineForm(
                        (previous) => ({
                          ...previous,
                          name:
                            event.target.value,
                        }),
                      )
                    }
                    placeholder="Line 126"
                  />

                </label>


                <div className="organization-form-actions">

                  <button
                    type="button"
                    className="secondary-button"
                    onClick={() =>
                      setShowLineForm(
                        false,
                      )
                    }
                  >
                    Cancel
                  </button>


                  <button
                    type="submit"
                    className="organization-primary-button"
                    disabled={saving}
                  >
                    {saving
                      ? "Saving..."
                      : editingLine
                        ? "Save Changes"
                        : "Create Line"}
                  </button>

                </div>

              </form>

            </div>

          </div>

        )}

      </div>

    </DashboardLayout>
  );
}


export default Organization;