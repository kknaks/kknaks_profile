"use client";

/**
 * PrintResume — KO + EN 합본. 두 Pager 가 각자 분할 → 한 PDF 안에 KO 페이지 + EN 페이지.
 * 원본: claude_design/kknaks_profile_v2.0.0/print/resume-sheet.jsx (lang prop 그대로)
 *
 * playwright wait selector: 두 Pager 모두 ready 시 [data-print-ready] sentinel.
 */

import { useCallback, useState, type ReactNode } from "react";
import { Pager, type PagerAtom } from "./pager";
import { Monogram } from "./monogram";
import type {
  PrintResumeResponse,
  I18nPair,
  PrintCareerItem,
  PrintSkills,
  PrintEducationItem,
  PrintAwardItem,
  PrintResumeProjectMini,
} from "@/lib/print-types";

type Lang = "ko" | "en";

const SITE = "kknaks.dev";

function pick<T>(val: I18nPair<T> | T | undefined | null, lang: Lang): T | undefined {
  if (val == null) return undefined;
  if (typeof val === "object" && val !== null && "ko" in (val as object) && "en" in (val as object)) {
    return (val as I18nPair<T>)[lang];
  }
  return val as T;
}

const LANG_LABEL: Record<Lang, string> = { ko: "한국어", en: "english" };

const T = (lang: Lang, ko: string, en: string) => (lang === "ko" ? ko : en);

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
          footer={<FooterRow lang={lang} />}
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

/* =========================================================
   Header / Footer
   ========================================================= */

function FullHeader({ data, lang }: { data: PrintResumeResponse; lang: Lang }) {
  const name = pick(data.profile.name, lang);
  const role = pick(data.profile.role, lang);
  const location = pick(data.profile.location, lang);
  const tagline = pick(data.profile.tagline, lang);
  return (
    <div>
      <header
        style={{
          display: "flex",
          alignItems: "flex-start",
          gap: 18,
          paddingBottom: 18,
          borderBottom: "1px solid var(--line-2)",
        }}
      >
        <Monogram size={44} />
        <div style={{ flex: 1, minWidth: 0 }}>
          <div
            className="mono"
            style={{
              fontSize: 10,
              color: "var(--fg-3)",
              textTransform: "uppercase",
              letterSpacing: "0.18em",
            }}
          >
            resume · {LANG_LABEL[lang]}
          </div>
          <h1
            style={{
              fontSize: 32,
              lineHeight: 1.05,
              marginTop: 4,
              fontWeight: 700,
              letterSpacing: "-0.025em",
              display: "flex",
              alignItems: "baseline",
              gap: 10,
              flexWrap: "wrap",
            }}
          >
            <span>{name}</span>
            <span
              className="mono"
              style={{ fontSize: 14, color: "var(--fg-3)", fontWeight: 400 }}
            >
              · {data.profile.handle}
            </span>
          </h1>
          <div className="mono" style={{ fontSize: 11, color: "var(--fg-2)", marginTop: 4 }}>
            {role}
            {location ? ` · ${location}` : ""}
          </div>
        </div>
        <div
          style={{
            textAlign: "right",
            fontFamily: "var(--font-mono)",
            fontSize: 10,
            lineHeight: 1.7,
            color: "var(--fg-1)",
          }}
        >
          <div>
            <span style={{ color: "var(--fg-3)" }}>email </span>
            {data.profile.email}
          </div>
          {data.profile.github && (
            <div>
              <span style={{ color: "var(--fg-3)" }}>github </span>
              {data.profile.github}
            </div>
          )}
          <div>
            <span style={{ color: "var(--fg-3)" }}>site </span>
            {SITE}
          </div>
        </div>
      </header>
      {tagline && (
        <p
          style={{
            fontSize: 14,
            lineHeight: 1.55,
            color: "var(--fg-0)",
            fontWeight: 500,
            marginTop: 18,
            letterSpacing: "-0.005em",
          }}
        >
          {tagline}
        </p>
      )}
    </div>
  );
}

