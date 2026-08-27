"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import { GateDetail, GateHistory } from "@/components/admin/gate-detail";
import type { AdminGateItem, AdminQueueItem, QueueKind, QueueStatus } from "@/lib/types";

// 수집함 · 인박스 — 케이스 1(2026-08-25 개정): 넣는 곳·보는 곳·승인하는 곳이 한 페이지다.
// 문서는 자동 착지라 사람이 승인하는 것은 개념 게이트 하나다. 행 펼침:
// review → 개념 승인/거절 UI(또는 문서 푸시 실패의 [재시도]) · done → 읽기 전용
// 이력 · failed → error + 재시도. 펼침은 한 번에 하나.
// queued·processing 이 있는 동안만 폴링해 상태를 따라간다.

/** 모달의 종류 세그먼트 — book·session 은 비활성 자리만(v1 구멍, 케이스 1). */
const KIND_SEGMENTS: { kind: string; enabled: boolean }[] = [
  { kind: "youtube", enabled: true },
  { kind: "docs", enabled: true },
  { kind: "article", enabled: true },
  { kind: "blog", enabled: true },
  { kind: "book", enabled: false },
  { kind: "session", enabled: false },
];

/** 종류를 고를 때마다 URL 칸의 문구가 바뀐다 — inbox.md Step 1 의 표 그대로. */
const URL_PLACEHOLDER: Record<QueueKind, string> = {
  youtube: "유튜브 링크를 넣는다",
  docs: "공식 문서 링크를 넣는다",
  article: "기사 링크를 넣는다",
  blog: "블로그 글 링크를 넣는다",
};

const STATUS_COLOR: Record<QueueStatus, string> = {
  queued: "var(--fg-3)",
  processing: "var(--info)",
  review: "var(--accent)",
  done: "var(--fg-4)",
  failed: "var(--danger, #e5534b)",
};

const STATUS_ORDER: QueueStatus[] = ["queued", "processing", "review", "done", "failed"];

const POLL_MS = 3000;

