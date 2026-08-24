"use client";

import { useCallback, useEffect, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import type { AdminEducation, EducationInput } from "@/lib/types";

// 커리어 · 교육 — 등록·수정·삭제. isCurrent·period 는 백엔드 파생값이라
// 여기선 읽기 전용 표시다 — 재계산하지 않는다(lib/types.ts 규약).
export default function AdminEducationPage() {
  const [items, setItems] = useState<AdminEducation[] | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [adding, setAdding] = useState(false);

  const reload = useCallback(() => {
    adminApi
      .education()
      .then(({ items }) => setItems(items))
      .catch((e) => setLoadError(String(e)));
  }, []);

  useEffect(() => {
    reload();
  }, [reload]);

  if (loadError) {
    return (
      <div className="admin-page" style={{ padding: "28px 32px" }}>
        <p className="mono" style={{ fontSize: 12, color: "var(--danger, #e5534b)" }}>
          교육 목록을 불러오지 못했습니다 — {loadError}
        </p>
      </div>
    );
  }

  if (!items) {
    return (
      <div className="admin-page" style={{ padding: "28px 32px" }}>
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          불러오는 중…
        </p>
      </div>
    );
  }

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
          <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>교육</h1>
          <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
            education — 한 행 = 교육과정 하나. 부트캠프·학력
          </p>
        </div>
        <button type="button" onClick={() => setAdding((a) => !a)} style={primaryBtn(!adding)}>
          {adding ? "닫기" : "+ 교육 추가"}
        </button>
      </header>

      {adding && (
        <EducationForm
          onDone={() => {
            setAdding(false);
            reload();
          }}
          onCancel={() => setAdding(false)}
        />
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {items.map((e) => (
          <EducationCard key={e.id} education={e} onChanged={reload} />
        ))}
      </div>
    </div>
  );
}

/* ── 카드 ───────────────────────────────────────────────────────────── */

function EducationCard({
  education,
  onChanged,
}: {
  education: AdminEducation;
  onChanged: () => void;
}) {
  const [editing, setEditing] = useState(false);
  const [deleteError, setDeleteError] = useState<string | null>(null);

  async function remove() {
    if (!window.confirm(`「${education.org} — ${education.title}」 을(를) 삭제할까요?`)) return;
    try {
      await adminApi.deleteEducation(education.id);
      onChanged();
    } catch (e) {
      setDeleteError(e instanceof AuthError ? e.message : String(e));
    }
  }

  if (editing) {
    return (
      <EducationForm
        education={education}
        onDone={() => {
          setEditing(false);
          onChanged();
        }}
        onCancel={() => setEditing(false)}
      />
    );
  }

  return (
    <div style={card}>
      <div style={{ display: "flex", alignItems: "baseline", gap: 12, flexWrap: "wrap" }}>
        <div style={{ minWidth: 0 }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 8, flexWrap: "wrap" }}>
            <span style={{ fontSize: 15, color: "var(--fg-0)", fontWeight: 600 }}>
              {education.title}
            </span>
            <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
              {education.org}
            </span>
          </div>
          <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginTop: 2 }}>
            {/* period 는 백엔드 렌더 — 진행 중이면 「현재」만 강조한다. */}
            {education.isCurrent ? (
              <>
                {education.period.replace(/현재$/, "")}
                <span style={{ color: "var(--accent)", fontWeight: 600 }}>현재</span>
              </>
            ) : (
              education.period
            )}
            {education.location && <> · {education.location}</>}
          </div>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 8 }}>
          <button type="button" onClick={() => setEditing(true)} style={ghostBtn}>
            수정
          </button>
          <button
            type="button"
            onClick={remove}
            style={{ ...ghostBtn, color: "var(--danger, #e5534b)" }}
          >
            삭제
          </button>
        </div>
      </div>

      {education.summary && (
        <p style={{ fontSize: 13, color: "var(--fg-2)", lineHeight: 1.6, margin: "10px 0 0" }}>
          {education.summary}
        </p>
      )}
      {education.stack.length > 0 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 10 }}>
          {education.stack.map((s) => (
            <span
              key={s}
              className="mono"
              style={{
                fontSize: 10,
                letterSpacing: "0.04em",
                color: "var(--fg-2)",
                border: "1px solid var(--line-1)",
                borderRadius: 4,
                padding: "2px 7px",
                background: "var(--bg-2)",
              }}
            >
              {s}
            </span>
          ))}
        </div>
      )}
      {deleteError && (
        <p className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "8px 0 0" }}>
          {deleteError}
        </p>
      )}
    </div>
  );
}

/* ── 폼 — 등록·수정 겸용 ────────────────────────────────────────────── */

type Draft = {
  org: string;
  title: string;
  location: string;
  startedMonth: string; // input type="month" — YYYY-MM
  endedMonth: string;   // "" = 현재
  summary: string;
  detailPath: string;   // "" = 상세 없음
  stack: string;        // 콤마 구분
};

/** date 컬럼은 YYYY-MM-DD, 입력은 월 단위 — 잘라서 채우고 붙여서 보낸다. */
const toMonth = (d?: string | null) => (d ? d.slice(0, 7) : "");
const toDate = (m: string) => `${m}-01`;
const parseStack = (s: string) =>
  s.split(",").map((t) => t.trim()).filter(Boolean);