function CompactHeader({ data, lang }: { data: PrintResumeResponse; lang: Lang }) {
  const name = pick(data.profile.name, lang);
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 12,
        paddingBottom: 10,
        borderBottom: "1px solid var(--line-1)",
      }}
    >
      <Monogram size={28} />
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 14, fontWeight: 600, lineHeight: 1.2 }}>
          {name}
          <span
            className="mono"
            style={{ fontSize: 10, color: "var(--fg-3)", fontWeight: 400, marginLeft: 8 }}
          >
            · {data.profile.handle}
          </span>
        </div>
        <div
          className="mono"
          style={{
            fontSize: 9.5,
            color: "var(--fg-3)",
            letterSpacing: "0.08em",
            marginTop: 1,
          }}
        >
          resume · {LANG_LABEL[lang]} · continued
        </div>
      </div>
      <div
        className="mono"
        style={{ fontSize: 9.5, color: "var(--fg-3)", textAlign: "right" }}
      >
        {data.profile.email}
        {data.profile.github && (
          <>
            <br />
            {data.profile.github}
          </>
        )}
      </div>
    </div>
  );
}

function FooterRow({ lang }: { lang: Lang }) {
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
      <span>
        {T(
          lang,
          "전체 프로젝트 케이스는 별도 포트폴리오 문서를 참고해주세요.",
          "See the separate portfolio document for full project cases.",
        )}
      </span>
      <span>{SITE}</span>
    </div>
  );
}

/* =========================================================
   Atom builder — 빈 배열 (education/awards/projects) 이면 SectionHeadOnly atom 도 push 안 함.
   ========================================================= */

function buildAtoms(data: PrintResumeResponse, lang: Lang): PagerAtom[] {
  const atoms: PagerAtom[] = [];

  // 01 About
  const intro = pick(data.about.intro, lang);
  const intro2 = pick(data.about.intro2, lang);
  const aboutParas = [intro, intro2].filter((p): p is string => Boolean(p));
  if (aboutParas.length > 0) {
    atoms.push({
      key: "about",
      node: (
        <SectionAtom idx="01" label="About" sublabel={T(lang, "한 줄 소개", "who I am")}>
          <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
            {aboutParas.map((p, i) => (
              <p
                key={i}
                style={{ fontSize: 11.5, lineHeight: 1.65, color: "var(--fg-1)" }}
              >
                {p}
              </p>
            ))}
          </div>
        </SectionAtom>
      ),
    });
  }

  // 02 Skills
  const skills = data.skills;
  if (
    skills &&
    ((skills.primary && skills.primary.length) ||
      (skills.secondary && skills.secondary.length) ||
      (skills.learning && skills.learning.length))
  ) {
    atoms.push({
      key: "skills",
      node: (
        <SectionAtom
          idx="02"
          label="Skills"
          sublabel={T(lang, "주력 / 익숙 / 학습", "primary / working / learning")}
        >
          <SkillsGrid skills={skills} lang={lang} />
        </SectionAtom>
      ),
    });
  }

  // 03 Career — head + per-item
  if (data.career.length > 0) {
    atoms.push({
      key: "career-head",
      node: (
        <SectionHeadOnly
          idx="03"
          label="Career"
          sublabel={T(lang, "언제 · 어디서", "when · where")}
        />
      ),
    });
    data.career.forEach((c, i) => {
      atoms.push({
        key: `career-${i}`,
        node: <CareerItem c={c} lang={lang} />,
      });
    });
  }

  // 04 Education
  if (data.education.length > 0) {
    atoms.push({
      key: "edu-head",
      node: <SectionHeadOnly idx="04" label="Education" sublabel={T(lang, "학력", "school")} />,
    });
    data.education.forEach((e, i) => {
      atoms.push({
        key: `edu-${i}`,
        node: <EducationItem e={e} lang={lang} />,
      });
    });
  }

  // 05 Activities
  if (data.awards.length > 0) {
    atoms.push({
      key: "awards-head",
      node: (
        <SectionHeadOnly idx="05" label="Activities" sublabel={T(lang, "수상", "awards")} />
      ),
    });
    data.awards.forEach((a, i) => {
      atoms.push({
        key: `awards-${i}`,
        node: <AwardItem a={a} lang={lang} />,
      });
    });
  }

  // 06 Projects mini
  if (data.projects.length > 0) {
    atoms.push({
      key: "projects-head",
      node: (
        <SectionHeadOnly
          idx="06"
          label="Projects"
          sublabel={T(lang, "상세는 포트폴리오 참고", "see portfolio for detail")}
        />
      ),
    });
    for (let i = 0; i < data.projects.length; i += 2) {
      const pair = data.projects.slice(i, i + 2);
      atoms.push({
        key: `projects-${i}`,
        node: <ProjectsPair pair={pair} lang={lang} />,
      });
    }
  }

  return atoms;
}