export default function AdminCapturePage() {
  const [items, setItems] = useState<AdminQueueItem[] | null>(null);
  const [counts, setCounts] = useState<Record<string, number>>({});
  const [gates, setGates] = useState<AdminGateItem[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [gateError, setGateError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  // 펼친 행 — queue id. 한 번에 하나만 연다(다른 행을 열면 이전 것은 접힌다).
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const reload = useCallback(() => {
    adminApi
      .queue()
      .then(({ items, counts }) => {
        setItems(items);
        setCounts(counts);
        setLoadError(null);
      })
      .catch((e) => setLoadError(String(e)));
    // 게이트 목록 — 닫힌 것 포함 전체(scope=all). queueId 로 행에 붙여
    // review 는 승인 UI 를, done 은 읽기 전용 이력을 그린다(2026-08-25 개정).
    adminApi
      .gates("all")
      .then(({ items }) => {
        setGates(items);
        setGateError(null);
      })
      .catch((e) => setGateError(String(e)));
  }, []);

  useEffect(reload, [reload]);

  // queue 행 → 그 행의 게이트 전부(document 자동 착지 기록 + concept). 생성 순서대로 온다.
  const gatesByQueue = useMemo(() => {
    const map = new Map<number, AdminGateItem[]>();
    for (const g of gates) {
      const list = map.get(g.queueId);
      if (list) list.push(g);
      else map.set(g.queueId, [g]);
    }
    return map;
  }, [gates]);

  // queued·processing 이 있는 동안만 폴링한다. 없으면 가만히 있는다(inbox.md Step 2).
  const inFlight = (items ?? []).some(
    (i) => i.status === "queued" || i.status === "processing",
  );
  useEffect(() => {
    if (!inFlight) return;
    const timer = window.setInterval(reload, POLL_MS);
    return () => window.clearInterval(timer);
  }, [inFlight, reload]);

  return (
    <div className="admin-page" style={{ padding: "28px 32px", maxWidth: 960, margin: "0 auto" }}>
      <header
        style={{
          marginBottom: 24,
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "space-between",
          gap: 16,
          flexWrap: "wrap",
        }}
      >
        <div>
          <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>인박스</h1>
          <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
            {items
              ? STATUS_ORDER.map((s) => `${s} ${counts[s] ?? 0}`).join(" · ")
              : "케이스 1 — 넣고 · 보고 · 승인하는 곳이 한 페이지"}
          </p>
        </div>
        <button type="button" onClick={() => setModalOpen(true)} style={primaryBtn(true)}>
          + 인박스
        </button>
      </header>

      {modalOpen && (
        <InboxModal
          onDone={() => {
            setModalOpen(false);
            reload();
          }}
          onCancel={() => setModalOpen(false)}
        />
      )}

      {loadError && (
        <p className="mono" style={{ fontSize: 12, color: "var(--danger, #e5534b)" }}>
          인박스를 불러오지 못했습니다 — {loadError}
        </p>
      )}
      {gateError && (
        <p className="mono" style={{ fontSize: 12, color: "var(--danger, #e5534b)" }}>
          게이트 목록을 불러오지 못했습니다 — {gateError}
        </p>
      )}
      {notice && (
        <p className="mono" style={{ fontSize: 12, color: "var(--accent)", marginBottom: 12 }}>
          {notice}
        </p>
      )}

      {!items && !loadError && (
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          불러오는 중…
        </p>
      )}

      {items && items.length === 0 && (
        <div
          style={{
            border: "1px dashed var(--line-2)",
            borderRadius: 8,
            padding: 48,
            textAlign: "center",
            color: "var(--fg-3)",
          }}
        >
          <p style={{ fontSize: 15, color: "var(--fg-1)", margin: 0 }}>비어 있다</p>
          <p className="mono" style={{ fontSize: 12, marginTop: 8 }}>
            밖에서 본 것을 「+ 인박스」로 넣는다
          </p>
        </div>
      )}

      {items && items.length > 0 && (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {items.map((item) => (
            <QueueRow
              key={item.id}
              item={item}
              gates={gatesByQueue.get(item.id) ?? []}
              expanded={expandedId === item.id}
              onToggle={() => setExpandedId(expandedId === item.id ? null : item.id)}
              onChanged={reload}
              onGateDone={(msg) => {
                setNotice(msg);
                setExpandedId(null);
                reload();
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
}

/* ── 목록 한 행 — 넣은 것 그대로: 종류·URL·메모·상태·error ───────────────
 * 게이트가 붙은 행은 클릭하면 행 바로 아래로 펼쳐진다(한 번에 하나) —
 * review 는 개념 승인 UI(또는 푸시 실패 [재시도]), done 은 읽기 전용 이력. */

function QueueRow({
  item,
  gates,
  expanded,
  onToggle,
  onChanged,
  onGateDone,
}: {
  item: AdminQueueItem;
  gates: AdminGateItem[];
  expanded: boolean;
  onToggle: () => void;
  onChanged: () => void;
  onGateDone: (msg: string) => void;
}) {
  const [retrying, setRetrying] = useState(false);
  const [retryError, setRetryError] = useState<string | null>(null);

  const expandable = gates.length > 0;
  // 사람 손이 필요한 게이트 — 열린 개념 게이트, 또는 「승인됨·푸시 실패」
  // (approved + commitRef·result 둘 다 없음 — 개념 0건 승인은 result 만 있다).
  const openGate = gates.find((g) => g.status === "open") ?? null;
  const pushFailedGate =
    gates.find((g) => g.status === "approved" && !g.commitRef && !g.result) ?? null;
  const pushFailed = pushFailedGate !== null;
  const actionGate = pushFailedGate ?? openGate;

  async function retry() {
    setRetrying(true);
    setRetryError(null);
    try {
      await adminApi.retryQueueItem(item.id);
      onChanged();
    } catch (e) {
      setRetryError(e instanceof AuthError ? e.message : String(e));
    } finally {
      setRetrying(false);
    }
  }

  return (
    <div style={{ ...card, borderColor: expanded ? "var(--accent)" : "var(--line-1)" }}>
      <div
        onClick={expandable ? onToggle : undefined}
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          flexWrap: "wrap",
          cursor: expandable ? "pointer" : "default",
        }}
      >
        <span
          className="mono"
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 6,
            fontSize: 11,
            color: STATUS_COLOR[item.status] ?? "var(--fg-3)",
            minWidth: 92,
          }}
        >
          <span
            style={{
              width: 7,
              height: 7,
              borderRadius: "50%",
              background: STATUS_COLOR[item.status] ?? "var(--fg-3)",
            }}
          />
          {item.status}
        </span>
        <span className="mono" style={{ fontSize: 11, color: "var(--fg-2)", minWidth: 56 }}>
          {item.kind}
        </span>
        <span
          className="mono"
          style={{
            fontSize: 12,
            color: "var(--fg-1)",
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
            flex: 1,
            minWidth: 120,
          }}
          title={item.sourceUrl ?? undefined}
        >
          {item.sourceUrl}
        </span>
        <span style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 8 }}>
          {expandable && (
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                onToggle();
              }}
              style={{
                ...ghostBtn,
                color: pushFailed
                  ? "var(--danger, #e5534b)"
                  : openGate
                    ? "var(--accent)"
                    : "var(--fg-3)",
              }}
            >
              {(pushFailed ? "재시도 " : openGate ? "승인 " : "이력 ") +
                (expanded ? "▴" : "▾")}
            </button>
          )}
          {item.status === "failed" && (
            <button type="button" onClick={retry} disabled={retrying} style={ghostBtn}>
              {retrying ? "재시도 중…" : "재시도"}
            </button>
          )}
        </span>
      </div>

      {item.note && (
        <p className="mono" style={{ fontSize: 11, color: "var(--fg-3)", margin: "8px 0 0" }}>
          메모: {item.note}
        </p>
      )}
      {item.status === "failed" && item.error && (
        <p
          className="mono"
          style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "8px 0 0" }}
        >
          error: {item.error}
        </p>
      )}
      {retryError && (
        <p
          className="mono"
          style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "8px 0 0" }}
        >
          재시도 실패 — {retryError}
        </p>
      )}

      {/* 행 펼침 — 손 댈 게이트가 있으면 그 상세(승인·재시도), 없으면 읽기 전용 이력.
       * key=gate.id 로 다른 게이트로 바뀌면 폼을 새로 그린다. */}
      {expanded && actionGate && (
        <div style={{ marginTop: 12 }}>
          <GateDetail key={actionGate.id} gate={actionGate} onDone={onGateDone} />
        </div>
      )}
      {expanded && !actionGate && expandable && (
        <div style={{ marginTop: 12 }}>
          <GateHistory gates={gates} />
        </div>
      )}
    </div>
  );
}

