// src/context/AuthProvider.jsx
import React, { useState, useEffect } from "react";
import axios from "axios";
import { AuthContext } from "./AuthContext.jsx";

const API_URL = "http://localhost:8000";

// single axios instance for auth-related requests.
// we mark the instance to avoid reattaching interceptors on HMR.
const axiosAuth = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

if (!axiosAuth.__hasAuthInterceptor) {
  axiosAuth.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = 'Bearer ${token}';
    }
    return config;
  });
  axiosAuth.__hasAuthInterceptor = true;
}

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null); // used for UI or debugging

  useEffect(() => {
    let mounted = true;

    const init = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) {
        if (mounted) setLoading(false);
        return;
      }

      try {
        const res = await axiosAuth.get("/api/auth/me/");
        if (!mounted) return;
        setUser(res.data);
        setError(null);
      } catch (err) {
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
  }, []); // axiosAuth is stable (declared outside) so no deps needed

  const register = async (username, email, password) => {
    try {
      const res = await axios.post(API_URL + "/api/auth/register/", {
        username,
        email,
        password,
      });
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
      const res = await axios.post(API_URL + "/api/auth/login/", {
        username,
        password,
      });

      localStorage.setItem("access_token", res.data.access);
      localStorage.setItem("refresh_token", res.data.refresh);

      const userRes = await axiosAuth.get("/api/auth/me/");
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
    <AuthContext.Provider
      value={{ user, loading, error, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;