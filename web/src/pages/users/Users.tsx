import {
  useEffect,
  useMemo,
  useState,
} from "react";

import type { FormEvent } from "react";

import "./User.css";

import {
  getUserByEmployeeId,
  updateUser,
  createUser,
} from "../../services/userService";

import {
  getOrganizationUnits,
} from "../../services/organizationService";

import type {
  User,
  UserCreate,
  UserUpdate,
} from "../../types/user";

import type {
  OrganizationUnit,
} from "../../types/organization";


import DashboardLayout from "../../layouts/DashboardLayout";

import Toast from "../../components/common/Toast";
import type { ToastType } from "../../components/common/Toast";
// ============================================================
// ROLE CONFIGURATION
// ============================================================

const roles = [
  {
    id: 1,
    name: "Administrator",
    shortName: "Admin",
    description: "Full system access",
  },
  {
    id: 2,
    name: "Deputy General Manager",
    shortName: "DGM",
    description: "Management-level access",
  },
  {
    id: 3,
    name: "Central Manager",
    shortName: "Central Manager",
    description: "Central management access",
  },
  {
    id: 4,
    name: "Group Manager",
    shortName: "Group Manager",
    description: "Manages an assigned group",
  },
  {
    id: 5,
    name: "Floor IE",
    shortName: "Floor IE",
    description: "Manages an assigned unit",
  },
  {
    id: 6,
    name: "Supervisor",
    shortName: "Supervisor",
    description: "Manages an assigned line",
  },
  {
    id: 8,
    name: "Deputy Production Manager",
    shortName: "DPM",
    description: "Manages an assigned unit",
  },
  {
    id: 9,
    name: "Assistant Production Manager",
    shortName: "APM",
    description: "Manages an assigned unit",
  },
  {
    id: 10,
    name: "In-Charge",
    shortName: "In-Charge",
    description: "Manages an assigned unit",
  },
];


// ============================================================
// ACCESS RULES
// ============================================================

const SYSTEM_ROLES = [1, 2, 3];

const GROUP_ROLES = [4];

const UNIT_ROLES = [
  5,  // Floor IE
  8,  // DPM
  9,  // APM
  10, // In-Charge
];

const LINE_ROLES = [6];


// ============================================================
// HELPERS
// ============================================================

function getRole(
  roleId: number | null | undefined,
) {
  return roles.find(
    (role) => role.id === roleId,
  );
}


function getRoleName(
  roleId: number | null | undefined,
) {
  return (
    getRole(roleId)?.name ??
    "Unknown Role"
  );
}


function getOrganization(
  organizationUnits: OrganizationUnit[],
  organizationId:
    | number
    | null
    | undefined,
) {
  if (
    organizationId === null ||
    organizationId === undefined
  ) {
    return null;
  }

  return organizationUnits.find(
    (organization) =>
      organization.id === organizationId,
  );
}


// ============================================================
// COMPONENT
// ============================================================

