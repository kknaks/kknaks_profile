"use client";

import { useCallback, useEffect, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import type { AdminProject, ProjectInput, WorkStatus } from "@/lib/types";

// 개인 프로젝트 — 등록·수정·삭제. project 는 profile 에 바로 붙는다(erd.md §project).
// slug 는 para/projects/summer-star/ 의 **디렉토리명**이다 — 디렉토리가 없으면
// 서버가 422 로 등록을 막는다. md 가 먼저, DB 가 나중(case_flow.md 케이스 2).
export default function AdminProjectsPage() {
  const [items, setItems] = useState<AdminProject[] | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [adding, setAdding] = useState(false);

  const reload = useCallback(() => {
    adminApi
      .projects()
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
          프로젝트 목록을 불러오지 못했습니다 — {loadError}
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
          <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>개인 프로젝트</h1>
          <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
            project — 혼자 만든 것. md 디렉토리가 먼저, DB 등록이 나중
          </p>
        </div>
        <button type="button" onClick={() => setAdding((a) => !a)} style={primaryBtn(!adding)}>
          {adding ? "닫기" : "+ 프로젝트 추가"}
        </button>
      </header>

      {adding && (
        <ProjectForm
          onDone={() => {
            setAdding(false);
            reload();
          }}
          onCancel={() => setAdding(false)}
        />
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {items.map((p) => (
          <ProjectCard key={p.id} project={p} onChanged={reload} />
        ))}
      </div>
    </div>
  );
}

/* ── 카드 ───────────────────────────────────────────────────────────── */

const STATUS_COLOR: Record<WorkStatus, string> = {
  live: "var(--accent)",
  wip: "var(--fg-2)",
  archived: "var(--fg-4)",
};

const LINK_KEYS = ["repo", "site", "store"] as const;

function ProjectCard({
  project,
  onChanged,
}: {
  project: AdminProject;
  onChanged: () => void;
}) {
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  async function toggleVisible() {
    setBusy(true);
    setActionError(null);
    try {
      await adminApi.patchProject(project.id, { visible: !project.visible });
      onChanged();
    } catch (e) {
      setActionError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    } finally {
      setBusy(false);
    }
  }

  async function remove() {
    if (!window.confirm(`「${project.title}」 을(를) 삭제할까요?`)) return;
    try {
      await adminApi.deleteProject(project.id);
      onChanged();
    } catch (e) {
      setActionError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    }
  }

  if (editing) {
    return (
      <ProjectForm
        project={project}
        onDone={() => {
          setEditing(false);
          onChanged();
        }}
        onCancel={() => setEditing(false)}
      />
    );
  }

  const links = LINK_KEYS.filter((k) => project.links?.[k]);

  return (
    <div style={card}>
      <div style={{ display: "flex", alignItems: "baseline", gap: 12, flexWrap: "wrap" }}>
        <div style={{ minWidth: 0 }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 8, flexWrap: "wrap" }}>
            <span style={{ fontSize: 15, color: "var(--fg-0)", fontWeight: 600 }}>
              {project.title}
            </span>
            <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
              {project.slug}
            </span>
            {project.category && (
              <span className="mono" style={{ fontSize: 10, letterSpacing: "0.08em", color: "var(--fg-3)" }}>
                {project.category}
              </span>
            )}
            {project.status && (
              <span
                className="mono"
                style={{
                  fontSize: 10,
                  letterSpacing: "0.08em",
                  color: STATUS_COLOR[project.status],
                  border: "1px solid var(--line-1)",
                  borderRadius: 4,
                  padding: "1px 6px",
                }}
              >
                {project.status}
              </span>
            )}
          </div>
          {project.startedOn && (
            <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginTop: 2 }}>
              {project.startedOn.slice(0, 7).replace("-", ".")} —
            </div>
          )}
        </div>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 8 }}>
          {/* visible — 누르면 즉시 PATCH. 공개 표면이 서면 이 값으로 걸러진다. */}
          <button
            type="button"
            onClick={toggleVisible}
            disabled={busy}
            title={project.visible ? "공개 중 — 누르면 숨김" : "숨김 — 누르면 공개"}
            className="mono"
            style={{
              fontSize: 10,
              letterSpacing: "0.08em",
              padding: "4px 10px",
              borderRadius: 999,
              cursor: "pointer",
              border: project.visible
                ? "1px solid var(--accent)"
                : "1px solid var(--line-2)",
              background: project.visible ? "var(--accent-soft)" : "transparent",
              color: project.visible ? "var(--accent)" : "var(--fg-3)",
            }}
          >
            {project.visible ? "visible" : "hidden"}
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

      {project.summary && (
        <p style={{ fontSize: 13, color: "var(--fg-2)", lineHeight: 1.6, margin: "10px 0 0" }}>
          {project.summary}
        </p>
      )}
      {project.stack.length > 0 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 10 }}>
          {project.stack.map((s) => (
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
      {links.length > 0 && (
        <div style={{ display: "flex", gap: 12, marginTop: 10 }}>
          {links.map((k) => (
            <a
              key={k}
              href={withScheme(project.links![k]!)}
              target="_blank"
              rel="noreferrer"
              className="mono"
              style={{ fontSize: 11, color: "var(--accent)" }}
            >
              {k} ↗
            </a>
          ))}
        </div>
      )}
      {actionError && (
        <p className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "8px 0 0" }}>
          {actionError}
        </p>
      )}
    </div>
  );
}

