/* global React */
const { useState: _useS, useEffect: _useE, useRef: _useR } = React;

/* =========================================================
   Hero — Terminal
   ========================================================= */

window.HeroTerminal = function HeroTerminal({ lang, setRoute }) {
  const T = (ko, en) => lang === 'en' ? en : ko;

  const lines = [
    { p: 'whoami', out: ['kknaks · full-stack engineer · seoul'] },
    { p: 'cat stack.txt', out: [
      'frontend  → Next.js, TypeScript, Tailwind',
      'backend   → Python, FastAPI, PostgreSQL',
      'infra     → Docker, Tailscale, homelab',
    ] },
    { p: 'wc -l ~/vault/**/*.md', out: [T('300+ 노트 · 자동 동기화', '300+ notes · auto-synced')] },
    { p: 'ls ~/now', out: ['portfolio.next  homelab-console.py  inbox-zero/'] },
  ];

  // Typing animation — lightweight, runs once
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
          // {T('포트폴리오', 'portfolio')} · v0.1.0
        </div>
        <h1 className="m-display" style={{ fontSize: 68, lineHeight: 1.05, letterSpacing: '-0.03em', margin: '0 0 22px', fontWeight: 600 }}>
          <span style={{ color: 'var(--fg-3)' }}>{T('나는 ', 'I build ')}</span>
          <span>{T('내 홈서버 위에서', 'products that')}</span>
          <br/>
          <span>{T('돌아가는 ', 'run on my own')}</span>
          <br/>
          <span style={{ color: 'var(--accent)' }}>{T('제품을 만든다.', 'home server.')}</span>
        </h1>
        <p style={{ fontSize: 16, color: 'var(--fg-1)', lineHeight: 1.7, margin: '0 0 28px', maxWidth: 480 }}>
          {T(
            '풀스택 엔지니어. Next.js로 프론트를 짓고 Python으로 백엔드를 돌립니다. 작은 도구를 직접 만들어 매일 씁니다.',
            'Full-stack engineer. Next.js on the front, Python on the back. I build small tools and use them every day.'
          )}
        </p>
        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          <button className="btn primary">{T('이력서 다운로드', 'Resume')} <span className="arrow">↓</span></button>
          <button className="btn" onClick={() => setRoute('projects')}>{T('프로젝트 보기', 'See projects')} <span className="arrow">→</span></button>
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
   Section preview rows on landing — quick glance into each page
   ========================================================= */

window.LandingPreview = function LandingPreview({ lang, setRoute }) {
  const T = (ko, en) => lang === 'en' ? en : ko;

  const Section = ({ idx, id, title, sub, children }) => (
    <section className="pad-x" style={{ padding: '56px 80px', borderTop: '1px solid var(--line-1)' }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 16, marginBottom: 28 }}>
        <span className="mono" style={{ fontSize: 12, color: 'var(--fg-3)' }}>{idx}</span>
        <h2 className="m-h2" style={{ fontSize: 32, letterSpacing: '-0.02em', margin: 0, fontWeight: 600 }}>{title}</h2>
        <span style={{ color: 'var(--fg-3)', fontSize: 14, marginLeft: 4 }}>· {sub}</span>
        <button className="btn ghost" onClick={() => setRoute(id)} style={{ marginLeft: 'auto', padding: '6px 10px', fontSize: 12 }}>
          {T('전체 보기', 'View all')} <span className="arrow">→</span>
        </button>
      </div>
      {children}
    </section>
  );

  return (
    <>
      {/* About preview */}
      <Section idx="01" id="about" title="About" sub={T('만드는 사람', 'who builds it')}>
        <div className="m-stack" style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: 48, alignItems: 'start' }}>
          <p style={{ fontSize: 19, lineHeight: 1.6, color: 'var(--fg-0)', margin: 0, maxWidth: 640 }}>
            {T(
              '저는 작은 도구를 직접 만들고 직접 운영하는 풀스택 엔지니어입니다. 데이터 모델부터 배포 파이프라인, UI의 한 픽셀까지 — 한 끝에서 다른 끝까지 책임지는 일을 좋아합니다.',
              'I am a full-stack engineer who builds small tools and runs them myself. I like owning the whole thing — from data model to deploy pipeline to a single pixel of the UI.'
            )}
          </p>
          <dl style={{ margin: 0, fontSize: 13 }}>
            {[
              ['location', 'Seoul, KR'],
              ['focus', T('내부 도구 · 셀프호스팅', 'Internal tools · Self-hosting')],
              ['stack', 'Next.js · Python'],
              ['email', 'hello@kknaks.dev'],
            ].map(([k, v]) => (
              <div key={k} style={{ display: 'grid', gridTemplateColumns: '90px 1fr', padding: '8px 0', borderTop: '1px solid var(--line-1)' }}>
                <dt className="mono" style={{ color: 'var(--fg-3)' }}>{k}</dt>
                <dd style={{ margin: 0, color: 'var(--fg-1)' }}>{v}</dd>
              </div>
            ))}
          </dl>
        </div>
      </Section>

      {/* Career preview — last 2 items */}
      <Section idx="02" id="career" title="Career" sub={T('4년 · 4개 역할', '4 years · 4 roles')}>
        <div style={{ position: 'relative', paddingLeft: 28, maxWidth: 720 }}>
          <div style={{ position: 'absolute', left: 5, top: 8, bottom: 8, width: 1, background: 'var(--line-2)' }} />
          {[
            { y: '2024 — present', t: 'Senior Engineer', org: 'Acme Corp.', d: T('내부 도구 플랫폼 리드. 12개 어드민 통합과 권한 시스템 설계.', 'Lead on internal tools platform. Unified 12 admins, designed RBAC.'), active: true },
            { y: '2022 — 2024', t: 'Software Engineer', org: 'Foo Studio', d: T('커머스 백엔드. 결제 모듈과 30× 트래픽 스케일업.', 'Commerce backend. Payments + 30× traffic scale-up.') },
          ].map((it, i) => (
            <div key={i} style={{ position: 'relative', marginBottom: 24 }}>
              <span style={{ position: 'absolute', left: -28, top: 8, width: 11, height: 11, borderRadius: 2, background: 'var(--bg-0)', border: `1px solid ${it.active ? 'var(--accent)' : 'var(--line-3)'}`, boxShadow: it.active ? '0 0 0 3px var(--accent-soft)' : 'none' }} />
              <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 4 }}>{it.y}{it.active && <span style={{ color: 'var(--accent)', marginLeft: 8 }}>● now</span>}</div>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginBottom: 4 }}>
                <h3 style={{ margin: 0, fontSize: 17, fontWeight: 500 }}>{it.t}</h3>
                <span style={{ color: 'var(--fg-3)' }}>·</span>
                <span style={{ color: 'var(--fg-1)' }}>{it.org}</span>
              </div>
              <p style={{ margin: 0, color: 'var(--fg-1)', fontSize: 14, lineHeight: 1.6 }}>{it.d}</p>
            </div>
          ))}
        </div>
      </Section>

      {/* Projects preview — 2 cards */}
      <Section idx="03" id="projects" title="Projects" sub={T('혼자 만든 것들', 'solo work')}>
        <div className="m-stack" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          {[
            { id: 'P-01', t: 'Homelab Console', d: T('홈서버 메트릭과 컨테이너 상태를 실시간으로 보는 대시보드.', 'Real-time dashboard for homelab metrics and containers.'), tags: ['Next.js', 'FastAPI', 'WebSocket'], status: 'live', date: '2026' },
            { id: 'P-02', t: 'Inbox Zero',      d: T('내가 안 읽는 뉴스레터를 자동 요약해주는 봇.', 'Bot that auto-summarizes newsletters I never read.'), tags: ['Python', 'OpenAI'], status: 'live', date: '2025' },
          ].map(p => (
            <article key={p.id} className="card" style={{ overflow: 'hidden', cursor: 'pointer' }} onClick={() => setRoute('projects')}>
              <div className="placeholder-hatch" style={{ aspectRatio: '16/9' }}>[ {p.t} · 1600×900 ]</div>
              <div style={{ padding: 18, borderTop: '1px solid var(--line-1)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>{p.id}</span>
                  <span className="tag" style={{ color: 'var(--accent)', background: 'var(--accent-soft)', borderColor: 'var(--accent-line)' }}><span className="tag-dot" style={{ background: 'var(--accent)' }} />live</span>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginLeft: 'auto' }}>{p.date}</span>
                </div>
                <h3 style={{ margin: '0 0 6px', fontSize: 17 }}>{p.t}</h3>
                <p style={{ margin: '0 0 10px', fontSize: 13, color: 'var(--fg-2)', lineHeight: 1.5 }}>{p.d}</p>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                  {p.tags.map(tg => <span key={tg} className="tag">{tg}</span>)}
                </div>
              </div>
            </article>
          ))}
        </div>
      </Section>

      {/* Notes preview */}
      <Section idx="04" id="notes" title="Notes" sub={T('옵시디언 vault 미러 · 300+ 노트', 'obsidian vault mirror · 300+ notes')}>
        <article className="m-stack" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32, paddingTop: 8 }}>
          <div>
            <div className="caps" style={{ marginBottom: 12 }}>recent</div>
            <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
              {[
                { d: '2026.04.10', t: T('RAG 기본 구조', 'RAG basics'),                 path: 'AI/LLM' },
                { d: '2026.03.22', t: T('Prompt Engineering 패턴', 'Prompt patterns'),  path: 'AI/LLM' },
                { d: '2026.01.30', t: T('Vector DB 비교', 'Vector DB compared'),        path: 'AI/Embedding' },
                { d: '2025.12.20', t: T('asyncio 동작 원리', 'asyncio internals'),      path: 'Python' },
                { d: '2025.08.25', t: T('Docker Compose 패턴 모음', 'Docker compose patterns'), path: 'Infra/Docker' },
              ].map(n => (
                <li key={n.t} style={{ display: 'grid', gridTemplateColumns: '88px 1fr 110px', gap: 16, padding: '10px 0', borderTop: '1px solid var(--line-1)', alignItems: 'baseline', fontSize: 14 }}>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>{n.d}</span>
                  <span style={{ color: 'var(--fg-0)' }}>{n.t}</span>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textAlign: 'right' }}>{n.path}</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <div className="caps" style={{ marginBottom: 12 }}>topics</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              {[
                ['AI', 42], ['Python', 38], ['Infra', 31], ['CS', 27], ['Docker', 18],
                ['LLM', 24], ['Database', 16], ['Network', 11], ['Daily', 64], ['Homelab', 9],
              ].map(([t, n]) => (
                <span key={t} className="tag" style={{ fontSize: 11 }}>
                  #{t} <span style={{ color: 'var(--fg-3)', marginLeft: 4 }}>{n}</span>
                </span>
              ))}
            </div>
            <div className="caps" style={{ marginTop: 24, marginBottom: 8 }}>graph</div>
            <div style={{ position: 'relative', height: 140, background: 'var(--bg-2)', border: '1px solid var(--line-1)', borderRadius: 6 }}>
              <svg viewBox="0 0 240 140" width="100%" height="100%">
                <line x1="120" y1="70" x2="50"  y2="30"  stroke="var(--line-3)" />
                <line x1="120" y1="70" x2="200" y2="30"  stroke="var(--line-3)" />
                <line x1="120" y1="70" x2="40"  y2="110" stroke="var(--line-3)" />
                <line x1="120" y1="70" x2="180" y2="115" stroke="var(--line-3)" />
                <line x1="50"  y1="30" x2="200" y2="30"  stroke="var(--line-2)" strokeDasharray="2 3" />
                <line x1="40"  y1="110" x2="180" y2="115" stroke="var(--line-2)" strokeDasharray="2 3" />
                <circle cx="120" cy="70"  r="6" fill="var(--accent)" />
                <circle cx="50"  cy="30"  r="4" fill="var(--fg-2)" />
                <circle cx="200" cy="30"  r="4" fill="var(--fg-2)" />
                <circle cx="40"  cy="110" r="4" fill="var(--fg-2)" />
                <circle cx="180" cy="115" r="4" fill="var(--fg-2)" />
              </svg>
              <div className="mono" style={{ position: 'absolute', bottom: 6, right: 8, fontSize: 10, color: 'var(--fg-3)' }}>// preview</div>
            </div>
          </div>
        </article>
      </Section>

      {/* Contents preview */}
      <Section idx="05" id="contents" title="Contents" sub={T('매일 업로드 · 영상 + 교안', 'daily uploads · video + notes')}>
        <article className="m-stack" style={{ display: 'grid', gridTemplateColumns: '1.1fr 1fr', gap: 32, paddingTop: 8 }}>
          {/* Latest video card */}
          <div
            className="card"
            onClick={() => setRoute('contents/C-005')}
            style={{ overflow: 'hidden', cursor: 'pointer', background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6 }}
          >
            <div style={{ position: 'relative', aspectRatio: '16/9', background: '#000', overflow: 'hidden' }}>
              <svg width="100%" height="100%" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" style={{ display: 'block' }}>
                <defs>
                  <pattern id="hatch-c1" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                    <line x1="0" y1="0" x2="0" y2="6" stroke="rgba(255,255,255,0.04)" strokeWidth="2" />
                  </pattern>
                </defs>
                <rect width="320" height="180" fill="#0a0b0d" />
                <rect width="320" height="180" fill="url(#hatch-c1)" />
              </svg>
              <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <div style={{ width: 56, height: 56, borderRadius: '50%', background: 'rgba(255,255,255,0.08)', border: '1px solid rgba(255,255,255,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <svg width="20" height="20" viewBox="0 0 20 20"><polygon points="6,4 6,16 16,10" fill="var(--fg-0)" /></svg>
                </div>
              </div>
              <div className="mono" style={{ position: 'absolute', bottom: 10, right: 10, fontSize: 11, color: 'var(--fg-0)', background: 'rgba(0,0,0,0.6)', padding: '2px 6px', borderRadius: 3 }}>18:42</div>
              <div className="mono" style={{ position: 'absolute', top: 10, left: 10, fontSize: 10, color: 'var(--accent)', textTransform: 'uppercase', letterSpacing: '0.14em' }}>// latest</div>
            </div>
            <div style={{ padding: '20px 24px' }}>
              <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 8, display: 'flex', gap: 12 }}>
                <span>2026.04.30</span>
                <span>·</span>
                <span>Day 05</span>
              </div>
              <div style={{ fontSize: 17, lineHeight: 1.4, color: 'var(--fg-0)', fontWeight: 500 }}>
                Vector DB {T('기본기 — HNSW가 왜 빠른가', 'basics — why HNSW is fast')}
              </div>
            </div>
          </div>

          {/* Recent list */}
          <div>
            <div className="caps" style={{ marginBottom: 12 }}>recent episodes</div>
            <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
              {[
                { id: 'C-004', d: '2026.04.29', day: 'Day 04', t: T('asyncio의 이벤트 루프', 'asyncio event loop'), dur: '14:08' },
                { id: 'C-003', d: '2026.04.28', day: 'Day 03', t: T('PostgreSQL의 MVCC', 'PostgreSQL MVCC'), dur: '21:55' },
                { id: 'C-002', d: '2026.04.27', day: 'Day 02', t: T('Tokenizer 비교', 'Tokenizer compared'), dur: '12:30' },
                { id: 'C-001', d: '2026.04.26', day: 'Day 01', t: T('Docker layer cache', 'Docker layer cache'), dur: '09:18' },
              ].map(c => (
                <li
                  key={c.id}
                  onClick={() => setRoute('contents/' + c.id)}
                  style={{
                    display: 'grid', gridTemplateColumns: '64px 1fr 56px',
                    gap: 16, padding: '12px 0', borderTop: '1px solid var(--line-1)',
                    alignItems: 'baseline', fontSize: 14, cursor: 'pointer',
                  }}
                >
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>{c.day}</span>
                  <span style={{ color: 'var(--fg-0)' }}>{c.t}</span>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textAlign: 'right' }}>{c.dur}</span>
                </li>
              ))}
            </ul>
            <div style={{ paddingTop: 16, borderTop: '1px solid var(--line-1)', marginTop: 4 }}>
              <button
                className="mono"
                onClick={() => setRoute('contents')}
                style={{ background: 'transparent', border: 'none', color: 'var(--fg-2)', fontSize: 12, cursor: 'pointer', padding: 0 }}
              >
                {T('전체 회차 보기 →', 'all episodes →')}
              </button>
            </div>
          </div>
        </article>
      </Section>
    </>
  );
};
