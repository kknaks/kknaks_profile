"use client";

import { useCallback, useEffect, useState } from "react";
import { adminApi, AuthError } from "@/lib/api";
import type {
  AdminRepo,
  GithubOwnerOption,
  GithubRepoOption,
  GitTokenMeta,
  RepoInput,
} from "@/lib/types";

// 레포 — 커밋을 긁을 GitHub 레포(erd.md §repo). 잔디의 원천이다(케이스 6·7).
// 레포는 제품/프로젝트의 **속성**이라 별도 페이지가 아니라 그 폼 안에서 등록한다.
// 행 조작(토글·삭제)은 즉시 API 호출 — 제품/프로젝트 저장 버튼과 무관하다.
// 등록은 「+ 레포 연결」 모달 — owner 후보는 폼 스코프대로만 온다(회사 제품 폼은
// 그 회사 것만, 개인 폼은 personal 만). 삭제하면 커밋이 CASCADE 로 쓸려간다.
export function RepoSection({
  productId,
  projectId,
}: {
  productId?: number;
  projectId?: number;
}) {
  const [repos, setRepos] = useState<AdminRepo[] | null>(null);
  // 전체 등록 slug — repo.slug 는 전역 UK 라 모달이 「이미 등록됨」을 전역으로 본다.
  const [registeredSlugs, setRegisteredSlugs] = useState<Set<string>>(new Set());
  const [tokens, setTokens] = useState<GitTokenMeta[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [collecting, setCollecting] = useState(false);
  const [note, setNote] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const reload = useCallback(() => {
    // 목록 API 는 전체 반환 — 이 제품/프로젝트 것만 걸러 보여준다.
    adminApi
      .repos()
      .then(({ items }) => {
        setRepos(
          items.filter((r) =>
            productId != null ? r.productId === productId : r.projectId === projectId,
          ),
        );
        setRegisteredSlugs(new Set(items.map((r) => r.slug)));
      })
      .catch((e) => setLoadError(String(e)));
    // 토큰 목록 — 행의 토큰 셀렉트 + 모달의 직접 입력 폴백용.
    adminApi
      .gitTokens()
      .then(({ items }) => setTokens(items))
      .catch(() => setTokens([]));
  }, [productId, projectId]);

  useEffect(() => {
    reload();
  }, [reload]);

  async function collectNow() {
    setCollecting(true);
    setNote(null);
    try {
      const { started } = await adminApi.collectRepos();
      setNote(
        started
          ? "수집을 걸었습니다 — 전체 레포 대상. 잠시 뒤 목록이 갱신됩니다"
          : "이미 수집이 돌고 있습니다",
      );
      // 202 즉시 반환 — 짧은 레포는 몇 초면 끝난다. 조금 뒤 재조회.
      setTimeout(reload, 4000);
    } catch (e) {
      setNote(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    } finally {
      setCollecting(false);
    }
  }

  return (
    <div style={{ marginTop: 16, paddingTop: 14, borderTop: "1px solid var(--line-1)" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
        <span
          className="mono"
          style={{ fontSize: 11, letterSpacing: "0.12em", color: "var(--fg-3)" }}
        >
          레포 — 커밋 수집 대상 · 즉시 반영
        </span>
        <button
          type="button"
          onClick={collectNow}
          disabled={collecting}
          style={{ ...ghostBtn, marginLeft: "auto" }}
        >
          {collecting ? "거는 중…" : "지금 수집"}
        </button>
      </div>

      {loadError && (
        <p className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "10px 0 0" }}>
          레포 목록을 불러오지 못했습니다 — {loadError}
        </p>
      )}

      {!repos && !loadError && (
        <p className="mono" style={{ fontSize: 11, color: "var(--fg-3)", margin: "10px 0 0" }}>
          불러오는 중…
        </p>
      )}

      {repos && (
        <div style={{ display: "flex", flexDirection: "column", gap: 6, marginTop: 10 }}>
          {repos.length === 0 && (
            <p className="mono" style={{ fontSize: 11, color: "var(--fg-3)", margin: 0 }}>
              연결된 레포가 없습니다 — 연결하면 다음 수집부터 잔디에 쌓입니다
            </p>
          )}
          {repos.map((r) => (
            <RepoRow key={r.id} repo={r} tokens={tokens} onChanged={reload} />
          ))}
        </div>
      )}

      {/* 등록은 모달로 — 연결은 이 폼의 제품/프로젝트로 고정된다. */}
      <div style={{ marginTop: 10 }}>
        <button type="button" onClick={() => setModalOpen(true)} style={ghostBtn}>
          + 레포 연결
        </button>
      </div>

      {note && (
        <p className="mono" style={{ fontSize: 11, color: "var(--fg-2)", margin: "8px 0 0" }}>
          {note}
        </p>
      )}

      {modalOpen && (
        <RepoConnectModal
          productId={productId}
          projectId={projectId}
          tokens={tokens}
          registeredSlugs={registeredSlugs}
          onDone={() => {
            setModalOpen(false);
            reload();
          }}
          onCancel={() => setModalOpen(false)}
        />
      )}
    </div>
  );
}

/* ── 레포 연결 모달 — owner 라디오 → [레포 불러오기] → 체크박스 → 저장 ── */

/** GitHub ISO → `2026.08.25`. 없으면 빈 문자열. */
function fmtDate(iso?: string | null): string {
  if (!iso) return "";
  const d = new Date(iso);
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}.${p(d.getMonth() + 1)}.${p(d.getDate())}`;
}

function RepoConnectModal({
  productId,
  projectId,
  tokens,
  registeredSlugs,
  onDone,
  onCancel,
}: {
  productId?: number;
  projectId?: number;
  tokens: GitTokenMeta[];
  registeredSlugs: Set<string>;
  onDone: () => void;
  onCancel: () => void;
}) {
  // owner 후보 — 폼 스코프대로만 온다. "manual" 은 「직접 입력…」 폴백.
  const [owners, setOwners] = useState<GithubOwnerOption[] | null>(null);
  const [ownersError, setOwnersError] = useState<string | null>(null);
  const [mode, setMode] = useState<number | "manual" | null>(null);

  // 불러온 레포 목록 + 체크 상태
  const [repoList, setRepoList] = useState<GithubRepoOption[] | null>(null);
  const [loadingRepos, setLoadingRepos] = useState(false);
  const [repoError, setRepoError] = useState<string | null>(null);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  // 검색 — 레포가 100개씩 온다. 이름 부분일치로 거른다(체크 상태는 유지).
  const [repoQuery, setRepoQuery] = useState("");

  // 직접 입력 모드 — 기존 인라인 행과 같은 재료(owner/name + 토큰 셀렉트)
  const [manualOwner, setManualOwner] = useState("");
  const [manualName, setManualName] = useState("");
  const [manualTokenId, setManualTokenId] = useState("");

  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  // 저장 도중 일부만 성공하고 실패했을 때 — 성공분을 재저장에서 뺀다.
  const [justCreated, setJustCreated] = useState<Set<string>>(new Set());

  useEffect(() => {
    adminApi
      .githubOwners(productId != null ? { productId } : { projectId })
      .then(({ items }) => {
        setOwners(items);
        if (items.length > 0) setMode(0);
      })
      .catch((e) =>
        setOwnersError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e)),
      );
  }, [productId, projectId]);

  function pickMode(next: number | "manual") {
    setMode(next);
    setRepoList(null);
    setRepoError(null);
    setSelected(new Set());
    setSaveError(null);
  }

  async function fetchRepos() {
    if (typeof mode !== "number" || !owners) return;
    const owner = owners[mode];
    setLoadingRepos(true);
    setRepoError(null);
    setRepoList(null);
    setSelected(new Set());
    setRepoQuery("");
    try {
      const { items } = await adminApi.githubRepos(owner.owner, owner.tokenId);
      setRepoList(items);
    } catch (e) {
      setRepoError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    } finally {
      setLoadingRepos(false);
    }
  }

  function toggle(slug: string) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(slug)) next.delete(slug);
      else next.add(slug);
      return next;
    });
  }

  const isRegistered = (slug: string) => registeredSlugs.has(slug) || justCreated.has(slug);

  const parentBody: Pick<RepoInput, "productId" | "projectId"> =
    productId != null ? { productId } : { projectId };

  async function save() {
    setSaveError(null);
    if (mode === "manual") {
      const slug = `${manualOwner.trim()}/${manualName.trim()}`;
      if (!/^[^/\s]+\/[^/\s]+$/.test(slug)) {
        setSaveError("owner 와 name 을 채우세요 — 예: kknaks / wine-log");
        return;
      }
      setSaving(true);
      try {
        const body: RepoInput = { slug, ...parentBody };
        if (manualTokenId) body.gitTokenId = Number(manualTokenId);
        await adminApi.createRepo(body);
        onDone();
      } catch (e) {
        setSaveError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
        setSaving(false);
      }
      return;
    }
    if (typeof mode !== "number" || !owners) return;
    const tokenId = owners[mode].tokenId;
    const slugs = [...selected].filter((s) => !isRegistered(s));
    if (slugs.length === 0) return;
    setSaving(true);
    // 순차 생성 — 하나가 실패하면 거기서 멈추고, 성공분은 등록된 것으로 표시한다.
    const created = new Set(justCreated);
    try {
      for (const slug of slugs) {
        const body: RepoInput = { slug, ...parentBody };
        if (tokenId != null) body.gitTokenId = tokenId;
        await adminApi.createRepo(body);
        created.add(slug);
      }
      onDone();
    } catch (e) {
      setJustCreated(created);
      setSelected((prev) => {
        const next = new Set(prev);
        created.forEach((s) => next.delete(s));
        return next;
      });
      setSaveError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
      setSaving(false);
    }
  }

  // 하나라도 만들었으면 닫기도 저장 완료 취급 — 부모 목록을 갱신해야 한다.
  const close = () => (justCreated.size > 0 ? onDone() : onCancel());

  const selectableCount = [...selected].filter((s) => !isRegistered(s)).length;
  const saveDisabled =
    saving ||
    (mode === "manual"
      ? !manualOwner.trim() || !manualName.trim()
      : selectableCount === 0);
  const saveLabel =
    mode === "manual" ? "저장 — 1개 연결" : `저장 — ${selectableCount}개 연결`;

  return (
    <div
      onClick={close}
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 50,
        background: "rgba(0, 0, 0, 0.55)",
        display: "flex",
        alignItems: "flex-start",
        justifyContent: "center",
        padding: "10vh 16px 16px",
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          width: "100%",
          maxWidth: 560,
          background: "var(--bg-1)",
          border: "1px solid var(--line-2)",
          borderRadius: 10,
          boxShadow: "var(--shadow-pop)",
        }}
      >
        {/* 머리 */}
        <div
          style={{
            display: "flex",
            alignItems: "baseline",
            gap: 10,
            padding: "16px 20px",
            borderBottom: "1px solid var(--line-1)",
          }}
        >
          <span style={{ fontSize: 15, color: "var(--fg-0)", fontWeight: 600 }}>레포 연결</span>
          <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
            {productId != null ? "이 제품의 회사 것만 뜬다" : "개인 계정 것만 뜬다"}
          </span>
          <button
            type="button"
            onClick={close}
            aria-label="닫기"
            style={{
              marginLeft: "auto",
              background: "transparent",
              border: "none",
              color: "var(--fg-3)",
              fontSize: 14,
              cursor: "pointer",
              padding: 2,
            }}
          >
            ✕
          </button>
        </div>

        <div style={{ padding: "16px 20px" }}>
          {/* owner — 라디오. 각 후보가 조회·저장에 쓸 토큰을 데리고 온다. */}
          <span className="mono" style={fieldLabel}>
            owner
          </span>
          {!owners && !ownersError && (
            <p className="mono" style={{ fontSize: 11, color: "var(--fg-3)", margin: "6px 0 0" }}>
              후보를 불러오는 중…
            </p>
          )}
          {ownersError && (
            <p className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "6px 0 0" }}>
              owner 후보를 불러오지 못했습니다 — {ownersError}
            </p>
          )}
          {owners && owners.length === 0 && (
            <p className="mono" style={{ fontSize: 11, color: "var(--fg-2)", margin: "6px 0 0" }}>
              {productId != null
                ? "이 회사에 연결된 토큰이 없습니다 — 설정 › 깃 토큰"
                : "개인 토큰이 없습니다 — 설정 › 깃 토큰"}
            </p>
          )}
          {owners && (
            <div style={{ display: "flex", flexDirection: "column", gap: 4, marginTop: 6 }}>
              {owners.map((o, i) => (
                <label
                  key={`${o.source}-${o.owner}-${o.tokenId ?? "none"}`}
                  className="mono"
                  style={radioRow(mode === i)}
                >
                  <input
                    type="radio"
                    name="repo-owner"
                    checked={mode === i}
                    onChange={() => pickMode(i)}
                    style={{ accentColor: "var(--accent)" }}
                  />
                  <span style={{ color: "var(--fg-1)" }}>{o.label}</span>
                  {o.tokenId == null && (
                    <span style={{ fontSize: 10, color: "var(--fg-4)" }}>무토큰 — 공개만</span>
                  )}
                </label>
              ))}
              <label className="mono" style={radioRow(mode === "manual")}>
                <input
                  type="radio"
                  name="repo-owner"
                  checked={mode === "manual"}
                  onChange={() => pickMode("manual")}
                  style={{ accentColor: "var(--accent)" }}
                />
                <span style={{ color: "var(--fg-2)" }}>직접 입력…</span>
              </label>
            </div>
          )}

          {/* 목록 모드 — [레포 불러오기] → 체크박스 목록 */}
          {typeof mode === "number" && owners && (
            <div style={{ marginTop: 14 }}>
              <button type="button" onClick={fetchRepos} disabled={loadingRepos} style={ghostBtn}>
                {loadingRepos ? "불러오는 중…" : "레포 불러오기"}
              </button>
              {repoError && (
                <p className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "8px 0 0" }}>
                  {repoError}
                </p>
              )}
              {repoList && repoList.length === 0 && (
                <p className="mono" style={{ fontSize: 11, color: "var(--fg-3)", margin: "8px 0 0" }}>
                  레포가 없습니다
                </p>
              )}
              {repoList && repoList.length > 0 && (
                <input
                  value={repoQuery}
                  onChange={(e) => setRepoQuery(e.target.value)}
                  placeholder={`검색 — ${repoList.length}개 중`}
                  autoFocus
                  style={{
                    display: "block",
                    width: "100%",
                    boxSizing: "border-box",
                    marginTop: 8,
                    padding: "7px 10px",
                    fontSize: 12,
                    background: "var(--bg-2)",
                    border: "1px solid var(--line-2)",
                    borderRadius: 6,
                    color: "var(--fg-0)",
                  }}
                />
              )}
              {repoList &&
                repoList.length > 0 &&
                repoQuery.trim() &&
                repoList.filter((r) =>
                  r.name.toLowerCase().includes(repoQuery.trim().toLowerCase()),
                ).length === 0 && (
                  <p className="mono" style={{ fontSize: 11, color: "var(--fg-3)", margin: "8px 0 0" }}>
                    「{repoQuery.trim()}」 에 걸리는 레포가 없습니다
                  </p>
                )}
              {repoList && repoList.length > 0 && (
                <div
                  style={{
                    marginTop: 8,
                    maxHeight: 260,
                    overflowY: "auto",
                    border: "1px solid var(--line-1)",
                    borderRadius: 6,
                  }}
                >
                  {repoList
                    .filter(
                      (r) =>
                        !repoQuery.trim() ||
                        r.name.toLowerCase().includes(repoQuery.trim().toLowerCase()),
                    )
                    .map((r) => {
                    const done = isRegistered(r.slug);
                    return (
                      <label
                        key={r.slug}
                        className="mono"
                        title={done ? "이미 등록된 레포입니다" : r.slug}
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: 8,
                          padding: "6px 10px",
                          borderBottom: "1px solid var(--line-1)",
                          fontSize: 12,
                          cursor: done ? "default" : "pointer",
                          opacity: done ? 0.45 : 1,
                        }}
                      >
                        <input
                          type="checkbox"
                          disabled={done}
                          checked={!done && selected.has(r.slug)}
                          onChange={() => toggle(r.slug)}
                          style={{ accentColor: "var(--accent)" }}
                        />
                        <span
                          style={{
                            color: "var(--fg-1)",
                            overflow: "hidden",
                            textOverflow: "ellipsis",
                            whiteSpace: "nowrap",
                          }}
                        >
                          {r.name}
                        </span>
                        <span
                          style={{
                            fontSize: 10,
                            letterSpacing: "0.08em",
                            color: r.private ? "var(--accent)" : "var(--fg-3)",
                            border: "1px solid var(--line-1)",
                            borderRadius: 4,
                            padding: "0 5px",
                            flexShrink: 0,
                          }}
                        >
                          {r.private ? "private" : "public"}
                        </span>
                        {done && (
                          <span style={{ fontSize: 10, color: "var(--fg-3)", flexShrink: 0 }}>
                            등록됨
                          </span>
                        )}
                        <span
                          style={{ marginLeft: "auto", fontSize: 10, color: "var(--fg-3)", flexShrink: 0 }}
                        >
                          {fmtDate(r.updatedAt)}
                        </span>
                      </label>
                    );
                  })}
                </div>
              )}
            </div>
          )}

          {/* 직접 입력 모드 — owner/name + 토큰 셀렉트(기존 인라인 행의 폴백) */}
          {mode === "manual" && (
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 14, flexWrap: "wrap" }}>
              <input
                value={manualOwner}
                onChange={(e) => setManualOwner(e.target.value)}
                placeholder="owner — 예: kknaks"
                style={{ ...input, marginTop: 0, flex: "1 1 120px", width: "auto" }}
              />
              <span className="mono" style={{ color: "var(--fg-3)" }}>/</span>
              <input
                value={manualName}
                onChange={(e) => setManualName(e.target.value)}
                placeholder="name — 예: wine-log"
                style={{ ...input, marginTop: 0, flex: "1 1 140px", width: "auto" }}
              />
              {/* 수집 토큰 — 설정에서 등록한 git_token 행. 미지정 = 무토큰(공개만). */}
              <select
                value={manualTokenId}
                onChange={(e) => setManualTokenId(e.target.value)}
                style={{ ...input, marginTop: 0, width: "auto", appearance: "auto" }}
              >
                <option value="">토큰 — 무토큰(공개)</option>
                {/* 비활성 토큰도 고를 수는 있다 — 다시 켜기 전까지 무토큰으로 수집된다. */}
                {tokens.map((t) => (
                  <option key={t.id} value={String(t.id)}>
                    {t.kind} · {t.account}
                    {t.enabled ? "" : " (비활성)"}
                  </option>
                ))}
              </select>
            </div>
          )}

          {saveError && (
            <p className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "10px 0 0" }}>
              {saveError}
            </p>
          )}
        </div>

        {/* 발 */}
        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            gap: 10,
            padding: "14px 20px",
            borderTop: "1px solid var(--line-1)",
          }}
        >
          <button type="button" onClick={close} style={ghostBtn}>
            취소
          </button>
          <button type="button" onClick={save} disabled={saveDisabled} style={primaryBtn(!saveDisabled)}>
            {saving ? "연결 중…" : saveLabel}
          </button>
        </div>
      </div>
    </div>
  );
}

/* ── 행 ─────────────────────────────────────────────────────────────── */

/** timestamptz → `2026.08.25 09:12` (로컬). null 은 「아직 안 돌았다」. */
function fmtFetchedAt(iso?: string | null): string {
  if (!iso) return "수집 전";
  const d = new Date(iso);
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}.${p(d.getMonth() + 1)}.${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
}

function RepoRow({
  repo,
  tokens,
  onChanged,
}: {
  repo: AdminRepo;
  tokens: GitTokenMeta[];
  onChanged: () => void;
}) {
  const [busy, setBusy] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  async function toggleEnabled() {
    setBusy(true);
    setActionError(null);
    try {
      await adminApi.patchRepo(repo.id, { enabled: !repo.enabled });
      onChanged();
    } catch (e) {
      setActionError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    } finally {
      setBusy(false);
    }
  }

  // 삭제 — 확인 없이 즉시. 커밋도 CASCADE 로 지워진다(잔디를 남기려면 enabled 를 끈다).
  async function remove() {
    setActionError(null);
    try {
      await adminApi.deleteRepo(repo.id);
      onChanged();
    } catch (e) {
      setActionError(e instanceof AuthError ? `${e.status} — ${e.message}` : String(e));
    }
  }

  return (
    <div
      style={{
        border: "1px solid var(--line-1)",
        borderRadius: 6,
        padding: "8px 10px",
        background: "var(--bg-2)",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
        <span className="mono" style={{ fontSize: 12, color: "var(--fg-0)", fontWeight: 600 }}>
          {repo.slug}
        </span>
        {repo.role && (
          <span
            className="mono"
            style={{
              fontSize: 10,
              letterSpacing: "0.08em",
              color: "var(--fg-2)",
              border: "1px solid var(--line-1)",
              borderRadius: 4,
              padding: "1px 6px",
            }}
          >
            {repo.role}
          </span>
        )}
        {/* 수집 토큰 — 바꾸면 즉시 PATCH. 다음 수집부터 그 토큰으로 읽는다. */}
        <select
          value={repo.gitTokenId != null ? String(repo.gitTokenId) : ""}
          disabled={busy}
          onChange={async (e) => {
            setBusy(true);
            setActionError(null);
            try {
              await adminApi.patchRepo(repo.id, {
                gitTokenId: e.target.value ? Number(e.target.value) : null,
              });
              onChanged();
            } catch (err) {
              setActionError(
                err instanceof AuthError ? `${err.status} — ${err.message}` : String(err),
              );
            } finally {
              setBusy(false);
            }
          }}
          className="mono"
          style={{
            fontSize: 10,
            padding: "2px 4px",
            borderRadius: 4,
            border: "1px solid var(--line-1)",
            background: "transparent",
            color: repo.gitTokenId != null ? "var(--fg-1)" : "var(--fg-3)",
          }}
        >
          <option value="">무토큰</option>
          {tokens.map((t) => (
            <option key={t.id} value={String(t.id)}>
              {t.kind} · {t.account}
              {t.enabled ? "" : " (비활성)"}
            </option>
          ))}
        </select>
        <span className="mono" style={{ fontSize: 10, color: "var(--fg-3)" }}>
          마지막 수집 {fmtFetchedAt(repo.lastFetchedAt)}
        </span>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 6 }}>
          {/* enabled — 누르면 즉시 PATCH. 꺼진 레포는 수집에서 빠진다. */}
          <button
            type="button"
            onClick={toggleEnabled}
            disabled={busy}
            title={repo.enabled ? "수집 중 — 누르면 제외" : "제외됨 — 누르면 수집"}
            className="mono"
            style={{
              fontSize: 10,
              letterSpacing: "0.08em",
              padding: "3px 9px",
              borderRadius: 999,
              cursor: "pointer",
              border: repo.enabled ? "1px solid var(--accent)" : "1px solid var(--line-2)",
              background: repo.enabled ? "var(--accent-soft)" : "transparent",
              color: repo.enabled ? "var(--accent)" : "var(--fg-3)",
            }}
          >
            {repo.enabled ? "enabled" : "disabled"}
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

      {repo.lastError && (
        <p
          className="mono"
          style={{
            fontSize: 11,
            color: "var(--danger, #e5534b)",
            lineHeight: 1.5,
            margin: "6px 0 0",
            wordBreak: "break-all",
          }}
        >
          last_error — {repo.lastError}
        </p>
      )}
      {actionError && (
        <p className="mono" style={{ fontSize: 11, color: "var(--danger, #e5534b)", margin: "6px 0 0" }}>
          {actionError}
        </p>
      )}
    </div>
  );
}

/* ── 스타일 조각 — 어드민 폼 패턴과 동일 ─────────────────────────────── */

const fieldLabel: React.CSSProperties = {
  fontSize: 10,
  letterSpacing: "0.08em",
  color: "var(--fg-4)",
};

function radioRow(active: boolean): React.CSSProperties {
  return {
    display: "flex",
    alignItems: "center",
    gap: 8,
    fontSize: 12,
    padding: "6px 10px",
    borderRadius: 6,
    border: active ? "1px solid var(--line-2)" : "1px solid var(--line-1)",
    background: active ? "var(--bg-2)" : "transparent",
    cursor: "pointer",
  };
}

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
    cursor: active ? "pointer" : "default",
  };
}
