"use client";

import { useCallback, useEffect, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import type { AdminCareer, AdminProduct, ProductInput, WorkStatus } from "@/lib/types";

// 회사 제품 — 등록·수정·삭제. product 는 career 에 속한다(erd.md §product) —
// 「회사명 · 역할명」은 2단 조인 파생 표시값이라 읽기 전용, 수정은 careerId 로 한다.
export default function AdminProductsPage() {
  const [items, setItems] = useState<AdminProduct[] | null>(null);
  const [careers, setCareers] = useState<AdminCareer[] | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [adding, setAdding] = useState(false);

  const reload = useCallback(() => {
    adminApi
      .products()
      .then(({ items }) => setItems(items))
      .catch((e) => setLoadError(String(e)));
  }, []);

  useEffect(() => {
    reload();
    // 폼의 역할 드롭다운 — 제품은 역할 없이 못 만든다.
    adminApi
      .careers()
      .then(({ items }) => setCareers(items))
      .catch((e) => setLoadError(String(e)));
  }, [reload]);

  if (loadError) {
    return (
      <div className="admin-page" style={{ padding: "28px 32px" }}>
        <p className="mono" style={{ fontSize: 12, color: "var(--danger, #e5534b)" }}>
          제품 목록을 불러오지 못했습니다 — {loadError}
        </p>
      </div>
    );
  }

  if (!items || !careers) {
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
          <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>회사 제품</h1>
          <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
            product — 그 역할에서 만든 것. 회사는 역할을 거쳐 닿는다
          </p>
        </div>
        <button type="button" onClick={() => setAdding((a) => !a)} style={primaryBtn(!adding)}>
          {adding ? "닫기" : "+ 제품 추가"}
        </button>
      </header>

      {adding && (
        <ProductForm
          careers={careers}
          onDone={() => {
            setAdding(false);
            reload();
          }}
          onCancel={() => setAdding(false)}
        />
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {items.map((p) => (
          <ProductCard key={p.id} product={p} careers={careers} onChanged={reload} />
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

function ProductCard({
  product,
  careers,
  onChanged,
}: {
  product: AdminProduct;
  careers: AdminCareer[];
  onChanged: () => void;
}) {
  const [editing, setEditing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  async function toggleVisible() {
    setBusy(true);
    setActionError(null);
    try {
      await adminApi.patchProduct(product.id, { visible: !product.visible });
      onChanged();
    } catch (e) {
      setActionError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    } finally {
      setBusy(false);
    }
  }

  async function remove() {
    if (!window.confirm(`「${product.title}」 을(를) 삭제할까요?`)) return;
    try {
      await adminApi.deleteProduct(product.id);
      onChanged();
    } catch (e) {
      setActionError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    }
  }

  if (editing) {
    return (
      <ProductForm
        product={product}
        careers={careers}
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
              {product.title}
            </span>
            <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
              {product.slug}
            </span>
            {product.status && (
              <span
                className="mono"
                style={{
                  fontSize: 10,
                  letterSpacing: "0.08em",
                  color: STATUS_COLOR[product.status],
                  border: "1px solid var(--line-1)",
                  borderRadius: 4,
                  padding: "1px 6px",
                }}
              >
                {product.status}
              </span>
            )}
          </div>
          <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginTop: 2 }}>
            {product.companyName} · {product.careerTitle}
            {product.startedOn && <> · {product.startedOn.slice(0, 7).replace("-", ".")}</>}
          </div>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 8 }}>
          {/* visible — 누르면 즉시 PATCH. 공개 표면이 서면 이 값으로 걸러진다. */}
          <button
            type="button"
            onClick={toggleVisible}
            disabled={busy}
            title={product.visible ? "공개 중 — 누르면 숨김" : "숨김 — 누르면 공개"}
            className="mono"
            style={{
              fontSize: 10,
              letterSpacing: "0.08em",
              padding: "4px 10px",
              borderRadius: 999,
              cursor: "pointer",
              border: product.visible
                ? "1px solid var(--accent)"
                : "1px solid var(--line-2)",
              background: product.visible ? "var(--accent-soft)" : "transparent",
              color: product.visible ? "var(--accent)" : "var(--fg-3)",
            }}
          >
            {product.visible ? "visible" : "hidden"}
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

      {product.summary && (
        <p style={{ fontSize: 13, color: "var(--fg-2)", lineHeight: 1.6, margin: "10px 0 0" }}>
          {product.summary}
        </p>
      )}
      {product.stack.length > 0 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 10 }}>
          {product.stack.map((s) => (
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
      {(product.links?.site || product.links?.docs) && (
        <div style={{ display: "flex", gap: 12, marginTop: 10 }}>
          {product.links?.site && (
            <a
              href={product.links.site}
              target="_blank"
              rel="noreferrer"
              className="mono"
              style={{ fontSize: 11, color: "var(--accent)" }}
            >
              site ↗
            </a>
          )}
          {product.links?.docs && (
            <a
              href={product.links.docs}
              target="_blank"
              rel="noreferrer"
              className="mono"
              style={{ fontSize: 11, color: "var(--accent)" }}
            >
              docs ↗
            </a>
          )}
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

/* ── 폼 — 등록·수정 겸용 ────────────────────────────────────────────── */

type Draft = {
  careerId: string;     // select value — "" = 미선택
  slug: string;
  title: string;
  summary: string;
  category: string;
  status: string;       // "" = 미지정
  startedMonth: string; // input type="month" — YYYY-MM
  stack: string;        // 콤마 구분
  thumbnail: string;
  linkSite: string;
  linkDocs: string;
  detailPath: string;
};

/** date 컬럼은 YYYY-MM-DD, 입력은 월 단위 — 잘라서 채우고 붙여서 보낸다. */
const toMonth = (d?: string | null) => (d ? d.slice(0, 7) : "");
const toDate = (m: string) => `${m}-01`;
const parseStack = (s: string) =>
  s.split(",").map((t) => t.trim()).filter(Boolean);

/** links jsonb — 빈 입력은 키를 만들지 않고, 둘 다 비면 null 로 지운다. */
function buildLinks(site: string, docs: string): { site?: string; docs?: string } | null {
  const links: { site?: string; docs?: string } = {};
  if (site.trim()) links.site = site.trim();
  if (docs.trim()) links.docs = docs.trim();
  return Object.keys(links).length > 0 ? links : null;
}

function ProductForm({
  product,
  careers,
  onDone,
  onCancel,
}: {
  product?: AdminProduct;
  careers: AdminCareer[];
  onDone: () => void;
  onCancel: () => void;
}) {
  const [draft, setDraft] = useState<Draft>({
    careerId: product ? String(product.careerId) : "",
    slug: product?.slug ?? "",
    title: product?.title ?? "",
    summary: product?.summary ?? "",
    category: product?.category ?? "",
    status: product?.status ?? "",
    startedMonth: toMonth(product?.startedOn),
    stack: product?.stack.join(", ") ?? "",
    thumbnail: product?.thumbnail ?? "",
    linkSite: product?.links?.site ?? "",
    linkDocs: product?.links?.docs ?? "",
    detailPath: product?.detailPath ?? "",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const set = <K extends keyof Draft>(key: K, value: string) =>
    setDraft((d) => ({ ...d, [key]: value }));

  async function save() {
    if (!draft.careerId || !draft.slug.trim() || !draft.title.trim()) {
      setError("역할·slug·제목은 비울 수 없습니다");
      return;
    }
    // 바뀐 필드만 담는다 — 안 보낸 것과 null 은 다르다. 빈 nullable 은 null 로.
    const body: ProductInput = {};
    const careerId = Number(draft.careerId);
    if (!product || careerId !== product.careerId) body.careerId = careerId;
    const slug = draft.slug.trim();
    if (!product || slug !== product.slug) body.slug = slug;
    const title = draft.title.trim();
    if (!product || title !== product.title) body.title = title;
    const summary = draft.summary.trim() || null;
    if (product ? summary !== (product.summary ?? null) : summary !== null)
      body.summary = summary;
    const category = draft.category.trim() || null;
    if (product ? category !== (product.category ?? null) : category !== null)
      body.category = category;
    const status = (draft.status || null) as ProductInput["status"];
    if (product ? status !== (product.status ?? null) : status !== null)
      body.status = status;
    const startedOn = draft.startedMonth ? toDate(draft.startedMonth) : null;
    if (product ? startedOn !== (product.startedOn ?? null) : startedOn !== null)
      body.startedOn = startedOn;
    const stack = parseStack(draft.stack);
    if (!product || stack.join(" ") !== product.stack.join(" ")) body.stack = stack;
    const thumbnail = draft.thumbnail.trim() || null;
    if (product ? thumbnail !== (product.thumbnail ?? null) : thumbnail !== null)
      body.thumbnail = thumbnail;
    const links = buildLinks(draft.linkSite, draft.linkDocs);
    const prevLinks = product ? buildLinks(product.links?.site ?? "", product.links?.docs ?? "") : null;
    if (JSON.stringify(links) !== JSON.stringify(prevLinks)) body.links = links;
    const detailPath = draft.detailPath.trim() || null;
    if (product ? detailPath !== (product.detailPath ?? null) : detailPath !== null)
      body.detailPath = detailPath;

    if (product && Object.keys(body).length === 0) {
      onDone();
      return;
    }
    setSaving(true);
    setError(null);
    try {
      if (product) await adminApi.patchProduct(product.id, body);
      else await adminApi.createProduct(body);
      onDone();
    } catch (e) {
      setError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
      setSaving(false);
    }
  }

  return (
    <div style={{ ...card, marginBottom: 10, borderColor: "var(--line-2)" }}>
      <div className="mono" style={{ fontSize: 11, letterSpacing: "0.12em", color: "var(--fg-3)", marginBottom: 12 }}>
        {product ? `수정 — ${product.title}` : "새 제품"}
      </div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
          gap: "10px 16px",
        }}
      >
        <label style={{ display: "block" }}>
          <span style={labelStyle}>역할 *</span>
          <select
            value={draft.careerId}
            onChange={(e) => set("careerId", e.target.value)}
            style={{ ...input, appearance: "auto" }}
          >
            <option value="">— 선택 —</option>
            {careers.map((c) => (
              <option key={c.id} value={c.id}>
                {c.companyName} · {c.title}
              </option>
            ))}
          </select>
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>slug *</span>
          <input
            value={draft.slug}
            onChange={(e) => set("slug", e.target.value)}
            placeholder="mediness"
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
            placeholder="web"
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
          <span style={labelStyle}>links.site</span>
          <input
            value={draft.linkSite}
            onChange={(e) => set("linkSite", e.target.value)}
            placeholder="https://…"
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>links.docs</span>
          <input
            value={draft.linkDocs}
            onChange={(e) => set("linkDocs", e.target.value)}
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
          <span style={labelStyle}>detail_path — 상세 md 경로. 비우면 상세 없음</span>
          <input
            value={draft.detailPath}
            onChange={(e) => set("detailPath", e.target.value)}
            placeholder="para/projects/company/mediness/showcase.md"
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
