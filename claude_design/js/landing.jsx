/* global React */

/* =========================================================
   LANDING PAGE VARIATIONS
   ========================================================= */

const NavBar = () => (
  <div style={{ padding: '14px 32px', display: 'flex', alignItems: 'center', gap: 24, borderBottom: '1px solid var(--line-1)' }}>
    <div className="mono" style={{ fontSize: 13, display: 'flex', alignItems: 'center', gap: 8 }}>
      <span style={{ width: 8, height: 8, background: 'var(--accent)', borderRadius: 2 }} />
      kknaks<span style={{ color: 'var(--fg-3)' }}>.dev</span>
    </div>
    <nav style={{ display: 'flex', gap: 4, marginLeft: 16 }}>
      {['About', 'Career', 'Projects', 'Products'].map((i, idx) => (
        <span key={i} style={{ fontFamily: 'var(--font-mono)', fontSize: 12, padding: '6px 10px', color: 'var(--fg-2)' }}>
          <span style={{ color: 'var(--fg-3)' }}>0{idx+1} </span>{i}
        </span>
      ))}
    </nav>
    <div style={{ marginLeft: 'auto', display: 'flex', gap: 8, alignItems: 'center' }}>
      <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>● online</span>
      <button className="btn" style={{ padding: '4px 8px', fontSize: 11 }}>KO / EN</button>
    </div>
  </div>
);

/* ---- Variant 1 — Terminal hero ---- */
window.LandingTerminal = function LandingTerminal() {
  return (
    <div style={{ width: 1280, height: 760, background: 'var(--bg-0)', display: 'flex', flexDirection: 'column' }}>
      <NavBar />
      <div style={{ flex: 1, display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: 40, padding: '64px 80px' }}>
        <div>
          <div className="mono" style={{ fontSize: 12, color: 'var(--fg-3)', marginBottom: 16 }}>// hello-world.sh</div>
          <h1 style={{ fontSize: 64, lineHeight: 1.05, letterSpacing: '-0.03em', margin: '0 0 20px', fontWeight: 600 }}>
            <span style={{ color: 'var(--fg-3)' }}>I build </span>
            <span>products that<br />run on my own<br /> </span>
            <span style={{ color: 'var(--accent)' }}>home server.</span>
          </h1>
          <p style={{ fontSize: 16, color: 'var(--fg-1)', lineHeight: 1.7, margin: '0 0 28px', maxWidth: 480 }}>
            풀스택 엔지니어. Next.js로 프론트를 짓고 Python으로 백엔드를 돌립니다. 작은 도구를 직접 만들어 매일 씁니다.
          </p>
          <div style={{ display: 'flex', gap: 10 }}>
            <button className="btn primary">이력서 다운로드 <span className="arrow">↓</span></button>
            <button className="btn">GitHub <span className="arrow">↗</span></button>
            <button className="btn ghost">메일 보내기</button>
          </div>
        </div>
        <div style={{ background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6, fontFamily: 'var(--font-mono)', fontSize: 12.5, lineHeight: 1.7, overflow: 'hidden' }}>
          <div style={{ display: 'flex', gap: 6, padding: '10px 12px', borderBottom: '1px solid var(--line-1)', alignItems: 'center' }}>
            <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#3a3f48' }} />
            <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#3a3f48' }} />
            <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#3a3f48' }} />
            <span style={{ marginLeft: 8, color: 'var(--fg-3)', fontSize: 11 }}>~/kknaks — zsh</span>
          </div>
          <div style={{ padding: 16, color: 'var(--fg-1)' }}>
            <div><span style={{ color: 'var(--accent)' }}>$</span> whoami</div>
            <div style={{ color: 'var(--fg-0)' }}>kknaks · full-stack · seoul</div>
            <div style={{ marginTop: 8 }}><span style={{ color: 'var(--accent)' }}>$</span> cat stack.txt</div>
            <div style={{ color: 'var(--fg-0)' }}>frontend <span style={{ color: 'var(--fg-3)' }}>→</span> Next.js, TypeScript</div>
            <div style={{ color: 'var(--fg-0)' }}>backend  <span style={{ color: 'var(--fg-3)' }}>→</span> Python, FastAPI, Postgres</div>
            <div style={{ color: 'var(--fg-0)' }}>infra    <span style={{ color: 'var(--fg-3)' }}>→</span> Docker, Tailscale, homelab</div>
            <div style={{ marginTop: 8 }}><span style={{ color: 'var(--accent)' }}>$</span> uptime</div>
            <div style={{ color: 'var(--fg-2)' }}>4 yrs shipping · 12 projects · 3 products</div>
            <div style={{ marginTop: 8 }}><span style={{ color: 'var(--accent)' }}>$</span> ls ~/now</div>
            <div style={{ color: 'var(--fg-0)' }}>portfolio.next  homelab-console.py  ...</div>
            <div style={{ marginTop: 8 }}><span style={{ color: 'var(--accent)' }}>$</span> <span style={{ background: 'var(--accent)', color: 'var(--accent-ink)', padding: '0 4px' }}>_</span></div>
          </div>
        </div>
      </div>
      <div style={{ padding: '12px 32px', borderTop: '1px solid var(--line-1)', display: 'flex', justifyContent: 'space-between' }} className="mono">
        <span style={{ fontSize: 11, color: 'var(--fg-3)' }}>// scroll for more</span>
        <span style={{ fontSize: 11, color: 'var(--fg-3)' }}>seoul · KST · 23:42</span>
      </div>
    </div>
  );
};

