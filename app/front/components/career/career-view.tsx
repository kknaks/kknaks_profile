"use client";

import { useEffect, useMemo, useState } from "react";
import { DocBody } from "@/components/markdown/doc-body";
import { ProseBody } from "@/components/markdown/prose-body";
import type {
  CareerItem,
  CareerProduct,
  EducationItem,
  TimelineItem,
} from "@/lib/types";

/**
 * `/career` 3열 레이아웃.
 *
 *   [ 사이드 ]        [ 타임라인 ]        [ 상세 ]
 *   메타(연차·roles·  career → education   선택 항목의 전체 상세
 *   courses·FOCUS)    compact row 목록      (body md · 만든 것 · 해결한 문제)
 *
 * 선택은 **단일** — career+education 을 합쳐 한 번에 하나만 활성. 기본은 가장 최근
 * 커리어(첫 role). 항목을 눌러도 아래를 밀지 않고 3열의 상세 칸만 바뀐다(desktop).
 * ≤900px 에서는 세로로 눕고 상세는 선택 항목 **아래**로 들어간다(모바일은 밀어내기 허용).
 *
 * 상세 렌더링(body md · 만든 것 카드 인라인 펼침 · mermaid)은 이전 CareerTimeline
 * 것을 그대로 옮겨 보존한다. 「만든 것」 카드는 클릭하면 카드 바로 아래로 showcase
 * 본문(ShowcaseBody)이 아코디언으로 펼쳐진다 — 한 번에 하나만.
 */

interface CareerMeta {
  totalYears?: string;
  totalRoles: string;
  focusLines: string[];
  educationCount: number;
}

/** 통합 선택키 — career/education 의 id 가 표를 넘어 겹칠 수 있어 kind 를 붙인다. */
type Kind = "career" | "education";
function keyOf(kind: Kind, item: TimelineItem) {
  return `${kind}:${item.id}`;
}

