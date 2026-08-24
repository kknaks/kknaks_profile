"use client";

import { useCallback, useEffect, useState } from "react";
import { Spinner, btn } from "@/components/admin/queue-gate";
import { Select } from "@/components/admin/select";
import {
  QueueError,
  productsApi,
  type CardInput,
  type DiscoveredRow,
  type ProductOptions,
  type RegistryRow,
} from "@/lib/api";

/* 제품 레지스트리 — KDEV-SPEC-014 U-1~U-4 / WORK-018 P4.
 *
 * 이 화면이 푸는 문제는 "등록이 번거롭다" 가 아니라 **"빠진 줄 모른다"** 다.
 * 레지스트리가 showcase 에서 시드돼 그 사각지대를 물려받았고, 그 뒤로 발견 장치가
 * 없어서 레포를 파도·커밋을 쌓아도 09:05 잔디는 매일 정상 종료했다. 실측으로 최근
 * 30일 본인 커밋 57건이 그렇게 빠져 있었다.
 *
 * 그래서 **배너가 표보다 위에 있다.** 표는 이미 아는 것을 보여주고, 배너는 모르는
 * 것을 보여준다.
 */

//: 클론이 도는 동안 따라붙는 주기. 최초 클론은 수 분 걸리므로 화면이 기다리지 않고
//: 행의 상태만 갱신한다.
const POLL_MS = 5000;

//: 표 필터. **회사와 개인은 성격이 다르다** — 회사 행은 career 로 가고 제품 문서가
//: 없으며(D9), 개인 행은 제품·카드로 간다. 섞어 두면 두 종류의 빈 칸이 같아 보인다.
type Tab = "all" | "company" | "studio";

const TABS: { key: Tab; label: string }[] = [
  { key: "all", label: "전체" },
  { key: "company", label: "회사" },
  { key: "studio", label: "프로젝트" },
];

const cell: React.CSSProperties = {
  padding: "9px 10px",
  fontSize: 12.5,
  color: "var(--fg-1)",
  borderBottom: "1px solid var(--line-1)",
  verticalAlign: "middle",
};

//: 헤더 부제 — 한 단어로는 뜻이 안 보이는 열이 셋 있다.
const sub: React.CSSProperties = {
  fontSize: 9.5,
  letterSpacing: 0,
  textTransform: "none",
  color: "var(--fg-4)",
  marginTop: 2,
  fontWeight: 400,
};

const head: React.CSSProperties = {
  ...cell,
  color: "var(--fg-3)",
  fontSize: 11,
  letterSpacing: "0.06em",
  textTransform: "uppercase",
  borderBottom: "1px solid var(--line-2)",
};

const input: React.CSSProperties = {
  width: "100%",
  padding: "7px 9px",
  fontSize: 12.5,
  background: "var(--bg-0)",
  border: "1px solid var(--line-2)",
  borderRadius: 5,
  color: "var(--fg-0)",
  // **네이티브 팝업까지 어둡게 만드는 유일한 방법이다.** `<option>` 의 배경색은
  // 브라우저가 대개 무시하지만 `color-scheme` 은 존중한다 — 이게 없으면 셀렉트를
  // 열었을 때 흰 목록이 튀어나온다.
  colorScheme: "dark",
};

function relTime(iso: string | null): string {
  if (!iso) return "—";
  const diff = Date.now() - new Date(iso).getTime();
  const m = Math.round(diff / 60000);
  if (m < 1) return "방금";
  if (m < 60) return `${m}분 전`;
  const h = Math.round(m / 60);
  if (h < 24) return `${h}시간 전`;
  return `${Math.round(h / 24)}일 전`;
}

/** 실패 사유의 **코드만** 뽑는다. 전문은 title 로 붙여 마우스로 본다. */
function errCode(raw: string | null): string {
  return raw ? String(raw).split(":", 1)[0] : "";
}

