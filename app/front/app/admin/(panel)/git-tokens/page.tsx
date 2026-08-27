"use client";

import { useCallback, useEffect, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import type { AdminCompany, GitTokenMeta } from "@/lib/types";

// 깃 토큰 — 커밋 수집(잔디)용. 원문은 등록·교체 순간에만 보내고, 서버가 즉시
// 암호화(키는 서버 .env 의 GIT_TOKEN_KEY)한다. 목록엔 구분·계정만 온다.
// 이직하면 회사 토큰의 「교체」로 값만 갈아끼운다 — 레포 연결은 안 바뀐다.
export default function AdminGitTokensPage() {
  const [items, setItems] = useState<GitTokenMeta[] | null>(null);
  const [companies, setCompanies] = useState<AdminCompany[]>([]);
  const [note, setNote] = useState<string | null>(null);

  // 등록 폼 — companyId 는 kind=company 일 때만 쓰고 필수("" = 미선택)
  const [kind, setKind] = useState("personal");
  const [account, setAccount] = useState("");
  const [email, setEmail] = useState("");
  const [token, setToken] = useState("");
  const [formCompanyId, setFormCompanyId] = useState("");
  const [busy, setBusy] = useState(false);

  const reload = useCallback(() => {
    adminApi
      .gitTokens()
      .then(({ items }) => setItems(items))
      .catch((e) => setNote(String(e)));
  }, []);

  useEffect(() => {
    reload();
    // 회사 목록 — company 토큰의 소속 드롭다운 후보. 실패해도 목록은 뜬다.
    adminApi
      .companies()
      .then(({ items }) => setCompanies(items))
      .catch(() => {});
  }, [reload]);

  async function add() {
    if (!account.trim() || !email.trim() || !token.trim()) {
      setNote("계정 id · email · 토큰을 입력하세요");
      return;
    }
    if (kind === "company" && !formCompanyId) {
      setNote("회사를 선택하세요 — company 토큰은 소속이 필수입니다");
      return;
    }
    setBusy(true);
    setNote(null);
    try {
      await adminApi.createGitToken({
        kind,
        account: account.trim(),
        email: email.trim(),
        token: token.trim(),
        ...(kind === "company" ? { companyId: Number(formCompanyId) } : {}),
      });
      setAccount("");
      setEmail("");
      setToken("");
      setFormCompanyId("");
      reload();
    } catch (e) {
      setNote(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    } finally {
      setBusy(false);
    }
  }

  // company 토큰 미연결 행의 즉시 연결 — 고르면 바로 PATCH { companyId }.
  const [linkingId, setLinkingId] = useState<number | null>(null);

  async function linkCompany(t: GitTokenMeta, companyId: number) {
    setLinkingId(t.id);
    setNote(null);
    try {
      await adminApi.patchGitToken(t.id, { companyId });
      reload();
    } catch (e) {
      setNote(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    } finally {
      setLinkingId(null);
    }
  }

  // 교체 — window.prompt 가 안 되는 환경이 있어 행 안에서 인라인 입력으로 받는다.
  const [replacingId, setReplacingId] = useState<number | null>(null);
  const [replaceValue, setReplaceValue] = useState("");

  async function submitReplace(id: number) {
    const next = replaceValue.trim();
    if (!next) {
      setNote("새 토큰 값을 입력하세요");
      return;
    }
    setNote(null);
    try {
      await adminApi.replaceGitToken(id, next);
      setNote("토큰을 교체했습니다 — 레포 연결은 그대로입니다");
      setReplacingId(null);
      setReplaceValue("");
      reload();
    } catch (e) {
      setNote(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    }
  }

  // 삭제 — 확인 없이 즉시. 붙어 있던 레포는 무토큰(공개만 수집)이 된다.
  async function remove(t: GitTokenMeta) {
    setNote(null);
    try {
      await adminApi.deleteGitToken(t.id);
      reload();
    } catch (e) {
      setNote(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    }
  }

  // enabled — 누르면 즉시 PATCH. 꺼진 토큰은 수집에서 무토큰 취급(공개 범위만).
  const [togglingId, setTogglingId] = useState<number | null>(null);

  async function toggleEnabled(t: GitTokenMeta) {
    setTogglingId(t.id);
    setNote(null);
    try {
      await adminApi.patchGitToken(t.id, { enabled: !t.enabled });
      reload();
    } catch (e) {
      setNote(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    } finally {
      setTogglingId(null);
    }
  }

  const input: React.CSSProperties = {
    padding: "8px 10px",
    fontSize: 13,
    background: "var(--bg-2)",
    border: "1px solid var(--line-2)",
    borderRadius: 6,
    color: "var(--fg-0)",
  };
  const ghostBtn: React.CSSProperties = {
    padding: "7px 12px",
    fontSize: 12,
    background: "transparent",
    border: "1px solid var(--line-2)",
    borderRadius: 6,
    color: "var(--fg-1)",
    cursor: "pointer",
  };

  return (
    <div className="admin-page" style={{ padding: "28px 32px", maxWidth: 760, margin: "0 auto" }}>
      <header style={{ marginBottom: 20 }}>
        <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>깃 토큰</h1>
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
          커밋 수집용 GitHub 토큰 — DB 에 암호문으로 저장, 원문은 다시 안 보인다
        </p>
      </header>

      {/* 등록 — 구분 · (company 면 회사) · 계정 id · email · 토큰 */}
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 20 }}>
        <select
          value={kind}
          onChange={(e) => setKind(e.target.value)}
          style={{ ...input, appearance: "auto" }}
        >
          <option value="personal">personal</option>
          <option value="company">company</option>
        </select>
        {kind === "company" && (
          <select
            value={formCompanyId}
            onChange={(e) => setFormCompanyId(e.target.value)}
            style={{ ...input, appearance: "auto" }}
          >
            <option value="">회사 선택 — 필수</option>
            {companies.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        )}
        <input
          value={account}
          onChange={(e) => setAccount(e.target.value)}
          placeholder="깃 계정 id — 예: kknaks"
          style={{ ...input, flex: "1 1 140px" }}
        />
        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="email — 착지 커밋의 git 신원"
          type="email"
          autoComplete="off"
          style={{ ...input, flex: "1 1 180px" }}
        />
        <input
          value={token}
          onChange={(e) => setToken(e.target.value)}
          placeholder="토큰 — ghp_…"
          type="password"
          autoComplete="off"
          style={{ ...input, flex: "2 1 220px" }}
        />
        <button type="button" onClick={add} disabled={busy} style={ghostBtn}>
          {busy ? "등록 중…" : "+ 등록"}
        </button>
      </div>

      {/* 목록 */}
      {!items && !note && (
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>불러오는 중…</p>
      )}
      {items && items.length === 0 && (
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          등록된 토큰이 없습니다 — 등록하면 레포 폼의 토큰 셀렉트에 뜹니다
        </p>
      )}
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        {items?.map((t) => (
          <div
            key={t.id}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10,
              border: "1px solid var(--line-1)",
              borderRadius: 6,
              padding: "10px 12px",
              background: "var(--bg-2)",
            }}
          >
            <span
              className="mono"
              style={{
                fontSize: 10,
                letterSpacing: "0.08em",
                border: "1px solid var(--line-1)",
                borderRadius: 4,
                padding: "1px 6px",
                color: t.kind === "company" ? "var(--accent)" : "var(--fg-2)",
              }}
            >
              {t.kind}
            </span>
            <span className="mono" style={{ fontSize: 13, color: "var(--fg-0)", fontWeight: 600 }}>
              {t.account}
            </span>
            {/* company 토큰의 소속 — 연결이면 회사명 뱃지, 미연결이면 즉시 연결 select */}
            {t.kind === "company" &&
              (t.companyId != null ? (
                <span
                  className="mono"
                  style={{
                    fontSize: 10,
                    letterSpacing: "0.04em",
                    border: "1px solid var(--accent)",
                    borderRadius: 999,
                    padding: "1px 8px",
                    color: "var(--accent)",
                    background: "var(--accent-soft)",
                  }}
                >
                  {t.companyName ?? `#${t.companyId}`}
                </span>
              ) : (
                <select
                  value=""
                  disabled={linkingId === t.id}
                  onChange={(e) => {
                    if (e.target.value) linkCompany(t, Number(e.target.value));
                  }}
                  className="mono"
                  style={{ ...input, appearance: "auto", padding: "3px 6px", fontSize: 11 }}
                  title="미연결 — 회사를 고르면 즉시 연결됩니다"
                >
                  <option value="">회사 연결…</option>
                  {companies.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
              ))}
            <span className="mono" style={{ fontSize: 11, color: "var(--fg-2)" }}>
              {t.email}
            </span>
            <span className="mono" style={{ fontSize: 10, color: "var(--fg-3)" }}>
              {t.createdAt ? `등록 ${t.createdAt.slice(0, 10)}` : ""}
            </span>
            <div style={{ marginLeft: "auto", display: "flex", gap: 6, alignItems: "center" }}>
              {replacingId === t.id ? (
                <>
                  <input
                    value={replaceValue}
                    onChange={(e) => setReplaceValue(e.target.value)}
                    placeholder="새 토큰 — ghp_…"
                    type="password"
                    autoComplete="off"
                    autoFocus
                    style={{ ...input, padding: "6px 8px", fontSize: 12, width: 200 }}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") submitReplace(t.id);
                      if (e.key === "Escape") setReplacingId(null);
                    }}
                  />
                  <button type="button" onClick={() => submitReplace(t.id)} style={ghostBtn}>
                    저장
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setReplacingId(null);
                      setReplaceValue("");
                    }}
                    style={ghostBtn}
                  >
                    취소
                  </button>
                </>
              ) : (
                <>
                  {/* enabled — repo-section 의 pill 패턴. 누르면 즉시 PATCH. */}
                  <button
                    type="button"
                    onClick={() => toggleEnabled(t)}
                    disabled={togglingId === t.id}
                    title={t.enabled ? "활성 — 누르면 무토큰 취급" : "비활성 — 누르면 다시 사용"}
                    className="mono"
                    style={{
                      fontSize: 10,
                      letterSpacing: "0.08em",
                      padding: "3px 9px",
                      borderRadius: 999,
                      cursor: "pointer",
                      border: t.enabled ? "1px solid var(--accent)" : "1px solid var(--line-2)",
                      background: t.enabled ? "var(--accent-soft)" : "transparent",
                      color: t.enabled ? "var(--accent)" : "var(--fg-3)",
                    }}
                  >
                    {t.enabled ? "enabled" : "disabled"}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setReplacingId(t.id);
                      setReplaceValue("");
                    }}
                    style={ghostBtn}
                  >
                    교체
                  </button>
                  <button
                    type="button"
                    onClick={() => remove(t)}
                    style={{ ...ghostBtn, color: "var(--danger, #e5534b)" }}
                  >
                    삭제
                  </button>
                </>
              )}
            </div>
          </div>
        ))}
      </div>

      {note && (
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-2)", marginTop: 12 }}>{note}</p>
      )}
    </div>
  );
}
