"use client";

import { useCallback, useEffect, useState } from "react";
import { GateCard, btn } from "@/components/admin/queue-gate";
import {
  QueueError,
  queueApi,
  type Gate,
  type QueueItem,
  type QueueItemDetail,
} from "@/lib/api";

/* 승인 큐 — KDEV-SPEC-007 U-1~U-3 / WORK-014 P4.
 *
 * 좌: 상태별로 묶인 목록. 우: 선택 항목의 준비 상태 + 게이트 스택.
 *
 * **실패가 눈에 띄어야 한다.** 조용히 묻히면 승인한 게 사라진 줄도 모른다.
 */

const STATUS_META: Record<string, { label: string; tone: string; order: number }> = {
  prepare_failed: { label: "준비 실패", tone: "#f85149", order: 0 },
  publish_failed: { label: "발행 실패", tone: "#f85149", order: 1 },
  in_review: { label: "검토 대기", tone: "var(--accent)", order: 2 },
  received: { label: "접수됨", tone: "var(--fg-2)", order: 3 },
  preparing: { label: "준비 중", tone: "var(--fg-2)", order: 4 },
  publishing: { label: "발행 중", tone: "var(--fg-2)", order: 5 },
};

const box = {
  border: "1px solid var(--line-2)",
  borderRadius: 6,
  background: "var(--bg-1)",
};

function statusMeta(status: string) {
  return STATUS_META[status] ?? { label: status, tone: "var(--fg-3)", order: 9 };
}

