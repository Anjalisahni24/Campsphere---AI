import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const ProtectedRoute = ({ children, allowedRoles }) => {
  const { currentUser, userRole } = useAuth();

  if (!currentUser) {
    // Not logged in
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(userRole)) {
    // Logged in but wrong role
    // Redirect them to their respective dashboard or a generic unauthorized page
    if (userRole === "student") return <Navigate to="/student-dashboard" replace />;
    if (userRole === "recruiter") return <Navigate to="/recruiter-dashboard" replace />;
    if (userRole === "admin") return <Navigate to="/admin-dashboard" replace />;
    
    // Fallback if role is unknown
    return <Navigate to="/login" replace />;
  }

  // All good! Render the protected component
  return children;
};

export default ProtectedRoute;
