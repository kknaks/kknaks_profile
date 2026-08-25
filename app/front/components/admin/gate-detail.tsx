"use client";

import { useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import type {
  AdminGateItem,
  GateConceptItem,
  GateConceptPayload,
  GateDocumentPayload,
} from "@/lib/types";

// 게이트 상세 — 케이스 1(2026-08-25 개정). 인박스(/admin/capture) 행 펼침 안에서 쓴다.
// 문서는 서버 검증 통과 시 **자동 착지**라 승인 UI 가 없다 — 사람이 만지는 것은
// 개념 게이트(승인/거절)와 「승인됨·푸시 실패」의 [재시도], 그리고 done 행의
// 읽기 전용 이력(GateHistory)뿐이다. 초안은 다듬어서 승인한다 — 화면에서 고친
// 내용이 payload 로 저장되고 그대로 착지한다(재생성 루프 없음, v1).

/** 행 펼침의 진입점 — 게이트 상태에 따라 개념 승인·푸시 재시도 중 하나를 그린다. */
export function GateDetail({
  gate,
  onDone,
}: {
  gate: AdminGateItem;
  onDone: (msg: string) => void;
}) {
  const pushFailed = gate.status === "approved" && !gate.commitRef && !gate.result;
  if (pushFailed) return <PushRetryDetail gate={gate} onDone={onDone} />;
  if (gate.status !== "open") return null;
  // 문서는 자동 착지(개정) — open document 는 정상 흐름에 없다. 승인 UI 를 안 그린다.
  if (gate.stage === "document") return null;
  return <ConceptGateDetail gate={gate} onDone={onDone} />;
}

/* ── done 행 펼침 — 읽기 전용 이력. 승인·거절 버튼이 없다 ─────────────── */

/** dev dry-run 확정 마커 — 커밋 자체가 없다(back gate_service.DRY_RUN_REF). */
const DRY_RUN_REF = "dry-run";

/** 커밋 표시 조각 — dry-run 확정은 「커밋 없음 (dry-run)」, 실패(null)와 구분. */
function commitLabel(gate: AdminGateItem): string | null {
  if (!gate.commitRef) return null;
  if (gate.commitRef === DRY_RUN_REF) return "커밋 없음 (dry-run)";
  return `커밋 ${gate.commitRef.slice(0, 7)}`;
}

/** 게이트 한 건의 이력 한 줄 — 「문서: <stem> · 커밋 <sha7> (자동 착지)」 류. */
function historyLine(gate: AdminGateItem): string {
  const commit = commitLabel(gate);
  if (gate.stage === "document") {
    const stem = (gate.payload as GateDocumentPayload).stem ?? "";
    if (gate.status === "rejected") return `문서: ${stem || gate.title} · 거절`;
    if (!commit) return `문서: ${stem} · 푸시 실패 — [재시도] 대기`;
    return `문서: ${stem} · ${commit} (자동 착지)`;
  }
  if (gate.status === "rejected") return "개념: 거절";
  if (gate.status === "open") return "개념: 승인 대기";
  const n = ((gate.payload as GateConceptPayload).concepts ?? []).length;
  if (n === 0) return "개념: 후보 없음";
  return `개념: 승인 ${n}건${commit ? ` · ${commit}` : ""}`;
}

export function GateHistory({ gates }: { gates: AdminGateItem[] }) {
  return (
    <div style={panel}>
      <div style={panelHead}>
        <span style={{ fontSize: 14, color: "var(--fg-0)", fontWeight: 600 }}>이력</span>
        <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
          {gates[0]?.title ?? ""}
        </span>
      </div>
      <div style={{ padding: "14px 20px", display: "flex", flexDirection: "column", gap: 6 }}>
        {gates.map((g) => (
          <div key={g.id}>
            <p className="mono" style={{ fontSize: 12, color: "var(--fg-2)", margin: 0 }}>
              {historyLine(g)}
              {g.decidedAt && (
                <span style={{ color: "var(--fg-4)" }}>
                  {" "}
                  · {new Date(g.decidedAt).toLocaleString()}
                </span>
              )}
            </p>
            {/* 생성된 콘텐츠 — 확정 게이트(result.contentId)의 제목 + 공개 페이지 링크 */}
            {g.contentTitle && g.contentSlug && (
              <p className="mono" style={{ fontSize: 12, color: "var(--fg-2)", margin: "2px 0 0" }}>
                콘텐츠:{" "}
                <a
                  href={`/contents/${g.contentSlug}`}
                  target="_blank"
                  rel="noreferrer"
                  style={{ color: "var(--accent)", textDecoration: "underline" }}
                >
                  {g.contentTitle} ({g.contentSlug})
                </a>
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

/* ── 승인됨 · 푸시 실패 — 승인은 저장돼 있다. 푸시만 다시 건다 ─────────── */

function PushRetryDetail({
  gate,
  onDone,
}: {
  gate: AdminGateItem;
  onDone: (msg: string) => void;
}) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function retryPush() {
    setBusy(true);
    setError(null);
    try {
      const res = await adminApi.retryGatePush(gate.id);
      if (res.pushError) {
        setError(`푸시 실패 — ${res.pushError}`);
        setBusy(false);
      } else if (res.commitRef === DRY_RUN_REF) {
        onDone("착지 완료 — 커밋 없음 (dry-run)");
      } else {
        onDone(`푸시 성공 — ${res.commitRef?.slice(0, 7) ?? ""}`);
      }
    } catch (e) {
      setError(e instanceof AuthError ? e.message : String(e));
      setBusy(false);
    }
  }

  return (
    <div style={panel}>
      <div style={panelHead}>
        <span style={{ fontSize: 14, color: "var(--fg-0)", fontWeight: 600 }}>
          승인됨 · 푸시 실패
        </span>
        <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
          {gate.stage === "document" ? "게이트1 · 문서" : "게이트2 · 개념"} · {gate.title}
        </span>
      </div>
      <div style={{ padding: "16px 20px" }}>
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-2)", margin: 0 }}>
          승인 내용은 저장돼 있다 — 커밋·푸시만 다시 시도한다.
        </p>
        {error && (
          <p
            className="mono"
            style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "10px 0 0" }}
          >
            {error}
          </p>
        )}
      </div>
      <div
        style={{
          borderTop: "1px solid var(--line-1)",
          padding: "14px 20px",
          display: "flex",
          justifyContent: "flex-end",
        }}
      >
        <button type="button" onClick={retryPush} disabled={busy} style={primaryBtn}>
          {busy ? "재시도 중…" : "재시도 — 커밋 · 푸시"}
        </button>
      </div>
    </div>
  );
}

/* ── 공용 — 승인·거절 버튼 줄 ──────────────────────────────────────────── */

function DecisionFooter({
  busy,
  error,
  onReject,
  onApprove,
}: {
  busy: boolean;
  error: string | null;
  onReject: () => void;
  onApprove: () => void;
}) {
  return (
    <div style={{ borderTop: "1px solid var(--line-1)", padding: "14px 20px" }}>
      {error && (
        <p className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "0 0 10px" }}>
          {error}
        </p>
      )}
      <div style={{ display: "flex", justifyContent: "flex-end", gap: 10 }}>
        <button type="button" onClick={onReject} disabled={busy} style={ghostBtn}>
          거절
        </button>
        <button type="button" onClick={onApprove} disabled={busy} style={primaryBtn}>
          {busy ? "처리 중…" : "승인 — 커밋 · 푸시"}
        </button>
      </div>
    </div>
  );
}

function useDecision(gateId: number, onDone: (msg: string) => void) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function reject() {
    setBusy(true);
    setError(null);
    try {
      await adminApi.rejectGate(gateId);
      onDone("거절했다 — queue 는 done 으로 종결");
    } catch (e) {
      setError(e instanceof AuthError ? e.message : String(e));
      setBusy(false);
    }
  }

  async function approve(payload: GateConceptPayload) {
    setBusy(true);
    setError(null);
    try {
      const res = await adminApi.approveGate(gateId, payload);
      if (res.pushError) {
        onDone(`승인은 저장됐지만 푸시 실패 — 행을 펼쳐 [재시도]로 다시: ${res.pushError}`);
      } else if (res.commitRef === DRY_RUN_REF) {
        onDone("착지 완료 — 커밋 없음 (dry-run) — 종결");
      } else {
        onDone(`착지·푸시 완료(${res.commitRef?.slice(0, 7) ?? "커밋 없음"}) — 종결`);
      }
    } catch (e) {
      setError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
      setBusy(false);
    }
  }

  return { busy, error, reject, approve };
}

/* ── 게이트(개념) 상세 — 개념 항목별 체크. 체크 해제 = 안 올림 ──────────
 * 문서 승인 UI 는 없다 — 문서는 서버 검증 + 자동 착지(2026-08-25 개정). */

function ConceptGateDetail({
  gate,
  onDone,
}: {
  gate: AdminGateItem;
  onDone: (msg: string) => void;
}) {
  const payload = gate.payload as GateConceptPayload;
  const [drafts, setDrafts] = useState<GateConceptItem[]>(payload.concepts);
  const [checked, setChecked] = useState<boolean[]>(payload.concepts.map(() => true));
  const { busy, error, reject, approve } = useDecision(gate.id, onDone);

  function submit() {
    approve({ concepts: drafts.filter((_, i) => checked[i]) });
  }

  return (
    <div style={panel}>
      <div style={panelHead}>
        <span style={{ fontSize: 14, color: "var(--fg-0)", fontWeight: 600 }}>게이트 2 · 개념</span>
        <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
          {gate.kind} · {gate.title}
        </span>
      </div>

      <div style={{ padding: "16px 20px", display: "flex", flexDirection: "column", gap: 14 }}>
        {drafts.length === 0 && (
          <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", margin: 0 }}>
            개념 후보가 없다 — 승인하면 커밋 없이 종결된다
          </p>
        )}
        {drafts.map((item, i) => (
          <div key={`${item.area}/${item.stem}`} style={{ border: "1px solid var(--line-1)", borderRadius: 6, padding: "10px 12px" }}>
            <label style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }}>
              <input
                type="checkbox"
                checked={checked[i]}
                onChange={(e) =>
                  setChecked(checked.map((c, j) => (j === i ? e.target.checked : c)))
                }
              />
              <span className="mono" style={{ fontSize: 11, color: item.mode === "create" ? "var(--accent)" : "var(--info)" }}>
                {item.mode === "create" ? "신규" : "보강"}
              </span>
              <span className="mono" style={{ fontSize: 12, color: "var(--fg-1)" }}>
                {item.area}/{item.stem}
              </span>
            </label>

            {checked[i] && item.mode === "create" && (
              <textarea
                value={item.body}
                onChange={(e) =>
                  setDrafts(drafts.map((d, j) => (j === i ? { ...d, body: e.target.value } : d)))
                }
                rows={12}
                style={{ ...input, marginTop: 8, resize: "vertical", fontFamily: "var(--font-mono)", fontSize: 12 }}
              />
            )}

            {checked[i] && item.mode === "supplement" && (
              <pre
                className="mono"
                style={{
                  marginTop: 8,
                  marginBottom: 0,
                  fontSize: 11,
                  lineHeight: 1.6,
                  background: "var(--bg-2)",
                  border: "1px solid var(--line-1)",
                  borderRadius: 5,
                  padding: "8px 10px",
                  overflowX: "auto",
                  whiteSpace: "pre",
                }}
              >
                {(item.diff || "(diff 없음)").split("\n").map((line, k) => (
                  <span
                    key={k}
                    style={{
                      display: "block",
                      color: line.startsWith("+")
                        ? "var(--accent)"
                        : line.startsWith("-")
                          ? "var(--danger, #e5534b)"
                          : "var(--fg-3)",
                    }}
                  >
                    {line}
                  </span>
                ))}
              </pre>
            )}
          </div>
        ))}
      </div>

      <DecisionFooter busy={busy} error={error} onReject={reject} onApprove={submit} />
    </div>
  );
}

