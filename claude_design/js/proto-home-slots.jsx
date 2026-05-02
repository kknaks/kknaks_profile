/* global React */
const { useState: _useS, useEffect: _useE } = React;

/* =========================================================
   Hero — Terminal (slot edition)
   - 좌측 카피: 한 줄 통째로 슬롯
   - 우측 터미널 출력: 데모 연출이라 slot화하지 않음 (CLAUDE.md 명시)
   ========================================================= */

window.HeroTerminal = function HeroTerminal({ lang, setRoute }) {
  const Slot = window.Slot;

  // 데모 연출 — 슬롯화 X (CLAUDE.md 결정)
  const lines = [
    { p: 'whoami', out: ['kknaks · backend engineer · seoul'] },
    { p: 'cat stack.txt', out: [
      'frontend  → Next.js, TypeScript',
      'backend   → Python, FastAPI, PostgreSQL',
      'infra     → Docker, Tailscale, homelab',
    ] },
    { p: 'wc -l ~/vault/**/*.md', out: ['300+ notes · auto-synced'] },
    { p: 'ls ~/now', out: ['portfolio.next  homelab-console.py  inbox-zero/'] },
  ];

  const [step, setStep] = _useS(0);
  _useE(() => {
    if (step >= lines.length) return;
    const id = setTimeout(() => setStep(s => s + 1), 700);
    return () => clearTimeout(id);
  }, [step]);

  return (
    <section className="pad-x m-stack" style={{ padding: '64px 80px 48px', display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: 48, alignItems: 'center', minHeight: 600 }}>
      <div>
        <div className="mono" style={{ fontSize: 12, color: 'var(--fg-3)', marginBottom: 16 }}>
          // portfolio · v<Slot k="site.version" />
        </div>
        <h1 className="m-display" style={{ fontSize: 68, lineHeight: 1.05, letterSpacing: '-0.03em', margin: '0 0 22px', fontWeight: 600 }}>
          <Slot k="hero.headline" hint="3줄짜리 카피 — 줄바꿈 포함, 마지막 줄은 accent 색" />
        </h1>
        <p style={{ fontSize: 16, color: 'var(--fg-1)', lineHeight: 1.7, margin: '0 0 28px', maxWidth: 480 }}>
          <Slot k="hero.subline" />
        </p>
        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          <button className="btn primary">Resume <span className="arrow">↓</span></button>
          <button className="btn" onClick={() => setRoute('projects')}>See projects <span className="arrow">→</span></button>
          <button className="btn ghost">GitHub <span className="arrow">↗</span></button>
        </div>
      </div>

      <div style={{ background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6, fontFamily: 'var(--font-mono)', fontSize: 12.5, lineHeight: 1.7, overflow: 'hidden', boxShadow: 'var(--shadow-card)' }}>
        <div style={{ display: 'flex', gap: 6, padding: '10px 12px', borderBottom: '1px solid var(--line-1)', alignItems: 'center' }}>
          <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#3a3f48' }} />
          <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#3a3f48' }} />
          <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#3a3f48' }} />
          <span style={{ marginLeft: 8, color: 'var(--fg-3)', fontSize: 11 }}>~/kknaks — zsh</span>
        </div>
        <div style={{ padding: 16, color: 'var(--fg-1)', minHeight: 280 }}>
          {lines.slice(0, step + 1).map((l, i) => (
            <div key={i} style={{ marginBottom: i < step ? 10 : 0 }}>
              <div><span style={{ color: 'var(--accent)' }}>$</span> {l.p}</div>
              {i < step && l.out.map((o, j) => <div key={j} style={{ color: j === 0 ? 'var(--fg-0)' : 'var(--fg-1)' }}>{o}</div>)}
              {i === step && <span style={{ display: 'inline-block', width: 8, height: 14, background: 'var(--accent)', verticalAlign: 'middle', marginLeft: 4, animation: 'blink 1s steps(2) infinite' }} />}
            </div>
          ))}
          {step >= lines.length && (
            <div><span style={{ color: 'var(--accent)' }}>$</span> <span style={{ display: 'inline-block', width: 8, height: 14, background: 'var(--accent)', verticalAlign: 'middle', animation: 'blink 1s steps(2) infinite' }} /></div>
          )}
        </div>
      </div>
    </section>
  );
};

/* =========================================================
   Landing previews — slot edition
   각 섹션의 미리보기는 N개 미리 받아온 데이터를 첫 N개만 보여줌.
   슬롯 키는 collection-level이라, 같은 키를 sub-page도 공유.
   ========================================================= */

