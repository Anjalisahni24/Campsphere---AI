import React, { useState, useEffect } from "react";
import { NavLink, useNavigate } from "react-router-dom";

import {
  LayoutDashboard,
  Briefcase,
  Users,
  BarChart2,
  Building2,
  User,
  LogOut,
  HelpCircle,
  Mail,
  Phone,
  MessageCircle,
  X,
} from "lucide-react";

const sidebarConfig = {
  student: [
    { to: "/student-dashboard", label: "Dashboard", icon: LayoutDashboard },
    { to: "/student-dashboard/jobs", label: "Jobs", icon: Briefcase },
    { to: "/student-dashboard/readiness-score", label: "ReadinessScore", icon: BarChart2 },
    { to: "/student-dashboard/profile", label: "Profile", icon: User },
  ],
  recruiter: [
    { to: "/recruiter-dashboard", label: "Dashboard", icon: LayoutDashboard },
    { to: "/recruiter-dashboard/jobs", label: "Jobs", icon: Briefcase },
    { to: "/recruiter-dashboard/candidate?tab=candidates", label: "Candidates", icon: Users },
    { to: "/recruiter-dashboard/analytics?tab=analytics", label: "Analytics", icon: BarChart2 },
  ],
  admin: [
    { to: "/admin-dashboard", label: "Dashboard", icon: LayoutDashboard },
    { to: "/admin-dashboard/users", label: "UserManagement", icon: Users },
    { to: "/admin-dashboard/jobs", label: "JobManagement", icon: Building2 },
    { to: "/admin-dashboard/analytics", label: "Analytics", icon: BarChart2 },
  ],
};

function Sidebar() {
  const navigate = useNavigate();

  const [role, setRole] = useState("student");
  const [showSupport, setShowSupport] = useState(false);
  const [showLogout, setShowLogout] = useState(false);

  useEffect(() => {
    const storedRole = localStorage.getItem("role") || "student";
    setRole(storedRole);

    const handleStorageChange = () => {
      setRole(localStorage.getItem("role") || "student");
    };

    window.addEventListener("storage", handleStorageChange);
    return () => window.removeEventListener("storage", handleStorageChange);
  }, []);

  const navItems = sidebarConfig[role] || [];

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  return (
    <>
      <aside className="hidden md:flex flex-col w-64 bg-[#f2f4f6] py-6 pr-4 sticky top-0 h-screen">

        {/* LOGO */}
        <div className="px-6 mb-8">
          <h2 className="text-lg font-extrabold text-[#24389c]">
            {role === "recruiter" ? "CampSphere" : "CampSphere"}
          </h2>
        </div>

        {/* NAV */}
        <nav className="flex-1 p-3 space-y-1">
          {navItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition ${
                  isActive
                    ? "bg-white text-[#24389c] shadow-sm"
                    : "text-gray-600 hover:bg-gray-200/50"
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* FOOTER */}
        <div className="p-3 border-t space-y-1">
          {[
            {
              icon: HelpCircle,
              label: "Support",
              action: () => setShowSupport(true),
            },
            {
              icon: LogOut,
              label: "Logout",
              action: () => setShowLogout(true),
            },
          ].map(({ icon: Icon, label, action }) => (
            <button
              key={label}
              onClick={action}
              className="flex items-center h-10 w-full rounded-xl text-sm font-medium text-gray-500
              hover:text-black hover:bg-gray-100 transition-all gap-3 px-3"
            >
              <Icon size={18} />
              {label}
            </button>
          ))}
        </div>
      </aside>

      {/* SUPPORT MODAL */}
      {showSupport && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white w-[350px] p-6 rounded-xl relative">

            <button
              onClick={() => setShowSupport(false)}
              className="absolute top-3 right-3 text-gray-500"
            >
              <X size={18} />
            </button>

            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <HelpCircle size={18} /> Support Center
            </h2>

            <p className="text-sm text-gray-500 mb-4">
              Need help? Our support team is available Monday–Friday, 9 AM – 6 PM IST.
            </p>

            <div className="space-y-3">
              {[
                {
                  icon: Mail,
                  label: "Email Us",
                  value: "support@campsphere.io",
                },
                {
                  icon: Phone,
                  label: "Call Us",
                  value: "+91 80 1234 5678",
                },
                {
                  icon: MessageCircle,
                  label: "Live Chat",
                  value: "Start a conversation",
                },
              ].map((item) => (
                <div
                  key={item.label}
                  className="flex items-center gap-3 p-3 border rounded-lg hover:bg-gray-100 cursor-pointer"
                >
                  <item.icon size={16} />
                  <div>
                    <p className="text-sm font-medium">{item.label}</p>
                    <p className="text-xs text-gray-500">{item.value}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* LOGOUT MODAL */}
      {showLogout && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-xl w-[320px]">

            <h2 className="font-semibold mb-3">Log out of CampSphere?</h2>

            <p className="text-sm text-gray-500 mb-4">
              You'll be signed out. Unsaved changes will be lost.
            </p>

            <div className="flex justify-end gap-2">
              <button
                onClick={() => setShowLogout(false)}
                className="px-3 py-1 border rounded"
              >
                Cancel
              </button>

              <button
                onClick={handleLogout}
                className="px-3 py-1  border rounded "
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Sidebar;