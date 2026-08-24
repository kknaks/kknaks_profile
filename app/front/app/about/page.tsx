import { api } from "@/lib/api";
import { ContribGrass } from "@/components/about/contrib-grass";

export const dynamic = "force-dynamic";

export default async function AboutPage() {
  let me, activity;
  try {
    [me, activity] = await Promise.all([api.profile(), api.activity()]);
  } catch (err) {
    return (
      <main className="pad-x" style={{ padding: "56px 80px" }}>
        <h1>About</h1>
        <p style={{ color: "var(--danger)" }}>
          백엔드 응답 실패: {(err as Error).message}
        </p>
      </main>
    );
  }

  const user = me.profile;
  const about = me.about;

  return (
    <main>
      <header
        className="pad-x m-pad-h"
        style={{
          padding: "56px 80px 32px",
          borderBottom: "1px solid var(--line-1)",
        }}
      >
        <div
          className="mono"
          style={{
            fontSize: 11,
            color: "var(--fg-3)",
            textTransform: "uppercase",
            letterSpacing: "0.14em",
            marginBottom: 12,
          }}
        >
          01 / About · {about?.subtitle ?? "만드는 사람"}
        </div>
        <div
          className="about-id"
          style={{
            display: "flex",
            alignItems: "center",
            gap: 24,
            flexWrap: "wrap",
          }}
        >
          {user.avatarUrl ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={user.avatarUrl}
              alt={`${user.name} avatar`}
              width={88}
              height={88}
              style={{
                width: 88,
                height: 88,
                borderRadius: "50%",
                border: "1px solid var(--line-2)",
                objectFit: "cover",
                flexShrink: 0,
              }}
            />
          ) : (
            <div
              style={{
                width: 88,
                height: 88,
                borderRadius: "50%",
                background: "var(--bg-2)",
                border: "1px solid var(--line-2)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 40,
                flexShrink: 0,
              }}
            >
              <span
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: 11,
                  color: "var(--fg-3)",
                }}
              >
                :)
              </span>
            </div>
          )}
          <div style={{ minWidth: 0 }}>
            <h1
              className="m-h1"
              style={{
                fontSize: 56,
                lineHeight: 1.05,
                letterSpacing: "-0.025em",
                margin: 0,
                fontWeight: 600,
              }}
            >
              {user.handle}{" "}
              <span
                className="about-id-sub"
                style={{
                  color: "var(--fg-3)",
                  fontSize: 28,
                  fontWeight: 400,
                }}
              >
                · {user.name}
              </span>
            </h1>
            <div
              className="mono"
              style={{ fontSize: 13, color: "var(--fg-2)", marginTop: 8 }}
            >
              {user.role.toLowerCase()}
              {user.years ? ` · ${user.years}` : ""}
              {user.location ? ` · ${user.location.toLowerCase()}` : ""}
            </div>
          </div>
        </div>
        <style>{`
          @media (max-width: 720px) {
            .about-id { gap: 16px !important; }
            .about-id-sub { font-size: 18px !important; display: block; margin-top: 4px; }
          }
        `}</style>
      </header>

      <div
        className="pad-x m-stack"
        style={{
          padding: "48px 80px",
          display: "grid",
          gridTemplateColumns: "minmax(0, 1.5fr) minmax(0, 1fr)",
          gap: 64,
        }}
      >
        <div style={{ minWidth: 0 }}>
          <p
            style={{
              fontSize: 22,
              lineHeight: 1.55,
              letterSpacing: "-0.01em",
              color: "var(--fg-0)",
              marginTop: 0,
              fontWeight: 500,
            }}
          >
            {user.tagline}
          </p>
          <p
            style={{
              fontSize: 16,
              lineHeight: 1.7,
              color: "var(--fg-1)",
              marginTop: 24,
            }}
          >
            {user.intro}
          </p>
          {user.intro2 && (
            <p
              style={{
                fontSize: 15,
                lineHeight: 1.7,
                color: "var(--fg-1)",
              }}
            >
              {user.intro2}
            </p>
          )}

          {user.cards && user.cards.length > 0 && (
            <div
              className="m-stack"
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: 16,
                marginTop: 36,
              }}
            >
              {user.cards.map((card, i) => (
                <div
                  key={i}
                  style={{
                    padding: 18,
                    background: "var(--bg-1)",
                    border: "1px solid var(--line-1)",
                    borderRadius: 6,
                  }}
                >
                  <div
                    className="mono"
                    style={{
                      fontSize: 11,
                      color: "var(--accent)",
                      marginBottom: 8,
                    }}
                  >
                    // {card.title}
                  </div>
                  <div
                    style={{
                      fontSize: 14,
                      color: "var(--fg-1)",
                      lineHeight: 1.6,
                    }}
                  >
                    {card.body}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <aside>
          <dl style={{ margin: 0, fontSize: 13 }}>
            {[
              ["name", `${user.name} (${user.handle})`],
              ["role", user.role],
              ...(user.location ? [["location", user.location]] : []),
              ...(user.focus ? [["focus", user.focus]] : []),
              ["email", user.email],
              ...(user.github ? [["github", user.github]] : []),
              ...(user.linkedin ? [["linkedin", user.linkedin]] : []),
            ].map(([k, v]) => (
              <div
                key={k}
                style={{
                  display: "grid",
                  gridTemplateColumns: "90px 1fr",
                  padding: "10px 0",
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

          <div
            style={{
              marginTop: 24,
              padding: 16,
              background: "var(--bg-1)",
              border: "1px solid var(--line-1)",
              borderRadius: 6,
            }}
          >
            <div
              className="mono"
              style={{
                fontSize: 11,
                color: "var(--accent)",
                marginBottom: 8,
              }}
            >
              // stack
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
              {user.stack.map((s) => (
                <span key={s} className="tag">
                  {s}
                </span>
              ))}
            </div>
          </div>
        </aside>
      </div>

      <div className="pad-x" style={{ padding: "8px 80px 64px" }}>
        <ContribGrass activity={activity} />
      </div>
    </main>
  );
}
