"use client";

import { useEffect, useState } from "react";
import {
  QueueError,
  queueApi,
  type Gate,
  type GatePayload,
  type NotePayload,
  type RouteResult,
} from "@/lib/api";

/* 게이트 카드 — KDEV-SPEC-008 U-3 / SPEC-009 U-4.
 *
 * 카드에 **인라인 입력창을 두지 않는다.** 버튼은 `피드백`·`승인` 둘뿐이고, 피드백은
 * 모달에서 받는다. 카드 안에 입력창이 있으면 "적다 말고 승인"이 쉬워진다.
 *
 * 승인된 게이트는 접는다. 지금 봐야 할 것 하나만 펼쳐져 있어야 한다.
 */

const STAGE_LABEL: Record<string, string> = {
  route: "목적지",
  source_note: "자료 노트",
  concept: "개념",
  derived: "교안",
};

const STATUS_LABEL: Record<string, { text: string; tone: "wait" | "ok" | "bad" | "idle" }> = {
  not_started: { text: "대기", tone: "idle" },
  generating: { text: "생성 중", tone: "wait" },
  review_pending: { text: "검토 대기", tone: "wait" },
  feedback_pending: { text: "피드백 반영 대기", tone: "wait" },
  regenerating: { text: "재생성 중", tone: "wait" },
  approved: { text: "승인됨", tone: "ok" },
  failed: { text: "실패", tone: "bad" },
  cancelled: { text: "무효화됨", tone: "idle" },
};

const TONE: Record<string, string> = {
  wait: "var(--accent)",
  ok: "#3fb950",
  bad: "#f85149",
  idle: "var(--fg-3)",
};

const box = {
  border: "1px solid var(--line-2)",
  borderRadius: 6,
  background: "var(--bg-1)",
};

function Badge({ status }: { status: string }) {
  const meta = STATUS_LABEL[status] ?? { text: status, tone: "idle" as const };
  return (
    <span
      className="mono"
      style={{
        fontSize: 10,
        letterSpacing: "0.06em",
        color: TONE[meta.tone],
        border: `1px solid ${TONE[meta.tone]}`,
        borderRadius: 3,
        padding: "1px 6px",
      }}
    >
      {meta.text}
    </span>
  );
}

function emptyRoute(): RouteResult {
  return {
    destinations: {
      reference: { enabled: false, group: "" },
      concept: { enabled: false },
      derived: { enabled: false },
    },
    exclusive: null,
  };
}