export function ProductRegistry() {
  const [rows, setRows] = useState<RegistryRow[] | null>(null);
  const [options, setOptions] = useState<ProductOptions | null>(null);
  const [missing, setMissing] = useState<DiscoveredRow[]>([]);
  const [hiddenOld, setHiddenOld] = useState(0);
  const [windowDays, setWindowDays] = useState(0);
  const [missingError, setMissingError] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [formOpen, setFormOpen] = useState(false);
  const [prefill, setPrefill] = useState<string>("");
  //: 어느 행이 무엇을 하는 중인지. boolean 이면 화면이 "왜 멈춰 있는지" 를 말하지 못한다.
  const [busy, setBusy] = useState<Record<number, string>>({});
  //: 카드 만들기 폼이 열린 행. 제품은 있는데 카드가 없는 행에서만 열린다.
  const [cardFor, setCardFor] = useState<RegistryRow | null>(null);
  const [tab, setTab] = useState<Tab>("all");

  const load = useCallback(async () => {
    try {
      const [list, opt] = await Promise.all([productsApi.list(), productsApi.options()]);
      setRows(list.items);
      setOptions(opt);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "목록을 불러오지 못했습니다");
    }
  }, []);

  const loadMissing = useCallback(async () => {
    // **배너 실패가 화면을 막지 않는다** — 표는 이미 떠 있어야 한다.
    try {
      const res = await productsApi.undiscovered();
      setMissing(res.items);
      setHiddenOld(res.hidden_old);
      setWindowDays(res.window_days);
      setMissingError(res.error);
    } catch (e) {
      setMissingError(e instanceof Error ? e.message : "미등록 확인 실패");
    }
  }, []);

  useEffect(() => {
    void load();
    void loadMissing();
  }, [load, loadMissing]);

  // 클론이 도는 동안만 폴링한다. 끝나면 멈춘다 — 조용한 화면에서 계속 두드릴 이유가 없다.
  const syncing = Object.values(busy).some((b) => b === "sync");
  useEffect(() => {
    if (!syncing) return;
    const t = setInterval(() => void load(), POLL_MS);
    return () => clearInterval(t);
  }, [syncing, load]);

  async function act(id: number, kind: string, fn: () => Promise<unknown>) {
    setBusy((b) => ({ ...b, [id]: kind }));
    try {
      await fn();
      await load();
    } catch (e) {
      setError(e instanceof QueueError ? e.message : "요청에 실패했습니다");
    } finally {
      setBusy((b) => {
        const next = { ...b };
        delete next[id];
        return next;
      });
    }
  }

  const visible = rows === null ? [] : rows.filter((r) => tab === "all" || r.type === tab);

  if (rows === null) {
    return (
      <div style={{ padding: 40, textAlign: "center", color: "var(--fg-3)" }}>
        <Spinner />
      </div>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      {error && (
        <div
          style={{
            padding: "10px 12px",
            border: "1px solid #f85149",
            borderRadius: 6,
            color: "#f85149",
            fontSize: 12.5,
          }}
        >
          {error}
        </div>
      )}

      <MissingBanner
        items={missing}
        hiddenOld={hiddenOld}
        windowDays={windowDays}
        error={missingError}
        onPick={(slug) => {
          setPrefill(slug);
          setFormOpen(true);
        }}
        onRetry={() => void loadMissing()}
      />

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ display: "flex", gap: 4 }}>
          {TABS.map((t) => {
            const count =
              t.key === "all" ? rows.length : rows.filter((r) => r.type === t.key).length;
            const on = tab === t.key;
            return (
              <button
                key={t.key}
                type="button"
                onClick={() => setTab(t.key)}
                style={{
                  padding: "5px 12px",
                  fontSize: 12.5,
                  borderRadius: 6,
                  cursor: "pointer",
                  background: on ? "var(--bg-3)" : "transparent",
                  border: `1px solid ${on ? "var(--line-3)" : "transparent"}`,
                  color: on ? "var(--fg-0)" : "var(--fg-3)",
                }}
              >
                {t.label}
                <span className="mono" style={{ marginLeft: 6, fontSize: 11, color: "var(--fg-4)" }}>
                  {count}
                </span>
              </button>
            );
          })}
        </div>
        <button
          type="button"
          style={btn("primary")}
          onClick={() => {
            setPrefill("");
            setFormOpen((v) => !v);
          }}
        >
          {formOpen ? "닫기" : "+ 새 제품"}
        </button>
      </div>

      {formOpen && options && (
        <RegisterForm
          options={options}
          prefillRepo={prefill}
          onDone={async () => {
            setFormOpen(false);
            await load();
            await loadMissing();
          }}
        />
      )}

      {cardFor && options && (
        <CardForm
          row={cardFor}
          options={options}
          onCancel={() => setCardFor(null)}
          onDone={async () => {
            setCardFor(null);
            await load();
          }}
        />
      )}

      <div style={{ overflowX: "auto", border: "1px solid var(--line-1)", borderRadius: 8 }}>
        <table style={{ width: "100%", borderCollapse: "collapse", minWidth: 900 }}>
          <thead>
            <tr>
              <th style={{ ...head, textAlign: "left" }}>레포</th>
              <th style={{ ...head, textAlign: "left" }}>제품</th>
              <th style={{ ...head, textAlign: "left" }}>커리어</th>
              <th
                style={{ ...head, textAlign: "center" }}
                title="켜면 매일 09:05 잔디가 이 레포의 커밋을 조사합니다. 끄면 클론과 행은 남고 조사만 멈춥니다"
              >
                추적
                <div style={sub}>잔디 조사</div>
              </th>
              <th
                style={{ ...head, textAlign: "center" }}
                title="공개 카드(showcase.md)의 visible 입니다. 누르면 그 파일을 고쳐 한 커밋으로 push 합니다"
              >
                노출
                <div style={sub}>사이트 · 파일 수정</div>
              </th>
              <th style={{ ...head, textAlign: "left" }}>
                마지막 조사
                <div style={sub}>클론 · fetch</div>
              </th>
              <th style={head} />
            </tr>
          </thead>
          <tbody>
            {visible.map((row) => (
              <Row
                key={row.id}
                row={row}
                options={options}
                busy={busy[row.id]}
                onPatch={(body) => act(row.id, "patch", () => productsApi.patch(row.id, body))}
                onVisible={(v) => act(row.id, "visible", () => productsApi.setVisible(row.id, v))}
                onAddCard={() => setCardFor(row)}
                onSync={() => act(row.id, "sync", () => productsApi.sync(row.id))}
              />
            ))}
          </tbody>
        </table>
      </div>

      <div className="mono" style={{ fontSize: 11, color: "var(--fg-4)", textAlign: "right" }}>
        {tab === "all" ? "" : `${visible.length} / `}
        레포 {rows.length} · 잔디 조사 대상 {rows.filter((r) => r.enabled).length}
      </div>
    </div>
  );
}