export function CareerView({
  roles,
  education,
  meta,
}: {
  roles: CareerItem[];
  education: EducationItem[];
  meta: CareerMeta;
}) {
  // 기본 선택 = 가장 최근 커리어 항목(첫 role). 없으면 첫 교육.
  const defaultKey = useMemo(() => {
    if (roles.length > 0) return keyOf("career", roles[0]);
    if (education.length > 0) return keyOf("education", education[0]);
    return null;
  }, [roles, education]);
  const [selectedKey, setSelectedKey] = useState<string | null>(defaultKey);

  // 「만든 것」 카드 클릭 → showcase(detail_path) 를 모달로 연다.
  const [activeProduct, setActiveProduct] = useState<CareerProduct | null>(null);

  // 좁은 화면에서는 상세를 선택 항목 아래에 인라인으로 그린다(3열 → 세로 스택).
  const [isNarrow, setIsNarrow] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia("(max-width: 900px)");
    const apply = () => setIsNarrow(mq.matches);
    apply();
    mq.addEventListener("change", apply);
    return () => mq.removeEventListener("change", apply);
  }, []);

  const selected = useMemo(() => {
    const inRoles = roles.find((r) => keyOf("career", r) === selectedKey);
    if (inRoles) return inRoles;
    return education.find((e) => keyOf("education", e) === selectedKey) ?? null;
  }, [roles, education, selectedKey]);

  const renderRow = (kind: Kind, it: TimelineItem) => {
    const k = keyOf(kind, it);
    const active = k === selectedKey;
    return (
      <div key={k}>
        <TimelineRow
          item={it}
          active={active}
          onSelect={() => setSelectedKey(k)}
        />
        {/* 모바일: 선택 항목 바로 아래에 상세를 편다(밀어내기 허용). */}
        {isNarrow && active && (
          <div style={{ margin: "4px 0 8px", paddingLeft: 28 }}>
            <DetailPanel item={it} onProduct={setActiveProduct} />
          </div>
        )}
      </div>
    );
  };

  return (
    <>
    {activeProduct && (
      <ProductModal product={activeProduct} onClose={() => setActiveProduct(null)} />
    )}
    <div className="career-2col">
        {/* ── 왼쪽 블록 — 섹션마다 [라벨 | 타임라인] 한 행 ─────────── */}
        <div className="career-left">
          {/* 커리어 행 */}
          <div className="career-section">
            <div className="career-section-label mono">
              <div style={{ color: "var(--accent)", fontSize: 13 }}>{"// 커리어"}</div>
              <div style={{ color: "var(--fg-3)", fontSize: 11, marginTop: 6 }}>
                {meta.totalYears ? `${meta.totalYears} · ` : ""}
                {meta.totalRoles}
              </div>
              {meta.focusLines.length > 0 && (
                <div style={{ marginTop: 16 }}>
                  <div
                    style={{ color: "var(--fg-4)", fontSize: 10, letterSpacing: "0.14em" }}
                  >
                    FOCUS
                  </div>
                  {meta.focusLines.map((line) => (
                    <div
                      key={line}
                      style={{ color: "var(--fg-2)", fontSize: 11, marginTop: 4 }}
                    >
                      {line}
                    </div>
                  ))}
                </div>
              )}
            </div>
            <div style={{ position: "relative", paddingLeft: 28, minWidth: 0 }}>
              <div className="career-rail" />
              {roles.map((it) => renderRow("career", it))}
            </div>
          </div>

          {/* 교육 행 */}
          {education.length > 0 && (
            <div className="career-section" style={{ marginTop: 40 }}>
              <div className="career-section-label mono">
                <div style={{ color: "var(--accent)", fontSize: 13 }}>{"// 교육"}</div>
                <div style={{ color: "var(--fg-3)", fontSize: 11, marginTop: 6 }}>
                  {meta.educationCount} course{meta.educationCount !== 1 ? "s" : ""}
                </div>
              </div>
              <div style={{ position: "relative", paddingLeft: 28, minWidth: 0 }}>
                <div className="career-rail" />
                {education.map((it) => renderRow("education", it))}
              </div>
            </div>
          )}
        </div>

        {/* ── 오른쪽 — 상세 (sticky · 자체 스크롤) ────────────────── */}
        {!isNarrow && (
          <div className="career-detail-col">
            {selected ? (
              <DetailPanel item={selected} onProduct={setActiveProduct} />
            ) : (
              <div className="mono" style={{ fontSize: 13, color: "var(--fg-3)" }}>
                {"// 항목을 선택하세요"}
              </div>
            )}
          </div>
        )}
    </div>
    </>
  );
}

/* ══════════════════════════════════════════════════════════════════════════
 * 타임라인 compact row — period · 제목·org · summary 한 줄 · stack. 행 전체 클릭.
 * ══════════════════════════════════════════════════════════════════════════ */

