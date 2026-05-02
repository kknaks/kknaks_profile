import Link from "next/link";
import type { Lang } from "@/lib/i18n";
import type {
  CareerResponse,
  ContentsResponse,
  MeResponse,
  NoteRecent,
  NotesGraphResponse,
  ProjectsResponse,
} from "@/lib/types";

interface Props {
  lang: Lang;
  me: MeResponse;
  career: CareerResponse;
  projects: ProjectsResponse;
  notesGraph: NotesGraphResponse;
  notesRecent: NoteRecent[];
  contents: ContentsResponse;
}

function Section({
  idx,
  id,
  title,
  sub,
  langSuffix,
  viewAllLabel,
  children,
}: {
  idx: string;
  id: string;
  title: string;
  sub: string;
  langSuffix: string;
  viewAllLabel: string;
  children: React.ReactNode;
}) {
  return (
    <section
      className="pad-x"
      style={{
        padding: "56px 80px",
        borderTop: "1px solid var(--line-1)",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "baseline",
          gap: 16,
          marginBottom: 28,
          flexWrap: "wrap",
        }}
      >
        <span className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          {idx}
        </span>
        <h2
          className="m-h2"
          style={{
            fontSize: 32,
            letterSpacing: "-0.02em",
            margin: 0,
            fontWeight: 600,
          }}
        >
          {title}
        </h2>
        <span style={{ color: "var(--fg-3)", fontSize: 14, marginLeft: 4 }}>
          · {sub}
        </span>
        <Link
          href={`/${id}${langSuffix}`}
          className="btn ghost"
          style={{ marginLeft: "auto", padding: "6px 10px", fontSize: 12 }}
        >
          {viewAllLabel} <span className="arrow">→</span>
        </Link>
      </div>
      {children}
    </section>
  );
}