function MissingBanner({
  items,
  hiddenOld,
  windowDays,
  error,
  onPick,
  onRetry,
}: {
  items: DiscoveredRow[];
  hiddenOld: number;
  windowDays: number;
  error: string | null;
  onPick: (slug: string) => void;
  onRetry: () => void;
}) {
  // 미등록이 0이면 **표시하지 않는다** — 늘 떠 있으면 아무도 안 본다.
  if (!error && items.length === 0) return null;

  if (error) {
    return (
      <div
        style={{
          padding: "10px 12px",
          border: "1px dashed var(--line-2)",
          borderRadius: 6,
          fontSize: 12.5,
          color: "var(--fg-3)",
          display: "flex",
          gap: 10,
          alignItems: "center",
        }}
      >
        <span>미등록 확인 실패 — {error}</span>
        <button type="button" style={{ ...btn("ghost"), padding: "2px 8px" }} onClick={onRetry}>
          재시도
        </button>
      </div>
    );
  }

  return (
    <div
      style={{
        padding: "12px 14px",
        border: "1px solid var(--accent)",
        borderRadius: 6,
        background: "var(--accent-soft)",
      }}
    >
      <div style={{ fontSize: 13, color: "var(--fg-0)", marginBottom: 8 }}>
        추적에 없는 레포 {items.length}건
      </div>
      <div style={{ fontSize: 11.5, color: "var(--fg-2)", marginBottom: 10 }}>
        여기 있는 레포의 커밋은 잔디에 잡히지 않습니다. 클릭하면 등록 폼이 열립니다.
        {hiddenOld > 0 && (
          // **조용히 자르지 않는다** — 감춘 게 있다는 사실 자체가 정보다.
          <span style={{ color: "var(--fg-4)" }}>
            {" "}· 최근 {windowDays}일 기준, 오래된 {hiddenOld}건은 감춤
          </span>
        )}
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
        {items.map((r) => (
          <button
            key={r.slug}
            type="button"
            onClick={() => onPick(r.slug)}
            className="mono"
            style={{
              ...btn("ghost"),
              padding: "3px 9px",
              fontSize: 11.5,
            }}
            title={r.pushed_at ? `마지막 push ${relTime(r.pushed_at)}` : undefined}
          >
            {r.slug}
            {r.private && <span style={{ color: "var(--fg-4)" }}> · private</span>}
          </button>
        ))}
      </div>
    </div>
  );
}

