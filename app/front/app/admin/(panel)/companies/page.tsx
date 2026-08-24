"use client";

import { useCallback, useEffect, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import type { AdminCompany, CompanyInput } from "@/lib/types";

// 커리어 · 회사 — 등록·수정·삭제. 역할 수·기간은 career 파생값이라 여기선 읽기 전용.
export default function AdminCompaniesPage() {
  const [items, setItems] = useState<AdminCompany[] | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [adding, setAdding] = useState(false);

  const reload = useCallback(() => {
    adminApi
      .companies()
      .then(({ items }) => setItems(items))
      .catch((e) => setLoadError(String(e)));
  }, []);

  useEffect(reload, [reload]);

  if (loadError) {
    return (
      <div className="admin-page" style={{ padding: "28px 32px" }}>
        <p className="mono" style={{ fontSize: 12, color: "var(--danger, #e5534b)" }}>
          회사 목록을 불러오지 못했습니다 — {loadError}
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
          <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>회사</h1>
          <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
            company — 역할·제품이 여기 매달린다
          </p>
        </div>
        <button type="button" onClick={() => setAdding((a) => !a)} style={primaryBtn(!adding)}>
          {adding ? "닫기" : "+ 회사 추가"}
        </button>
      </header>

      {adding && (
        <CompanyForm
          onDone={() => {
            setAdding(false);
            reload();
          }}
          onCancel={() => setAdding(false)}
        />
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {items.map((c) => (
          <CompanyCard key={c.id} company={c} onChanged={reload} />
        ))}
      </div>
    </div>
  );
}

/* ── 카드 ───────────────────────────────────────────────────────────── */

function CompanyCard({
  company,
  onChanged,
}: {
  company: AdminCompany;
  onChanged: () => void;
}) {
  const [editing, setEditing] = useState(false);
  const [deleteError, setDeleteError] = useState<string | null>(null);

  async function remove() {
    if (!window.confirm(`「${company.name}」 을(를) 삭제할까요?`)) return;
    try {
      await adminApi.deleteCompany(company.id);
      onChanged();
    } catch (e) {
      setDeleteError(e instanceof AuthError ? e.message : String(e));
    }
  }

  if (editing) {
    return (
      <CompanyForm
        company={company}
        onDone={() => {
          setEditing(false);
          onChanged();
        }}
        onCancel={() => setEditing(false)}
      />
    );
  }

  const hasCareers = company.careerCount > 0;

  return (
    <div style={card}>
      <div style={{ display: "flex", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
        {company.logoUrl && (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={company.logoUrl}
            alt=""
            width={36}
            height={36}
            style={{ borderRadius: 6, border: "1px solid var(--line-1)", objectFit: "cover" }}
          />
        )}
        <div style={{ minWidth: 0 }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 8, flexWrap: "wrap" }}>
            <span style={{ fontSize: 15, color: "var(--fg-0)", fontWeight: 600 }}>
              {company.name}
            </span>
            <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
              {company.slug}
            </span>
          </div>
          <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginTop: 2 }}>
            {[company.location, company.site].filter(Boolean).join(" · ")}
          </div>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 8 }}>
          <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
            역할 {company.careerCount}
            {company.period ? ` · ${company.period}` : ""}
          </span>
          <button type="button" onClick={() => setEditing(true)} style={ghostBtn}>
            수정
          </button>
          <button
            type="button"
            onClick={remove}
            disabled={hasCareers}
            title={hasCareers ? "역할을 먼저 지우세요" : undefined}
            style={{
              ...ghostBtn,
              color: hasCareers ? "var(--fg-4)" : "var(--danger, #e5534b)",
              cursor: hasCareers ? "default" : "pointer",
            }}
          >
            삭제
          </button>
        </div>
      </div>

      {company.description && (
        <p style={{ fontSize: 13, color: "var(--fg-2)", lineHeight: 1.6, margin: "10px 0 0" }}>
          {company.description}
        </p>
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

type DraftKey = "slug" | "name" | "description" | "location" | "site" | "logoUrl";
const FIELDS: { key: DraftKey; label: string; required?: boolean; textarea?: boolean }[] = [
  { key: "slug", label: "slug", required: true },
  { key: "name", label: "이름", required: true },
  { key: "location", label: "위치" },
  { key: "site", label: "site" },
  { key: "logoUrl", label: "로고 경로" },
  { key: "description", label: "소개", textarea: true },
];

function CompanyForm({
  company,
  onDone,
  onCancel,
}: {
  company?: AdminCompany;
  onDone: () => void;
  onCancel: () => void;
}) {
  const [draft, setDraft] = useState<Record<DraftKey, string>>({
    slug: company?.slug ?? "",
    name: company?.name ?? "",
    description: company?.description ?? "",
    location: company?.location ?? "",
    site: company?.site ?? "",
    logoUrl: company?.logoUrl ?? "",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function save() {
    if (!draft.slug.trim() || !draft.name.trim()) {
      setError("slug 과 이름은 비울 수 없습니다");
      return;
    }
    // 바뀐 필드만 담는다 — 안 보낸 것과 null 은 다르다. 빈 nullable 은 null 로.
    const body: CompanyInput = {};
    for (const { key, required } of FIELDS) {
      const next = draft[key].trim();
      const prev = company?.[key] ?? "";
      if (company && next === prev) continue;
      if (!next && !required) {
        // required 가드 뒤라 nullable 키만 남는다 — slug·name 은 여기 못 온다.
        if (company) body[key as Exclude<DraftKey, "slug" | "name">] = null;
        continue;
      }
      body[key] = next;
    }
    if (company && Object.keys(body).length === 0) {
      onDone();
      return;
    }
    setSaving(true);
    setError(null);
    try {
      if (company) await adminApi.patchCompany(company.id, body);
      else await adminApi.createCompany(body);
      onDone();
    } catch (e) {
      setError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
      setSaving(false);
    }
  }

  return (
    <div style={{ ...card, marginBottom: 10, borderColor: "var(--line-2)" }}>
      <div className="mono" style={{ fontSize: 11, letterSpacing: "0.12em", color: "var(--fg-3)", marginBottom: 12 }}>
        {company ? `수정 — ${company.name}` : "새 회사"}
      </div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
          gap: "10px 16px",
        }}
      >
        {FIELDS.filter((f) => !f.textarea).map(({ key, label, required }) => (
          <label key={key} style={{ display: "block" }}>
            <span className="mono" style={{ fontSize: 10, letterSpacing: "0.08em", color: "var(--fg-4)" }}>
              {label}
              {required ? " *" : ""}
            </span>
            <input
              value={draft[key]}
              onChange={(e) => setDraft((d) => ({ ...d, [key]: e.target.value }))}
              style={input}
            />
          </label>
        ))}
      </div>
      {FIELDS.filter((f) => f.textarea).map(({ key, label }) => (
        <label key={key} style={{ display: "block", marginTop: 10 }}>
          <span className="mono" style={{ fontSize: 10, letterSpacing: "0.08em", color: "var(--fg-4)" }}>
            {label}
          </span>
          <textarea
            value={draft[key]}
            onChange={(e) => setDraft((d) => ({ ...d, [key]: e.target.value }))}
            rows={3}
            style={{ ...input, resize: "vertical" }}
          />
        </label>
      ))}

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