/** 시드 원료에 `github.com/...` 처럼 스킴 없는 값이 있다 — 링크로 열 때만 붙인다. */
const withScheme = (url: string) => (/^https?:\/\//.test(url) ? url : `https://${url}`);

/* ── 폼 — 등록·수정 겸용 ────────────────────────────────────────────── */

type Draft = {
  slug: string;
  title: string;
  summary: string;
  category: string;
  status: string;       // "" = 미지정
  startedMonth: string; // input type="month" — YYYY-MM
  stack: string;        // 콤마 구분
  thumbnail: string;
  linkRepo: string;
  linkSite: string;
  linkStore: string;
  detailPath: string;
};

/** date 컬럼은 YYYY-MM-DD, 입력은 월 단위 — 잘라서 채우고 붙여서 보낸다. */
const toMonth = (d?: string | null) => (d ? d.slice(0, 7) : "");
const toDate = (m: string) => `${m}-01`;
const parseStack = (s: string) =>
  s.split(",").map((t) => t.trim()).filter(Boolean);

/** links jsonb — 빈 입력은 키를 만들지 않고, 다 비면 null 로 지운다. */
function buildLinks(
  repo: string,
  site: string,
  store: string,
): { repo?: string; site?: string; store?: string } | null {
  const links: { repo?: string; site?: string; store?: string } = {};
  if (repo.trim()) links.repo = repo.trim();
  if (site.trim()) links.site = site.trim();
  if (store.trim()) links.store = store.trim();
  return Object.keys(links).length > 0 ? links : null;
}

function ProjectForm({
  project,
  onDone,
  onCancel,
}: {
  project?: AdminProject;
  onDone: () => void;
  onCancel: () => void;
}) {
  const [draft, setDraft] = useState<Draft>({
    slug: project?.slug ?? "",
    title: project?.title ?? "",
    summary: project?.summary ?? "",
    category: project?.category ?? "",
    status: project?.status ?? "",
    startedMonth: toMonth(project?.startedOn),
    stack: project?.stack.join(", ") ?? "",
    thumbnail: project?.thumbnail ?? "",
    linkRepo: project?.links?.repo ?? "",
    linkSite: project?.links?.site ?? "",
    linkStore: project?.links?.store ?? "",
    detailPath: project?.detailPath ?? "",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const set = <K extends keyof Draft>(key: K, value: string) =>
    setDraft((d) => ({ ...d, [key]: value }));

  async function save() {
    if (!draft.slug.trim() || !draft.title.trim()) {
      setError("slug·제목은 비울 수 없습니다");
      return;
    }
    // 바뀐 필드만 담는다 — 안 보낸 것과 null 은 다르다. 빈 nullable 은 null 로.
    const body: ProjectInput = {};
    const slug = draft.slug.trim();
    if (!project || slug !== project.slug) body.slug = slug;
    const title = draft.title.trim();
    if (!project || title !== project.title) body.title = title;
    const summary = draft.summary.trim() || null;
    if (project ? summary !== (project.summary ?? null) : summary !== null)
      body.summary = summary;
    const category = draft.category.trim() || null;
    if (project ? category !== (project.category ?? null) : category !== null)
      body.category = category;
    const status = (draft.status || null) as ProjectInput["status"];
    if (project ? status !== (project.status ?? null) : status !== null)
      body.status = status;
    const startedOn = draft.startedMonth ? toDate(draft.startedMonth) : null;
    if (project ? startedOn !== (project.startedOn ?? null) : startedOn !== null)
      body.startedOn = startedOn;
    const stack = parseStack(draft.stack);
    if (!project || stack.join(" ") !== project.stack.join(" ")) body.stack = stack;
    const thumbnail = draft.thumbnail.trim() || null;
    if (project ? thumbnail !== (project.thumbnail ?? null) : thumbnail !== null)
      body.thumbnail = thumbnail;
    const links = buildLinks(draft.linkRepo, draft.linkSite, draft.linkStore);
    const prevLinks = project
      ? buildLinks(
          project.links?.repo ?? "",
          project.links?.site ?? "",
          project.links?.store ?? "",
        )
      : null;
    if (JSON.stringify(links) !== JSON.stringify(prevLinks)) body.links = links;
    const detailPath = draft.detailPath.trim() || null;
    if (project ? detailPath !== (project.detailPath ?? null) : detailPath !== null)
      body.detailPath = detailPath;

    if (project && Object.keys(body).length === 0) {
      onDone();
      return;
    }
    setSaving(true);
    setError(null);
    try {
      if (project) await adminApi.patchProject(project.id, body);
      else await adminApi.createProject(body);
      onDone();
    } catch (e) {
      // 422(디렉토리 없음 등)는 서버 detail 을 그대로 보여준다 — 케이스 2 안내가 담겨 있다.
      setError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
      setSaving(false);
    }
  }

  return (
    <div style={{ ...card, marginBottom: 10, borderColor: "var(--line-2)" }}>
      <div className="mono" style={{ fontSize: 11, letterSpacing: "0.12em", color: "var(--fg-3)", marginBottom: 12 }}>
        {project ? `수정 — ${project.title}` : "새 프로젝트"}
      </div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
          gap: "10px 16px",
        }}
      >
        <label style={{ display: "block" }}>
          <span style={labelStyle}>slug * — para/projects/summer-star/ 디렉토리명</span>
          <input
            value={draft.slug}
            onChange={(e) => set("slug", e.target.value)}
            placeholder="wine-log (디렉토리명)"
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
          <span style={labelStyle}>category</span>
          <input
            value={draft.category}
            onChange={(e) => set("category", e.target.value)}
            placeholder="mobile / web / cli"
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>status</span>
          <select
            value={draft.status}
            onChange={(e) => set("status", e.target.value)}
            style={{ ...input, appearance: "auto" }}
          >
            <option value="">— 미지정 —</option>
            <option value="live">live</option>
            <option value="wip">wip</option>
            <option value="archived">archived</option>
          </select>
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>시작</span>
          <input
            type="month"
            value={draft.startedMonth}
            onChange={(e) => set("startedMonth", e.target.value)}
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>thumbnail</span>
          <input
            value={draft.thumbnail}
            onChange={(e) => set("thumbnail", e.target.value)}
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>links.repo</span>
          <input
            value={draft.linkRepo}
            onChange={(e) => set("linkRepo", e.target.value)}
            placeholder="github.com/…"
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>links.site</span>
          <input
            value={draft.linkSite}
            onChange={(e) => set("linkSite", e.target.value)}
            placeholder="https://…"
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>links.store</span>
          <input
            value={draft.linkStore}
            onChange={(e) => set("linkStore", e.target.value)}
            placeholder="https://…"
            style={input}
          />
        </label>
        <label style={{ display: "block", gridColumn: "1 / -1" }}>
          <span style={labelStyle}>stack — 콤마로 구분</span>
          <input
            value={draft.stack}
            onChange={(e) => set("stack", e.target.value)}
            placeholder="FastAPI, PostgreSQL"
            style={input}
          />
        </label>
        <label style={{ display: "block", gridColumn: "1 / -1" }}>
          <span style={labelStyle}>detail_path — 비우면 서버가 showcase.md 경로로 채움</span>
          <input
            value={draft.detailPath}
            onChange={(e) => set("detailPath", e.target.value)}
            placeholder="para/projects/summer-star/wine-log/showcase.md"
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