function Row({
  row,
  options,
  busy,
  onPatch,
  onVisible,
  onAddCard,
  onSync,
}: {
  row: RegistryRow;
  options: ProductOptions | null;
  busy?: string;
  onPatch: (body: Partial<Pick<RegistryRow, "detail" | "product_slug" | "enabled">>) => void;
  onVisible: (value: boolean) => void;
  onAddCard: () => void;
  onSync: () => void;
}) {
  const failed = Boolean(row.last_error);
  return (
    <tr style={{ opacity: row.enabled ? 1 : 0.55 }}>
      <td style={cell}>
        <span className="mono" style={{ fontSize: 12 }}>
          {row.slug}
        </span>
        <div style={{ fontSize: 10.5, color: "var(--fg-4)" }}>
          {row.type} · {row.account}
        </div>
      </td>

      <td style={cell}>
        <Select
          ariaLabel="제품 연결"
          value={row.product_slug ?? ""}
          options={options?.products ?? []}
          emptyLabel="—"
          disabled={Boolean(busy)}
          width={170}
          onChange={(v) => onPatch({ product_slug: v || null })}
        />
        {row.product_slug && !row.product_exists && (
          <div style={{ fontSize: 10.5, color: "#d29922", marginTop: 3 }}>
            ⚠ 제품 폴더 없음
          </div>
        )}
      </td>

      <td style={cell}>
        {row.type === "company" ? (
          <Select
            ariaLabel="커리어 귀속"
            value={row.detail ?? ""}
            options={options?.careers ?? []}
            emptyLabel="—"
            disabled={Boolean(busy)}
            width={150}
            onChange={(v) => onPatch({ detail: v || null })}
          />
        ) : (
          <span style={{ color: "var(--fg-4)" }}>—</span>
        )}
      </td>

      <td style={{ ...cell, textAlign: "center" }}>
        <input
          type="checkbox"
          checked={row.enabled}
          disabled={Boolean(busy)}
          onChange={(e) => onPatch({ enabled: e.target.checked })}
          title="끄면 다음 09:05 조사부터 빠집니다. 클론과 행은 남아서 다시 켜면 그대로 이어집니다"
        />
      </td>

      {/* 값은 `showcase.md` 에 있고 토글이 **그 파일을 고쳐 커밋한다**(D18).
          DB 를 안 거치므로 Obsidian 에서 고친 것과 충돌하지 않는다. */}
      <td style={{ ...cell, textAlign: "center" }}>
        {row.card_visible === null ? (
          row.product_slug && row.product_exists ? (
            // **카드가 없으면 사이트에 뜰 방법이 없다.** 그 자리를 만드는 버튼으로 쓴다.
            <button
              type="button"
              disabled={Boolean(busy)}
              onClick={onAddCard}
              title="이 제품에 공개 카드(showcase.md)를 만듭니다"
              style={{
                padding: "2px 9px",
                fontSize: 11.5,
                borderRadius: 999,
                cursor: "pointer",
                background: "transparent",
                border: "1px dashed var(--line-3)",
                color: "var(--fg-3)",
              }}
            >
              + 카드
            </button>
          ) : (
            <span style={{ color: "var(--fg-4)" }} title="연결된 제품이 없습니다">
              —
            </span>
          )
        ) : (
          <button
            type="button"
            disabled={Boolean(busy)}
            onClick={() => onVisible(!row.card_visible)}
            title="showcase.md 의 visible 을 바꾸고 한 커밋으로 push 합니다"
            style={{
              padding: "2px 9px",
              fontSize: 11.5,
              borderRadius: 999,
              cursor: busy ? "default" : "pointer",
              background: "transparent",
              border: `1px solid ${row.card_visible ? "var(--accent)" : "var(--line-2)"}`,
              color: row.card_visible ? "var(--accent)" : "var(--fg-3)",
              opacity: busy === "visible" ? 0.5 : 1,
            }}
          >
            {busy === "visible" ? "…" : row.card_visible ? "공개" : "숨김"}
          </button>
        )}
      </td>

      <td style={cell}>
        {busy === "sync" ? (
          <span style={{ color: "var(--fg-3)" }}>동기화 중…</span>
        ) : failed ? (
          <span className="mono" style={{ color: "#f85149", fontSize: 11.5 }} title={row.last_error ?? ""}>
            ✕ {errCode(row.last_error)}
          </span>
        ) : (
          <span style={{ color: "var(--fg-2)" }}>{relTime(row.last_fetched_at)}</span>
        )}
      </td>

      <td style={{ ...cell, textAlign: "right" }}>
        <button
          type="button"
          disabled={Boolean(busy)}
          onClick={onSync}
          style={{ ...btn("ghost"), padding: "3px 9px", fontSize: 11.5 }}
        >
          재동기화
        </button>
      </td>
    </tr>
  );
}