function Users() {


  const [toast, setToast] = useState<{
    message: string;
    type: ToastType;
  } | null>(null);

  // ==========================================================
  // PAGE MODE
  // ==========================================================

  const [mode, setMode] = useState<
    "home" | "create" | "update"
  >("home");


  // ==========================================================
  // COMMON STATE
  // ==========================================================

  const [loading, setLoading] =
    useState(false);


  // ==========================================================
  // ORGANIZATION
  // ==========================================================

  const [
    organizationUnits,
    setOrganizationUnits,
  ] = useState<OrganizationUnit[]>([]);

  const [
    organizationLoading,
    setOrganizationLoading,
  ] = useState(false);

  const [
    selectedGroupId,
    setSelectedGroupId,
  ] = useState<number | null>(null);

  const [
    selectedUnitId,
    setSelectedUnitId,
  ] = useState<number | null>(null);


  // ==========================================================
  // UPDATE
  // ==========================================================

  const [employeeId, setEmployeeId] =
    useState("");

  const [user, setUser] =
    useState<User | null>(null);

  const [editing, setEditing] =
    useState(false);

  const [form, setForm] =
    useState<UserUpdate>({});


  // ==========================================================
  // CREATE
  // ==========================================================

  const [createForm, setCreateForm] =
    useState<UserCreate>({
      employee_id: 0,
      full_name: "",
      designation: "",
      email: null,
      password: "",
      role_id: 0,
      organization_unit_id: null,
    });


  // ==========================================================
  // LOAD ORGANIZATION
  // ==========================================================

  useEffect(() => {

    async function loadOrganizations() {

      try {

        setOrganizationLoading(true);

        const result =
          await getOrganizationUnits();

        setOrganizationUnits(
          result.filter(
            (item) => item.is_active,
          ),
        );

      } catch (err) {

        console.error(err);

        showToast(
          "Unable to load organization structure.",
          "error",
        );

      } finally {

        setOrganizationLoading(false);

      }
    }

    loadOrganizations();

  }, []);


  // ==========================================================
  // GROUPS
  // ==========================================================

  const groups = useMemo(
    () =>
      organizationUnits.filter(
        (item) =>
          item.unit_type === "GROUP",
      ),
    [organizationUnits],
  );


  // ==========================================================
  // UNITS
  // ==========================================================

  const units = useMemo(
    () =>
      organizationUnits.filter(
        (item) =>
          item.unit_type === "UNIT",
      ),
    [organizationUnits],
  );


  // ==========================================================
  // SELECTED GROUP UNITS
  // ==========================================================

  const selectedGroupUnits =
    useMemo(
      () =>
        units.filter(
          (unit) =>
            unit.parent_id ===
            selectedGroupId,
        ),
      [
        units,
        selectedGroupId,
      ],
    );


  // ==========================================================
  // CLEAR
  // ==========================================================

  function clearMessages() {
    setToast(null);
  }

  function showToast(
    message: string,
    type: ToastType,
  ) {
    setToast({
      message,
      type,
    });
  }


  // ==========================================================
  // RESET ORGANIZATION
  // ==========================================================

  function resetOrganization() {

    setSelectedGroupId(null);

    setSelectedUnitId(null);

  }


  // ==========================================================
  // BACK TO DASHBOARD
  // ==========================================================

  function backToDashboard() {

    /*
     * Change this to your actual dashboard route
     * if it is different.
     */

    window.location.href = "/dashboard";

  }


  // ==========================================================
  // BACK TO USER MANAGEMENT
  // ==========================================================

  function goHome() {

    setMode("home");

    setUser(null);

    setEditing(false);

    setEmployeeId("");

    resetOrganization();

    clearMessages();

  }


  // ==========================================================
  // CREATE PAGE
  // ==========================================================

  function openCreateUser() {

    clearMessages();

    resetOrganization();

    setCreateForm({
      employee_id: 0,
      full_name: "",
      designation: "",
      email: "",
      password: "",
      role_id: 0,
      organization_unit_id: null,
    });

    setMode("create");

  }


  // ==========================================================
  // UPDATE PAGE
  // ==========================================================

  function openUpdateUser() {

    clearMessages();

    resetOrganization();

    setEmployeeId("");

    setUser(null);

    setEditing(false);

    setMode("update");

  }


  // ==========================================================
  // SET ORGANIZATION FROM USER
  // ==========================================================

  function setOrganizationFromUser(
    organizationId:
      | number
      | null
      | undefined,
  ) {

    resetOrganization();

    if (
      organizationId === null ||
      organizationId === undefined
    ) {
      return;
    }

    const organization =
      getOrganization(
        organizationUnits,
        organizationId,
      );

    if (!organization) {
      return;
    }

    if (
      organization.unit_type ===
      "GROUP"
    ) {

      setSelectedGroupId(
        organization.id,
      );

      return;
    }

    if (
      organization.unit_type ===
      "UNIT"
    ) {

      setSelectedUnitId(
        organization.id,
      );

      if (
        organization.parent_id !== null
      ) {

        setSelectedGroupId(
          organization.parent_id,
        );

      }

    }

  }


  // ==========================================================
  // SEARCH
  // ==========================================================

  async function handleSearch(
    event: FormEvent<HTMLFormElement>,
  ) {

    event.preventDefault();

    clearMessages();

    setUser(null);

    setEditing(false);

    resetOrganization();

    const id = Number(
      employeeId.trim(),
    );

    if (
      !Number.isInteger(id) ||
      id <= 0
    ) {

      showToast(
        "Please enter a valid Employee ID.",
        "warning",
      );

      return;
    }

    try {

      setLoading(true);

      const result =
        await getUserByEmployeeId(id);

      setUser(result);

      setForm({
        full_name:
          result.full_name,
        designation:
          result.designation,
        email:
          result.email,
        role_id:
          result.role_id,
        organization_unit_id:
          result.organization_unit_id,
      });

      setOrganizationFromUser(
        result.organization_unit_id,
      );

    } catch (err: any) {

      console.error(err);

      showToast(
        err.response?.data?.detail ??
        "Employee could not be found.",
        "error",
      );

    } finally {

      setLoading(false);

    }

  }


  // ==========================================================
  // START EDIT
  // ==========================================================

  function startEditing() {

    if (!user) {
      return;
    }

    clearMessages();

    setForm({
      full_name:
        user.full_name,
      designation:
        user.designation,
      email:
        user.email,
      role_id:
        user.role_id,
      organization_unit_id:
        user.organization_unit_id,
    });

    setOrganizationFromUser(
      user.organization_unit_id,
    );

    setEditing(true);

  }


  // ==========================================================
  // CANCEL EDIT
  // ==========================================================

  function cancelEditing() {

    setEditing(false);

    if (user) {

      setOrganizationFromUser(
        user.organization_unit_id,
      );

    }

    clearMessages();

  }


  // ==========================================================
  // UPDATE
  // ==========================================================

  async function handleUpdate(
    event: FormEvent<HTMLFormElement>,
  ) {

    event.preventDefault();

    if (!user) {
      return;
    }

    clearMessages();

    try {

      setLoading(true);

      const updatedUser =
        await updateUser(
          user.employee_id,
          form,
        );

      setUser(updatedUser);

      setEditing(false);

      setOrganizationFromUser(
        updatedUser.organization_unit_id,
      );

      showToast(
        "User updated successfully.",
        "success",
      );

    } catch (err: any) {

      console.error(err);

      showToast(
        err.response?.data?.detail ??
        "Failed to update user.",
        "error",
      );

    } finally {

      setLoading(false);

    }

  }


  // ==========================================================
  // ACTIVATE / DEACTIVATE
  // ==========================================================

  async function handleStatusChange() {

    if (!user) {
      return;
    }

    const action =
      user.is_active
        ? "deactivate"
        : "reactivate";

    if (
      !window.confirm(
        `Are you sure you want to ${action} this user?`,
      )
    ) {
      return;
    }

    clearMessages();

    try {

      setLoading(true);

      const updatedUser =
        await updateUser(
          user.employee_id,
          {
            is_active:
              !user.is_active,
          },
        );

      setUser(updatedUser);

      showToast(
        user.is_active
          ? "User deactivated successfully."
          : "User reactivated successfully.",
        "success",
      );

    } catch (err: any) {

      console.error(err);

      showToast(
        err.response?.data?.detail ??
        "Failed to update user status.",
        "error",
      );

    } finally {

      setLoading(false);

    }

  }


  // ==========================================================
  // CREATE
  // ==========================================================

  async function handleCreateUser(
    event: FormEvent<HTMLFormElement>,
  ) {

    event.preventDefault();

    clearMessages();

    if (
      !Number.isInteger(
        createForm.employee_id,
      ) ||
      createForm.employee_id <= 0
    ) {

      showToast(
        "Employee ID must be a positive number.",
        "warning",
      );

      return;
    }

    if (
      !createForm.full_name.trim()
    ) {

      showToast(
        "Full name is required.",
        "warning",
      );

      return;
    }

    if (
      !createForm.password.trim()
    ) {

      showToast(
        "Password is required.",
        "warning",
      );

      return;
    }

    if (!createForm.role_id) {

      showToast(
        "Please select a role.",
        "warning",
      );

      return;
    }

    const requiresOrganization =
      GROUP_ROLES.includes(
        createForm.role_id,
      ) ||
      UNIT_ROLES.includes(
        createForm.role_id,
      ) ||
      LINE_ROLES.includes(
        createForm.role_id,
      );

    if (
      requiresOrganization &&
      !createForm.organization_unit_id
    ) {

      showToast(
        "Please complete the organization assignment.",
        "warning",
      );

      return;
    }

    try {

      setLoading(true);

      await createUser({
        ...createForm,
        email: createForm.email?.trim() || null,
      });

      showToast(
        "User created successfully.",
        "success",
      );

      resetOrganization();

      setCreateForm({
        employee_id: 0,
        full_name: "",
        designation: "",
        email: "",
        password: "",
        role_id: 0,
        organization_unit_id: null,
      });

    } catch (err: any) {

      console.error(err);

      const detail =
        err.response?.data?.detail ??
        "Failed to create user.";

      showToast(
        detail,
        typeof detail === "string" &&
          detail.toLowerCase().includes("already exists")
          ? "warning"
          : "error",
      );

    } finally {

      setLoading(false);

    }

  }


  // ==========================================================
  // CREATE ROLE
  // ==========================================================

  function handleCreateRoleChange(
    roleId: number,
  ) {

    resetOrganization();

    setCreateForm(
      (previous) => ({
        ...previous,
        role_id: roleId,
        organization_unit_id:
          null,
      }),
    );

  }


  // ==========================================================
  // UPDATE ROLE
  // ==========================================================

  function handleUpdateRoleChange(
    roleId: number,
  ) {

    resetOrganization();

    setForm(
      (previous) => ({
        ...previous,
        role_id: roleId,
        organization_unit_id:
          null,
      }),
    );

  }


  // ==========================================================
  // CREATE GROUP
  // ==========================================================

  function handleCreateGroup(
    groupId: number | null,
  ) {

    setSelectedGroupId(groupId);

    setSelectedUnitId(null);

    setCreateForm(
      (previous) => ({
        ...previous,
        organization_unit_id:
          groupId,
      }),
    );

  }


  // ==========================================================
  // CREATE UNIT
  // ==========================================================

  function handleCreateUnit(
    unitId: number | null,
  ) {

    setSelectedUnitId(unitId);

    setCreateForm(
      (previous) => ({
        ...previous,
        organization_unit_id:
          unitId,
      }),
    );

  }


  // ==========================================================
  // UPDATE GROUP
  // ==========================================================

  function handleUpdateGroup(
    groupId: number | null,
  ) {

    setSelectedGroupId(groupId);

    setSelectedUnitId(null);

    setForm(
      (previous) => ({
        ...previous,
        organization_unit_id:
          groupId,
      }),
    );

  }


  // ==========================================================
  // UPDATE UNIT
  // ==========================================================

  function handleUpdateUnit(
    unitId: number | null,
  ) {

    setSelectedUnitId(unitId);

    setForm(
      (previous) => ({
        ...previous,
        organization_unit_id:
          unitId,
      }),
    );

  }


  // ==========================================================
  // ORGANIZATION SELECTOR
  // ==========================================================

  function OrganizationSelector({
    roleId,
    update,
  }: {
    roleId: number;
    update: boolean;
  }) {

    const groupHandler =
      update
        ? handleUpdateGroup
        : handleCreateGroup;

    const unitHandler =
      update
        ? handleUpdateUnit
        : handleCreateUnit;


    // --------------------------------------------------------
    // SYSTEM
    // --------------------------------------------------------

    if (
      SYSTEM_ROLES.includes(roleId)
    ) {

      return (
        <div className="organization-system-card">

          <div className="organization-system-check">
            ✓
          </div>

          <div className="organization-system-content">

            <span className="organization-system-label">
              SYSTEM WIDE
            </span>

            <strong>
              No organization assignment required
            </strong>

            <p>
              This role has access across
              the applicable SFMS scope.
            </p>

          </div>

        </div>
      );
    }


    // --------------------------------------------------------
    // GROUP
    // --------------------------------------------------------

    if (
      GROUP_ROLES.includes(roleId)
    ) {

      return (
        <div className="organization-flow">

          <div className="organization-step">

            <div className="organization-step-number">
              01
            </div>

            <div className="organization-step-content">

              <label>
                GROUP
              </label>

              <select
                value={
                  selectedGroupId ?? ""
                }
                onChange={(event) => {

                  const value =
                    event.target.value;

                  groupHandler(
                    value
                      ? Number(value)
                      : null,
                  );

                }}
                required
              >

                <option value="">
                  Select Group
                </option>

                {groups.map(
                  (group) => (

                    <option
                      key={group.id}
                      value={group.id}
                    >
                      {group.name} — {group.code}
                    </option>

                  ),
                )}

              </select>

            </div>

          </div>

        </div>
      );
    }


    // --------------------------------------------------------
    // UNIT
    // --------------------------------------------------------

    if (
      UNIT_ROLES.includes(roleId)
    ) {

      return (
        <div className="organization-flow">

          <div className="organization-step">

            <div className="organization-step-number">
              01
            </div>

            <div className="organization-step-content">

              <label>
                GROUP
              </label>

              <select
                value={
                  selectedGroupId ?? ""
                }
                onChange={(event) => {

                  const value =
                    event.target.value;

                  groupHandler(
                    value
                      ? Number(value)
                      : null,
                  );

                }}
                required
              >

                <option value="">
                  Select Group
                </option>

                {groups.map(
                  (group) => (

                    <option
                      key={group.id}
                      value={group.id}
                    >
                      {group.name} — {group.code}
                    </option>

                  ),
                )}

              </select>

            </div>

          </div>


          <div className="organization-connector">
            ↓
          </div>


          <div className="organization-step">

            <div className="organization-step-number">
              02
            </div>

            <div className="organization-step-content">

              <label>
                UNIT
              </label>

              <select
                value={
                  selectedUnitId ?? ""
                }
                disabled={
                  selectedGroupId === null
                }
                onChange={(event) => {

                  const value =
                    event.target.value;

                  unitHandler(
                    value
                      ? Number(value)
                      : null,
                  );

                }}
                required
              >

                <option value="">
                  {
                    selectedGroupId === null
                      ? "Select Group First"
                      : "Select Unit"
                  }
                </option>

                {selectedGroupUnits.map(
                  (unit) => (

                    <option
                      key={unit.id}
                      value={unit.id}
                    >
                      {unit.name} — {unit.code}
                    </option>

                  ),
                )}

              </select>

            </div>

          </div>

        </div>
      );
    }


    // --------------------------------------------------------
    // LINE
    // --------------------------------------------------------

    if (
      LINE_ROLES.includes(roleId)
    ) {

      return (
        <div className="organization-flow">

          <div className="organization-step">

            <div className="organization-step-number">
              01
            </div>

            <div className="organization-step-content">

              <label>
                GROUP
              </label>

              <select
                value={
                  selectedGroupId ?? ""
                }
                onChange={(event) => {

                  const value =
                    event.target.value;

                  groupHandler(
                    value
                      ? Number(value)
                      : null,
                  );

                }}
                required
              >

                <option value="">
                  Select Group
                </option>

                {groups.map(
                  (group) => (

                    <option
                      key={group.id}
                      value={group.id}
                    >
                      {group.name} — {group.code}
                    </option>

                  ),
                )}

              </select>

            </div>

          </div>


          <div className="organization-connector">
            ↓
          </div>


          <div className="organization-step">

            <div className="organization-step-number">
              02
            </div>

            <div className="organization-step-content">

              <label>
                UNIT
              </label>

              <select
                value={
                  selectedUnitId ?? ""
                }
                disabled={
                  selectedGroupId === null
                }
                onChange={(event) => {

                  const value =
                    event.target.value;

                  unitHandler(
                    value
                      ? Number(value)
                      : null,
                  );

                }}
                required
              >

                <option value="">
                  {
                    selectedGroupId === null
                      ? "Select Group First"
                      : "Select Unit"
                  }
                </option>

                {selectedGroupUnits.map(
                  (unit) => (

                    <option
                      key={unit.id}
                      value={unit.id}
                    >
                      {unit.name} — {unit.code}
                    </option>

                  ),
                )}

              </select>

            </div>

          </div>


          <div className="organization-connector">
            ↓
          </div>


          <div className="organization-step organization-line-disabled">

            <div className="organization-step-number">
              03
            </div>

            <div className="organization-step-content">

              <label>
                LINE
              </label>

              <select disabled>

                <option>
                  Line data not available yet
                </option>

              </select>

            </div>

          </div>

        </div>
      );
    }

    return null;
  }


  // ==========================================================
  // HOME
  // ==========================================================

  if (mode === "home") {

    return (
      <DashboardLayout>
        {toast && (
          <Toast
            message={toast.message}
            type={toast.type}
            onClose={() => setToast(null)}
          />
        )}

        <div className="users-page">

          <div className="users-hero">

            <div className="users-hero-content">

              <span className="users-eyebrow">
                SFMS • ADMINISTRATION
              </span>

              <h1>
                User Management
              </h1>

              <p>
                Manage employee accounts,
                roles and organizational
                assignments.
              </p>

            </div>

            <div className="users-hero-decoration">

              <div className="hero-orbit orbit-one" />
              <div className="hero-orbit orbit-two" />

              <div className="hero-center">
                U
              </div>

            </div>

          </div>


          <div className="management-intro">

            <div>
              <button
                type="button"
                className="dashboard-back-button"
                onClick={backToDashboard}
              >
                <span>←</span>
                Back to Dashboard
              </button>
            </div>

            {/* <span>
            ACCOUNT OPERATIONS
          </span> */}

            <h2>
              Manage Employees
            </h2>

          </div>


          <div className="management-cards">

            <button
              type="button"
              className="management-card management-card-update"
              onClick={
                openUpdateUser
              }
            >

              <div className="management-icon">
                ✎
              </div>

              <span className="management-card-label">
                EXISTING ACCOUNT
              </span>

              <h3>
                Update User
              </h3>

              {/* <p>
              Find an employee and update
              their profile, role or
              organizational assignment.
            </p> */}

              <div className="management-card-footer">
                Update employee
                <span>→</span>
              </div>

            </button>


            <button
              type="button"
              className="management-card management-card-create"
              onClick={
                openCreateUser
              }
            >

              <div className="management-icon">
                +
              </div>

              <span className="management-card-label">
                NEW ACCOUNT
              </span>

              <h3>
                Create User
              </h3>

              {/* <p>
              Create a new employee account
              and assign their role and
              organization.
            </p> */}

              <div className="management-card-footer">
                Add employee
                <span>→</span>
              </div>

            </button>

          </div>

        </div>
      </DashboardLayout>
    );
  }


  // ==========================================================
  // CREATE PAGE
  // ==========================================================

  if (mode === "create") {

    return (
      <DashboardLayout>
        {toast && (
          <Toast
            message={toast.message}
            type={toast.type}
            onClose={() => setToast(null)}
          />
        )}

        <div className="users-page">

          <div className="page-navigation">

            <button
              type="button"
              className="dashboard-back-button"
              onClick={backToDashboard}
            >
              <span>←</span>
              Back to Dashboard
            </button>

            <button
              type="button"
              className="management-back-button"
              onClick={goHome}
            >
              User Management
            </button>

          </div>


          <div className="compact-page-header">

            <div>

              <span className="users-eyebrow">
                SFMS • NEW ACCOUNT
              </span>

              <h1>
                Create User
              </h1>

              <p>
                Create an employee account
                and assign the appropriate
                access scope.
              </p>

            </div>

            <div className="form-hero-badge">
              +
            </div>

          </div>


          <form
            className="compact-user-form"
            onSubmit={
              handleCreateUser
            }
          >

            {/* BASIC */}

            <section className="compact-form-section">

              <div className="compact-section-header">

                <div className="compact-section-number">
                  01
                </div>

                <div>
                  <span>
                    EMPLOYEE PROFILE
                  </span>

                  <h2>
                    Basic Information
                  </h2>
                </div>

              </div>


              <div className="modern-form-grid">

                <div className="modern-field">

                  <label>
                    Employee ID
                    <span>*</span>
                  </label>

                  <input
                    type="number"
                    min="1"
                    placeholder="Employee ID"
                    value={
                      createForm.employee_id ||
                      ""
                    }
                    onChange={(event) =>
                      setCreateForm(
                        (previous) => ({
                          ...previous,
                          employee_id:
                            Number(
                              event.target.value,
                            ),
                        }),
                      )
                    }
                    required
                  />

                </div>


                <div className="modern-field">

                  <label>
                    Full Name
                    <span>*</span>
                  </label>

                  <input
                    type="text"
                    placeholder="Full name"
                    value={
                      createForm.full_name
                    }
                    onChange={(event) =>
                      setCreateForm(
                        (previous) => ({
                          ...previous,
                          full_name:
                            event.target.value,
                        }),
                      )
                    }
                    required
                  />

                </div>


                <div className="modern-field">

                  <label>
                    Designation
                  </label>

                  <input
                    type="text"
                    placeholder="Designation"
                    value={
                      createForm.designation ??
                      ""
                    }
                    onChange={(event) =>
                      setCreateForm(
                        (previous) => ({
                          ...previous,
                          designation:
                            event.target.value,
                        }),
                      )
                    }
                  />

                </div>


                <div className="modern-field">

                  <label>
                    Email
                  </label>

                  <input
                    type="email"
                    placeholder="Email address"
                    value={
                      createForm.email ??
                      ""
                    }
                    onChange={(event) =>
                      setCreateForm(
                        (previous) => ({
                          ...previous,
                          email:
                            event.target.value,
                        }),
                      )
                    }
                  />

                </div>


                <div className="modern-field">

                  <label>
                    Password
                    <span>*</span>
                  </label>

                  <input
                    type="password"
                    placeholder="Create password"
                    value={
                      createForm.password
                    }
                    onChange={(event) =>
                      setCreateForm(
                        (previous) => ({
                          ...previous,
                          password:
                            event.target.value,
                        }),
                      )
                    }
                    required
                  />

                </div>

              </div>

            </section>


            {/* ROLE */}

            <section className="compact-form-section">

              <div className="compact-section-header">

                <div className="compact-section-number">
                  02
                </div>

                <div>
                  <span>
                    ACCESS CONTROL
                  </span>

                  <h2>
                    Role & Rule
                  </h2>
                </div>

              </div>


              <div className="role-select-wrapper">

                <label>
                  Select Role
                  <span>*</span>
                </label>

                <select
                  className="large-role-select"
                  value={
                    createForm.role_id || ""
                  }
                  onChange={(event) =>
                    handleCreateRoleChange(
                      Number(
                        event.target.value,
                      ),
                    )
                  }
                  required
                >

                  <option value="">
                    Choose employee role
                  </option>

                  {roles.map(
                    (role) => (
                      <option
                        key={role.id}
                        value={role.id}
                      >
                        {role.name} —{" "}
                        {role.description}
                      </option>
                    ),
                  )}

                </select>


                {createForm.role_id > 0 && (

                  <div className="selected-role-info">

                    <span className="selected-role-check">
                      ✓
                    </span>

                    <div>

                      <strong>
                        {
                          getRole(
                            createForm.role_id,
                          )?.name
                        }
                      </strong>

                      <p>
                        {
                          getRole(
                            createForm.role_id,
                          )?.description
                        }
                      </p>

                    </div>

                  </div>

                )}

              </div>

            </section>


            {/* ORGANIZATION */}

            <section className="compact-form-section">

              <div className="compact-section-header">

                <div className="compact-section-number">
                  03
                </div>

                <div>
                  <span>
                    ORGANIZATION
                  </span>

                  <h2>
                    Assignment
                  </h2>
                </div>

              </div>


              <div className="organization-panel">

                {createForm.role_id === 0 ? (

                  <div className="organization-empty">

                    <strong>
                      Select a role first
                    </strong>

                    <p>
                      The required organization
                      fields will appear here.
                    </p>

                  </div>

                ) : organizationLoading ? (

                  <div className="organization-loading-modern">

                    <div className="loading-spinner" />

                    Loading organization...

                  </div>

                ) : (

                  <OrganizationSelector
                    roleId={
                      createForm.role_id
                    }
                    update={false}
                  />

                )}

              </div>

            </section>


            {/* ACTIONS */}

            <div className="modern-form-actions">

              <button
                type="button"
                className="modern-secondary-button"
                onClick={goHome}
              >
                Cancel
              </button>

              <button
                type="submit"
                className="modern-primary-button"
                disabled={loading}
              >

                {loading ? (
                  <>
                    <span className="button-spinner" />
                    Creating...
                  </>
                ) : (
                  <>
                    ✓ Create User
                  </>
                )}

              </button>

            </div>

          </form>

        </div>
      </DashboardLayout>
    );
  }


  // ==========================================================
  // UPDATE PAGE
  // ==========================================================

  return (
    <DashboardLayout>
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      <div className="users-page">

        <div className="page-navigation">

          <button
            type="button"
            className="dashboard-back-button"
            onClick={backToDashboard}
          >
            <span>←</span>
            Back to Dashboard
          </button>

          <button
            type="button"
            className="management-back-button"
            onClick={goHome}
          >
            User Management
          </button>

        </div>


        <div className="compact-page-header">

          <div>

            <span className="users-eyebrow">
              SFMS • ACCOUNT MANAGEMENT
            </span>

            <h1>
              Update User
            </h1>

            <p>
              Search an employee to update
              their account.
            </p>

          </div>

          <div className="form-hero-badge update-badge">
            ✎
          </div>

        </div>


        {/* SEARCH */}

        <section className="search-user-panel">

          <div className="search-user-heading">

            <div className="search-user-icon">
              ⌕
            </div>

            <div>

              <span>
                FIND EMPLOYEE
              </span>

              <h2>
                Search User
              </h2>

            </div>

          </div>


          <form
            className="modern-search-form"
            onSubmit={
              handleSearch
            }
          >

            <div className="modern-search-input">

              <span>
                #
              </span>

              <input
                type="text"
                inputMode="numeric"
                placeholder="Employee ID"
                value={employeeId}
                onChange={(event) =>
                  setEmployeeId(
                    event.target.value,
                  )
                }
              />

            </div>

            <button
              type="submit"
              className="modern-search-button"
              disabled={loading}
            >

              {loading ? (
                <>
                  <span className="button-spinner" />
                  Searching...
                </>
              ) : (
                <>
                  Search
                  <span>→</span>
                </>
              )}

            </button>

          </form>

        </section>


        {/* USER PROFILE */}

        {user && !editing && (

          <section className="modern-user-profile">

            <div className="profile-top">

              <div className="profile-identity">

                <div className="profile-avatar">
                  {user.full_name
                    .charAt(0)
                    .toUpperCase()}
                </div>

                <div>

                  <span className="profile-status">

                    <span
                      className={
                        user.is_active
                          ? "status-dot status-dot-active"
                          : "status-dot"
                      }
                    />

                    {user.is_active
                      ? "ACTIVE"
                      : "INACTIVE"}

                  </span>

                  <h2>
                    {user.full_name}
                  </h2>

                  <p>
                    {user.designation ??
                      "Employee"}
                  </p>

                </div>

              </div>


              <div className="profile-actions">

                <button
                  type="button"
                  className="profile-edit-button"
                  onClick={
                    startEditing
                  }
                >
                  ✎ Edit
                </button>

                <button
                  type="button"
                  className={
                    user.is_active
                      ? "profile-danger-button"
                      : "profile-success-button"
                  }
                  onClick={
                    handleStatusChange
                  }
                >
                  {user.is_active
                    ? "Deactivate"
                    : "Reactivate"}
                </button>

              </div>

            </div>


            <div className="profile-divider" />


            <div className="profile-grid">

              <div className="profile-item">
                <span>
                  EMPLOYEE ID
                </span>

                <strong>
                  {user.employee_id}
                </strong>
              </div>

              <div className="profile-item">
                <span>
                  USERNAME
                </span>

                <strong>
                  {user.username}
                </strong>
              </div>

              <div className="profile-item">
                <span>
                  EMAIL
                </span>

                <strong>
                  {user.email ?? "—"}
                </strong>
              </div>

              <div className="profile-item">
                <span>
                  ROLE
                </span>

                <strong>
                  {getRoleName(
                    user.role_id,
                  )}
                </strong>
              </div>

            </div>


            <div className="profile-organization">

              <div className="profile-organization-icon">
                ◈
              </div>

              <div>

                <span>
                  ORGANIZATION
                </span>

                <strong>

                  {getOrganization(
                    organizationUnits,
                    user.organization_unit_id,
                  )
                    ? `${getOrganization(
                      organizationUnits,
                      user.organization_unit_id,
                    )?.name} — ${getOrganization(
                      organizationUnits,
                      user.organization_unit_id,
                    )?.code
                    }`
                    : "System-wide"}

                </strong>

              </div>

            </div>

          </section>
        )}


        {/* EDIT */}

        {user && editing && (

          <form
            className="compact-user-form"
            onSubmit={
              handleUpdate
            }
          >

            <section className="compact-form-section">

              <div className="compact-section-header">

                <div className="compact-section-number">
                  01
                </div>

                <div>

                  <span>
                    EMPLOYEE PROFILE
                  </span>

                  <h2>
                    Account Information
                  </h2>

                </div>

              </div>


              <div className="modern-form-grid">

                <div className="modern-field">

                  <label>
                    Employee ID
                  </label>

                  <input
                    value={
                      user.employee_id
                    }
                    disabled
                  />

                </div>


                <div className="modern-field">

                  <label>
                    Username
                  </label>

                  <input
                    value={
                      user.username
                    }
                    disabled
                  />

                </div>


                <div className="modern-field">

                  <label>
                    Full Name
                    <span>*</span>
                  </label>

                  <input
                    value={
                      form.full_name ?? ""
                    }
                    onChange={(event) =>
                      setForm(
                        (previous) => ({
                          ...previous,
                          full_name:
                            event.target.value,
                        }),
                      )
                    }
                    required
                  />

                </div>


                <div className="modern-field">

                  <label>
                    Designation
                  </label>

                  <input
                    value={
                      form.designation ?? ""
                    }
                    onChange={(event) =>
                      setForm(
                        (previous) => ({
                          ...previous,
                          designation:
                            event.target.value,
                        }),
                      )
                    }
                  />

                </div>


                <div className="modern-field">

                  <label>
                    Email
                  </label>

                  <input
                    type="email"
                    value={
                      form.email ?? ""
                    }
                    onChange={(event) =>
                      setForm(
                        (previous) => ({
                          ...previous,
                          email:
                            event.target.value,
                        }),
                      )
                    }
                  />

                </div>


                <div className="modern-field">

                  <label>
                    New Password
                  </label>

                  <input
                    type="password"
                    placeholder="Leave blank to keep current"
                    onChange={(event) =>
                      setForm(
                        (previous) => ({
                          ...previous,
                          password:
                            event.target.value ||
                            null,
                        }),
                      )
                    }
                  />

                </div>

              </div>

            </section>


            <section className="compact-form-section">

              <div className="compact-section-header">

                <div className="compact-section-number">
                  02
                </div>

                <div>

                  <span>
                    ACCESS CONTROL
                  </span>

                  <h2>
                    Role & Rule
                  </h2>

                </div>

              </div>


              <div className="role-select-wrapper">

                <label>
                  Select Role
                  <span>*</span>
                </label>

                <select
                  className="large-role-select"
                  value={
                    form.role_id ?? ""
                  }
                  onChange={(event) =>
                    handleUpdateRoleChange(
                      Number(
                        event.target.value,
                      ),
                    )
                  }
                  required
                >

                  <option value="">
                    Choose employee role
                  </option>

                  {roles.map(
                    (role) => (
                      <option
                        key={role.id}
                        value={role.id}
                      >
                        {role.name} —{" "}
                        {role.description}
                      </option>
                    ),
                  )}

                </select>


                {form.role_id && (

                  <div className="selected-role-info">

                    <span className="selected-role-check">
                      ✓
                    </span>

                    <div>

                      <strong>
                        {
                          getRole(
                            form.role_id,
                          )?.name
                        }
                      </strong>

                      <p>
                        {
                          getRole(
                            form.role_id,
                          )?.description
                        }
                      </p>

                    </div>

                  </div>

                )}

              </div>

            </section>


            <section className="compact-form-section">

              <div className="compact-section-header">

                <div className="compact-section-number">
                  03
                </div>

                <div>

                  <span>
                    ORGANIZATION
                  </span>

                  <h2>
                    Assignment
                  </h2>

                </div>

              </div>


              <div className="organization-panel">

                {organizationLoading ? (

                  <div className="organization-loading-modern">

                    <div className="loading-spinner" />

                    Loading organization...

                  </div>

                ) : (

                  <OrganizationSelector
                    roleId={
                      form.role_id ?? 0
                    }
                    update={true}
                  />

                )}

              </div>

            </section>


            <div className="modern-form-actions">

              <button
                type="button"
                className="modern-secondary-button"
                onClick={
                  cancelEditing
                }
              >
                Cancel
              </button>

              <button
                type="submit"
                className="modern-primary-button"
                disabled={loading}
              >

                {loading ? (
                  <>
                    <span className="button-spinner" />
                    Saving...
                  </>
                ) : (
                  <>
                    ✓ Save Changes
                  </>
                )}

              </button>

            </div>

          </form>
        )}

      </div>
    </DashboardLayout>
  );
}


export default Users;