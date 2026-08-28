"use client";

import { useEffect, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import type { ChatExposureKind } from "@/lib/types";

/**
 * 채팅 노출 토글 (KDEV-SPEC-017 §2 U-7) — career · project · problem · product
 * 어드민 목록의 각 행에 붙는다. **기본 off**, 켠 것만 AI tool 응답에 실린다
 * (DEC-027 D4). kind 만 다르고 동작은 같다.
 *
 * 목록 재조회를 부르지 않는다 — 이 값만 바뀌므로 행을 다시 그릴 이유가 없다.
 * 스타일은 옆 `visible` 토글 관례를 그대로 따른다.
 */
export function ChatExposureToggle({
  kind,
  id,
  exposed,
}: {
  kind: ChatExposureKind;
  id: number;
  exposed?: boolean;
}) {
  const [on, setOn] = useState(!!exposed);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 목록이 다시 로드되면 서버 값이 기준이다.
  useEffect(() => setOn(!!exposed), [exposed]);

  async function toggle() {
    const next = !on;
    setBusy(true);
    setError(null);
    try {
      await adminApi.patchChatExposure(kind, id, next);
      setOn(next);
    } catch (e) {
      setError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <button
        type="button"
        onClick={toggle}
        disabled={busy}
        title={on ? "채팅 노출 중 — 누르면 끔" : "채팅 숨김 — 누르면 켬"}
        className="mono"
        style={{
          fontSize: 10,
          letterSpacing: "0.08em",
          padding: "4px 10px",
          borderRadius: 999,
          cursor: "pointer",
          border: on ? "1px solid var(--accent)" : "1px solid var(--line-2)",
          background: on ? "var(--accent-soft)" : "transparent",
          color: on ? "var(--accent)" : "var(--fg-3)",
        }}
      >
        {on ? "채팅 노출" : "채팅 숨김"}
      </button>
      {error && (
        <span className="mono" style={{ fontSize: 11, color: "var(--danger)" }}>
          {error}
        </span>
      )}
    </>
  );
}