const EMPTY_CARD: CardInput = {
  title: "",
  summary: "",
  category: "",
  status: "wip",
  stack: [],
};

function RegisterForm({
  options,
  prefillRepo,
  onDone,
}: {
  options: ProductOptions;
  prefillRepo: string;
  onDone: () => void;
}) {
  const [kind, setKind] = useState<"studio" | "company">("studio");
  const [repo, setRepo] = useState(prefillRepo);
  const [detail, setDetail] = useState("");
  const [productSlug, setProductSlug] = useState("");
  const [card, setCard] = useState<CardInput>(EMPTY_CARD);
  const [stackRaw, setStackRaw] = useState("");
  const [sending, setSending] = useState(false);
  //: 필드별 오류. 전역 배너에 뭉뚱그리면 어디를 고쳐야 하는지 알 수 없다.
  const [fieldError, setFieldError] = useState<{ field: string | null; message: string } | null>(
    null,
  );

  useEffect(() => setRepo(prefillRepo), [prefillRepo]);

  async function submit() {
    setSending(true);
    setFieldError(null);
    try {
      await productsApi.register({
        repo,
        type: kind,
        detail: kind === "company" ? detail || null : null,
        product_slug: kind === "studio" ? productSlug || null : null,
        card:
          kind === "studio"
            ? {
                ...card,
                stack: stackRaw
                  .split(",")
                  .map((s) => s.trim())
                  .filter(Boolean),
              }
            : null,
      });
      onDone();
    } catch (e) {
      if (e instanceof QueueError) {
        const d = e.detail as { field?: string } | undefined;
        setFieldError({ field: d?.field ?? null, message: e.message });
      } else {
        setFieldError({ field: null, message: "등록에 실패했습니다" });
      }
    } finally {
      setSending(false);
    }
  }

  const err = (field: string) =>
    fieldError?.field === field ? (
      <div style={{ fontSize: 11, color: "#f85149", marginTop: 4 }}>{fieldError.message}</div>
    ) : null;

  return (
    <div
      style={{
        border: "1px solid var(--line-2)",
        borderRadius: 8,
        padding: 16,
        display: "flex",
        flexDirection: "column",
        gap: 12,
      }}
    >
      <div style={{ display: "flex", gap: 8 }}>
        {(["studio", "company"] as const).map((k) => (
          <button
            key={k}
            type="button"
            onClick={() => setKind(k)}
            style={kind === k ? btn("primary") : btn("ghost")}
          >
            {k === "studio" ? "개인 제품" : "회사 레포"}
          </button>
        ))}
      </div>

      <div style={{ fontSize: 11.5, color: "var(--fg-3)" }}>
        {kind === "studio"
          ? "제품 문서 골격과 공개 카드를 만들고 한 커밋으로 push 합니다."
          : "레지스트리 행만 만듭니다 — 회사 레포는 문서도 카드도 만들지 않습니다."}
      </div>

      <Field label="레포">
        <input
          value={repo}
          onChange={(e) => setRepo(e.target.value)}
          placeholder="owner/name 또는 GitHub 주소"
          style={input}
        />
        {err("repo")}
      </Field>

      {kind === "company" ? (
        <Field label="커리어 귀속">
          <Select
            value={detail}
            options={options.careers}
            emptyLabel="선택"
            onChange={setDetail}
          />
          {err("detail")}
        </Field>
      ) : (
        <>
          <Field label="제품 slug">
            <input
              value={productSlug}
              onChange={(e) => setProductSlug(e.target.value)}
              placeholder="mac-remote — 소문자·숫자·하이픈"
              style={input}
            />
            {err("product_slug")}
          </Field>

          <Field label="제목">
            <input
              value={card.title}
              onChange={(e) => setCard({ ...card, title: e.target.value })}
              style={input}
            />
          </Field>
          {err("title")}

          <Field label="요약">
            <input
              value={card.summary}
              onChange={(e) => setCard({ ...card, summary: e.target.value })}
              style={input}
            />
          </Field>
          {err("summary")}

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 2fr", gap: 10 }}>
            <Field label="분류">
              {/* **자유입력이 아니다** — 목록 밖 값 하나가 사이트를 옛 데이터에 묶는다. */}
              <Select
                value={card.category}
                options={options.categories}
                emptyLabel="선택"
                onChange={(v) => setCard({ ...card, category: v })}
              />
              {err("category")}
            </Field>
            <Field label="상태">
              <Select
                value={card.status}
                options={options.statuses}
                onChange={(v) => setCard({ ...card, status: v })}
              />
            </Field>
            <Field label="스택 (쉼표)">
              <input
                value={stackRaw}
                onChange={(e) => setStackRaw(e.target.value)}
                placeholder="FastAPI, Postgres"
                style={input}
              />
              {err("stack")}
            </Field>
          </div>
        </>
      )}

      {fieldError && !fieldError.field && (
        <div style={{ fontSize: 12, color: "#f85149" }}>{fieldError.message}</div>
      )}

      <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
        <button type="button" disabled={sending} onClick={submit} style={btn("primary")}>
          {sending ? "등록 중…" : "등록"}
        </button>
      </div>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label style={{ display: "block" }}>
      <div style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 5 }}>{label}</div>
      {children}
    </label>
  );
}


