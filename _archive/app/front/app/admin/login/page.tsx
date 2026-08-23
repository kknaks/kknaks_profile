"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { authApi, AuthError } from "@/lib/api";

export default function AdminLoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  // 이미 로그인돼 있으면 /admin 으로.
  useEffect(() => {
    authApi
      .me()
      .then(() => router.replace("/admin"))
      .catch(() => {
        /* 미인증 — 로그인 화면 유지 */
      });
  }, [router]);

  const canSubmit = username.trim() !== "" && password.trim() !== "" && !submitting;

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!canSubmit) return;
    setSubmitting(true);
    setError(null);
    try {
      await authApi.login(username, password);
      router.replace("/admin");
    } catch (err) {
      // 자격 불일치는 통합 문구 — 아이디/비밀번호 어느 쪽이 틀렸는지 구분하지 않는다.
      const msg =
        err instanceof AuthError && err.status === 401
          ? "아이디 또는 비밀번호가 올바르지 않습니다."
          : "로그인 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.";
      setError(msg);
      setSubmitting(false);
    }
  }

  return (
    <main
      style={{
        minHeight: "70vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "48px 20px",
      }}
    >
      <form
        onSubmit={onSubmit}
        style={{
          width: "100%",
          maxWidth: 360,
          background: "var(--bg-1)",
          border: "1px solid var(--line-1)",
          borderRadius: 8,
          padding: 28,
          display: "flex",
          flexDirection: "column",
          gap: 16,
        }}
      >
        <div>
          <h1 style={{ fontSize: 20, color: "var(--fg-0)", margin: 0 }}>관리자 로그인</h1>
          <p
            className="mono"
            style={{ fontSize: 11, color: "var(--fg-3)", marginTop: 6 }}
          >
            kknaks.dev admin
          </p>
        </div>

        <label style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          <span style={{ fontSize: 12, color: "var(--fg-2)" }}>아이디</span>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            autoFocus
            style={inputStyle}
          />
        </label>

        <label style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          <span style={{ fontSize: 12, color: "var(--fg-2)" }}>비밀번호</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            style={inputStyle}
          />
        </label>

        {error && (
          <div
            role="alert"
            style={{
              fontSize: 12,
              color: "var(--danger)",
              background: "color-mix(in oklab, var(--danger) 12%, transparent)",
              border: "1px solid color-mix(in oklab, var(--danger) 32%, transparent)",
              borderRadius: 4,
              padding: "8px 10px",
            }}
          >
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={!canSubmit}
          style={{
            marginTop: 4,
            padding: "10px 12px",
            borderRadius: 4,
            border: "1px solid var(--accent-line)",
            background: canSubmit ? "var(--accent)" : "var(--bg-3)",
            color: canSubmit ? "var(--accent-ink)" : "var(--fg-3)",
            fontSize: 13,
            fontWeight: 600,
            cursor: canSubmit ? "pointer" : "not-allowed",
          }}
        >
          {submitting ? "로그인 중…" : "로그인"}
        </button>
      </form>
    </main>
  );
}

const inputStyle: React.CSSProperties = {
  background: "var(--bg-0)",
  border: "1px solid var(--line-2)",
  borderRadius: 4,
  padding: "9px 11px",
  color: "var(--fg-0)",
  fontSize: 14,
  outline: "none",
};
