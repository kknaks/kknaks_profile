"use client";

import { useCallback, useEffect, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import type { AdminAlgorithm, AlgorithmInput, AlgoDifficulty } from "@/lib/types";

// 알고리즘 — 메타 관리 + today 토글. 본문 단계(Problem→…→Solution)는
// detailPath 의 md 몫이라 여기서 다루지 않는다(erd.md §algorithm).
// 「오늘의 문제」는 DB partial unique(uq_algorithm_today)가 하나만 허용한다 —
// today=true 를 보내면 서버가 한 트랜잭션에서 이전 today 행을 먼저 내린다.
// 94건이라 카드가 아니라 컴팩트 행 리스트로 그린다. 서버가 today 행을 맨 앞에,
// 그 뒤를 published_on DESC 로 내려주므로 순서는 재정렬하지 않는다.
export default function AdminAlgorithmsPage() {
  const [items, setItems] = useState<AdminAlgorithm[] | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [adding, setAdding] = useState(false);

  const reload = useCallback(() => {
    adminApi
      .algorithms()
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
          알고리즘 목록을 불러오지 못했습니다 — {loadError}
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
    <div className="admin-page" style={{ padding: "28px 32px", maxWidth: 1080, margin: "0 auto" }}>
      <header
        style={{
          marginBottom: 20,
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "space-between",
          gap: 16,
          flexWrap: "wrap",
        }}
      >
        <div>
          <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>알고리즘</h1>
          <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
            algorithm — 메타 관리 + 오늘의 문제. 본문 단계는 md 원장의 몫 · 총 {items.length}건
          </p>
        </div>
        <button type="button" onClick={() => setAdding((a) => !a)} style={primaryBtn(!adding)}>
          {adding ? "닫기" : "+ 문제 추가"}
        </button>
      </header>

      {adding && (
        <AlgorithmForm
          onDone={() => {
            setAdding(false);
            reload();
          }}
          onCancel={() => setAdding(false)}
        />
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
        {items.map((a) => (
          <AlgorithmRow key={a.id} algo={a} onChanged={reload} />
        ))}
      </div>
    </div>
  );
}

/* ── 행 ─────────────────────────────────────────────────────────────── */

const DIFFICULTY_COLOR: Record<AlgoDifficulty, string> = {
  easy: "var(--ok, #3fb950)",
  medium: "var(--warn, #d29922)",
  hard: "var(--danger, #e5534b)",
};

function AlgorithmRow({
  algo,
  onChanged,
}: {
  algo: AdminAlgorithm;
  onChanged: () => void;
}) {
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  async function patch(body: AlgorithmInput) {
    setBusy(true);
    setActionError(null);
    try {
      await adminApi.patchAlgorithm(algo.id, body);
      onChanged();
    } catch (e) {
      setActionError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    } finally {
      setBusy(false);
    }
  }

  // today 토글 — 올리면 서버가 이전 today 를 내린다. 이미 today 면 해제만 한다.
  const toggleToday = () => patch({ today: !algo.today });
  const toggleVisible = () => patch({ visible: !algo.visible });

  async function remove() {
    if (!window.confirm(`「${algo.slug} · ${algo.title}」 을(를) 삭제할까요?`)) return;
    try {
      await adminApi.deleteAlgorithm(algo.id);
      onChanged();
    } catch (e) {
      setActionError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    }
  }

  if (editing) {
    return (
      <AlgorithmForm
        algo={algo}
        onDone={() => {
          setEditing(false);
          onChanged();
        }}
        onCancel={() => setEditing(false)}
      />
    );
  }

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 10,
        flexWrap: "wrap",
        padding: "8px 12px",
        borderRadius: 6,
        background: algo.today ? "var(--bg-2)" : "var(--bg-1)",
        // today 행은 리스트 상단(서버 정렬) + accent 보더로 강조한다.
        border: algo.today ? "1px solid var(--accent)" : "1px solid var(--line-1)",
      }}
    >
      <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)", width: 44, flexShrink: 0 }}>
        {algo.slug}
      </span>
      <span
        style={{
          fontSize: 13,
          color: "var(--fg-0)",
          fontWeight: algo.today ? 600 : 400,
          minWidth: 0,
          overflow: "hidden",
          textOverflow: "ellipsis",
          whiteSpace: "nowrap",
          flex: "1 1 200px",
        }}
        title={algo.summary ?? undefined}
      >
        {algo.title}
      </span>
      <span
        className="mono"
        style={{
          fontSize: 10,
          letterSpacing: "0.06em",
          color: DIFFICULTY_COLOR[algo.difficulty],
          border: "1px solid var(--line-1)",
          borderRadius: 4,
          padding: "1px 6px",
          flexShrink: 0,
          width: 58,
          textAlign: "center",
          boxSizing: "border-box",
        }}
      >
        {algo.difficulty}
      </span>
      <span
        className="mono"
        style={{
          fontSize: 10,
          color: "var(--fg-4)",
          flexShrink: 0,
          width: 130,
          overflow: "hidden",
          textOverflow: "ellipsis",
          whiteSpace: "nowrap",
        }}
        title={algo.curatedIn.join(", ")}
      >
        {algo.curatedIn.join(" · ")}
      </span>
      <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)", flexShrink: 0, width: 78 }}>
        {algo.publishedOn ?? "—"}
      </span>

      {/* today — 누르면 PATCH today=true(서버가 이전 것을 내림). 이미 today 면 해제. */}
      <button
        type="button"
        onClick={toggleToday}
        disabled={busy}
        title={
          algo.today
            ? "오늘의 문제 — 누르면 해제"
            : "누르면 오늘의 문제로 — 이전 문제는 서버가 내린다"
        }
        className="mono"
        style={{
          fontSize: 10,
          letterSpacing: "0.08em",
          padding: "3px 9px",
          borderRadius: 999,
          cursor: "pointer",
          flexShrink: 0,
          border: algo.today ? "1px solid var(--accent)" : "1px solid var(--line-2)",
          background: algo.today ? "var(--accent-soft)" : "transparent",
          color: algo.today ? "var(--accent)" : "var(--fg-3)",
        }}
      >
        today
      </button>

      {/* visible — 공개 표면이 서면 이 값으로 걸러진다. */}
      <button
        type="button"
        onClick={toggleVisible}
        disabled={busy}
        title={algo.visible ? "공개 중 — 누르면 숨김" : "숨김 — 누르면 공개"}
        className="mono"
        style={{
          fontSize: 10,
          letterSpacing: "0.08em",
          padding: "3px 9px",
          borderRadius: 999,
          cursor: "pointer",
          flexShrink: 0,
          border: algo.visible ? "1px solid var(--line-2)" : "1px solid var(--line-1)",
          background: "transparent",
          color: algo.visible ? "var(--fg-1)" : "var(--fg-4)",
        }}
      >
        {algo.visible ? "visible" : "hidden"}
      </button>

      <button type="button" onClick={() => setEditing(true)} style={ghostBtn}>
        수정
      </button>
      <button type="button" onClick={remove} style={{ ...ghostBtn, color: "var(--danger, #e5534b)" }}>
        삭제
      </button>

      {actionError && (
        <span className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)", width: "100%" }}>
          {actionError}
        </span>
      )}
    </div>
  );
}

