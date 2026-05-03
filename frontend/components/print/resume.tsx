"use client";

/**
 * PrintResume — KO + EN 두 lang 을 각각 Pager 로 렌더.
 * playwright 가 두 Pager 의 모든 sheet 를 한 PDF 안에 캡처.
 * 둘 다 ready 되면 root 에 `data-print-ready` 박아 playwright wait selector 로 사용.
 */

import { useCallback, useState } from "react";
import { Pager, type PagerAtom } from "./pager";
import type { PrintResumeResponse, I18nPair, PrintCareerItem } from "@/lib/print-types";

type Lang = "ko" | "en";

function pick<T>(val: I18nPair<T> | T | undefined, lang: Lang): T | undefined {
  if (val == null) return undefined;
  if (typeof val === "object" && val !== null && "ko" in val && "en" in val) {
    return (val as I18nPair<T>)[lang];
  }
  return val as T;
}

function buildAtoms(data: PrintResumeResponse, lang: Lang): PagerAtom[] {
  const atoms: PagerAtom[] = [];

  // 01 About
  const intro = pick(data.about.intro, lang);
  const intro2 = pick(data.about.intro2, lang);
  atoms.push({
    key: "about",
    node: (
      <section>
        <div className="caps" style={{ marginBottom: 8 }}>01 / About</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          {intro && <p style={atomP}>{intro}</p>}
          {intro2 && <p style={atomP}>{intro2}</p>}
        </div>
      </section>
    ),
  });

  // 02 Career — 1 item = 1 atom
  data.career.forEach((c, idx) => {
    atoms.push({
      key: `career-${idx}`,
      node: <CareerAtom item={c} lang={lang} idx={idx} />,
    });
  });

  return atoms;
}

const atomP: React.CSSProperties = {
  fontSize: 11.5,
  lineHeight: 1.65,
  color: "var(--fg-1)",
  margin: 0,
};

function CareerAtom({ item, lang, idx }: { item: PrintCareerItem; lang: Lang; idx: number }) {
  const title = pick(item.title, lang);
  const org = typeof item.org === "string" ? item.org : pick(item.org, lang);
  const loc =
    typeof item.location === "string"
      ? item.location
      : pick(item.location, lang);
  const summary = pick(item.summary, lang);
  return (
    <div>
      {idx === 0 && (
        <div className="caps" style={{ marginBottom: 8 }}>02 / Career</div>
      )}
      <div style={{ display: "flex", alignItems: "baseline", gap: 8, flexWrap: "wrap" }}>
        <span className="mono" style={{ fontSize: 10.5, color: item.is_current ? "var(--accent)" : "var(--fg-3)" }}>
          {item.period}
        </span>
      </div>
      <h3 style={{ fontSize: 13.5, margin: "4px 0 2px", fontWeight: 600 }}>
        {title} <span style={{ fontSize: 11.5, color: "var(--fg-2)", fontWeight: 400 }}>· {org}</span>
        {loc && <span className="mono" style={{ fontSize: 10, color: "var(--fg-3)", marginLeft: 6 }}>· {loc}</span>}
      </h3>
      {summary && <p style={{ ...atomP, marginTop: 4 }}>{summary}</p>}
      {item.stack.length > 0 && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 4, marginTop: 6 }}>
          {item.stack.map((s) => (
            <span
              key={s}
              className="mono"
              style={{
                fontSize: 9,
                padding: "1px 5px",
                border: "1px solid var(--line-2)",
                borderRadius: 3,
                color: "var(--fg-2)",
              }}
            >
              {s}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

function FullHeader({ data, lang }: { data: PrintResumeResponse; lang: Lang }) {
  const tagline = pick(data.profile.tagline, lang);
  const langLabel = lang === "en" ? "english" : "한국어";
  return (
    <div style={{ paddingBottom: 18, borderBottom: "1px solid var(--line-2)" }}>
      <div className="caps">resume · {langLabel}</div>
      <h1
        style={{
          fontSize: 32,
          lineHeight: 1.05,
          marginTop: 4,
          fontWeight: 700,
          letterSpacing: "-0.025em",
        }}
      >
        {data.profile.name}{" "}
        <span className="mono" style={{ fontSize: 14, color: "var(--fg-3)", fontWeight: 400 }}>
          · {data.profile.handle}
        </span>
      </h1>
      <div className="mono" style={{ fontSize: 11, color: "var(--fg-2)", marginTop: 4 }}>
        {data.profile.role}
        {data.profile.location ? ` · ${data.profile.location}` : ""}
      </div>
      {tagline && (
        <p style={{ fontSize: 13, lineHeight: 1.55, color: "var(--fg-0)", fontWeight: 500, marginTop: 14 }}>
          {tagline}
        </p>
      )}
    </div>
  );
}

function CompactHeader({ data, lang }: { data: PrintResumeResponse; lang: Lang }) {
  const langLabel = lang === "en" ? "english" : "한국어";
  return (
    <div style={{ paddingBottom: 10, borderBottom: "1px solid var(--line-1)" }}>
      <div style={{ fontSize: 14, fontWeight: 600 }}>
        {data.profile.name} · {data.profile.handle}
      </div>
      <div className="caps">resume · {langLabel} · continued</div>
    </div>
  );
}

function Footer({ data }: { data: PrintResumeResponse }) {
  return (
    <div
      style={{
        borderTop: "1px solid var(--line-1)",
        paddingTop: 10,
        marginTop: 12,
        display: "flex",
        justifyContent: "space-between",
        fontFamily: "var(--font-mono)",
        fontSize: 9,
        color: "var(--fg-3)",
      }}
    >
      <span>kknaks.dev</span>
      <span>{data.profile.email}</span>
    </div>
  );
}

export function PrintResume({ data }: { data: PrintResumeResponse }) {
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
        <Pager
          key={lang}
          orientation="portrait"
          contentWidth={794}
          contentHeight={1123}
          paddingX={56}
          paddingY={52}
          header={<FullHeader data={data} lang={lang} />}
          compactHeader={<CompactHeader data={data} lang={lang} />}
          footer={<Footer data={data} />}
          atoms={buildAtoms(data, lang)}
          gap={14}
          meta={`resume · ${lang.toUpperCase()}`}
          onReady={() => onPagerReady(lang)}
        />
      ))}
      {allReady && <div data-print-ready aria-hidden style={{ display: "none" }} />}
    </>
  );
}
