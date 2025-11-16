// src/hooks/useAuth.js
import { useContext } from "react";
// FIX: Use a named import to match the new AuthContext.jsx
import { AuthContext } from "../context/AuthContext.jsx";

export default function useAuth() {
return useContext(AuthContext);
}