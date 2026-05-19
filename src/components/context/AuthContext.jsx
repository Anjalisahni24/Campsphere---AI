import React, { createContext, useContext, useEffect, useState } from "react";
import {
  signInWithPopup,
  signOut as firebaseSignOut,
} from "firebase/auth";
import { auth, googleProvider } from "../../firebase/firebase";

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [userRole, setUserRole] = useState(null);
  const [loading, setLoading] = useState(true);

  const API_BASE_URL = "http://localhost:8000/api/auth"; // Update this with env var if needed

  useEffect(() => {
    // Check if user is logged in via JWT
    const token = localStorage.getItem("accessToken");
    const storedUser = localStorage.getItem("user");
    const savedRole = localStorage.getItem("userRole");

    if (token && storedUser && savedRole) {
      setCurrentUser(JSON.parse(storedUser));
      setUserRole(savedRole);
    }
    setLoading(false);
  }, []);

  // Sign up
  const signup = async (name, email, password, role, companyName = "") => {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, password, role, company_name: companyName }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Signup failed");
    }

    const data = await response.json();
    localStorage.setItem("accessToken", data.access_token);
    localStorage.setItem("userRole", data.user.role);
    localStorage.setItem("user", JSON.stringify(data.user));
    
    setCurrentUser(data.user);
    setUserRole(data.user.role);
    return data;
  };

  // Log in
  const login = async (email, password, role) => {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password, role }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Login failed");
    }

    const data = await response.json();
    localStorage.setItem("accessToken", data.access_token);
    localStorage.setItem("userRole", data.user.role);
    localStorage.setItem("user", JSON.stringify(data.user));
    
    setCurrentUser(data.user);
    setUserRole(data.user.role);
    return data;
  };

  // Google Login (Keep Firebase for now, but we'd ideally sync it to our DB)
  const loginWithGoogle = async (role) => {
    const userCredential = await signInWithPopup(auth, googleProvider);
    localStorage.setItem("userRole", role);
    setUserRole(role);
    setCurrentUser(userCredential.user);
    return userCredential;
  };

  // Log out
  const logout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("userRole");
    localStorage.removeItem("user");
    setUserRole(null);
    setCurrentUser(null);
    return firebaseSignOut(auth); // Sign out of firebase too if they used Google
  };

  const value = {
    currentUser,
    userRole,
    login,
    signup,
    logout,
    loginWithGoogle,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