/* ---- Variant 2 — Editorial hero (large type, asym grid) ---- */
window.LandingEditorial = function LandingEditorial() {
  return (
    <div style={{ width: 1280, height: 760, background: 'var(--bg-0)', display: 'flex', flexDirection: 'column' }}>
      <NavBar />
      <div style={{ flex: 1, padding: '48px 80px', position: 'relative' }}>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', display: 'flex', justifyContent: 'space-between', marginBottom: 40, letterSpacing: '0.12em', textTransform: 'uppercase' }}>
          <span>Index · 01 / 04</span>
          <span>Updated 2026.04.18</span>
        </div>
        <h1 style={{ fontSize: 132, lineHeight: 0.92, letterSpacing: '-0.04em', margin: '0 0 24px', fontWeight: 600 }}>
          Build.<br /><span style={{ color: 'var(--fg-3)' }}>Ship.</span><br /><span style={{ color: 'var(--accent)' }}>Self-host.</span>
        </h1>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 40, marginTop: 48, paddingTop: 24, borderTop: '1px solid var(--line-1)' }}>
          <div>
            <div className="caps" style={{ marginBottom: 8 }}>Currently</div>
            <div style={{ fontSize: 15, color: 'var(--fg-1)', lineHeight: 1.6 }}>Acme Corp.<br />Senior Engineer · 내부 도구 플랫폼</div>
          </div>
          <div>
            <div className="caps" style={{ marginBottom: 8 }}>Stack</div>
            <div className="mono" style={{ fontSize: 13, color: 'var(--fg-1)', lineHeight: 1.6 }}>Next.js · TypeScript<br />Python · FastAPI · Postgres</div>
          </div>
          <div>
            <div className="caps" style={{ marginBottom: 8 }}>Reach</div>
            <div className="mono" style={{ fontSize: 13, color: 'var(--fg-1)', lineHeight: 1.6 }}>github.com/kknaks<br />hello@kknaks.dev</div>
          </div>
        </div>
      </div>
    </div>
  );
};

