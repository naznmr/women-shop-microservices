"use client";

import { useState } from "react";
import { apiFetch } from "../lib/api";

function byteLen(s) {
  return new TextEncoder().encode(s).length;
}

export default function AuthPage() {
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  async function register() {
    setMsg("");
    if (byteLen(password) > 72) {
      setMsg("رمز عبور برای bcrypt نباید بیشتر از 72 بایت باشد (رمز کوتاه‌تر بزن).");
      return;
    }
    try {
      await apiFetch("/api/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, full_name: fullName, password, phone: null }),
      });
      setMsg("✅ ثبت‌نام انجام شد. حالا ورود بزن.");
    } catch (e) {
      setMsg("❌ " + e.message);
    }
  }

  async function login() {
    setMsg("");
    try {
      const token = await apiFetch("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      localStorage.setItem("token", token.access_token);
      setMsg("✅ ورود موفق");
      window.location.href = "/";
    } catch (e) {
      setMsg("❌ " + e.message);
    }
  }

  return (
    <div style={{ maxWidth: 520 }}>
      <h1 className="h1">ورود / ثبت‌نام</h1>

      <label className="label">ایمیل</label>
      <input className="input" value={email} onChange={(e) => setEmail(e.target.value)} />

      <label className="label" style={{ marginTop: 10 }}>نام کامل (برای ثبت‌نام)</label>
      <input className="input" value={fullName} onChange={(e) => setFullName(e.target.value)} />

      <label className="label" style={{ marginTop: 10 }}>رمز عبور</label>
      <input className="input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

      <div style={{ display: "flex", gap: 10, marginTop: 12 }}>
        <button className="btn" onClick={register}>ثبت‌نام</button>
        <button className="btn btn--primary" onClick={login}>ورود</button>
      </div>

      {msg ? <p style={{ marginTop: 12 }}>{msg}</p> : null}
    </div>
  );
}