/* =========================================================
   Section heading primitives
   ========================================================= */

function SectionHeadOnly({
  idx,
  label,
  sublabel,
}: {
  idx: string;
  label: string;
  sublabel?: string;
}) {
  return (
    <div
      className="mono"
      style={{
        fontSize: 9.5,
        color: "var(--fg-3)",
        textTransform: "uppercase",
        letterSpacing: "0.16em",
        display: "flex",
        alignItems: "center",
        gap: 8,
      }}
    >
      <span style={{ color: "var(--accent)", flexShrink: 0 }}>{idx}</span>
      <span style={{ color: "var(--fg-0)", fontWeight: 600, flexShrink: 0 }}>{label}</span>
      <span style={{ flex: 1, minWidth: 12, height: 1, background: "var(--line-1)" }} />
      {sublabel && (
        <span style={{ color: "var(--fg-3)", flexShrink: 0, whiteSpace: "nowrap" }}>
          {sublabel}
        </span>
      )}
    </div>
  );
}

function SectionAtom({
  idx,
  label,
  sublabel,
  children,
}: {
  idx: string;
  label: string;
  sublabel?: string;
  children: ReactNode;
}) {
  return (
    <section>
      <div
        className="mono"
        style={{
          fontSize: 9.5,
          color: "var(--fg-3)",
          textTransform: "uppercase",
          letterSpacing: "0.16em",
          marginBottom: 8,
          display: "flex",
          alignItems: "center",
          gap: 8,
        }}
      >
        <span style={{ color: "var(--accent)", flexShrink: 0 }}>{idx}</span>
        <span style={{ color: "var(--fg-0)", fontWeight: 600, flexShrink: 0 }}>{label}</span>
        <span
          style={{ flex: 1, minWidth: 12, height: 1, background: "var(--line-1)" }}
        />
        {sublabel && (
          <span style={{ color: "var(--fg-3)", flexShrink: 0, whiteSpace: "nowrap" }}>
            {sublabel}
          </span>
        )}
      </div>
      {children}
    </section>
  );
}

/* =========================================================
   02 Skills — 3-col grid
   ========================================================= */

