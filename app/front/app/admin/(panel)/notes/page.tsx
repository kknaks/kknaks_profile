"use client";

import { useCallback, useEffect, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import type { AdminNote, NoteFileCandidate, NoteInput } from "@/lib/types";

// 노트 — 등록·수정·삭제. 원장은 para/resources/note/ 의 md 다(erd.md §note).
// **공개는 선택이다** — 글을 쓴다고 사이트에 뜨지 않고, 여기서 파일을 골라
// 등록해야 뜬다(case_flow.md 케이스 4). 삭제는 등록 해제일 뿐 md 는 남는다.
export default function AdminNotesPage() {
  const [items, setItems] = useState<AdminNote[] | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [adding, setAdding] = useState(false);

  const reload = useCallback(() => {
    adminApi
      .notes()
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
          노트 목록을 불러오지 못했습니다 — {loadError}
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
          <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>노트</h1>
          <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
            note — 내가 쓴 글. 등록한 것만 사이트에 뜬다 (케이스 4)
          </p>
        </div>
        <button type="button" onClick={() => setAdding((a) => !a)} style={primaryBtn(!adding)}>
          {adding ? "닫기" : "+ 노트 등록"}
        </button>
      </header>

      {adding && (
        <NoteForm
          onDone={() => {
            setAdding(false);
            reload();
          }}
          onCancel={() => setAdding(false)}
        />
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {items.map((n) => (
          <NoteCard key={n.id} note={n} onChanged={reload} />
        ))}
      </div>
    </div>
  );
}

/* ── 카드 ───────────────────────────────────────────────────────────── */

function NoteCard({ note, onChanged }: { note: AdminNote; onChanged: () => void }) {
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  async function toggleVisible() {
    setBusy(true);
    setActionError(null);
    try {
      await adminApi.patchNote(note.id, { visible: !note.visible });
      onChanged();
    } catch (e) {
      setActionError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    } finally {
      setBusy(false);
    }
  }

  async function remove() {
    if (!window.confirm(`「${note.title}」 등록을 해제할까요? md 파일은 그대로 남습니다.`))
      return;
    try {
      await adminApi.deleteNote(note.id);
      onChanged();
    } catch (e) {
      setActionError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    }
  }

  if (editing) {
    return (
      <NoteForm
        note={note}
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
              {note.title}
            </span>
            <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
              {note.slug}
            </span>
          </div>
          {note.publishedOn && (
            <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginTop: 2 }}>
              {note.publishedOn.replaceAll("-", ".")}
            </div>
          )}
        </div>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 8 }}>
          {/* visible — 누르면 즉시 PATCH. 공개 표면이 서면 이 값으로 걸러진다. */}
          <button
            type="button"
            onClick={toggleVisible}
            disabled={busy}
            title={note.visible ? "공개 중 — 누르면 숨김" : "숨김 — 누르면 공개"}
            className="mono"
            style={{
              fontSize: 10,
              letterSpacing: "0.08em",
              padding: "4px 10px",
              borderRadius: 999,
              cursor: "pointer",
              border: note.visible ? "1px solid var(--accent)" : "1px solid var(--line-2)",
              background: note.visible ? "var(--accent-soft)" : "transparent",
              color: note.visible ? "var(--accent)" : "var(--fg-3)",
            }}
          >
            {note.visible ? "visible" : "hidden"}
          </button>
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

      {note.summary && (
        <p style={{ fontSize: 13, color: "var(--fg-2)", lineHeight: 1.6, margin: "10px 0 0" }}>
          {note.summary}
        </p>
      )}
      {note.tags.length > 0 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 10 }}>
          {note.tags.map((t) => (
            <span
              key={t}
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
              {t}
            </span>
          ))}
        </div>
      )}
      <div className="mono" style={{ fontSize: 10, color: "var(--fg-4)", marginTop: 10 }}>
        {note.detailPath}
      </div>
      {actionError && (
        <p className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "8px 0 0" }}>
          {actionError}
        </p>
      )}
    </div>
  );
}

/* ── 폼 — 등록·수정 겸용 ────────────────────────────────────────────── */

type Draft = {
  detailPath: string;
  slug: string;
  title: string;
  summary: string;
  tags: string;        // 콤마 구분
  publishedOn: string; // input type="date" — YYYY-MM-DD
  visible: boolean;
};

const parseTags = (s: string) =>
  s.split(",").map((t) => t.trim()).filter(Boolean);

