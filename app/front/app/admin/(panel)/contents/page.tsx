"use client";

import { useCallback, useEffect, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import type { AdminContent, ContentInput } from "@/lib/types";

// 콘텐츠(영상 + 교안) — 등록·수정·삭제. content 는 profile 에 바로 붙는다(erd.md §content).
// 원장은 para/resources/youtube/ 의 md — detailPath 가 가리키는 파일이 없으면
// 서버가 422 로 등록을 막는다. 정보는 DB, 상세는 md.
export default function AdminContentsPage() {
  const [items, setItems] = useState<AdminContent[] | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [adding, setAdding] = useState(false);

  const reload = useCallback(() => {
    adminApi
      .contents()
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
          콘텐츠 목록을 불러오지 못했습니다 — {loadError}
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
          <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>콘텐츠</h1>
          <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
            content — 영상 + 교안. 원장은 para/resources/youtube/ 의 md
          </p>
        </div>
        <button type="button" onClick={() => setAdding((a) => !a)} style={primaryBtn(!adding)}>
          {adding ? "닫기" : "+ 콘텐츠 추가"}
        </button>
      </header>

      {adding && (
        <ContentForm
          onDone={() => {
            setAdding(false);
            reload();
          }}
          onCancel={() => setAdding(false)}
        />
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {items.map((c) => (
          <ContentCard key={c.id} content={c} onChanged={reload} />
        ))}
      </div>
    </div>
  );
}

/* ── 카드 ───────────────────────────────────────────────────────────── */

function ContentCard({
  content,
  onChanged,
}: {
  content: AdminContent;
  onChanged: () => void;
}) {
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  async function toggleVisible() {
    setBusy(true);
    setActionError(null);
    try {
      await adminApi.patchContent(content.id, { visible: !content.visible });
      onChanged();
    } catch (e) {
      setActionError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    } finally {
      setBusy(false);
    }
  }

  async function remove() {
    if (!window.confirm(`「${content.title}」 을(를) 삭제할까요?`)) return;
    try {
      await adminApi.deleteContent(content.id);
      onChanged();
    } catch (e) {
      setActionError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    }
  }

  if (editing) {
    return (
      <ContentForm
        content={content}
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
      <div style={{ display: "flex", gap: 14, alignItems: "flex-start" }}>
        {/* 유튜브 썸네일 — youtube_id 에서 파생. DB 에 이미지가 없다. */}
        <a
          href={`https://youtu.be/${content.youtubeId}`}
          target="_blank"
          rel="noreferrer"
          style={{ flexShrink: 0, lineHeight: 0 }}
          title={`youtu.be/${content.youtubeId} ↗`}
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={`https://i.ytimg.com/vi/${content.youtubeId}/mqdefault.jpg`}
            alt={content.title}
            width={120}
            style={{
              display: "block",
              width: 120,
              aspectRatio: "16 / 9",
              objectFit: "cover",
              borderRadius: 6,
              border: "1px solid var(--line-1)",
              background: "var(--bg-2)",
            }}
          />
        </a>

        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 12, flexWrap: "wrap" }}>
            <div style={{ minWidth: 0 }}>
              <div style={{ display: "flex", alignItems: "baseline", gap: 8, flexWrap: "wrap" }}>
                <span style={{ fontSize: 15, color: "var(--fg-0)", fontWeight: 600 }}>
                  {content.title}
                </span>
                <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
                  {content.slug}
                </span>
              </div>
              <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginTop: 2 }}>
                {[
                  content.speaker,
                  content.duration,
                  content.publishedOn?.replaceAll("-", "."),
                ]
                  .filter(Boolean)
                  .join(" · ")}
              </div>
            </div>
            <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 8 }}>
              {/* visible — 누르면 즉시 PATCH. 공개 표면(/contents)이 이 값으로 거른다. */}
              <button
                type="button"
                onClick={toggleVisible}
                disabled={busy}
                title={content.visible ? "공개 중 — 누르면 숨김" : "숨김 — 누르면 공개"}
                className="mono"
                style={{
                  fontSize: 10,
                  letterSpacing: "0.08em",
                  padding: "4px 10px",
                  borderRadius: 999,
                  cursor: "pointer",
                  border: content.visible
                    ? "1px solid var(--accent)"
                    : "1px solid var(--line-2)",
                  background: content.visible ? "var(--accent-soft)" : "transparent",
                  color: content.visible ? "var(--accent)" : "var(--fg-3)",
                }}
              >
                {content.visible ? "visible" : "hidden"}
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

          {content.summary && (
            <p style={{ fontSize: 13, color: "var(--fg-2)", lineHeight: 1.6, margin: "10px 0 0" }}>
              {content.summary}
            </p>
          )}
          {content.tags.length > 0 && (
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 10 }}>
              {content.tags.map((t) => (
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
          {actionError && (
            <p className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "8px 0 0" }}>
              {actionError}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

/* ── 폼 — 등록·수정 겸용 ────────────────────────────────────────────── */

type Draft = {
  slug: string;
  title: string;
  youtubeId: string;
  detailPath: string;
  duration: string;
  speaker: string;
  summary: string;
  tags: string;        // 콤마 구분
  publishedOn: string; // input type="date" — YYYY-MM-DD
};

const parseTags = (s: string) =>
  s.split(",").map((t) => t.trim()).filter(Boolean);

function ContentForm({
  content,
  onDone,
  onCancel,
}: {
  content?: AdminContent;
  onDone: () => void;
  onCancel: () => void;
}) {
  const [draft, setDraft] = useState<Draft>({
    slug: content?.slug ?? "",
    title: content?.title ?? "",
    youtubeId: content?.youtubeId ?? "",
    detailPath: content?.detailPath ?? "",
    duration: content?.duration ?? "",
    speaker: content?.speaker ?? "",
    summary: content?.summary ?? "",
    tags: content?.tags.join(", ") ?? "",
    publishedOn: content?.publishedOn ?? "",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const set = <K extends keyof Draft>(key: K, value: string) =>
    setDraft((d) => ({ ...d, [key]: value }));

  async function save() {
    if (
      !draft.slug.trim() ||
      !draft.title.trim() ||
      !draft.youtubeId.trim() ||
      !draft.detailPath.trim()
    ) {
      setError("slug·제목·youtubeId·detail_path 는 비울 수 없습니다");
      return;
    }
    // 바뀐 필드만 담는다 — 안 보낸 것과 null 은 다르다. 빈 nullable 은 null 로.
    const body: ContentInput = {};
    const slug = draft.slug.trim();
    if (!content || slug !== content.slug) body.slug = slug;
    const title = draft.title.trim();
    if (!content || title !== content.title) body.title = title;
    const youtubeId = draft.youtubeId.trim();
    if (!content || youtubeId !== content.youtubeId) body.youtubeId = youtubeId;
    const detailPath = draft.detailPath.trim();
    if (!content || detailPath !== content.detailPath) body.detailPath = detailPath;
    const duration = draft.duration.trim() || null;
    if (content ? duration !== (content.duration ?? null) : duration !== null)
      body.duration = duration;
    const speaker = draft.speaker.trim() || null;
    if (content ? speaker !== (content.speaker ?? null) : speaker !== null)
      body.speaker = speaker;
    const summary = draft.summary.trim() || null;
    if (content ? summary !== (content.summary ?? null) : summary !== null)
      body.summary = summary;
    const tags = parseTags(draft.tags);
    if (!content || tags.join(" ") !== content.tags.join(" ")) body.tags = tags;
    const publishedOn = draft.publishedOn || null;
    if (content ? publishedOn !== (content.publishedOn ?? null) : publishedOn !== null)
      body.publishedOn = publishedOn;

    if (content && Object.keys(body).length === 0) {
      onDone();
      return;
    }
    setSaving(true);
    setError(null);
    try {
      if (content) await adminApi.patchContent(content.id, body);
      else await adminApi.createContent(body);
      onDone();
    } catch (e) {
      // 422(원장 md 없음 등)·409(slug 중복)는 서버 detail 을 그대로 보여준다.
      setError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
      setSaving(false);
    }
  }

  return (
    <div style={{ ...card, marginBottom: 10, borderColor: "var(--line-2)" }}>
      <div className="mono" style={{ fontSize: 11, letterSpacing: "0.12em", color: "var(--fg-3)", marginBottom: 12 }}>
        {content ? `수정 — ${content.title}` : "새 콘텐츠"}
      </div>
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
            placeholder="C-027"
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
          <span style={labelStyle}>youtube_id *</span>
          <input
            value={draft.youtubeId}
            onChange={(e) => set("youtubeId", e.target.value)}
            placeholder="RVngRYqs7kA"
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>duration</span>
          <input
            value={draft.duration}
            onChange={(e) => set("duration", e.target.value)}
            placeholder="5:54"
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>speaker — 출처 채널</span>
          <input
            value={draft.speaker}
            onChange={(e) => set("speaker", e.target.value)}
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
        <label style={{ display: "block", gridColumn: "1 / -1" }}>
          <span style={labelStyle}>detail_path * — para/resources/youtube/ 하위 원장 md</span>
          <input
            value={draft.detailPath}
            onChange={(e) => set("detailPath", e.target.value)}
            placeholder="para/resources/youtube/C-027-….md"
            style={input}
          />
        </label>
        <label style={{ display: "block", gridColumn: "1 / -1" }}>
          <span style={labelStyle}>tags — 콤마로 구분</span>
          <input
            value={draft.tags}
            onChange={(e) => set("tags", e.target.value)}
            placeholder="mcp, protocol"
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
