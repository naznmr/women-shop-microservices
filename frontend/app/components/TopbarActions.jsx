"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "../lib/api";

export default function TopbarActions() {
  const [me, setMe] = useState(null);
  const [loading, setLoading] = useState(true);

  async function loadMe() {
    setLoading(true);
    const token = localStorage.getItem("token");
    if (!token) {
      setMe(null);
      setLoading(false);
      return;
    }
    try {
      const data = await apiFetch("/api/users/me", { method: "GET" });
      setMe(data);
    } catch {
      // توکن خراب/منقضی
      localStorage.removeItem("token");
      setMe(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadMe();
    window.addEventListener("storage", loadMe);
    return () => window.removeEventListener("storage", loadMe);
  }, []);

  function logout() {
    localStorage.removeItem("token");
    setMe(null);
    window.location.href = "/";
  }

  if (loading) return null;

  if (!me) {
    return <a className="nav__link nav__link--primary" href="/auth">ورود / ثبت‌نام</a>;
  }

  return (
    <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
      <span className="nav__link" style={{ cursor: "default" }}>👤 {me.full_name || me.email}</span>
      <button className="nav__link nav__link--primary" onClick={logout}>خروج</button>
    </div>
  );
}