/** 이미 있는 제품에 카드를 붙이는 폼. 등록 폼과 달리 **레포·제품 slug 를 안 받는다** —
 *  둘 다 이미 정해져 있다. */
function CardForm({
  row,
  options,
  onCancel,
  onDone,
}: {
  row: RegistryRow;
  options: ProductOptions;
  onCancel: () => void;
  onDone: () => void;
}) {
  const [card, setCard] = useState<CardInput>(EMPTY_CARD);
  const [stackRaw, setStackRaw] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<{ field: string | null; message: string } | null>(null);

  async function submit() {
    setSending(true);
    setError(null);
    try {
      await productsApi.addCard(row.id, {
        ...card,
        stack: stackRaw.split(",").map((s) => s.trim()).filter(Boolean),
      });
      onDone();
    } catch (e) {
      if (e instanceof QueueError) {
        const d = e.detail as { field?: string } | undefined;
        setError({ field: d?.field ?? null, message: e.message });
      } else {
        setError({ field: null, message: "카드 생성에 실패했습니다" });
      }
    } finally {
      setSending(false);
    }
  }

  const err = (field: string) =>
    error?.field === field ? (
      <div style={{ fontSize: 11, color: "#f85149", marginTop: 4 }}>{error.message}</div>
    ) : null;

  return (
    <div
      style={{
        border: "1px solid var(--accent)",
        borderRadius: 8,
        padding: 16,
        display: "flex",
        flexDirection: "column",
        gap: 12,
      }}
    >
      <div style={{ fontSize: 13, color: "var(--fg-0)" }}>
        공개 카드 만들기 — <span className="mono">{row.product_slug}</span>
      </div>
      <div style={{ fontSize: 11.5, color: "var(--fg-3)" }}>
        `products/{row.product_slug}/showcase.md` 를 만들고 한 커밋으로 push 합니다.
        <b> 숨김 상태로 만들어집니다</b> — 본문을 채운 뒤 노출을 켜세요.
      </div>

      <Field label="제목">
        <input
          value={card.title}
          onChange={(e) => setCard({ ...card, title: e.target.value })}
          style={input}
        />
      </Field>
      {err("title")}

      <Field label="요약">
        <input
          value={card.summary}
          onChange={(e) => setCard({ ...card, summary: e.target.value })}
          style={input}
        />
      </Field>
      {err("summary")}

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 2fr", gap: 10 }}>
        <Field label="분류">
          <Select
            value={card.category}
            options={options.categories}
            emptyLabel="선택"
            onChange={(v) => setCard({ ...card, category: v })}
          />
          {err("category")}
        </Field>
        <Field label="상태">
          <Select
            value={card.status}
            options={options.statuses}
            onChange={(v) => setCard({ ...card, status: v })}
          />
        </Field>
        <Field label="스택 (쉼표)">
          <input
            value={stackRaw}
            onChange={(e) => setStackRaw(e.target.value)}
            placeholder="Swift, SwiftUI"
            style={input}
          />
          {err("stack")}
        </Field>
      </div>

      {error && !error.field && (
        <div style={{ fontSize: 12, color: "#f85149" }}>{error.message}</div>
      )}

      <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
        <button type="button" onClick={onCancel} style={btn("ghost")}>
          취소
        </button>
        <button type="button" disabled={sending} onClick={submit} style={btn("primary")}>
          {sending ? "만드는 중…" : "카드 만들기"}
        </button>
      </div>
    </div>
  );
}

