"use client";

/**
 * PrintPortfolio — A4 landscape, cover sheet + KO/EN 합본.
 * 1 프로젝트 = 1+ atom (Pager 가 길이에 따라 자동 분할).
 * 케이스 스터디 필드 (problem/approach/impact/learnings/troubles) 비면 atom skip.
 */

import { useCallback, useState } from "react";
import { Sheet } from "./sheet";
import { Pager, type PagerAtom } from "./pager";
import type {
  PrintPortfolioResponse,
  PrintProjectItem,
  I18nPair,
  PrintTrouble,
} from "@/lib/print-types";

type Lang = "ko" | "en";

function pick<T>(val: I18nPair<T> | T | undefined, lang: Lang): T | undefined {
  if (val == null) return undefined;
  if (typeof val === "object" && val !== null && "ko" in val && "en" in val) {
    return (val as I18nPair<T>)[lang];
  }
  return val as T;
}

const STATUS_STYLES: Record<string, { bg: string; fg: string }> = {
  live:     { bg: "var(--accent-soft)", fg: "var(--accent)" },
  wip:      { bg: "#eef3fa",            fg: "var(--info)" },
  archived: { bg: "var(--bg-2)",         fg: "var(--fg-3)" },
};

function StatusPill({ s }: { s: string }) {
  const style = STATUS_STYLES[s] ?? STATUS_STYLES.archived;
  return (
    <span
      className="mono"
      style={{
        display: "inline-flex",
        gap: 4,
        alignItems: "center",
        fontSize: 9.5,
        color: style.fg,
        background: style.bg,
        border: `1px solid ${style.fg}33`,
        padding: "2px 7px",
        borderRadius: 3,
      }}
    >
      <span style={{ width: 5, height: 5, borderRadius: "50%", background: style.fg }} />
      {s}
    </span>
  );
}

function CoverSheet({ data, lang }: { data: PrintPortfolioResponse; lang: Lang }) {
  const T = (ko: string, en: string) => (lang === "en" ? en : ko);
  return (
    <Sheet orientation="landscape" meta={`portfolio · ${lang.toUpperCase()} · cover`}>
      <div
        style={{
          padding: "64px 72px",
          height: "100%",
          display: "grid",
          gridTemplateColumns: "1.4fr 1fr",
          gap: 64,
          alignItems: "center",
        }}
      >
        <div>
          <div className="caps" style={{ marginBottom: 24 }}>
            portfolio · 2026 · {lang === "en" ? "english" : "한국어"}
          </div>
          <h1 style={{ fontSize: 84, lineHeight: 0.95, letterSpacing: "-0.04em", fontWeight: 700, margin: 0 }}>
            {data.profile.name}
            <span style={{ color: "var(--accent)" }}>.</span>
          </h1>
          <div className="mono" style={{ fontSize: 14, color: "var(--fg-2)", marginTop: 16 }}>
            {data.profile.handle} · {data.profile.role}
            {data.profile.location ? ` · ${data.profile.location}` : ""}
          </div>
          <p style={{ fontSize: 16, lineHeight: 1.55, color: "var(--fg-1)", marginTop: 32, maxWidth: 460, fontWeight: 500 }}>
            {T(
              "각 프로젝트는 문제·접근·임팩트·배운 점·트러블 로그 순으로 정리되어 있습니다.",
              "Each project is organized as problem · approach · impact · learnings · trouble log.",
            )}
          </p>
          <div style={{ display: "flex", gap: 24, marginTop: 48, fontFamily: "var(--font-mono)", fontSize: 11 }}>
            <div><span style={{ color: "var(--fg-3)" }}>email </span>{data.profile.email}</div>
            {data.profile.github && (
              <div><span style={{ color: "var(--fg-3)" }}>github </span>{data.profile.github}</div>
            )}
          </div>
        </div>
        <div>
          <div className="caps" style={{ marginBottom: 12 }}>
            // contents · {data.projects.length} {T("프로젝트", "projects")}
          </div>
          <ol style={{ listStyle: "none", padding: 0, margin: 0, borderTop: "1px solid var(--line-2)" }}>
            {data.projects.map((p) => (
              <li
                key={p.id}
                style={{
                  display: "grid",
                  gridTemplateColumns: "32px 1fr 60px",
                  gap: 8,
                  alignItems: "baseline",
                  padding: "10px 0",
                  borderBottom: "1px solid var(--line-1)",
                }}
              >
                <span className="mono" style={{ fontSize: 10, color: "var(--fg-3)" }}>{p.id}</span>
                <span style={{ fontSize: 14, fontWeight: 600 }}>{pick(p.title, lang)}</span>
                <span className="mono" style={{ fontSize: 10, color: "var(--fg-3)", textAlign: "right" }}>{p.status}</span>
              </li>
            ))}
          </ol>
        </div>
      </div>
    </Sheet>
  );
}

