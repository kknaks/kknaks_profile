"use client";

import { useCallback, useEffect, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import { ChatExposureToggle } from "@/components/admin/chat-exposure-toggle";
import type { AdminCareer, AdminProblem, AdminProduct, ProblemInput } from "@/lib/types";

// 해결한 문제 — 등록·수정·삭제. problem 은 career 에 속한다(erd.md §problem) —
// 「회사명 · 역할명」·제품명은 조인 파생 표시값이라 읽기 전용, 수정은 careerId·productId 로 한다.
// 이력서의 알맹이다 — 자동 파이프라인(케이스 6 게이트)이 서기 전까지는 여기서 수동 등록한다.
export default function AdminProblemsPage() {
  const [items, setItems] = useState<AdminProblem[] | null>(null);
  const [careers, setCareers] = useState<AdminCareer[] | null>(null);
  const [products, setProducts] = useState<AdminProduct[] | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [adding, setAdding] = useState(false);

  const reload = useCallback(() => {
    adminApi
      .problems()
      .then(({ items }) => setItems(items))
      .catch((e) => setLoadError(String(e)));
  }, []);

  useEffect(() => {
    reload();
    // 폼의 드롭다운 — 문제는 역할 없이 못 만들고, 제품은 그 역할의 것만 붙는다.
    adminApi
      .careers()
      .then(({ items }) => setCareers(items))
      .catch((e) => setLoadError(String(e)));
    adminApi
      .products()
      .then(({ items }) => setProducts(items))
      .catch((e) => setLoadError(String(e)));
  }, [reload]);

  if (loadError) {
    return (
      <div className="admin-page" style={{ padding: "28px 32px" }}>
        <p className="mono" style={{ fontSize: 12, color: "var(--danger, #e5534b)" }}>
          문제 목록을 불러오지 못했습니다 — {loadError}
        </p>
      </div>
    );
  }

  if (!items || !careers || !products) {
    return (
      <div className="admin-page" style={{ padding: "28px 32px" }}>
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          불러오는 중…
        </p>
      </div>
    );
  }

  // 역할별로 묶는다 — 서버가 이미 career.started_on DESC · display_order ASC 로
  // 내려주므로 만난 순서대로 묶기만 하면 그룹 순서가 유지된다.
  const groups: { careerId: number; label: string; items: AdminProblem[] }[] = [];
  for (const p of items) {
    const last = groups[groups.length - 1];
    if (last && last.careerId === p.careerId) last.items.push(p);
    else
      groups.push({
        careerId: p.careerId,
        label: `${p.companyName} · ${p.careerTitle}`,
        items: [p],
      });
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
          <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>해결한 문제</h1>
          <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
            problem — 그 역할에서 푼 문제. 이력서의 알맹이다
          </p>
        </div>
        <button type="button" onClick={() => setAdding((a) => !a)} style={primaryBtn(!adding)}>
          {adding ? "닫기" : "+ 문제 추가"}
        </button>
      </header>

      {adding && (
        <ProblemForm
          careers={careers}
          products={products}
          onDone={() => {
            setAdding(false);
            reload();
          }}
          onCancel={() => setAdding(false)}
        />
      )}

      {groups.length === 0 && !adding && (
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          아직 등록된 문제가 없습니다
        </p>
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: 22 }}>
        {groups.map((g) => (
          <section key={g.careerId}>
            <div
              className="mono"
              style={{
                fontSize: 11,
                letterSpacing: "0.1em",
                color: "var(--fg-3)",
                paddingBottom: 6,
                marginBottom: 10,
                borderBottom: "1px solid var(--line-1)",
              }}
            >
              {g.label}
              <span style={{ color: "var(--fg-4)", marginLeft: 8 }}>{g.items.length}건</span>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {g.items.map((p) => (
                <ProblemCard
                  key={p.id}
                  problem={p}
                  careers={careers}
                  products={products}
                  onChanged={reload}
                />
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}

/* ── 카드 ───────────────────────────────────────────────────────────── */

/** body 미리보기 — 카드가 본문 전체를 삼키지 않게 자른다. */
const PREVIEW_LEN = 200;
const preview = (body: string) =>
  body.length > PREVIEW_LEN ? `${body.slice(0, PREVIEW_LEN).trimEnd()}…` : body;

function ProblemCard({
  problem,
  careers,
  products,
  onChanged,
}: {
  problem: AdminProblem;
  careers: AdminCareer[];
  products: AdminProduct[];
  onChanged: () => void;
}) {
  const [editing, setEditing] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  async function remove() {
    if (!window.confirm(`「${problem.title}」 을(를) 삭제할까요?`)) return;
    try {
      await adminApi.deleteProblem(problem.id);
      onChanged();
    } catch (e) {
      setActionError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    }
  }

  if (editing) {
    return (
      <ProblemForm
        problem={problem}
        careers={careers}
        products={products}
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
              {problem.title}
            </span>
            {problem.productTitle && (
              <span
                className="mono"
                title="이 문제가 나온 제품"
                style={{
                  fontSize: 10,
                  letterSpacing: "0.08em",
                  color: "var(--accent)",
                  border: "1px solid var(--line-1)",
                  borderRadius: 4,
                  padding: "1px 6px",
                  background: "var(--accent-soft)",
                }}
              >
                {problem.productTitle}
              </span>
            )}
          </div>
          <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginTop: 2 }}>
            {problem.companyName} · {problem.careerTitle}
            <span style={{ color: "var(--fg-4)" }}> · order {problem.displayOrder}</span>
          </div>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 8 }}>
          {/* 채팅 노출 — 켠 것만 AI tool 응답에 실린다(SPEC-017 U-7). */}
          <ChatExposureToggle kind="problem" id={problem.id} exposed={problem.chatExposed} />
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

      {problem.body && (
        <p
          style={{
            fontSize: 13,
            color: "var(--fg-2)",
            lineHeight: 1.6,
            margin: "10px 0 0",
            whiteSpace: "pre-line",
          }}
        >
          {preview(problem.body)}
        </p>
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
  careerId: string; // select value — "" = 미선택
  productId: string; // "" = 없음(제품에 매이지 않은 문제)
  title: string;
  body: string;
  displayOrder: string; // input type="number" — "" 는 0 으로 보낸다
};

function ProblemForm({
  problem,
  careers,
  products,
  onDone,
  onCancel,
}: {
  problem?: AdminProblem;
  careers: AdminCareer[];
  products: AdminProduct[];
  onDone: () => void;
  onCancel: () => void;
}) {
  const [draft, setDraft] = useState<Draft>({
    careerId: problem ? String(problem.careerId) : "",
    productId: problem?.productId != null ? String(problem.productId) : "",
    title: problem?.title ?? "",
    body: problem?.body ?? "",
    displayOrder: problem ? String(problem.displayOrder) : "0",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const set = <K extends keyof Draft>(key: K, value: string) =>
    setDraft((d) => ({ ...d, [key]: value }));

  // 그 역할의 제품만 — 서버도 소속을 검증하지만(422) 화면이 먼저 거른다.
  const careerProducts = draft.careerId
    ? products.filter((p) => p.careerId === Number(draft.careerId))
    : [];

  async function save() {
    if (!draft.careerId || !draft.title.trim()) {
      setError("역할·제목은 비울 수 없습니다");
      return;
    }
    // 바뀐 필드만 담는다 — 안 보낸 것과 null(productId 연결 해제) 은 다르다.
    const body: ProblemInput = {};
    const careerId = Number(draft.careerId);
    if (!problem || careerId !== problem.careerId) body.careerId = careerId;
    const productId = draft.productId ? Number(draft.productId) : null;
    if (problem ? productId !== (problem.productId ?? null) : productId !== null)
      body.productId = productId;
    const title = draft.title.trim();
    if (!problem || title !== problem.title) body.title = title;
    const bodyText = draft.body.trim() || null;
    if (problem ? bodyText !== (problem.body ?? null) : bodyText !== null)
      body.body = bodyText;
    const displayOrder = draft.displayOrder === "" ? 0 : Number(draft.displayOrder);
    if (!problem || displayOrder !== problem.displayOrder) body.displayOrder = displayOrder;

    if (problem && Object.keys(body).length === 0) {
      onDone();
      return;
    }
    setSaving(true);
    setError(null);
    try {
      if (problem) await adminApi.patchProblem(problem.id, body);
      else await adminApi.createProblem(body);
      onDone();
    } catch (e) {
      setError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
      setSaving(false);
    }
  }

  return (
    <div style={{ ...card, marginBottom: 10, borderColor: "var(--line-2)" }}>
      <div className="mono" style={{ fontSize: 11, letterSpacing: "0.12em", color: "var(--fg-3)", marginBottom: 12 }}>
        {problem ? `수정 — ${problem.title}` : "새 문제"}
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
            onChange={(e) =>
              // 역할이 바뀌면 제품 선택은 초기화 — 그 역할의 제품만 보인다.
              setDraft((d) => ({ ...d, careerId: e.target.value, productId: "" }))
            }
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
          <span style={labelStyle}>제품 — 조직·프로세스 문제면 「없음」</span>
          <select
            value={draft.productId}
            onChange={(e) => set("productId", e.target.value)}
            disabled={!draft.careerId}
            style={{ ...input, appearance: "auto", opacity: draft.careerId ? 1 : 0.5 }}
          >
            <option value="">— 없음 —</option>
            {careerProducts.map((p) => (
              <option key={p.id} value={p.id}>
                {p.title}
              </option>
            ))}
          </select>
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>제목 * — 무엇을 풀었나</span>
          <input
            value={draft.title}
            onChange={(e) => set("title", e.target.value)}
            maxLength={128}
            style={input}
          />
        </label>
        <label style={{ display: "block" }}>
          <span style={labelStyle}>순서 — 역할 안에서 작은 것 먼저</span>
          <input
            type="number"
            value={draft.displayOrder}
            onChange={(e) => set("displayOrder", e.target.value)}
            style={input}
          />
        </label>
      </div>
      <label style={{ display: "block", marginTop: 10 }}>
        <span style={labelStyle}>body — 어떻게 풀었나</span>
        <textarea
          value={draft.body}
          onChange={(e) => set("body", e.target.value)}
          rows={5}
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
