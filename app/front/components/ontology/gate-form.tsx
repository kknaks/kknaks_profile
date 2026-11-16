"use client";

import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { ontologyApi } from "@/lib/ontology/client";
import { OntButton } from "./primitives";

/**
 * 접속 게이트(SPEC-004 U-2 · SPEC-003 U-1).
 *
 * 문구는 SPEC-003 U-1 그대로다. **시도 횟수·잠금·계정 안내를 만들지 않는다**
 * (DEC-005 D2 — rate limit 을 두지 않는다).
 *
 * 성공하면 세션 마커가 남고 `router.refresh()` 로 미들웨어를 다시 태운다 — rewrite 라
 * URL 이 유지돼 **원래 가려던 라우트로 그대로 복귀**한다.
 */
export function GateForm() {
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [failed, setFailed] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (password.trim().length === 0) return; // 빈 입력은 no-op — 에러를 띄우지 않는다.
    setSubmitting(true);
    setFailed(false);
    try {
      await ontologyApi.createSession(password);
      router.refresh();
    } catch {
      setFailed(true);
      setSubmitting(false);
    }
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "var(--ont-canvas)",
      }}
    >
      <form
        onSubmit={submit}
        style={{
          width: 400,
          borderRadius: 12,
          background: "var(--ont-surface)",
          border: "1px solid var(--ont-border-card)",
          boxShadow: "var(--ont-shadow-card)",
          padding: 32,
          display: "flex",
          flexDirection: "column",
          gap: 16,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span
            style={{
              width: 26,
              height: 26,
              borderRadius: 6,
              background: "var(--ont-grad-logo)",
              color: "#fff",
              fontSize: 13,
              fontWeight: 800,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            O
          </span>
          <span style={{ fontSize: 17, fontWeight: 800, letterSpacing: "-0.01em" }}>Ontology</span>
        </div>

        <p style={{ margin: 0, fontSize: 14, lineHeight: 1.6, color: "var(--ont-body)" }}>
          내부 공유용 데모입니다. 공유받은 비밀번호를 입력해 주세요.
        </p>

        <input
          type="password"
          value={password}
          onChange={(event) => {
            setPassword(event.target.value);
            setFailed(false);
          }}
          placeholder="비밀번호"
          autoFocus
          style={{
            height: 56,
            borderRadius: 8,
            padding: "0 16px",
            fontSize: 15,
            color: "var(--ont-ink)",
            background: "var(--ont-surface)",
            border: `1px solid ${failed ? "var(--ont-alert-border)" : "var(--ont-border-card)"}`,
            outline: "none",
          }}
        />

        {failed && (
          <p style={{ margin: 0, fontSize: 12, color: "var(--ont-alert-text)" }}>
            비밀번호가 올바르지 않습니다.
          </p>
        )}

        <OntButton tone="primary" full submit disabled={submitting}>
          들어가기
        </OntButton>
      </form>
    </div>
  );
}
