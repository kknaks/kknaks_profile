"use client";

import { useEffect, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import type { SiteConfigItem } from "@/lib/types";

// 프로필 · 사이트 문구 — site_config 행 그대로 (key · value · note).
// 항목별 편집 — 바뀐 필드(value·note)만 PATCH /api/admin/site-config/{key} 로 보낸다.
export default function AdminSiteConfigPage() {
  const [items, setItems] = useState<SiteConfigItem[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    adminApi
      .siteConfig()
      .then(({ items }) => setItems(items))
      .catch((e) => setError(String(e)));
  }, []);

  if (error) {
    return (
      <div style={{ padding: "28px 32px" }}>
        <p className="mono" style={{ fontSize: 12, color: "var(--danger, #e5534b)" }}>
          사이트 문구를 불러오지 못했습니다 — {error}
        </p>
      </div>
    );
  }

  if (!items) {
    return (
      <div style={{ padding: "28px 32px" }}>
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          불러오는 중…
        </p>
      </div>
    );
  }

  return (
    <div className="admin-page" style={{ padding: "28px 32px", maxWidth: 960, margin: "0 auto" }}>
      <header style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>사이트 문구</h1>
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
          site_config — 히어로 · 소개 · 카드 · footer. key 는{" "}
          <span style={{ color: "var(--fg-1)" }}>&lt;표면&gt;.&lt;자리&gt;</span>
        </p>
      </header>

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {items.map((item) => (
          <ItemEditor key={item.key} item={item} />
        ))}
      </div>
    </div>
  );
}

/* ── 항목 하나 ──────────────────────────────────────────────────────── */

/** 문자열은 문장 textarea, 구조(배열·객체)는 JSON textarea — 저장 전에 parse 검증. */
function ItemEditor({ item }: { item: SiteConfigItem }) {
  const isString = typeof item.value === "string";

  // 서버가 마지막으로 확인해 준 값 — dirty 판정의 기준.
  const [savedValueText, setSavedValueText] = useState(() =>
    isString ? (item.value as string) : JSON.stringify(item.value, null, 2),
  );
  const [savedNote, setSavedNote] = useState(item.note ?? "");

  const [valueText, setValueText] = useState(savedValueText);
  const [noteText, setNoteText] = useState(savedNote);

  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [itemError, setItemError] = useState<string | null>(null);

  const dirty = valueText !== savedValueText || noteText !== savedNote;

  async function save() {
    const body: { value?: unknown; note?: string | null } = {};

    if (valueText !== savedValueText) {
      if (isString) {
        body.value = valueText;
      } else {
        try {
          body.value = JSON.parse(valueText);
        } catch {
          setItemError("JSON 이 아닙니다 — 저장하지 않았습니다");
          return;
        }
      }
    }
    if (noteText !== savedNote) {
      body.note = noteText.trim() ? noteText : null;
    }
    if (Object.keys(body).length === 0) return;

    setSaving(true);
    setItemError(null);
    try {
      const next = await adminApi.patchSiteConfig(item.key, body);
      const nextValueText =
        typeof next.value === "string"
          ? next.value
          : JSON.stringify(next.value, null, 2);
      setSavedValueText(nextValueText);
      setSavedNote(next.note ?? "");
      setValueText(nextValueText);
      setNoteText(next.note ?? "");
      setSaved(true);
    } catch (e) {
      setItemError(
        e instanceof AuthError ? `${e.status} — ${e.message}` : String(e),
      );
    } finally {
      setSaving(false);
    }
  }

  return (
    <div
      style={{
        border: "1px solid var(--line-1)",
        borderRadius: 8,
        padding: "14px 16px",
        background: "var(--bg-1)",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "baseline",
          gap: 10,
          marginBottom: 8,
          flexWrap: "wrap",
        }}
      >
        <span className="mono" style={{ fontSize: 12.5, color: "var(--accent)" }}>
          {item.key}
        </span>
        {!isString && (
          <span className="mono" style={{ fontSize: 10, color: "var(--fg-4)" }}>
            JSON
          </span>
        )}
        <span style={{ flex: 1 }} />
        {itemError && (
          <span className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)" }}>
            {itemError}
          </span>
        )}
        {saved && !dirty && !itemError && (
          <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
            저장됨
          </span>
        )}
        <button
          type="button"
          onClick={save}
          disabled={saving || !dirty}
          className="mono"
          style={{
            fontSize: 11,
            padding: "4px 12px",
            borderRadius: 5,
            border: "1px solid var(--line-2)",
            background: dirty ? "var(--fg-0)" : "var(--bg-2)",
            color: dirty ? "var(--bg-0)" : "var(--fg-4)",
            cursor: saving || !dirty ? "default" : "pointer",
          }}
        >
          {saving ? "저장 중…" : "저장"}
        </button>
      </div>

      <textarea
        value={valueText}
        onChange={(e) => {
          setValueText(e.target.value);
          setSaved(false);
          setItemError(null);
        }}
        rows={isString ? Math.max(2, valueText.split("\n").length) : Math.min(14, Math.max(4, valueText.split("\n").length))}
        spellCheck={false}
        className={isString ? undefined : "mono"}
        style={{
          width: "100%",
          boxSizing: "border-box",
          fontSize: isString ? 13.5 : 11.5,
          lineHeight: 1.6,
          color: isString ? "var(--fg-1)" : "var(--fg-2)",
          background: "var(--bg-2)",
          border: `1px solid ${itemError ? "var(--danger, #e5534b)" : "var(--line-1)"}`,
          borderRadius: 6,
          padding: "10px 12px",
          resize: "vertical",
          outline: "none",
        }}
      />

      <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 8 }}>
        <span
          className="mono"
          style={{ fontSize: 10, letterSpacing: "0.08em", color: "var(--fg-4)", flexShrink: 0 }}
        >
          note
        </span>
        <input
          type="text"
          value={noteText}
          onChange={(e) => {
            setNoteText(e.target.value);
            setSaved(false);
            setItemError(null);
          }}
          placeholder="어디에 쓰이는지"
          style={{
            flex: 1,
            fontSize: 11.5,
            color: "var(--fg-3)",
            background: "var(--bg-2)",
            border: "1px solid var(--line-1)",
            borderRadius: 5,
            padding: "5px 10px",
            outline: "none",
          }}
        />
      </div>
    </div>
  );
}