function NoteForm({
  note,
  onDone,
  onCancel,
}: {
  note?: AdminNote;
  onDone: () => void;
  onCancel: () => void;
}) {
  const [draft, setDraft] = useState<Draft>({
    detailPath: note?.detailPath ?? "",
    slug: note?.slug ?? "",
    title: note?.title ?? "",
    summary: note?.summary ?? "",
    tags: note?.tags.join(", ") ?? "",
    publishedOn: note?.publishedOn ?? "",
    visible: note?.visible ?? true,
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 등록일 때만 — 후보 파일 목록. 선택하면 frontmatter 값으로 폼을 프리필한다.
  const [files, setFiles] = useState<NoteFileCandidate[] | null>(null);
  const [filesError, setFilesError] = useState<string | null>(null);

  useEffect(() => {
    if (note) return; // 수정은 파일을 다시 고르지 않는다 — detailPath 를 그대로 보여준다.
    adminApi
      .noteFiles()
      .then(({ items }) => setFiles(items))
      .catch((e) =>
        setFilesError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e)),
      );
  }, [note]);

  const set = <K extends keyof Draft>(key: K, value: Draft[K]) =>
    setDraft((d) => ({ ...d, [key]: value }));

  /** 파일을 고르면 frontmatter 값으로 프리필한다 — 전부 수정 가능한 초안일 뿐이다. */
  function pickFile(path: string) {
    const f = files?.find((c) => c.path === path);
    if (!f) {
      set("detailPath", path);
      return;
    }
    setDraft((d) => ({
      ...d,
      detailPath: f.path,
      slug: f.stem,
      title: f.title ?? "",
      summary: f.summary ?? "",
      tags: f.tags.join(", "),
      publishedOn: f.date ?? "",
    }));
  }

  async function save() {
    if (!draft.detailPath.trim()) {
      setError("파일을 선택해야 합니다");
      return;
    }
    if (!draft.slug.trim() || !draft.title.trim()) {
      setError("slug·제목은 비울 수 없습니다");
      return;
    }
    // 바뀐 필드만 담는다 — 안 보낸 것과 null 은 다르다. 빈 nullable 은 null 로.
    const body: NoteInput = {};
    const detailPath = draft.detailPath.trim();
    if (!note || detailPath !== note.detailPath) body.detailPath = detailPath;
    const slug = draft.slug.trim();
    if (!note || slug !== note.slug) body.slug = slug;
    const title = draft.title.trim();
    if (!note || title !== note.title) body.title = title;
    const summary = draft.summary.trim() || null;
    if (note ? summary !== (note.summary ?? null) : summary !== null)
      body.summary = summary;
    const tags = parseTags(draft.tags);
    if (!note || tags.join(" ") !== note.tags.join(" ")) body.tags = tags;
    const publishedOn = draft.publishedOn || null;
    if (note ? publishedOn !== (note.publishedOn ?? null) : publishedOn !== null)
      body.publishedOn = publishedOn;
    if (!note || draft.visible !== note.visible) body.visible = draft.visible;

    if (note && Object.keys(body).length === 0) {
      onDone();
      return;
    }
    setSaving(true);
    setError(null);
    try {
      if (note) await adminApi.patchNote(note.id, body);
      else await adminApi.createNote(body);
      onDone();
    } catch (e) {
      // 422(파일 없음 등)·409(slug 중복)는 서버 detail 을 그대로 보여준다.
      setError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
      setSaving(false);
    }
  }

  return (
    <div style={{ ...card, marginBottom: 10, borderColor: "var(--line-2)" }}>
      <div className="mono" style={{ fontSize: 11, letterSpacing: "0.12em", color: "var(--fg-3)", marginBottom: 12 }}>
        {note ? `수정 — ${note.title}` : "노트 등록"}
      </div>

      {/* 파일 — 등록은 드롭다운으로 고르고, 수정은 경로를 그대로 보여준다. */}
      {note ? (
        <div style={{ marginBottom: 10 }}>
          <span style={labelStyle}>detail_path — 원장 md (여기서는 안 바꾼다)</span>
          <div className="mono" style={{ fontSize: 11, color: "var(--fg-2)", marginTop: 4 }}>
            {note.detailPath}
          </div>
        </div>
      ) : (
        <label style={{ display: "block", marginBottom: 10 }}>
          <span style={labelStyle}>파일 * — para/resources/note/ 의 미등록 md</span>
          {filesError ? (
            <div className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)", marginTop: 4 }}>
              후보 파일을 불러오지 못했습니다 — {filesError}
            </div>
          ) : (
            <select
              value={draft.detailPath}
              onChange={(e) => pickFile(e.target.value)}
              disabled={!files}
              style={{ ...input, appearance: "auto" }}
            >
              <option value="">
                {files ? `— 파일 선택 (${files.length}건) —` : "불러오는 중…"}
              </option>
              {files?.map((f) => (
                <option key={f.path} value={f.path}>
                  {f.stem}
                </option>
              ))}
            </select>
          )}
        </label>
      )}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
          gap: "10px 16px",
        }}
      >
        <label style={{ display: "block" }}>
          <span style={labelStyle}>slug *</span>
          <input
            value={draft.slug}
            onChange={(e) => set("slug", e.target.value)}
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>제목 *</span>
          <input
            value={draft.title}
            onChange={(e) => set("title", e.target.value)}
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>발행일</span>
          <input
            type="date"
            value={draft.publishedOn}
            onChange={(e) => set("publishedOn", e.target.value)}
            style={input}
          />
        </label>
        <label style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 18 }}>
          <input
            type="checkbox"
            checked={draft.visible}
            onChange={(e) => set("visible", e.target.checked)}
          />
          <span className="mono" style={{ fontSize: 11, color: "var(--fg-2)" }}>
            visible — 사이트에 공개
          </span>
        </label>
        <label style={{ display: "block", gridColumn: "1 / -1" }}>
          <span style={labelStyle}>tags — 콤마로 구분</span>
          <input
            value={draft.tags}
            onChange={(e) => set("tags", e.target.value)}
            style={input}
          />
        </label>
      </div>
      <label style={{ display: "block", marginTop: 10 }}>
        <span style={labelStyle}>summary — 카드에 뜨는 한 줄</span>
        <textarea
          value={draft.summary}
          onChange={(e) => set("summary", e.target.value)}
          rows={3}
          style={{ ...input, resize: "vertical" }}
        />
      </label>

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