/* ── 스타일 조각 ────────────────────────────────────────────────────── */

const panel: React.CSSProperties = {
  border: "1px solid var(--line-2)",
  borderRadius: 10,
  background: "var(--bg-1)",
};

const panelHead: React.CSSProperties = {
  display: "flex",
  alignItems: "baseline",
  gap: 10,
  flexWrap: "wrap",
  padding: "14px 20px",
  borderBottom: "1px solid var(--line-1)",
};

const fieldLabel: React.CSSProperties = {
  fontSize: 10,
  letterSpacing: "0.08em",
  color: "var(--fg-4)",
};

const input: React.CSSProperties = {
  display: "block",
  width: "100%",
  boxSizing: "border-box",
  marginTop: 4,
  fontSize: 13,
  color: "var(--fg-1)",
  background: "var(--bg-2)",
  border: "1px solid var(--line-1)",
  borderRadius: 5,
  padding: "7px 10px",
  outline: "none",
};

const ghostBtn: React.CSSProperties = {
  fontSize: 11,
  fontFamily: "var(--font-mono)",
  padding: "4px 12px",
  borderRadius: 5,
  border: "1px solid var(--line-2)",
  background: "transparent",
  color: "var(--fg-2)",
  cursor: "pointer",
};

const primaryBtn: React.CSSProperties = {
  fontSize: 11,
  fontFamily: "var(--font-mono)",
  padding: "6px 14px",
  borderRadius: 5,
  border: "1px solid var(--line-2)",
  background: "var(--fg-0)",
  color: "var(--bg-0)",
  cursor: "pointer",
};