function SkillsGrid({ skills, lang }: { skills: PrintSkills; lang: Lang }) {
  const tiers: Array<{ key: keyof PrintSkills; labelKo: string; labelEn: string; accent: boolean }> = [
    { key: "primary",   labelKo: "주력",        labelEn: "Primary",  accent: true },
    { key: "secondary", labelKo: "익숙",        labelEn: "Working",  accent: false },
    { key: "learning",  labelKo: "관심·학습 중", labelEn: "Learning", accent: false },
  ];
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 14 }}>
      {tiers.map(({ key, labelKo, labelEn, accent }) => {
        const list = skills[key] ?? [];
        return (
          <div key={key}>
            <div
              className="mono"
              style={{
                fontSize: 10,
                color: accent ? "var(--accent)" : "var(--fg-3)",
                textTransform: "uppercase",
                letterSpacing: "0.12em",
                marginBottom: 6,
              }}
            >
              // {lang === "en" ? labelEn : labelKo}
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
              {list.map((s) => (
                <span
                  key={s}
                  className={accent ? "tag accent" : "tag"}
                  style={{ fontSize: 10 }}
                >
                  {s}
                </span>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

/* =========================================================
   03 Career — 110px 1fr 2-col
   ========================================================= */

function CareerItem({ c, lang }: { c: PrintCareerItem; lang: Lang }) {
  const role = pick(c.title, lang);
  const org = pick(c.org, lang);
  const loc = pick(c.location, lang);
  const summary = pick(c.summary, lang);
  const bullets = pick(c.bullets, lang) as string[] | undefined;
  return (
    <div style={{ display: "grid", gridTemplateColumns: "110px 1fr", gap: 16 }}>
      <div>
        <div className="mono" style={{ fontSize: 10, color: c.is_current ? "var(--accent)" : "var(--fg-3)" }}>
          {c.period}
        </div>
      </div>
      <div>
        <div style={{ display: "flex", alignItems: "baseline", gap: 6, flexWrap: "wrap" }}>
          <span style={{ fontSize: 13, fontWeight: 600 }}>{role}</span>
          {org && (
            <>
              <span style={{ color: "var(--fg-3)" }}>·</span>
              <span style={{ fontSize: 12, color: "var(--fg-1)" }}>{org}</span>
            </>
          )}
          {loc && (
            <span
              className="mono"
              style={{ marginLeft: "auto", fontSize: 10, color: "var(--fg-3)" }}
            >
              {loc}
            </span>
          )}
        </div>
        {summary && (
          <p style={{ fontSize: 11, color: "var(--fg-1)", lineHeight: 1.6, marginTop: 4 }}>
            {summary}
          </p>
        )}
        {bullets && bullets.length > 0 && (
          <ul style={{ marginTop: 6, paddingLeft: 14, color: "var(--fg-1)" }}>
            {bullets.map((b, j) => (
              <li key={j} style={{ fontSize: 10.5, lineHeight: 1.55, marginBottom: 2 }}>
                {b}
              </li>
            ))}
          </ul>
        )}
        {c.stack.length > 0 && (
          <div style={{ display: "flex", flexWrap: "wrap", gap: 4, marginTop: 7 }}>
            {c.stack.map((t) => (
              <span key={t} className="tag" style={{ fontSize: 9.5 }}>
                {t}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   04 Education / 05 Activities — 같은 110px 1fr
   ========================================================= */

function EducationItem({ e, lang }: { e: PrintEducationItem; lang: Lang }) {
  const degree = pick(e.degree, lang);
  const org = pick(e.org, lang);
  const note = pick(e.note, lang);
  return (
    <div style={{ display: "grid", gridTemplateColumns: "110px 1fr", gap: 16 }}>
      <div className="mono" style={{ fontSize: 10, color: "var(--fg-3)" }}>
        {e.period}
      </div>
      <div>
        <div style={{ fontSize: 12, fontWeight: 600 }}>
          {degree}
          {org && (
            <>
              <span style={{ color: "var(--fg-3)", fontWeight: 400 }}> · </span>
              <span style={{ color: "var(--fg-1)", fontWeight: 400 }}>{org}</span>
            </>
          )}
        </div>
        {note && (
          <p style={{ fontSize: 11, color: "var(--fg-2)", lineHeight: 1.55, marginTop: 4 }}>
            {note}
          </p>
        )}
      </div>
    </div>
  );
}

function AwardItem({ a, lang }: { a: PrintAwardItem; lang: Lang }) {
  const title = pick(a.title, lang);
  const note = pick(a.note, lang);
  return (
    <div style={{ display: "grid", gridTemplateColumns: "110px 1fr", gap: 16 }}>
      <div className="mono" style={{ fontSize: 10, color: "var(--fg-3)" }}>
        {a.period}
      </div>
      <div>
        <div style={{ fontSize: 12, fontWeight: 600 }}>{title}</div>
        {note && (
          <div style={{ fontSize: 11, color: "var(--fg-2)", marginTop: 2 }}>{note}</div>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   06 Projects mini — 2-col 페어 카드
   ========================================================= */

function ProjectsPair({
  pair,
  lang,
}: {
  pair: PrintResumeProjectMini[];
  lang: Lang;
}) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
      {pair.map((p) => (
        <div key={p.id} style={{ borderTop: "1px solid var(--line-1)", paddingTop: 7 }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 6 }}>
            <span className="mono" style={{ fontSize: 9, color: "var(--fg-3)" }}>
              {p.id}
            </span>
            <span style={{ fontSize: 11.5, fontWeight: 600 }}>{pick(p.title, lang)}</span>
            {p.period && (
              <span
                className="mono"
                style={{ fontSize: 9, color: "var(--fg-3)", marginLeft: "auto" }}
              >
                {p.period}
              </span>
            )}
          </div>
          <p style={{ fontSize: 10.5, color: "var(--fg-2)", lineHeight: 1.5, marginTop: 3 }}>
            {pick(p.summary, lang)}
          </p>
        </div>
      ))}
    </div>
  );
}