function TimelineRow({
  item: it,
  active,
  onSelect,
}: {
  item: TimelineItem;
  active: boolean;
  onSelect: () => void;
}) {
  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onSelect}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onSelect();
        }
      }}
      className={active ? "career-row career-row--active" : "career-row"}
    >
      <span
        className="career-node"
        style={{
          border: `1px solid ${
            it.isCurrent ? "var(--accent)" : "var(--line-3)"
          }`,
          boxShadow: it.isCurrent ? "0 0 0 3px var(--accent-soft)" : "none",
        }}
      />
      <div
        className="mono"
        style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 5 }}
      >
        {it.period}
        {it.isCurrent && (
          <span style={{ color: "var(--accent)", marginLeft: 8 }}>● now</span>
        )}
      </div>
      <div
        style={{
          display: "flex",
          alignItems: "baseline",
          gap: 8,
          marginBottom: 5,
          flexWrap: "wrap",
        }}
      >
        <h3 style={{ margin: 0, fontSize: 17, letterSpacing: "-0.01em" }}>
          {it.title}
        </h3>
        <span style={{ color: "var(--fg-3)" }}>·</span>
        <span style={{ color: "var(--fg-1)", fontSize: 14 }}>{it.org}</span>
      </div>
      {it.summary && (
        <p
          className="career-row-summary"
          style={{
            margin: "0 0 8px",
            color: "var(--fg-2)",
            fontSize: 13,
            lineHeight: 1.55,
          }}
        >
          {it.summary}
        </p>
      )}
      {it.stack && it.stack.length > 0 && (
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
          {it.stack.map((s) => (
            <span key={s} className="tag">
              {s}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

/* ══════════════════════════════════════════════════════════════════════════
 * 상세 패널 — 선택 항목의 전체 상세. body md + 「만든 것」 + 「해결한 문제」.
 * (이전 CareerTimeline 펼침 내용 그대로. mermaid 는 ProductModal 몫이던 것을 보존.)
 * ══════════════════════════════════════════════════════════════════════════ */

function DetailPanel({
  item: it,
  onProduct,
}: {
  item: TimelineItem;
  onProduct: (p: CareerProduct) => void;
}) {
  // career 항목만 products·problems 를 갖는다 — education 은 body 뿐이다.
  const products = "products" in it ? it.products : [];
  const problems = "problems" in it ? it.problems : [];
  const hasBody = !!it.body && it.body.trim().length > 0;

  return (
    <div
      style={{
        padding: "24px 26px",
        background: "var(--bg-1)",
        border: "1px solid var(--line-1)",
        borderRadius: 8,
      }}
    >
      {/* 상세 머리 — 어느 항목의 상세인지 다시 명시(period · 제목 · org). */}
      <div
        className="mono"
        style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 4 }}
      >
        {it.period}
        {it.isCurrent && (
          <span style={{ color: "var(--accent)", marginLeft: 8 }}>● now</span>
        )}
        {it.location && (
          <span style={{ marginLeft: 8, color: "var(--fg-4)" }}>
            {it.location}
          </span>
        )}
      </div>
      <div
        style={{
          display: "flex",
          alignItems: "baseline",
          gap: 8,
          marginBottom: hasBody || products.length || problems.length ? 18 : 0,
          flexWrap: "wrap",
        }}
      >
        <h2 style={{ margin: 0, fontSize: 22, letterSpacing: "-0.01em" }}>
          {it.title}
        </h2>
        <span style={{ color: "var(--fg-3)" }}>·</span>
        <span style={{ color: "var(--fg-1)", fontSize: 16 }}>{it.org}</span>
      </div>

      {hasBody && <ProseBody body={it.body} />}

      {products.length > 0 && (
        <div style={{ marginTop: hasBody ? 20 : 0 }}>
          <div
            className="mono"
            style={{ fontSize: 11, color: "var(--accent)", marginBottom: 10 }}
          >
            // 만든 것
          </div>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
              gap: 12,
            }}
          >
            {products.map((p) => (
              <div
                key={p.id}
                role="button"
                tabIndex={0}
                onClick={() => onProduct(p)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    onProduct(p);
                  }
                }}
                className="career-product-card"
                style={{
                  padding: 14,
                  background: "var(--bg-0)",
                  border: "1px solid var(--line-1)",
                  borderRadius: 6,
                  cursor: "pointer",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "baseline",
                    gap: 8,
                    marginBottom: 6,
                  }}
                >
                  <span style={{ fontSize: 15, fontWeight: 600 }}>
                    {p.title}
                  </span>
                  {p.status && (
                    <span
                      className="mono"
                      style={{ fontSize: 10, color: "var(--fg-3)" }}
                    >
                      {p.status}
                    </span>
                  )}
                  <span
                    className="mono"
                    style={{
                      marginLeft: "auto",
                      fontSize: 11,
                      color: "var(--accent)",
                    }}
                  >
                    자세히 ↗
                  </span>
                </div>
                {p.summary && (
                  <p
                    style={{
                      margin: 0,
                      fontSize: 13,
                      lineHeight: 1.6,
                      color: "var(--fg-1)",
                    }}
                  >
                    {p.summary}
                  </p>
                )}
                {(p.links?.site || p.links?.docs) && (
                  <div
                    className="mono"
                    style={{ marginTop: 8, fontSize: 11, display: "flex", gap: 10 }}
                  >
                    {p.links?.site && (
                      <a
                        href={p.links.site}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        style={{ color: "var(--accent)" }}
                      >
                        site ↗
                      </a>
                    )}
                    {p.links?.docs && (
                      <a
                        href={p.links.docs}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        style={{ color: "var(--accent)" }}
                      >
                        docs ↗
                      </a>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {problems.length > 0 && (
        <div style={{ marginTop: hasBody || products.length > 0 ? 20 : 0 }}>
          <div
            className="mono"
            style={{ fontSize: 11, color: "var(--accent)", marginBottom: 4 }}
          >
            // 해결한 문제
          </div>
          {problems.map((pr) => (
            <div
              key={pr.id}
              style={{ padding: "10px 0", borderTop: "1px solid var(--line-1)" }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "baseline",
                  gap: 8,
                  flexWrap: "wrap",
                }}
              >
                <span style={{ fontSize: 14, fontWeight: 600 }}>{pr.title}</span>
                {pr.productTitle && (
                  <span
                    className="mono"
                    style={{ fontSize: 10, color: "var(--fg-3)" }}
                  >
                    @ {pr.productTitle}
                  </span>
                )}
              </div>
              {pr.body && (
                <p
                  style={{
                    margin: "6px 0 0",
                    fontSize: 13,
                    lineHeight: 1.65,
                    color: "var(--fg-1)",
                  }}
                >
                  {pr.body}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {!hasBody && products.length === 0 && problems.length === 0 && (
        <div className="mono" style={{ fontSize: 13, color: "var(--fg-3)" }}>
          {"// 상세 — 준비 중"}
        </div>
      )}
    </div>
  );
}

/* ══════════════════════════════════════════════════════════════════════════
 * ProductModal — 「만든 것」 카드 클릭 시 showcase(detail_path)를 모달로 연다.
 * 이 페이지의 핵심이라 화면을 덮어 크게 보여준다. 본문은 ShowcaseBody 재사용.
 * ══════════════════════════════════════════════════════════════════════════ */

function ProductModal({
  product,
  onClose,
}: {
  product: CareerProduct;
  onClose: () => void;
}) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = prev;
    };
  }, [onClose]);

  return (
    <div
      role="dialog"
      aria-modal="true"
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 100,
        background: "rgba(0,0,0,0.6)",
        display: "flex",
        alignItems: "flex-start",
        justifyContent: "center",
        padding: "48px 20px",
        overflowY: "auto",
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          position: "relative",
          width: "100%",
          maxWidth: 860,
          maxHeight: "calc(100vh - 96px)",
          display: "flex",
          flexDirection: "column",
          background: "var(--bg-1)",
          border: "1px solid var(--line-2)",
          borderRadius: 10,
          boxShadow: "var(--shadow-pop)",
          overflow: "hidden",
        }}
      >
        <button
          type="button"
          onClick={onClose}
          aria-label="닫기"
          className="mono"
          style={{
            position: "absolute",
            top: 14,
            right: 16,
            zIndex: 1,
            width: 28,
            height: 28,
            border: "1px solid var(--line-2)",
            borderRadius: 6,
            background: "var(--bg-2)",
            color: "var(--fg-2)",
            cursor: "pointer",
          }}
        >
          ✕
        </button>
        <div style={{ overflowY: "auto", padding: "40px 44px" }}>
          <ShowcaseBody product={product} />
        </div>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════════════════════════════
 * ShowcaseBody — 제품 showcase(detail_path) 를 md 로 그린다.
 * (remark-gfm · mermaid · assetUrl 이미지 rewrite 보존.)
 * ══════════════════════════════════════════════════════════════════════════ */

function ShowcaseBody({ product }: { product: CareerProduct }) {
  // 이미지 상대참조의 기준은 그 제품의 원장 디렉토리다.
  return (
    <DocBody
      body={product.body}
      assetBase={`para/projects/company/${product.slug}/`}
    />
  );
}