/* ── 폼 — 등록·수정 겸용 ────────────────────────────────────────────── */

type Draft = {
  slug: string;
  title: string;
  difficulty: string;   // "" = 미선택 — 등록 시 필수
  sourcePlatform: string;
  sourceNumber: string; // 숫자 입력 — 빈 문자열이면 null
  sourceUrl: string;
  curatedIn: string;    // 콤마 구분
  tags: string;         // 콤마 구분
  summary: string;
  detailPath: string;
  publishedOn: string;  // input type="date" — YYYY-MM-DD
  visible: boolean;
};

const parseList = (s: string) =>
  s.split(",").map((t) => t.trim()).filter(Boolean);

function AlgorithmForm({
  algo,
  onDone,
  onCancel,
}: {
  algo?: AdminAlgorithm;
  onDone: () => void;
  onCancel: () => void;
}) {
  const [draft, setDraft] = useState<Draft>({
    slug: algo?.slug ?? "",
    title: algo?.title ?? "",
    difficulty: algo?.difficulty ?? "",
    sourcePlatform: algo?.sourcePlatform ?? "",
    sourceNumber: algo?.sourceNumber != null ? String(algo.sourceNumber) : "",
    sourceUrl: algo?.sourceUrl ?? "",
    curatedIn: algo?.curatedIn.join(", ") ?? "",
    tags: algo?.tags.join(", ") ?? "",
    summary: algo?.summary ?? "",
    detailPath: algo?.detailPath ?? "",
    publishedOn: algo?.publishedOn ?? "",
    visible: algo?.visible ?? true,
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const set = <K extends keyof Draft>(key: K, value: Draft[K]) =>
    setDraft((d) => ({ ...d, [key]: value }));

  async function save() {
    if (
      !draft.slug.trim() ||
      !draft.title.trim() ||
      !draft.difficulty ||
      !draft.sourcePlatform.trim() ||
      !draft.detailPath.trim()
    ) {
      setError("slug·제목·difficulty·플랫폼·detail_path 는 비울 수 없습니다");
      return;
    }
    // 바뀐 필드만 담는다 — 안 보낸 것과 null 은 다르다. 빈 nullable 은 null 로.
    const body: AlgorithmInput = {};
    const slug = draft.slug.trim();
    if (!algo || slug !== algo.slug) body.slug = slug;
    const title = draft.title.trim();
    if (!algo || title !== algo.title) body.title = title;
    const difficulty = draft.difficulty as AlgoDifficulty;
    if (!algo || difficulty !== algo.difficulty) body.difficulty = difficulty;
    const sourcePlatform = draft.sourcePlatform.trim();
    if (!algo || sourcePlatform !== algo.sourcePlatform)
      body.sourcePlatform = sourcePlatform;
    const sourceNumber = draft.sourceNumber.trim()
      ? Number(draft.sourceNumber.trim())
      : null;
    if (sourceNumber !== null && !Number.isInteger(sourceNumber)) {
      setError("출처 번호는 정수여야 합니다");
      return;
    }
    if (algo ? sourceNumber !== (algo.sourceNumber ?? null) : sourceNumber !== null)
      body.sourceNumber = sourceNumber;
    const sourceUrl = draft.sourceUrl.trim() || null;
    if (algo ? sourceUrl !== (algo.sourceUrl ?? null) : sourceUrl !== null)
      body.sourceUrl = sourceUrl;
    const curatedIn = parseList(draft.curatedIn);
    if (!algo || curatedIn.join(" ") !== algo.curatedIn.join(" "))
      body.curatedIn = curatedIn;
    const tags = parseList(draft.tags);
    if (!algo || tags.join(" ") !== algo.tags.join(" ")) body.tags = tags;
    const summary = draft.summary.trim() || null;
    if (algo ? summary !== (algo.summary ?? null) : summary !== null)
      body.summary = summary;
    const detailPath = draft.detailPath.trim();
    if (!algo || detailPath !== algo.detailPath) body.detailPath = detailPath;
    const publishedOn = draft.publishedOn || null;
    if (algo ? publishedOn !== (algo.publishedOn ?? null) : publishedOn !== null)
      body.publishedOn = publishedOn;
    if (!algo || draft.visible !== algo.visible) body.visible = draft.visible;

    if (algo && Object.keys(body).length === 0) {
      onDone();
      return;
    }
    setSaving(true);
    setError(null);
    try {
      if (algo) await adminApi.patchAlgorithm(algo.id, body);
      else await adminApi.createAlgorithm(body);
      onDone();
    } catch (e) {
      // 422(md 부재·difficulty 오값)·409(slug 중복)는 서버 detail 을 그대로 보여준다.
      setError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
      setSaving(false);
    }
  }

  return (
    <div style={{ ...formCard, marginBottom: 10 }}>
      <div className="mono" style={{ fontSize: 11, letterSpacing: "0.12em", color: "var(--fg-3)", marginBottom: 12 }}>
        {algo ? `수정 — ${algo.slug} · ${algo.title}` : "새 문제"}
      </div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
          gap: "10px 16px",
        }}
      >
        <label style={{ display: "block" }}>
          <span style={labelStyle}>slug * — frontmatter 의 id</span>
          <input
            value={draft.slug}
            onChange={(e) => set("slug", e.target.value)}
            placeholder="A-001"
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
          <span style={labelStyle}>difficulty *</span>
          <select
            value={draft.difficulty}
            onChange={(e) => set("difficulty", e.target.value)}
            style={{ ...input, appearance: "auto" }}
          >
            <option value="">— 선택 —</option>
            <option value="easy">easy</option>
            <option value="medium">medium</option>
            <option value="hard">hard</option>
          </select>
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>출처 플랫폼 *</span>
          <input
            value={draft.sourcePlatform}
            onChange={(e) => set("sourcePlatform", e.target.value)}
            placeholder="leetcode"
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>출처 번호</span>
          <input
            type="number"
            value={draft.sourceNumber}
            onChange={(e) => set("sourceNumber", e.target.value)}
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>출처 URL</span>
          <input
            value={draft.sourceUrl}
            onChange={(e) => set("sourceUrl", e.target.value)}
            placeholder="https://leetcode.com/problems/…"
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>curated_in — 콤마로 구분</span>
          <input
            value={draft.curatedIn}
            onChange={(e) => set("curatedIn", e.target.value)}
            placeholder="neetcode150, blind75"
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>tags — 콤마로 구분</span>
          <input
            value={draft.tags}
            onChange={(e) => set("tags", e.target.value)}
            placeholder="array, hash"
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
        <label style={{ display: "flex", alignItems: "center", gap: 8, alignSelf: "end", paddingBottom: 7 }}>
          <input
            type="checkbox"
            checked={draft.visible}
            onChange={(e) => set("visible", e.target.checked)}
          />
          <span style={{ ...labelStyle, fontSize: 11 }}>visible</span>
        </label>
        <label style={{ display: "block", gridColumn: "1 / -1" }}>
          <span style={labelStyle}>detail_path * — para/resources/algorithms/ 하위 실존 md</span>
          <input
            value={draft.detailPath}
            onChange={(e) => set("detailPath", e.target.value)}
            placeholder="para/resources/algorithms/A-001-two-sum.md"
            style={input}
          />
        </label>
      </div>
      <label style={{ display: "block", marginTop: 10 }}>
        <span style={labelStyle}>summary — 원료 frontmatter 에 없으면 비워 둔다</span>
        <textarea
          value={draft.summary}
          onChange={(e) => set("summary", e.target.value)}
          rows={2}
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

const formCard: React.CSSProperties = {
  border: "1px solid var(--line-2)",
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
  flexShrink: 0,
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
