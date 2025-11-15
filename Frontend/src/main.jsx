import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
// FIX: Use a default import for AuthProvider
import AuthProvider from "./context/AuthProvider.jsx";

createRoot(document.getElementById("root")).render(
 <AuthProvider>
  <App />
 </AuthProvider>
);