function EducationForm({
  education,
  onDone,
  onCancel,
}: {
  education?: AdminEducation;
  onDone: () => void;
  onCancel: () => void;
}) {
  const [draft, setDraft] = useState<Draft>({
    org: education?.org ?? "",
    title: education?.title ?? "",
    location: education?.location ?? "",
    startedMonth: toMonth(education?.startedOn),
    endedMonth: toMonth(education?.endedOn),
    summary: education?.summary ?? "",
    detailPath: education?.detailPath ?? "",
    stack: education?.stack.join(", ") ?? "",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const set = <K extends keyof Draft>(key: K, value: string) =>
    setDraft((d) => ({ ...d, [key]: value }));

  async function save() {
    if (!draft.org.trim() || !draft.title.trim() || !draft.startedMonth) {
      setError("기관·제목·시작은 비울 수 없습니다");
      return;
    }
    // 바뀐 필드만 담는다 — 안 보낸 것과 null 은 다르다. 빈 nullable 은 null 로.
    const body: EducationInput = {};
    const org = draft.org.trim();
    if (!education || org !== education.org) body.org = org;
    const title = draft.title.trim();
    if (!education || title !== education.title) body.title = title;
    const location = draft.location.trim() || null;
    if (education ? location !== (education.location ?? null) : location !== null)
      body.location = location;
    const startedOn = toDate(draft.startedMonth);
    if (!education || startedOn !== education.startedOn) body.startedOn = startedOn;
    const endedOn = draft.endedMonth ? toDate(draft.endedMonth) : null;
    if (education ? endedOn !== (education.endedOn ?? null) : endedOn !== null)
      body.endedOn = endedOn;
    const summary = draft.summary.trim() || null;
    if (education ? summary !== (education.summary ?? null) : summary !== null)
      body.summary = summary;
    const detailPath = draft.detailPath.trim() || null;
    if (education ? detailPath !== (education.detailPath ?? null) : detailPath !== null)
      body.detailPath = detailPath;
    const stack = parseStack(draft.stack);
    if (!education || stack.join(" ") !== education.stack.join(" "))
      body.stack = stack;

    if (education && Object.keys(body).length === 0) {
      onDone();
      return;
    }
    setSaving(true);
    setError(null);
    try {
      if (education) await adminApi.patchEducation(education.id, body);
      else await adminApi.createEducation(body);
      onDone();
    } catch (e) {
      setError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
      setSaving(false);
    }
  }

  return (
    <div style={{ ...card, marginBottom: 10, borderColor: "var(--line-2)" }}>
      <div className="mono" style={{ fontSize: 11, letterSpacing: "0.12em", color: "var(--fg-3)", marginBottom: 12 }}>
        {education ? `수정 — ${education.org} · ${education.title}` : "새 교육"}
      </div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
          gap: "10px 16px",
        }}
      >
        <label style={{ display: "block" }}>
          <span style={labelStyle}>기관 *</span>
          <input
            value={draft.org}
            onChange={(e) => set("org", e.target.value)}
            placeholder="비트캠프"
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>제목 *</span>
          <input
            value={draft.title}
            onChange={(e) => set("title", e.target.value)}
            placeholder="풀스택 엔지니어 과정"
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>시작 *</span>
          <input
            type="month"
            value={draft.startedMonth}
            onChange={(e) => set("startedMonth", e.target.value)}
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>종료 — 비우면 현재</span>
          <input
            type="month"
            value={draft.endedMonth}
            onChange={(e) => set("endedMonth", e.target.value)}
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>location</span>
          <input
            value={draft.location}
            onChange={(e) => set("location", e.target.value)}
            placeholder="서울"
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>detail_path — 상세 md 경로, 비우면 상세 없음</span>
          <input
            value={draft.detailPath}
            onChange={(e) => set("detailPath", e.target.value)}
            style={input}
          />
        </label>
        <label style={{ display: "block", gridColumn: "1 / -1" }}>
          <span style={labelStyle}>summary — 카드에 뜨는 한 줄</span>
          <input
            value={draft.summary}
            onChange={(e) => set("summary", e.target.value)}
            style={input}
          />
        </label>
        <label style={{ display: "block", gridColumn: "1 / -1" }}>
          <span style={labelStyle}>stack — 콤마로 구분</span>
          <input
            value={draft.stack}
            onChange={(e) => set("stack", e.target.value)}
            placeholder="Java, Spring, MySQL"
            style={input}
          />
        </label>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: 10, marginTop: 14 }}>
        <button type="button" onClick={save} disabled={saving} style={primaryBtn(true)}>
          {saving ? "저장 중…" : "저장"}
        </button>
        <button type="button" onClick={onCancel} style={ghostBtn}>
          취소
        </button>
        {error && (
          <span className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)" }}>
            {error}
          </span>
        )}
      </div>
    </div>
  );
}

/* ── 스타일 조각 ────────────────────────────────────────────────────── */

const card: React.CSSProperties = {
  border: "1px solid var(--line-1)",
  borderRadius: 8,
  padding: "14px 16px",
  background: "var(--bg-1)",
};

const labelStyle: React.CSSProperties = {
  fontFamily: "var(--font-mono)",
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