export function LandingPreview({
  lang,
  me,
  career,
  projects,
  notesGraph,
  notesRecent,
  contents,
}: Props) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);
  const langSuffix = lang === "ko" ? "" : `?lang=${lang}`;
  const viewAllLabel = t("전체 보기", "View all");
  const { user } = me;

  const careerItems = career["career[]"].slice(0, 2);
  const projectItems = projects["projects[]"].slice(0, 2);
  const recentNotes = notesRecent.slice(0, 5);
  const stacks = notesGraph.notes.stacks.slice(0, 10);
  const contentItems = contents["contents[]"];
  const latestContent = contentItems[0];
  const olderContents = contentItems.slice(1, 5);

  return (
    <>
      {/* About preview */}
      <Section
        idx="01"
        id="about"
        title="About"
        sub={me.about?.subtitle ?? t("만드는 사람", "who builds it")}
        langSuffix={langSuffix}
        viewAllLabel={viewAllLabel}
      >
        <div
          className="m-stack"
          style={{
            display: "grid",
            gridTemplateColumns: "1.4fr 1fr",
            gap: 48,
            alignItems: "start",
          }}
        >
          <p
            style={{
              fontSize: 19,
              lineHeight: 1.6,
              color: "var(--fg-0)",
              margin: 0,
              maxWidth: 640,
            }}
          >
            {user.tagline}
          </p>
          <dl style={{ margin: 0, fontSize: 13 }}>
            {[
              ["location", user.location ?? "—"],
              ["focus", user.focus ?? "—"],
              ["stack", user.stackShort ?? user.stack.slice(0, 3).join(" · ")],
              ["email", user.email],
            ].map(([k, v]) => (
              <div
                key={k}
                style={{
                  display: "grid",
                  gridTemplateColumns: "90px 1fr",
                  padding: "8px 0",
                  borderTop: "1px solid var(--line-1)",
                }}
              >
                <dt className="mono" style={{ color: "var(--fg-3)" }}>
                  {k}
                </dt>
                <dd style={{ margin: 0, color: "var(--fg-1)" }}>{v}</dd>
              </div>
            ))}
          </dl>
        </div>
      </Section>

      {/* Career preview */}
      <Section
        idx="02"
        id="career"
        title="Career"
        sub={career.career?.subtitle ?? t("최근 이력", "recent roles")}
        langSuffix={langSuffix}
        viewAllLabel={viewAllLabel}
      >
        <div style={{ position: "relative", paddingLeft: 28, maxWidth: 720 }}>
          <div
            style={{
              position: "absolute",
              left: 5,
              top: 8,
              bottom: 8,
              width: 1,
              background: "var(--line-2)",
            }}
          />
          {careerItems.map((it, i) => (
            <div key={i} style={{ position: "relative", marginBottom: 24 }}>
              <span
                style={{
                  position: "absolute",
                  left: -28,
                  top: 8,
                  width: 11,
                  height: 11,
                  borderRadius: 2,
                  background: "var(--bg-0)",
                  border: `1px solid ${
                    it.is_current ? "var(--accent)" : "var(--line-3)"
                  }`,
                  boxShadow: it.is_current
                    ? "0 0 0 3px var(--accent-soft)"
                    : "none",
                }}
              />
              <div
                className="mono"
                style={{
                  fontSize: 11,
                  color: "var(--fg-3)",
                  marginBottom: 4,
                }}
              >
                {it.period}
                {it.is_current && (
                  <span style={{ color: "var(--accent)", marginLeft: 8 }}>
                    ● now
                  </span>
                )}
              </div>
              <div
                style={{
                  display: "flex",
                  alignItems: "baseline",
                  gap: 8,
                  marginBottom: 4,
                }}
              >
                <h3 style={{ margin: 0, fontSize: 17, fontWeight: 500 }}>
                  {it.title}
                </h3>
                <span style={{ color: "var(--fg-3)" }}>·</span>
                <span style={{ color: "var(--fg-1)" }}>{it.org}</span>
              </div>
              <p
                style={{
                  margin: 0,
                  color: "var(--fg-1)",
                  fontSize: 14,
                  lineHeight: 1.6,
                }}
              >
                {it.summary}
              </p>
            </div>
          ))}
        </div>
      </Section>

      {/* Projects preview */}
      <Section
        idx="03"
        id="projects"
        title="Projects"
        sub={projects.projects?.subtitle ?? t("혼자 만든 것들", "solo work")}
        langSuffix={langSuffix}
        viewAllLabel={viewAllLabel}
      >
        <div
          className="m-stack"
          style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}
        >
          {projectItems.map((p) => (
            <Link
              key={p.id}
              href={`/projects${langSuffix}#${p.id}`}
              className="card"
              style={{ overflow: "hidden", display: "block" }}
            >
              <div
                className="placeholder-hatch"
                style={{ aspectRatio: "16/9" }}
              >
                [ {p.title} · 1600×900 ]
              </div>
              <div
                style={{
                  padding: 18,
                  borderTop: "1px solid var(--line-1)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                    marginBottom: 8,
                  }}
                >
                  <span
                    className="mono"
                    style={{ fontSize: 11, color: "var(--fg-3)" }}
                  >
                    {p.id}
                  </span>
                  <span
                    className={`tag${p.status === "live" ? " accent" : ""}`}
                  >
                    {p.status === "live" && (
                      <span
                        className="tag-dot"
                        style={{ background: "var(--accent)" }}
                      />
                    )}
                    {p.status}
                  </span>
                  {p.date && (
                    <span
                      className="mono"
                      style={{
                        fontSize: 11,
                        color: "var(--fg-3)",
                        marginLeft: "auto",
                      }}
                    >
                      {p.date}
                    </span>
                  )}
                </div>
                <h3 style={{ margin: "0 0 6px", fontSize: 17 }}>{p.title}</h3>
                <p
                  style={{
                    margin: "0 0 10px",
                    fontSize: 13,
                    color: "var(--fg-2)",
                    lineHeight: 1.5,
                  }}
                >
                  {p.summary}
                </p>
                <div
                  style={{
                    display: "flex",
                    gap: 6,
                    flexWrap: "wrap",
                  }}
                >
                  {p.stack.map((tg) => (
                    <span key={tg} className="tag">
                      {tg}
                    </span>
                  ))}
                </div>
              </div>
            </Link>
          ))}
        </div>
      </Section>

      {/* Notes preview */}
      <Section
        idx="04"
        id="notes"
        title="Notes"
        sub={t(
          `옵시디언 vault 미러 · ${notesGraph.notes.totalCount}+ 노트`,
          `obsidian vault mirror · ${notesGraph.notes.totalCount}+ notes`,
        )}
        langSuffix={langSuffix}
        viewAllLabel={viewAllLabel}
      >
        <div
          className="m-stack"
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 32,
            paddingTop: 8,
          }}
        >
          <div>
            <div className="caps" style={{ marginBottom: 12 }}>
              recent
            </div>
            <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
              {recentNotes.map((n) => (
                <li
                  key={n.id}
                  style={{
                    display: "grid",
                    gridTemplateColumns: "88px 1fr 110px",
                    gap: 16,
                    padding: "10px 0",
                    borderTop: "1px solid var(--line-1)",
                    alignItems: "baseline",
                    fontSize: 14,
                  }}
                >
                  <span
                    className="mono"
                    style={{ fontSize: 11, color: "var(--fg-3)" }}
                  >
                    {n.date ?? ""}
                  </span>
                  <Link
                    href={`/notes${langSuffix}#${n.id}`}
                    style={{ color: "var(--fg-0)" }}
                  >
                    {n.title}
                  </Link>
                  <span
                    className="mono"
                    style={{
                      fontSize: 11,
                      color: "var(--fg-3)",
                      textAlign: "right",
                    }}
                  >
                    {n.path}
                  </span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <div className="caps" style={{ marginBottom: 12 }}>
              tech stack
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
              {stacks.map((s) => (
                <span
                  key={s.name}
                  className="tag"
                  style={{
                    fontSize: 11,
                    color: "oklch(0.82 0.13 80)",
                    borderColor: "oklch(0.82 0.13 80 / 0.3)",
                  }}
                >
                  {s.name}
                  <span style={{ color: "var(--fg-3)", marginLeft: 4 }}>
                    {s.count}
                  </span>
                </span>
              ))}
            </div>
            <div className="caps" style={{ marginTop: 24, marginBottom: 8 }}>
              graph
            </div>
            <div
              style={{
                position: "relative",
                height: 180,
                background: "var(--bg-2)",
                border: "1px solid var(--line-1)",
                borderRadius: 6,
                overflow: "hidden",
              }}
            >
              <NotesGraphPreview
                stacks={stacks.slice(0, 5)}
                noteCount={notesGraph.notes.totalCount}
              />
              <div
                className="mono"
                style={{
                  position: "absolute",
                  bottom: 6,
                  right: 8,
                  fontSize: 10,
                  color: "var(--fg-3)",
                }}
              >
                // preview
              </div>
            </div>
          </div>
        </div>
      </Section>

      {/* Contents preview */}
      <Section
        idx="05"
        id="contents"
        title="Contents"
        sub={contents.contents?.subtitle ?? t("매일 업로드 · 영상 + 교안", "daily uploads · video + notes")}
        langSuffix={langSuffix}
        viewAllLabel={viewAllLabel}
      >
        {latestContent && (
          <div
            className="m-stack"
            style={{
              display: "grid",
              gridTemplateColumns: "1.1fr 1fr",
              gap: 32,
              paddingTop: 8,
            }}
          >
            <Link
              href={`/contents/${latestContent.id}${langSuffix}`}
              className="card"
              style={{
                overflow: "hidden",
                display: "block",
                background: "var(--bg-1)",
                border: "1px solid var(--line-1)",
                borderRadius: 6,
              }}
            >
              <div
                style={{
                  position: "relative",
                  aspectRatio: "16/9",
                  background: "#000",
                  overflow: "hidden",
                }}
              >
                <div
                  className="placeholder-hatch"
                  style={{ position: "absolute", inset: 0 }}
                />
                <div
                  style={{
                    position: "absolute",
                    inset: 0,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <div
                    style={{
                      width: 56,
                      height: 56,
                      borderRadius: "50%",
                      background: "rgba(255,255,255,0.08)",
                      border: "1px solid rgba(255,255,255,0.2)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <svg width="20" height="20" viewBox="0 0 20 20">
                      <polygon
                        points="6,4 6,16 16,10"
                        fill="var(--fg-0)"
                      />
                    </svg>
                  </div>
                </div>
                {latestContent.duration && (
                  <div
                    className="mono"
                    style={{
                      position: "absolute",
                      bottom: 10,
                      right: 10,
                      fontSize: 11,
                      color: "var(--fg-0)",
                      background: "rgba(0,0,0,0.6)",
                      padding: "2px 6px",
                      borderRadius: 3,
                    }}
                  >
                    {latestContent.duration}
                  </div>
                )}
                <div
                  className="mono"
                  style={{
                    position: "absolute",
                    top: 10,
                    left: 10,
                    fontSize: 10,
                    color: "var(--accent)",
                    textTransform: "uppercase",
                    letterSpacing: "0.14em",
                  }}
                >
                  // latest
                </div>
              </div>
              <div style={{ padding: "20px 24px" }}>
                <div
                  className="mono"
                  style={{
                    fontSize: 11,
                    color: "var(--fg-3)",
                    marginBottom: 8,
                    display: "flex",
                    gap: 12,
                  }}
                >
                  <span>{latestContent.date}</span>
                  <span>·</span>
                  <span>{latestContent.day}</span>
                </div>
                <div
                  style={{
                    fontSize: 17,
                    lineHeight: 1.4,
                    color: "var(--fg-0)",
                    fontWeight: 500,
                  }}
                >
                  {latestContent.title}
                </div>
              </div>
            </Link>

            <div>
              <div className="caps" style={{ marginBottom: 12 }}>
                recent episodes
              </div>
              {olderContents.length === 0 ? (
                <p style={{ color: "var(--fg-3)", fontSize: 13 }}>
                  {t("회차 추가 예정", "more episodes coming")}
                </p>
              ) : (
                <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
                  {olderContents.map((c) => (
                    <li key={c.id}>
                      <Link
                        href={`/contents/${c.id}${langSuffix}`}
                        style={{
                          display: "grid",
                          gridTemplateColumns: "64px 1fr 56px",
                          gap: 16,
                          padding: "12px 0",
                          borderTop: "1px solid var(--line-1)",
                          alignItems: "baseline",
                          fontSize: 14,
                        }}
                      >
                        <span
                          className="mono"
                          style={{ fontSize: 11, color: "var(--fg-3)" }}
                        >
                          {c.day}
                        </span>
                        <span style={{ color: "var(--fg-0)" }}>{c.title}</span>
                        <span
                          className="mono"
                          style={{
                            fontSize: 11,
                            color: "var(--fg-3)",
                            textAlign: "right",
                          }}
                        >
                          {c.duration ?? ""}
                        </span>
                      </Link>
                    </li>
                  ))}
                </ul>
              )}
              <div
                style={{
                  paddingTop: 16,
                  borderTop: "1px solid var(--line-1)",
                  marginTop: 4,
                }}
              >
                <Link
                  href={`/contents${langSuffix}`}
                  className="mono"
                  style={{
                    color: "var(--fg-2)",
                    fontSize: 12,
                  }}
                >
                  {t("전체 회차 보기 →", "all episodes →")}
                </Link>
              </div>
            </div>
          </div>
        )}
      </Section>
    </>
  );
}

function NotesGraphPreview({
  stacks,
  noteCount,
}: {
  stacks: { name: string; count: number }[];
  noteCount: number;
}) {
  // top 5 stack 을 hub 로, 주위에 작은 note 노드 — 노트 페이지 패턴 미리보기
  const W = 320;
  const H = 180;
  const cx = W / 2;
  const cy = H / 2;
  const hubs = stacks.slice(0, 5).map((s, i) => {
    const angle = (i / 5) * Math.PI * 2 - Math.PI / 2;
    return {
      ...s,
      x: cx + Math.cos(angle) * 45,
      y: cy + Math.sin(angle) * 45,
      r: Math.max(4, Math.min(8, s.count / 12)),
    };
  });
  // 각 hub 주위 작은 note 노드 — 결정론적
  const notes = hubs.flatMap((hub, hi) => {
    const n = Math.min(6, Math.max(2, Math.floor(hub.count / 6)));
    return Array.from({ length: n }, (_, ni) => {
      const angle = (ni / n) * Math.PI * 2 + hi;
      const dist = 22 + (ni % 2) * 6;
      return {
        x: hub.x + Math.cos(angle) * dist,
        y: hub.y + Math.sin(angle) * dist,
        hub: hi,
      };
    });
  });

  return (
    <svg
      viewBox={`0 0 ${W} ${H}`}
      width="100%"
      height="100%"
      preserveAspectRatio="xMidYMid meet"
    >
      {/* hub-hub 연결선 (희미) */}
      {hubs.map((h, i) =>
        hubs.slice(i + 1).map((h2, j) => (
          <line
            key={`hh-${i}-${j}`}
            x1={h.x}
            y1={h.y}
            x2={h2.x}
            y2={h2.y}
            stroke="rgba(255,255,255,0.05)"
          />
        )),
      )}
      {/* hub-note 연결선 */}
      {notes.map((n, i) => (
        <line
          key={`hn-${i}`}
          x1={hubs[n.hub].x}
          y1={hubs[n.hub].y}
          x2={n.x}
          y2={n.y}
          stroke="rgba(255,255,255,0.08)"
        />
      ))}
      {/* note 노드 (초록) */}
      {notes.map((n, i) => (
        <circle
          key={`n-${i}`}
          cx={n.x}
          cy={n.y}
          r={2}
          fill="oklch(0.78 0.14 145)"
        />
      ))}
      {/* hub 노드 (주황) — count 비례 */}
      {hubs.map((h, i) => (
        <g key={`h-${i}`}>
          <circle cx={h.x} cy={h.y} r={h.r} fill="oklch(0.82 0.13 80)" />
        </g>
      ))}
      {/* 좌측 하단 카운트 */}
      <text
        x={8}
        y={H - 8}
        fontSize={9}
        fontFamily="var(--font-mono)"
        fill="var(--fg-3)"
      >
        {noteCount} notes · {hubs.length} hubs
      </text>
    </svg>
  );
}
