import type { Permission } from "./permissions";

export interface SidebarItem {
  label: string;
  path: string;
  permission: Permission;
}

export const sidebarItems: SidebarItem[] = [
  {
    label: "Dashboard",
    path: "/dashboard",
    permission: "VIEW_DASHBOARD",
  },

  {
    label: "Users",
    path: "/users",
    permission: "MANAGE_USERS",
  },

  {
    label: "Organizations",
    path: "/organizations",
    permission: "VIEW_ORGANIZATIONS",
  },

  {
    label: "Lines",
    path: "/lines",
    permission: "VIEW_LINES",
  },

  {
    label: "Layout",
    path: "/layout",
    permission: "VIEW_LAYOUT",
  },

  {
    label: "Production",
    path: "/production",
    permission: "VIEW_PRODUCTION",
  },

  {
    label: "Reports",
    path: "/reports",
    permission: "VIEW_REPORTS",
  },
];