function ProjectAtom({ p, lang }: { p: PrintProjectItem; lang: Lang }) {
  const title = pick(p.title, lang);
  const summary = pick(p.summary, lang);
  const problem = pick(p.problem, lang);
  const approach = pick(p.approach, lang);
  const impact = pick(p.impact, lang);
  const learnings = pick(p.learnings, lang);
  return (
    <div>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "baseline", gap: 12, paddingBottom: 12, borderBottom: "1px solid var(--line-2)" }}>
        <span className="mono" style={{ fontSize: 11, color: "var(--accent)" }}>{p.id}</span>
        {p.code && <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>/ {p.code}</span>}
        <h2 style={{ fontSize: 24, lineHeight: 1, marginLeft: 4, fontWeight: 700, margin: 0 }}>{title}</h2>
        <StatusPill s={p.status} />
        {p.date && <span className="mono" style={{ marginLeft: "auto", fontSize: 11, color: "var(--fg-3)" }}>{p.date}</span>}
      </div>

      {/* Summary */}
      {summary && (
        <p style={{ fontSize: 12, lineHeight: 1.6, color: "var(--fg-1)", marginTop: 10, marginBottom: 0 }}>{summary}</p>
      )}

      {/* Stack */}
      {p.stack.length > 0 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 4, marginTop: 8 }}>
          {p.stack.map((s) => (
            <span
              key={s}
              className="mono"
              style={{ fontSize: 9.5, padding: "1px 6px", border: "1px solid var(--line-2)", borderRadius: 3, color: "var(--fg-2)" }}
            >
              {s}
            </span>
          ))}
        </div>
      )}

      {/* Problem */}
      {problem && (
        <SubBlock label={lang === "en" ? "Problem" : "문제"}>
          <p style={atomP}>{problem}</p>
        </SubBlock>
      )}

      {/* Approach */}
      {approach && approach.length > 0 && (
        <SubBlock label={lang === "en" ? "Approach" : "접근"}>
          <BulletList items={approach} />
        </SubBlock>
      )}

      {/* Impact */}
      {impact && impact.length > 0 && (
        <SubBlock label={lang === "en" ? "Impact" : "임팩트"}>
          <BulletList items={impact} />
        </SubBlock>
      )}

      {/* Learnings */}
      {learnings && learnings.length > 0 && (
        <SubBlock label={lang === "en" ? "Learnings" : "배운 점"}>
          <BulletList items={learnings} />
        </SubBlock>
      )}

      {/* Trouble log */}
      {p.troubles.length > 0 && (
        <SubBlock label={lang === "en" ? "Trouble log" : "트러블 로그"}>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {p.troubles.map((t, i) => (
              <TroubleEntry key={i} t={t} lang={lang} />
            ))}
          </div>
        </SubBlock>
      )}
    </div>
  );
}

function SubBlock({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div style={{ marginTop: 12 }}>
      <div className="caps" style={{ fontSize: 9.5, marginBottom: 4 }}>{label}</div>
      {children}
    </div>
  );
}