/** 목적지 토글 — 승인 대상은 AI 제안이 아니라 **여기서 사람이 고친 결과**다. */
function RouteEditor({
  value,
  groups,
  disabled,
  onChange,
}: {
  value: RouteResult;
  groups: string[];
  disabled: boolean;
  onChange: (next: RouteResult) => void;
}) {
  const d = value.destinations;
  const anyEnabled = d.reference.enabled || d.concept.enabled || d.derived.enabled;

  function toggle(key: "reference" | "concept" | "derived", enabled: boolean) {
    onChange({
      ...value,
      // 목적지를 켜면 exclusive 는 자동으로 풀린다 — 서버가 동시 설정을 거부한다.
      exclusive: enabled ? null : value.exclusive,
      destinations: { ...d, [key]: { ...d[key], enabled } },
    });
  }

  function setExclusive(next: RouteResult["exclusive"]) {
    onChange({
      ...value,
      exclusive: next,
      destinations: next
        ? {
            reference: { ...d.reference, enabled: false },
            concept: { enabled: false },
            derived: { enabled: false },
          }
        : d,
    });
  }

  const row = {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "8px 10px",
    borderTop: "1px solid var(--line-1)",
  } as const;

  return (
    <div style={{ ...box, marginTop: 10 }}>
      <div style={{ padding: "8px 10px", fontSize: 12, color: "var(--fg-2)" }}>
        만들 것
      </div>

      <label style={row}>
        <input
          type="checkbox"
          checked={d.reference.enabled}
          disabled={disabled}
          onChange={(e) => toggle("reference", e.target.checked)}
        />
        <span style={{ fontSize: 13, color: "var(--fg-1)", flex: 1 }}>
          자료 노트 <span style={{ color: "var(--fg-3)" }}>reference/</span>
        </span>
        <select
          value={d.reference.group ?? ""}
          disabled={disabled || !d.reference.enabled}
          onChange={(e) =>
            onChange({
              ...value,
              destinations: {
                ...d,
                reference: { enabled: d.reference.enabled, group: e.target.value },
              },
            })
          }
          className="mono"
          style={{
            fontSize: 11,
            padding: "3px 6px",
            background: "var(--bg-0)",
            color: "var(--fg-1)",
            border: "1px solid var(--line-2)",
            borderRadius: 4,
          }}
        >
          <option value="">group 선택</option>
          {groups.map((g) => (
            <option key={g} value={g}>
              {g}
            </option>
          ))}
        </select>
      </label>

      <label style={row}>
        <input
          type="checkbox"
          checked={d.concept.enabled}
          disabled={disabled}
          onChange={(e) => toggle("concept", e.target.checked)}
        />
        <span style={{ fontSize: 13, color: "var(--fg-1)", flex: 1 }}>
          개념 <span style={{ color: "var(--fg-3)" }}>permanent/concept/</span>
        </span>
      </label>

      <label style={row}>
        <input
          type="checkbox"
          checked={d.derived.enabled}
          disabled={disabled}
          onChange={(e) => toggle("derived", e.target.checked)}
        />
        <span style={{ fontSize: 13, color: "var(--fg-1)", flex: 1 }}>
          교안 <span style={{ color: "var(--fg-3)" }}>persona/contents/</span>
        </span>
      </label>

      <div style={{ ...row, gap: 8 }}>
        <span style={{ fontSize: 12, color: "var(--fg-3)", flex: 1 }}>
          아무것도 안 만든다면
        </span>
        {(
          [
            [null, "—"],
            ["inbox_hold", "보류"],
            ["discard", "폐기"],
          ] as const
        ).map(([key, label]) => (
          <button
            key={String(key)}
            type="button"
            disabled={disabled || (anyEnabled && key !== null)}
            onClick={() => setExclusive(key)}
            className="mono"
            style={{
              fontSize: 11,
              padding: "3px 9px",
              borderRadius: 4,
              cursor: disabled ? "default" : "pointer",
              border: `1px solid ${value.exclusive === key ? "var(--accent)" : "var(--line-2)"}`,
              background: value.exclusive === key ? "var(--accent-soft)" : "transparent",
              color: value.exclusive === key ? "var(--accent)" : "var(--fg-2)",
              opacity: anyEnabled && key !== null ? 0.4 : 1,
            }}
          >
            {label}
          </button>
        ))}
      </div>

      {value.exclusive === "discard" && (
        <div style={{ ...row, color: "#f85149", fontSize: 12 }}>
          승인하면 이 항목은 종료되고 아무 파일도 만들어지지 않습니다.
        </div>
      )}
    </div>
  );
}

function isNote(payload: GatePayload | null | undefined): payload is NotePayload {
  return !!payload && "filename_stem" in payload;
}

/** 노트 초안 미리보기 — 전문과 **저장될 경로**를 함께 보여준다.
 *
 * 경로를 감추면 "어디에 생기는지 모른 채 승인"하게 된다. AI 는 stem 만 내고
 * 디렉토리는 시스템이 조립하므로, 그 결과를 사람이 확인할 수 있어야 한다. */