window.LandingPreview = function LandingPreview({ lang, setRoute }) {
  const Slot = window.Slot;

  const Section = ({ idx, id, title, subKey, children }) => (
    <section className="pad-x" style={{ padding: '56px 80px', borderTop: '1px solid var(--line-1)' }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 16, marginBottom: 28 }}>
        <span className="mono" style={{ fontSize: 12, color: 'var(--fg-3)' }}>{idx}</span>
        <h2 className="m-h2" style={{ fontSize: 32, letterSpacing: '-0.02em', margin: 0, fontWeight: 600 }}>{title}</h2>
        <span style={{ color: 'var(--fg-3)', fontSize: 14, marginLeft: 4 }}>· <Slot k={subKey} /></span>
        <button className="btn ghost" onClick={() => setRoute(id)} style={{ marginLeft: 'auto', padding: '6px 10px', fontSize: 12 }}>
          View all <span className="arrow">→</span>
        </button>
      </div>
      {children}
    </section>
  );

  // 미리보기 카드 N개 — index가 같으면 동일 collection의 같은 record
  const Idx = (i) => `[${i}]`;

  return (
    <>
      {/* About preview */}
      <Section idx="01" id="about" title="About" subKey="about.subtitle">
        <div className="m-stack" style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: 48, alignItems: 'start' }}>
          <p style={{ fontSize: 19, lineHeight: 1.6, color: 'var(--fg-0)', margin: 0, maxWidth: 640 }}>
            <Slot k="user.intro" hint="2~3 문장 자기소개" />
          </p>
          <dl style={{ margin: 0, fontSize: 13 }}>
            {[
              ['location', 'user.location'],
              ['focus',    'user.focus'],
              ['stack',    'user.stackShort'],
              ['email',    'user.email'],
            ].map(([k, slotK]) => (
              <div key={k} style={{ display: 'grid', gridTemplateColumns: '90px 1fr', padding: '8px 0', borderTop: '1px solid var(--line-1)' }}>
                <dt className="mono" style={{ color: 'var(--fg-3)' }}>{k}</dt>
                <dd style={{ margin: 0, color: 'var(--fg-1)' }}><Slot k={slotK} /></dd>
              </div>
            ))}
          </dl>
        </div>
      </Section>

      {/* Career preview — 최근 2건 */}
      <Section idx="02" id="career" title="Career" subKey="career.subtitle">
        <div style={{ position: 'relative', paddingLeft: 28, maxWidth: 720 }}>
          <div style={{ position: 'absolute', left: 5, top: 8, bottom: 8, width: 1, background: 'var(--line-2)' }} />
          {[0, 1].map(i => (
            <div key={i} style={{ position: 'relative', marginBottom: 24 }}>
              <span style={{ position: 'absolute', left: -28, top: 8, width: 11, height: 11, borderRadius: 2, background: 'var(--bg-0)', border: `1px solid ${i===0 ? 'var(--accent)' : 'var(--line-3)'}`, boxShadow: i===0 ? '0 0 0 3px var(--accent-soft)' : 'none' }} />
              <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 4 }}>
                <Slot k={`career[${i}].period`} />
                {i===0 && <span style={{ color: 'var(--accent)', marginLeft: 8 }}>● now</span>}
              </div>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginBottom: 4 }}>
                <h3 style={{ margin: 0, fontSize: 17, fontWeight: 500 }}><Slot k={`career[${i}].title`} /></h3>
                <span style={{ color: 'var(--fg-3)' }}>·</span>
                <span style={{ color: 'var(--fg-1)' }}><Slot k={`career[${i}].org`} /></span>
              </div>
              <p style={{ margin: 0, color: 'var(--fg-1)', fontSize: 14, lineHeight: 1.6 }}>
                <Slot k={`career[${i}].summary`} />
              </p>
            </div>
          ))}
        </div>
      </Section>

      {/* Projects preview — 최근 2건 */}
      <Section idx="03" id="projects" title="Projects" subKey="projects.subtitle">
        <div className="m-stack" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          {[0, 1].map(i => (
            <article key={i} className="card" style={{ overflow: 'hidden', cursor: 'pointer' }} onClick={() => setRoute('projects')}>
              <div className="placeholder-hatch" style={{ aspectRatio: '16/9' }}>
                [ projects{Idx(i)}.thumbnail · 1600×900 ]
              </div>
              <div style={{ padding: 18, borderTop: '1px solid var(--line-1)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}><Slot k={`projects[${i}].id`} /></span>
                  <span className="tag" style={{ color: 'var(--accent)', background: 'var(--accent-soft)', borderColor: 'var(--accent-line)' }}>
                    <span className="tag-dot" style={{ background: 'var(--accent)' }} /><Slot k={`projects[${i}].status`} />
                  </span>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginLeft: 'auto' }}><Slot k={`projects[${i}].date`} /></span>
                </div>
                <h3 style={{ margin: '0 0 6px', fontSize: 17 }}><Slot k={`projects[${i}].title`} /></h3>
                <p style={{ margin: '0 0 10px', fontSize: 13, color: 'var(--fg-2)', lineHeight: 1.5 }}>
                  <Slot k={`projects[${i}].summary`} />
                </p>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                  <span className="tag"><Slot k={`projects[${i}].stack[]`} hint="stack 배열을 통째로 — 콤마로 구분된 텍스트" /></span>
                </div>
              </div>
            </article>
          ))}
        </div>
      </Section>

      {/* Notes preview */}
      <Section idx="04" id="notes" title="Notes" subKey="notes.subtitle">
        <article className="m-stack" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32, paddingTop: 8 }}>
          <div>
            <div className="caps" style={{ marginBottom: 12 }}>recent</div>
            <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
              {[0,1,2,3,4].map(i => (
                <li key={i} style={{ display: 'grid', gridTemplateColumns: '88px 1fr 110px', gap: 16, padding: '10px 0', borderTop: '1px solid var(--line-1)', alignItems: 'baseline', fontSize: 14 }}>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}><Slot k={`notes.recent[${i}].date`} /></span>
                  <span style={{ color: 'var(--fg-0)' }}><Slot k={`notes.recent[${i}].title`} /></span>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textAlign: 'right' }}><Slot k={`notes.recent[${i}].path`} /></span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <div className="caps" style={{ marginBottom: 12 }}>topics</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              <Slot k="notes.topics[]" hint='[{tag, count}, ...] 통째로 — 프론트가 #tag <count> 로 렌더' />
            </div>
            <div className="caps" style={{ marginTop: 24, marginBottom: 8 }}>graph</div>
            <div style={{ position: 'relative', height: 140, background: 'var(--bg-2)', border: '1px solid var(--line-1)', borderRadius: 6, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>// notes.graph preview — same data as Notes page</span>
            </div>
          </div>
        </article>
      </Section>

      {/* Contents preview */}
      <Section idx="05" id="contents" title="Contents" subKey="contents.subtitle">
        <article className="m-stack" style={{ display: 'grid', gridTemplateColumns: '1.1fr 1fr', gap: 32, paddingTop: 8 }}>
          <div className="card"
            onClick={() => setRoute('contents/' /* + contents[0].id */)}
            style={{ overflow: 'hidden', cursor: 'pointer', background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6 }}
          >
            <div style={{ position: 'relative', aspectRatio: '16/9', background: '#000', overflow: 'hidden' }}>
              <div className="placeholder-hatch" style={{ position: 'absolute', inset: 0 }}>
                [ contents[0].thumbnail · youtu.be/<Slot k="contents[0].youtubeId" /> ]
              </div>
              <div className="mono" style={{ position: 'absolute', bottom: 10, right: 10, fontSize: 11, color: 'var(--fg-0)', background: 'rgba(0,0,0,0.6)', padding: '2px 6px', borderRadius: 3 }}>
                <Slot k="contents[0].duration" />
              </div>
              <div className="mono" style={{ position: 'absolute', top: 10, left: 10, fontSize: 10, color: 'var(--accent)', textTransform: 'uppercase', letterSpacing: '0.14em' }}>// latest</div>
            </div>
            <div style={{ padding: '20px 24px' }}>
              <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 8, display: 'flex', gap: 12 }}>
                <span><Slot k="contents[0].date" /></span>
                <span>·</span>
                <span><Slot k="contents[0].day" /></span>
              </div>
              <div style={{ fontSize: 17, lineHeight: 1.4, color: 'var(--fg-0)', fontWeight: 500 }}>
                <Slot k="contents[0].title" />
              </div>
            </div>
          </div>

          <div>
            <div className="caps" style={{ marginBottom: 12 }}>recent episodes</div>
            <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
              {[1,2,3,4].map(i => (
                <li key={i}
                  style={{
                    display: 'grid', gridTemplateColumns: '64px 1fr 56px',
                    gap: 16, padding: '12px 0', borderTop: '1px solid var(--line-1)',
                    alignItems: 'baseline', fontSize: 14, cursor: 'pointer',
                  }}
                >
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}><Slot k={`contents[${i}].day`} /></span>
                  <span style={{ color: 'var(--fg-0)' }}><Slot k={`contents[${i}].title`} /></span>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textAlign: 'right' }}><Slot k={`contents[${i}].duration`} /></span>
                </li>
              ))}
            </ul>
            <div style={{ paddingTop: 16, borderTop: '1px solid var(--line-1)', marginTop: 4 }}>
              <button className="mono" onClick={() => setRoute('contents')}
                style={{ background: 'transparent', border: 'none', color: 'var(--fg-2)', fontSize: 12, cursor: 'pointer', padding: 0 }}>
                all episodes →
              </button>
            </div>
          </div>
        </article>
      </Section>
    </>
  );
};