function BulletList({ items }: { items: string[] }) {
  return (
    <ul style={{ margin: 0, paddingLeft: 16 }}>
      {items.map((b, i) => (
        <li key={i} style={atomP}>{b}</li>
      ))}
    </ul>
  );
}

function TroubleEntry({ t, lang }: { t: PrintTrouble; lang: Lang }) {
  const title = pick(t.title, lang);
  const cause = pick(t.cause, lang);
  const fix = pick(t.fix, lang);
  return (
    <div style={{ borderLeft: "2px solid var(--line-2)", paddingLeft: 8 }}>
      <div className="mono" style={{ fontSize: 10, color: "var(--fg-3)" }}>{t.when}</div>
      <div style={{ fontSize: 11.5, fontWeight: 600 }}>{title}</div>
      <div style={atomP}><span style={{ color: "var(--fg-3)" }}>원인 — </span>{cause}</div>
      <div style={atomP}><span style={{ color: "var(--accent)" }}>해결 — </span>{fix}</div>
    </div>
  );
}

const atomP: React.CSSProperties = {
  fontSize: 11,
  lineHeight: 1.55,
  color: "var(--fg-1)",
  margin: 0,
};

function FullHeader({ data, lang }: { data: PrintPortfolioResponse; lang: Lang }) {
  return (
    <div style={{ paddingBottom: 12, borderBottom: "1px solid var(--line-2)", display: "flex", alignItems: "center", gap: 16 }}>
      <div style={{ flex: 1 }}>
        <div className="caps">portfolio · {lang === "en" ? "english" : "한국어"}</div>
        <div style={{ fontSize: 16, fontWeight: 600, marginTop: 2 }}>
          {data.profile.name} <span style={{ color: "var(--fg-3)", fontWeight: 400 }}>· {data.profile.handle}</span>
        </div>
      </div>
      <div className="mono" style={{ fontSize: 10, color: "var(--fg-3)", textAlign: "right" }}>
        {data.profile.email}
        {data.profile.github && <><br />{data.profile.github}</>}
      </div>
    </div>
  );
}

function Footer({ data }: { data: PrintPortfolioResponse }) {
  return (
    <div
      style={{
        borderTop: "1px solid var(--line-1)",
        paddingTop: 8,
        marginTop: 12,
        display: "flex",
        justifyContent: "space-between",
        fontFamily: "var(--font-mono)",
        fontSize: 9,
        color: "var(--fg-3)",
      }}
    >
      <span>kknaks.dev</span>
      <span>portfolio · {data.profile.handle}</span>
    </div>
  );
}

export function PrintPortfolio({ data }: { data: PrintPortfolioResponse }) {
  const langs: Lang[] = ["ko", "en"];
  const [readySet, setReadySet] = useState<Set<Lang>>(new Set());
  const allReady = readySet.size === langs.length;

  const onPagerReady = useCallback((lang: Lang) => {
    setReadySet((prev) => {
      if (prev.has(lang)) return prev;
      const next = new Set(prev);
      next.add(lang);
      return next;
    });
  }, []);

  return (
    <>
      {langs.map((lang) => (
        <div key={lang}>
          <CoverSheet data={data} lang={lang} />
          <Pager
            orientation="landscape"
            contentWidth={1123}
            contentHeight={794}
            paddingX={64}
            paddingY={48}
            header={<FullHeader data={data} lang={lang} />}
            compactHeader={<FullHeader data={data} lang={lang} />}
            footer={<Footer data={data} />}
            atoms={data.projects.map(
              (p): PagerAtom => ({
                key: `${lang}-${p.id}`,
                node: <ProjectAtom p={p} lang={lang} />,
              }),
            )}
            gap={24}
            meta={`portfolio · ${lang.toUpperCase()}`}
            onReady={() => onPagerReady(lang)}
          />
        </div>
      ))}
      {allReady && <div data-print-ready aria-hidden style={{ display: "none" }} />}
    </>
  );
}