function NotePreview({ payload }: { payload: NotePayload }) {
  const [expanded, setExpanded] = useState(false);
  const lines = payload.content.split("\n");
  const shown = expanded ? payload.content : lines.slice(0, 24).join("\n");

  return (
    <div style={{ marginTop: 10 }}>
      <div
        className="mono"
        style={{
          fontSize: 11,
          color: "var(--fg-2)",
          padding: "6px 10px",
          border: "1px solid var(--line-2)",
          borderRadius: "5px 5px 0 0",
          background: "var(--bg-0)",
          wordBreak: "break-all",
        }}
      >
        {payload.target_path ?? `${payload.filename_stem}.md`}
      </div>
      <pre
        style={{
          margin: 0,
          padding: 12,
          fontSize: 11.5,
          lineHeight: 1.6,
          color: "var(--fg-1)",
          background: "var(--bg-0)",
          border: "1px solid var(--line-2)",
          borderTop: "none",
          borderRadius: expanded || lines.length <= 24 ? "0 0 5px 5px" : 0,
          overflowX: "auto",
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
        }}
      >
        {shown}
      </pre>
      {lines.length > 24 && (
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className="mono"
          style={{
            width: "100%",
            fontSize: 10.5,
            padding: "5px 0",
            border: "1px solid var(--line-2)",
            borderTop: "none",
            borderRadius: "0 0 5px 5px",
            background: "var(--bg-1)",
            color: "var(--fg-3)",
            cursor: "pointer",
          }}
        >
          {expanded ? "접기" : `전문 보기 (${lines.length}줄)`}
        </button>
      )}
    </div>
  );
}

function FeedbackModal({
  onClose,
  onSubmit,
}: {
  onClose: () => void;
  onSubmit: (body: string) => Promise<void>;
}) {
  const [body, setBody] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    setBusy(true);
    setError(null);
    try {
      await onSubmit(body);
      onClose();
    } catch (e) {
      setError(e instanceof Error ? e.message : "재생성에 실패했습니다.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.55)",
        display: "grid",
        placeItems: "center",
        zIndex: 50,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{ ...box, width: 520, maxWidth: "92vw", padding: 18 }}
      >
        <h3 style={{ margin: 0, fontSize: 15, color: "var(--fg-0)" }}>피드백</h3>
        <p style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
          어떻게 고쳐야 하는지 적으면 새 버전을 만듭니다. 지금 버전은 그대로 남습니다.
        </p>
        <textarea
          autoFocus
          value={body}
          onChange={(e) => setBody(e.target.value)}
          rows={5}
          placeholder="예) 개념을 하나로 합쳐 달라 / 교안은 필요 없다"
          style={{
            width: "100%",
            marginTop: 10,
            padding: 10,
            fontSize: 13,
            background: "var(--bg-0)",
            color: "var(--fg-1)",
            border: "1px solid var(--line-2)",
            borderRadius: 5,
            resize: "vertical",
          }}
        />
        {error && (
          <p style={{ color: "#f85149", fontSize: 12, marginTop: 8 }}>{error}</p>
        )}
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end", marginTop: 12 }}>
          <button type="button" onClick={onClose} style={btn("ghost")}>
            취소
          </button>
          <button type="button" onClick={submit} disabled={busy} style={btn("primary")}>
            {busy ? "재생성 중…" : "재생성"}
          </button>
        </div>
      </div>
    </div>
  );
}

export function btn(kind: "primary" | "ghost" | "danger") {
  const base = {
    fontSize: 12,
    padding: "6px 14px",
    borderRadius: 5,
    cursor: "pointer",
    border: "1px solid var(--line-2)",
    background: "transparent",
    color: "var(--fg-1)",
  };
  if (kind === "primary")
    return { ...base, border: "1px solid var(--accent)", color: "var(--accent)" };
  if (kind === "danger") return { ...base, border: "1px solid #f85149", color: "#f85149" };
  return base;
}