function AddModal({ onClose, onDone }: { onClose: () => void; onDone: () => void }) {
  const [url, setUrl] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [duplicate, setDuplicate] = useState<number | null>(null);

  async function submit(allowRepublish = false) {
    setBusy(true);
    setError(null);
    try {
      await queueApi.create({
        source_url: url.trim() || null,
        note: note.trim() || null,
        allow_republish: allowRepublish,
      });
      onDone();
      onClose();
    } catch (e) {
      if (e instanceof QueueError && e.code === "DUPLICATE_PUBLISHED") {
        // 막지 않는다 — 같은 자료의 재정리가 정당한 경우가 있다(S-4).
        const detail = e.detail as { existing_item_id?: number } | undefined;
        setDuplicate(detail?.existing_item_id ?? 0);
      } else {
        setError(e instanceof Error ? e.message : "저장에 실패했습니다.");
      }
    } finally {
      setBusy(false);
    }
  }

  const field = {
    width: "100%",
    padding: 9,
    fontSize: 13,
    background: "var(--bg-0)",
    color: "var(--fg-1)",
    border: "1px solid var(--line-2)",
    borderRadius: 5,
    marginTop: 6,
  } as const;

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
        <h3 style={{ margin: 0, fontSize: 15, color: "var(--fg-0)" }}>항목 추가</h3>

        <label style={{ display: "block", marginTop: 14, fontSize: 12, color: "var(--fg-2)" }}>
          URL
          <input
            autoFocus
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://youtu.be/..."
            style={field}
          />
        </label>

        <label style={{ display: "block", marginTop: 12, fontSize: 12, color: "var(--fg-2)" }}>
          메모
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            rows={4}
            placeholder="왜 남기는지, 어디에 쓸 생각인지"
            style={{ ...field, resize: "vertical" }}
          />
          <span style={{ fontSize: 11, color: "var(--fg-4)" }}>
            메모는 항상 요약에 함께 넘어갑니다. 원문 수집이 막히면 <b>원문 대신</b> 쓰입니다.
          </span>
        </label>

        {duplicate !== null && (
          <div
            style={{
              marginTop: 12,
              padding: 10,
              border: "1px solid var(--accent)",
              borderRadius: 5,
              fontSize: 12,
              color: "var(--fg-1)",
            }}
          >
            이미 발행된 자료입니다{duplicate ? ` (항목 #${duplicate})` : ""}. 새로 진행할까요?
            <div style={{ display: "flex", gap: 8, marginTop: 10, justifyContent: "flex-end" }}>
              <button type="button" onClick={onClose} style={btn("ghost")}>
                취소
              </button>
              <button type="button" onClick={() => submit(true)} style={btn("primary")}>
                새로 진행
              </button>
            </div>
          </div>
        )}

        {error && <p style={{ color: "#f85149", fontSize: 12, marginTop: 10 }}>{error}</p>}

        {duplicate === null && (
          <div style={{ display: "flex", gap: 8, justifyContent: "flex-end", marginTop: 14 }}>
            <button type="button" onClick={onClose} style={btn("ghost")}>
              취소
            </button>
            <button
              type="button"
              disabled={busy || (!url.trim() && !note.trim())}
              onClick={() => submit(false)}
              style={btn("primary")}
            >
              {busy ? "저장 중…" : "저장"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

function Detail({
  item,
  gates,
  groups,
  onChanged,
}: {
  item: QueueItemDetail;
  gates: Gate[];
  groups: string[];
  onChanged: () => void;
}) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [note, setNote] = useState(item.note ?? "");

  useEffect(() => setNote(item.note ?? ""), [item.id, item.note]);

  const lastPrep = item.preparations[item.preparations.length - 1];
  const failedTasks = item.ai_tasks.filter((t) => t.status === "failed");

  async function run(fn: () => Promise<unknown>) {
    setBusy(true);
    setError(null);
    try {
      await fn();
      onChanged();
    } catch (e) {
      setError(e instanceof Error ? e.message : "요청에 실패했습니다.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div style={{ flex: 1, minWidth: 0, padding: "4px 4px 40px" }}>
      <header style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
        <span className="mono" style={{ fontSize: 11, color: "var(--fg-4)" }}>
          #{item.id}
        </span>
        <h2 style={{ margin: 0, fontSize: 17, color: "var(--fg-0)", wordBreak: "break-all" }}>
          {item.source_url ?? "(URL 없음 — 메모 항목)"}
        </h2>
      </header>
      <p className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginTop: 6 }}>
        {item.source_kind} · {item.channel} ·{" "}
        {item.submitted_at ? new Date(item.submitted_at).toLocaleString("ko-KR") : "—"}
        {item.submitted_by ? ` · ${item.submitted_by}` : ""}
      </p>

      {/* 메모 */}
      <div style={{ ...box, marginTop: 14, padding: 12 }}>
        <div style={{ fontSize: 12, color: "var(--fg-2)", marginBottom: 6 }}>메모</div>
        <textarea
          value={note}
          onChange={(e) => setNote(e.target.value)}
          rows={3}
          style={{
            width: "100%",
            padding: 9,
            fontSize: 13,
            background: "var(--bg-0)",
            color: "var(--fg-1)",
            border: "1px solid var(--line-2)",
            borderRadius: 5,
            resize: "vertical",
          }}
        />
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end", marginTop: 8 }}>
          <button
            type="button"
            disabled={busy || note === (item.note ?? "")}
            onClick={() => run(() => queueApi.updateNote(item.id, note))}
            style={btn("ghost")}
          >
            메모 저장
          </button>
          {(item.status === "prepare_failed" || item.status === "received") && (
            <button
              type="button"
              disabled={busy}
              onClick={() => run(() => queueApi.retryPrepare(item.id))}
              style={btn("primary")}
            >
              준비 재시도
            </button>
          )}
        </div>
      </div>

      {/* 준비 상태 */}
      <div style={{ ...box, marginTop: 12, padding: 12 }}>
        <div style={{ fontSize: 12, color: "var(--fg-2)" }}>자동 준비 (수집 → 요약)</div>
        {!lastPrep && (
          <p style={{ fontSize: 12.5, color: "var(--fg-3)", margin: "8px 0 0" }}>
            아직 준비가 실행되지 않았습니다.
          </p>
        )}
        {lastPrep && (
          <>
            <p className="mono" style={{ fontSize: 10.5, color: "var(--fg-4)", margin: "6px 0" }}>
              v{lastPrep.version} · {lastPrep.status}
              {typeof lastPrep.payload?.material_source === "string" && (
                <>
                  {" · 근거: "}
                  {lastPrep.payload.material_source === "note"
                    ? "메모 (원문 수집 실패)"
                    : "원문"}
                </>
              )}
            </p>
            {typeof lastPrep.payload?.summary === "string" && (
              <p
                style={{
                  fontSize: 12.5,
                  color: "var(--fg-2)",
                  lineHeight: 1.65,
                  whiteSpace: "pre-wrap",
                  margin: 0,
                }}
              >
                {lastPrep.payload.summary}
              </p>
            )}
            {typeof lastPrep.payload?.error_message === "string" && (
              <p style={{ fontSize: 12.5, color: "#f85149", margin: 0 }}>
                {lastPrep.payload.error_message}
              </p>
            )}
          </>
        )}
      </div>

      {/* 실패 이력 — 재시도 판단의 근거라 감추지 않는다. */}
      {failedTasks.length > 0 && (
        <div style={{ ...box, marginTop: 12, padding: 12 }}>
          <div style={{ fontSize: 12, color: "#f85149" }}>실패한 실행 {failedTasks.length}건</div>
          {failedTasks.map((t) => (
            <p
              key={t.id}
              className="mono"
              style={{ fontSize: 11, color: "var(--fg-3)", margin: "6px 0 0" }}
            >
              {t.kind} · {t.error_code} · {t.error_message?.slice(0, 160)}
            </p>
          ))}
        </div>
      )}

      {error && <p style={{ color: "#f85149", fontSize: 12, marginTop: 10 }}>{error}</p>}

      {/* 게이트 스택 */}
      <h3 style={{ fontSize: 13, color: "var(--fg-2)", margin: "22px 0 0" }}>승인 게이트</h3>
      {gates.length === 0 && (
        <p style={{ fontSize: 12.5, color: "var(--fg-3)", marginTop: 8 }}>
          아직 게이트가 없습니다. 준비가 끝나면 목적지 게이트가 열립니다.
        </p>
      )}
      {gates.map((g) => (
        <GateCard key={g.id} gate={g} itemId={item.id} groups={groups} onChanged={onChanged} />
      ))}

      <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 24 }}>
        <button
          type="button"
          disabled={busy || item.status === "publishing"}
          onClick={() => run(() => queueApi.remove(item.id))}
          style={btn("danger")}
        >
          삭제
        </button>
      </div>
    </div>
  );
}

export default function QueuePage() {
  const [items, setItems] = useState<QueueItem[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [detail, setDetail] = useState<QueueItemDetail | null>(null);
  const [gates, setGates] = useState<Gate[]>([]);
  const [groups, setGroups] = useState<string[]>([]);
  const [adding, setAdding] = useState(false);
  const [loading, setLoading] = useState(true);

  const reloadList = useCallback(async () => {
    const { items } = await queueApi.list();
    setItems(items);
    setLoading(false);
    return items;
  }, []);

  const reloadDetail = useCallback(async (id: number) => {
    const [d, g] = await Promise.all([queueApi.detail(id), queueApi.gates(id)]);
    setDetail(d);
    setGates(g.gates);
  }, []);

  useEffect(() => {
    queueApi.meta().then((m) => setGroups(m.reference_groups)).catch(() => setGroups([]));
    reloadList().catch(() => setLoading(false));
  }, [reloadList]);

  useEffect(() => {
    if (selected === null) {
      setDetail(null);
      setGates([]);
      return;
    }
    reloadDetail(selected).catch(() => setDetail(null));
  }, [selected, reloadDetail]);

  const onChanged = useCallback(async () => {
    const fresh = await reloadList();
    if (selected !== null) {
      // 승인·삭제로 목록에서 빠졌으면 상세를 닫는다.
      if (!fresh.some((i) => i.id === selected)) setSelected(null);
      else await reloadDetail(selected);
    }
  }, [reloadList, reloadDetail, selected]);

  const grouped = [...items].sort(
    (a, b) => statusMeta(a.status).order - statusMeta(b.status).order,
  );

  return (
    <div style={{ padding: "28px 32px", maxWidth: 1180, margin: "0 auto" }}>
      <header style={{ display: "flex", alignItems: "center", marginBottom: 20 }}>
        <div style={{ flex: 1 }}>
          <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>승인 큐</h1>
          <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
            승인 전에는 레포에 아무것도 쓰이지 않습니다.
          </p>
        </div>
        <button type="button" onClick={() => setAdding(true)} style={btn("primary")}>
          항목 추가
        </button>
      </header>

      <div style={{ display: "flex", gap: 20, alignItems: "flex-start" }}>
        {/* 목록 */}
        <div style={{ width: 320, flexShrink: 0 }}>
          {loading && (
            <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
              불러오는 중…
            </p>
          )}
          {!loading && grouped.length === 0 && (
            <div
              style={{
                border: "1px dashed var(--line-2)",
                borderRadius: 8,
                padding: 28,
                textAlign: "center",
                color: "var(--fg-3)",
                fontSize: 12.5,
              }}
            >
              비어 있습니다.
              <br />
              Slack에 링크를 던지거나 항목을 추가하세요.
            </div>
          )}
          {grouped.map((item) => {
            const meta = statusMeta(item.status);
            const active = item.id === selected;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => setSelected(item.id)}
                style={{
                  display: "block",
                  width: "100%",
                  textAlign: "left",
                  marginBottom: 8,
                  padding: "10px 12px",
                  borderRadius: 6,
                  cursor: "pointer",
                  background: active ? "var(--bg-3)" : "var(--bg-1)",
                  border: `1px solid ${active ? "var(--accent)" : "var(--line-2)"}`,
                  borderLeft: `3px solid ${meta.tone}`,
                }}
              >
                <div
                  style={{
                    fontSize: 12.5,
                    color: "var(--fg-1)",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}
                >
                  {item.source_url ?? item.note ?? "(제목 없음)"}
                </div>
                <div
                  className="mono"
                  style={{ fontSize: 10, color: meta.tone, marginTop: 5 }}
                >
                  {meta.label} · {item.source_kind}
                </div>
              </button>
            );
          })}
        </div>

        {/* 상세 */}
        {detail ? (
          <Detail item={detail} gates={gates} groups={groups} onChanged={onChanged} />
        ) : (
          <div
            style={{
              flex: 1,
              border: "1px dashed var(--line-2)",
              borderRadius: 8,
              padding: 60,
              textAlign: "center",
              color: "var(--fg-3)",
              fontSize: 13,
            }}
          >
            왼쪽에서 항목을 선택하세요.
          </div>
        )}
      </div>

      {adding && <AddModal onClose={() => setAdding(false)} onDone={reloadList} />}
    </div>
  );
}
