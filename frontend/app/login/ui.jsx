"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";

export default function AuthClient() {
  const router = useRouter();
  const USER_BASE = useMemo(
    () => process.env.NEXT_PUBLIC_USER_BASE || "http://localhost:8001",
    []
  );

  const [mode, setMode] = useState("login");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("test@example.com");
  const [password, setPassword] = useState("Test12345");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  async function submit(e) {
    e.preventDefault();
    setMsg("");
    setLoading(true);

    try {
      if (mode === "register") {
        const r = await fetch(`${USER_BASE}/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password, full_name: fullName || "کاربر جدید" }),
        });
        if (!r.ok) throw new Error(await r.text());
      }

      const res = await fetch(`${USER_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) throw new Error(await res.text());

      const data = await res.json();
      localStorage.setItem("access_token", data.access_token);
      setMsg("✅ ورود موفق");
      router.push("/");
      router.refresh();
    } catch (err) {
      setMsg("❌ " + (err?.message || "خطا"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth">
      <div className="auth__card">
        <div className="auth__head">
          <div className="auth__title">{mode === "login" ? "ورود" : "ثبت‌نام"}</div>
          <div className="auth__tabs">
            <button className={"auth__tab " + (mode === "login" ? "isActive" : "")} onClick={() => setMode("login")}>
              ورود
            </button>
            <button className={"auth__tab " + (mode === "register" ? "isActive" : "")} onClick={() => setMode("register")}>
              ثبت‌نام
            </button>
          </div>
        </div>

        <form onSubmit={submit} className="auth__form">
          {mode === "register" && (
            <label className="field">
              <span>نام و نام خانوادگی</span>
              <input value={fullName} onChange={(e) => setFullName(e.target.value)} />
            </label>
          )}

          <label className="field">
            <span>ایمیل</span>
            <input value={email} onChange={(e) => setEmail(e.target.value)} dir="ltr" />
          </label>

          <label className="field">
            <span>رمز عبور</span>
            <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" dir="ltr" />
          </label>

          <button className="btn auth__btn" disabled={loading}>
            {loading ? "..." : mode === "login" ? "ورود" : "ثبت‌نام و ورود"}
          </button>

          {msg && <div className="auth__msg">{msg}</div>}
        </form>
      </div>
    </div>
  );
}