export function GateCard({
  gate,
  groups,
  onChanged,
}: {
  gate: Gate;
  groups: string[];
  onChanged: () => void;
}) {
  const active =
    gate.revisions.find((r) => r.id === gate.active_revision_id) ??
    gate.revisions[gate.revisions.length - 1];
  const approved = gate.status === "approved";
  const [open, setOpen] = useState(!approved);
  const [draft, setDraft] = useState<RouteResult>(
    isNote(active?.payload) ? emptyRoute() : (active?.payload ?? emptyRoute()),
  );
  const [feedbackOpen, setFeedbackOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setDraft(!isNote(active?.payload) ? (active?.payload ?? emptyRoute()) : emptyRoute());
    setOpen(gate.status !== "approved");
  }, [active?.id, active?.payload, gate.status]);

  const canAct = gate.status === "review_pending" || gate.status === "feedback_pending";

  async function run(fn: () => Promise<unknown>) {
    setBusy(true);
    setError(null);
    try {
      await fn();
      onChanged();
    } catch (e) {
      setError(
        e instanceof QueueError
          ? e.code === "STALE_REVISION"
            ? "최신 상태를 다시 확인해 주세요."
            : e.message
          : "요청에 실패했습니다.",
      );
    } finally {
      setBusy(false);
    }
  }

  const failedNote =
    gate.status === "failed"
      ? "제안을 만들지 못했습니다. 재시도하면 새 실행으로 다시 만듭니다."
      : null;

  return (
    <div style={{ ...box, marginTop: 12 }}>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        style={{
          width: "100%",
          display: "flex",
          alignItems: "center",
          gap: 10,
          padding: "10px 12px",
          background: "transparent",
          border: "none",
          cursor: "pointer",
          textAlign: "left",
        }}
      >
        <span className="mono" style={{ fontSize: 11, color: "var(--fg-4)" }}>
          {gate.stage_no}
        </span>
        <span style={{ fontSize: 14, color: "var(--fg-0)", flex: 1 }}>
          {STAGE_LABEL[gate.stage_name] ?? gate.stage_name}
        </span>
        {active && (
          <span className="mono" style={{ fontSize: 10, color: "var(--fg-4)" }}>
            v{active.version}
          </span>
        )}
        <Badge status={gate.status} />
      </button>

      {open && (
        <div style={{ padding: "0 12px 12px" }}>
          {failedNote && (
            <p style={{ fontSize: 12, color: "#f85149", margin: "4px 0 10px" }}>{failedNote}</p>
          )}

          {!isNote(active?.payload) && active?.payload?.rationale && (
            <p
              style={{
                fontSize: 12.5,
                color: "var(--fg-2)",
                lineHeight: 1.6,
                margin: 0,
                whiteSpace: "pre-wrap",
              }}
            >
              {active.payload.rationale}
            </p>
          )}

          {gate.stage_name === "route" && active?.payload && !isNote(active.payload) && (
            <RouteEditor
              value={draft}
              groups={groups}
              disabled={!canAct || busy}
              onChange={setDraft}
            />
          )}

          {isNote(active?.payload) && <NotePreview payload={active.payload} />}

          {gate.revisions.length > 1 && (
            <p className="mono" style={{ fontSize: 10.5, color: "var(--fg-4)", marginTop: 8 }}>
              이전 버전 {gate.revisions.length - 1}개는 읽기 전용으로 남아 있습니다.
            </p>
          )}

          {error && <p style={{ color: "#f85149", fontSize: 12, marginTop: 8 }}>{error}</p>}

          <div style={{ display: "flex", gap: 8, justifyContent: "flex-end", marginTop: 12 }}>
            {gate.status === "failed" && (
              <button
                type="button"
                disabled={busy}
                onClick={() => run(() => queueApi.retryGate(gate.id))}
                style={btn("ghost")}
              >
                재시도
              </button>
            )}
            {canAct && (
              <>
                <button
                  type="button"
                  disabled={busy}
                  onClick={() => setFeedbackOpen(true)}
                  style={btn("ghost")}
                >
                  피드백
                </button>
                <button
                  type="button"
                  disabled={busy}
                  onClick={() =>
                    run(() =>
                      queueApi.approve(
                        gate.id,
                        gate.stage_name === "route" ? draft : null,
                        active?.id ?? null,
                      ),
                    )
                  }
                  style={btn(draft.exclusive === "discard" ? "danger" : "primary")}
                >
                  {draft.exclusive === "discard" ? "폐기 승인" : "승인"}
                </button>
              </>
            )}
          </div>
        </div>
      )}

      {feedbackOpen && (
        <FeedbackModal
          onClose={() => setFeedbackOpen(false)}
          onSubmit={async (body) => {
            await queueApi.feedback(gate.id, body);
            await queueApi.regenerate(gate.id);
            onChanged();
          }}
        />
      )}
    </div>
  );
}