/* ---- Variant 3 — Index/manifest list ---- */
window.LandingIndex = function LandingIndex() {
  const rows = [
    { n: '01', label: 'About',    desc: '왜 만드는지, 어떻게 일하는지' },
    { n: '02', label: 'Career',   desc: '4년차 풀스택 · 3 회사 · 1 사이드' },
    { n: '03', label: 'Projects', desc: '혼자 만든 12개의 도구와 사이트' },
    { n: '04', label: 'Products', desc: '회사에서 출시한 3개의 제품' },
  ];
  return (
    <div style={{ width: 1280, height: 760, background: 'var(--bg-0)', display: 'flex', flexDirection: 'column' }}>
      <NavBar />
      <div style={{ flex: 1, padding: '48px 80px', display: 'grid', gridTemplateColumns: '1fr 1.4fr', gap: 80 }}>
        <div>
          <div className="eyebrow" style={{ marginBottom: 16 }}>portfolio · v0.1.0</div>
          <h1 style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.025em', margin: '0 0 24px', fontWeight: 600 }}>
            안녕하세요,<br />kknaks 입니다.
          </h1>
          <p style={{ fontSize: 16, color: 'var(--fg-1)', lineHeight: 1.7, marginBottom: 24 }}>
            풀스택 엔지니어. 작은 제품을 직접 만들고, 직접 운영하며, 직접 사용합니다.
          </p>
          <div style={{ padding: 16, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6 }}>
            <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 6 }}>// now</div>
            <div style={{ fontSize: 14, color: 'var(--fg-1)', lineHeight: 1.6 }}>
              홈서버를 다시 세팅 중입니다. Tailscale + Docker로 작은 서비스 5개를 운영합니다.
            </div>
          </div>
        </div>
        <div>
          <div className="caps" style={{ marginBottom: 8 }}>Index</div>
          <div style={{ borderTop: '1px solid var(--line-2)' }}>
            {rows.map((r, i) => (
              <a key={r.n} href="#" style={{ display: 'grid', gridTemplateColumns: '60px 1fr auto', alignItems: 'baseline', gap: 24, padding: '24px 4px', borderBottom: '1px solid var(--line-1)' }}>
                <span className="mono" style={{ fontSize: 12, color: i===0 ? 'var(--accent)' : 'var(--fg-3)' }}>{r.n}</span>
                <div>
                  <div style={{ fontSize: 28, letterSpacing: '-0.02em', marginBottom: 4 }}>{r.label}</div>
                  <div style={{ fontSize: 13, color: 'var(--fg-2)' }}>{r.desc}</div>
                </div>
                <span className="mono" style={{ fontSize: 14, color: 'var(--fg-3)' }}>→</span>
              </a>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

/* ---- Variant 4 — Status board / dashboard ---- */
window.LandingStatus = function LandingStatus() {
  const Stat = ({ label, value, sub }) => (
    <div style={{ padding: 20, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6 }}>
      <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.12em' }}>{label}</div>
      <div style={{ fontSize: 32, letterSpacing: '-0.02em', lineHeight: 1, marginBottom: 6 }}>{value}</div>
      <div style={{ fontSize: 12, color: 'var(--fg-2)' }}>{sub}</div>
    </div>
  );
  return (
    <div style={{ width: 1280, height: 760, background: 'var(--bg-0)', display: 'flex', flexDirection: 'column' }}>
      <NavBar />
      <div style={{ flex: 1, padding: '40px 56px', display: 'grid', gridTemplateRows: 'auto 1fr', gap: 24 }}>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: 32 }}>
          <h1 style={{ fontSize: 48, lineHeight: 1.05, letterSpacing: '-0.025em', margin: 0, fontWeight: 600 }}>
            Status: <span style={{ color: 'var(--accent)' }}>shipping</span>
          </h1>
          <div className="mono" style={{ fontSize: 12, color: 'var(--fg-2)', marginBottom: 8 }}>
            kknaks · full-stack engineer · seoul
          </div>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
          <Stat label="years" value="4+" sub="full-stack production" />
          <Stat label="projects" value="12" sub="personal · open source" />
          <Stat label="products" value="3" sub="shipped at companies" />
          <Stat label="uptime" value="99.4%" sub="self-hosted homelab" />
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: 12 }}>
          <div style={{ padding: 24, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6 }}>
            <div className="caps" style={{ marginBottom: 16 }}>Latest deploy</div>
            <div style={{ display: 'grid', gridTemplateColumns: '110px 1fr auto', gap: 16, alignItems: 'baseline', marginBottom: 12 }}>
              <span className="mono" style={{ fontSize: 12, color: 'var(--fg-3)' }}>2026.04.18</span>
              <div>
                <div style={{ fontSize: 16, marginBottom: 2 }}>Homelab Console v0.6</div>
                <div style={{ fontSize: 13, color: 'var(--fg-2)' }}>WebSocket 메트릭 푸시 안정화 + 로그 뷰어</div>
              </div>
              <span className="tag accent"><span className="tag-dot" style={{ background: 'var(--accent)' }} />live</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '110px 1fr auto', gap: 16, alignItems: 'baseline', marginBottom: 12, paddingTop: 12, borderTop: '1px solid var(--line-1)' }}>
              <span className="mono" style={{ fontSize: 12, color: 'var(--fg-3)' }}>2026.03.02</span>
              <div>
                <div style={{ fontSize: 16, marginBottom: 2 }}>kknaks.dev v0.1</div>
                <div style={{ fontSize: 13, color: 'var(--fg-2)' }}>새 포트폴리오 사이트 배포</div>
              </div>
              <span className="tag">staging</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '110px 1fr auto', gap: 16, alignItems: 'baseline', paddingTop: 12, borderTop: '1px solid var(--line-1)' }}>
              <span className="mono" style={{ fontSize: 12, color: 'var(--fg-3)' }}>2026.01.20</span>
              <div>
                <div style={{ fontSize: 16, marginBottom: 2 }}>Acme Admin · 권한 v2</div>
                <div style={{ fontSize: 13, color: 'var(--fg-2)' }}>역할 기반 접근 제어 리팩터링</div>
              </div>
              <span className="tag">work</span>
            </div>
          </div>
          <div style={{ padding: 24, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6 }}>
            <div className="caps" style={{ marginBottom: 16 }}>Now</div>
            <div style={{ fontSize: 14, color: 'var(--fg-1)', lineHeight: 1.7, marginBottom: 16 }}>
              Next.js 15와 React Server Component를 학습 중. 팀 내 admin 도구를 점진 마이그레이션 중입니다.
            </div>
            <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>// reading</div>
            <div style={{ fontSize: 13, color: 'var(--fg-1)', marginBottom: 8 }}>Designing Data-Intensive Applications</div>
            <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>// listening</div>
            <div style={{ fontSize: 13, color: 'var(--fg-1)' }}>Lo-fi · Brian Eno</div>
          </div>
        </div>
      </div>
    </div>
  );
};
