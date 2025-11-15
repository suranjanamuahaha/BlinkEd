// src/context/AuthProvider.jsx
import React, { useState, useEffect } from "react";
import { AuthContext } from "./AuthContext.jsx";
import { authService } from "../services/authService";

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;

    const init = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) {
        if (mounted) setLoading(false);
        return;
      }

      try {
        const res = await authService.getMe();
        if (!mounted) return;
        setUser(res.data);
        setError(null);
      } catch (err) {
        // keep 'err' so linter doesn't complain; log it for debugging
        console.error("auth init error:", err);
        if (!mounted) return;
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        setUser(null);
        setError(null);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    init();

    return () => {
      mounted = false;
    };
  }, []);

  const register = async (username, email, password) => {
    try {
      const res = await authService.register(username, email, password);
      setError(null);
      return res.data;
    } catch (err) {
      console.error("register error:", err);
      const errorMsg = err.response?.data?.detail || "Registration failed";
      setError(errorMsg);
      throw new Error(errorMsg);
    }
  };

  const login = async (username, password) => {
    try {
      const res = await authService.login(username, password);
      localStorage.setItem("access_token", res.data.access);
      localStorage.setItem("refresh_token", res.data.refresh);

      const userRes = await authService.getMe();
      setUser(userRes.data);
      setError(null);
      return userRes.data;
    } catch (err) {
      console.error("login error:", err);
      const errorMsg = err.response?.data?.detail || "Login failed";
      setError(errorMsg);
      throw new Error(errorMsg);
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    setError(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, error, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