/* ── 인박스 모달 — 종류(사람이 고른다) + URL(필수) + 메모(선택) ────────── */

function InboxModal({ onDone, onCancel }: { onDone: () => void; onCancel: () => void }) {
  const [kind, setKind] = useState<QueueKind>("youtube");
  const [url, setUrl] = useState("");
  const [note, setNote] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const urlRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    urlRef.current?.focus();
  }, [kind]);

  async function submit() {
    // 검증은 「비었나」 정도만 — fallback 안 쌓는다(inbox.md 정책). 중복도 안 막는다.
    if (!url.trim()) {
      setError("URL 이 비었습니다");
      return;
    }
    setSaving(true);
    setError(null);
    try {
      await adminApi.createQueueItem({
        kind,
        sourceUrl: url.trim(),
        ...(note.trim() ? { note: note.trim() } : {}),
      });
      onDone();
    } catch (e) {
      setError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
      setSaving(false);
    }
  }

  return (
    <div
      onClick={onCancel}
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 50,
        background: "rgba(0, 0, 0, 0.55)",
        display: "flex",
        alignItems: "flex-start",
        justifyContent: "center",
        padding: "10vh 16px 16px",
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          width: "100%",
          maxWidth: 520,
          background: "var(--bg-1)",
          border: "1px solid var(--line-2)",
          borderRadius: 10,
          boxShadow: "var(--shadow-pop)",
        }}
      >
        {/* 머리 */}
        <div
          style={{
            display: "flex",
            alignItems: "baseline",
            gap: 10,
            padding: "16px 20px",
            borderBottom: "1px solid var(--line-1)",
          }}
        >
          <span style={{ fontSize: 15, color: "var(--fg-0)", fontWeight: 600 }}>인박스</span>
          <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
            밖에서 본 것을 넣는다
          </span>
          <button
            type="button"
            onClick={onCancel}
            aria-label="닫기"
            style={{
              marginLeft: "auto",
              background: "transparent",
              border: "none",
              color: "var(--fg-3)",
              fontSize: 14,
              cursor: "pointer",
              padding: 2,
            }}
          >
            ✕
          </button>
        </div>

        <div style={{ padding: "16px 20px" }}>
          {/* 종류 — 사람이 고른다. 분류를 AI 에 안 맡긴다(케이스 1 결정). */}
          <span className="mono" style={fieldLabel}>
            종류
          </span>
          <div
            style={{
              display: "flex",
              border: "1px solid var(--line-2)",
              borderRadius: 6,
              overflow: "hidden",
              marginTop: 4,
            }}
          >
            {KIND_SEGMENTS.map(({ kind: k, enabled }, i) => {
              const active = enabled && kind === k;
              return (
                <button
                  key={k}
                  type="button"
                  disabled={!enabled}
                  title={enabled ? undefined : "준비 중"}
                  onClick={() => enabled && setKind(k as QueueKind)}
                  className="mono"
                  style={{
                    flex: 1,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    gap: 1,
                    padding: "7px 2px",
                    fontSize: 10,
                    border: "none",
                    borderLeft: i > 0 ? "1px solid var(--line-1)" : "none",
                    background: active ? "var(--fg-0)" : "transparent",
                    color: active ? "var(--bg-0)" : enabled ? "var(--fg-2)" : "var(--fg-4)",
                    cursor: enabled ? "pointer" : "default",
                  }}
                >
                  {k}
                  {!enabled && (
                    <span style={{ fontSize: 8, letterSpacing: "0.08em", color: "var(--fg-4)" }}>
                      soon
                    </span>
                  )}
                </button>
              );
            })}
          </div>

          {/* URL — 필수는 이것 하나. placeholder 는 고른 종류를 따라 바뀐다. */}
          <label style={{ display: "block", marginTop: 14 }}>
            <span className="mono" style={fieldLabel}>
              URL
            </span>
            <input
              ref={urlRef}
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") submit();
              }}
              placeholder={URL_PLACEHOLDER[kind]}
              style={input}
            />
          </label>

          {/* 메모 — 선택. 왜 잡아뒀는지 한 줄. */}
          <label style={{ display: "block", marginTop: 14 }}>
            <span className="mono" style={fieldLabel}>
              메모 · 선택
            </span>
            <textarea
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="왜 잡아뒀는지 한 줄"
              rows={2}
              style={{ ...input, resize: "vertical" }}
            />
          </label>

          {error && (
            <p
              className="mono"
              style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "10px 0 0" }}
            >
              {error}
            </p>
          )}
        </div>

        {/* 발 */}
        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            gap: 10,
            padding: "14px 20px",
            borderTop: "1px solid var(--line-1)",
          }}
        >
          <button type="button" onClick={onCancel} style={ghostBtn}>
            취소
          </button>
          <button type="button" onClick={submit} disabled={saving} style={primaryBtn(true)}>
            {saving ? "넣는 중…" : "넣기"}
          </button>
        </div>
      </div>
    </div>
  );
}

/* ── 스타일 조각 ────────────────────────────────────────────────────── */

const card: React.CSSProperties = {
  border: "1px solid var(--line-1)",
  borderRadius: 8,
  padding: "12px 16px",
  background: "var(--bg-1)",
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

function primaryBtn(active: boolean): React.CSSProperties {
  return {
    fontSize: 11,
    fontFamily: "var(--font-mono)",
    padding: "6px 14px",
    borderRadius: 5,
    border: "1px solid var(--line-2)",
    background: active ? "var(--fg-0)" : "var(--bg-2)",
    color: active ? "var(--bg-0)" : "var(--fg-2)",
    cursor: "pointer",
  };
}
