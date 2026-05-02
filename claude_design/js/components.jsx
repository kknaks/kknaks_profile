/* global React */
const { useState: useStateC } = React;

/* =========================================================
   COMPONENTS
   ========================================================= */

window.ComponentButtons = function ComponentButtons() {
  return (
    <div style={{ width: 760, padding: 32, background: 'var(--bg-0)' }}>
      <div className="eyebrow" style={{ marginBottom: 6 }}>components / buttons</div>
      <h3 style={{ fontSize: 20, margin: '0 0 20px', fontWeight: 500 }}>Buttons</h3>
      <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 16 }}>
        <button className="btn primary">이력서 다운로드 <span className="arrow">↓</span></button>
        <button className="btn">GitHub <span className="arrow">↗</span></button>
        <button className="btn ghost">자세히 보기 <span className="arrow">→</span></button>
      </div>
      <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
        <button className="btn" style={{ padding: '6px 10px', fontSize: 12 }}>EN / KO</button>
        <button className="btn" style={{ padding: '6px 10px', fontSize: 12 }}><span className="mono">⌘K</span></button>
        <button className="btn ghost" style={{ padding: '6px 10px', fontSize: 12 }}>Filter</button>
      </div>
    </div>
  );
};

window.ComponentTags = function ComponentTags() {
  const tags = ['Next.js', 'TypeScript', 'Python', 'FastAPI', 'PostgreSQL', 'Docker', 'Tailwind', 'React Query'];
  return (
    <div style={{ width: 760, padding: 32, background: 'var(--bg-0)' }}>
      <div className="eyebrow" style={{ marginBottom: 6 }}>components / tags</div>
      <h3 style={{ fontSize: 20, margin: '0 0 20px', fontWeight: 500 }}>Tech tags</h3>
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 16 }}>
        {tags.map(t => <span key={t} className="tag">{t}</span>)}
      </div>
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 16 }}>
        <span className="tag accent"><span className="tag-dot" style={{ background: 'var(--accent)' }} />Production</span>
        <span className="tag"><span className="tag-dot" />Archived</span>
        <span className="tag"><span className="tag-dot" style={{ background: 'var(--info)' }} />WIP</span>
        <span className="tag"><span className="tag-dot" style={{ background: 'var(--warn)' }} />Beta</span>
      </div>
      <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>// 모노스페이스 + bg-2 표면. 액센트는 핵심 상태에만.</div>
    </div>
  );
};

window.ComponentNav = function ComponentNav() {
  const [active, setA] = useStateC('Projects');
  const items = ['About', 'Career', 'Projects', 'Products'];
  return (
    <div style={{ width: 1100, padding: 0, background: 'var(--bg-0)' }}>
      <div style={{ padding: '12px 24px', display: 'flex', alignItems: 'center', gap: 24, borderBottom: '1px solid var(--line-1)', background: 'var(--bg-0)' }}>
        <div className="mono" style={{ fontSize: 13, color: 'var(--fg-0)', display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ width: 8, height: 8, background: 'var(--accent)', borderRadius: 2 }} />
          kknaks<span style={{ color: 'var(--fg-3)' }}>.dev</span>
        </div>
        <nav style={{ display: 'flex', gap: 4, marginLeft: 16 }}>
          {items.map(i => (
            <button key={i} onClick={() => setA(i)} style={{
              fontFamily: 'var(--font-mono)', fontSize: 12, padding: '6px 10px',
              background: 'transparent', border: 'none', cursor: 'pointer',
              color: active === i ? 'var(--fg-0)' : 'var(--fg-2)',
              borderBottom: active === i ? '1px solid var(--accent)' : '1px solid transparent',
              borderRadius: 0,
            }}>
              <span style={{ color: 'var(--fg-3)' }}>0{items.indexOf(i)+1} </span>{i}
            </button>
          ))}
        </nav>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: 8, alignItems: 'center' }}>
          <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>v0.1.0</span>
          <button className="btn" style={{ padding: '4px 8px', fontSize: 11 }}>KO / EN</button>
        </div>
      </div>
      <div style={{ padding: 16 }} className="mono">
        <span style={{ fontSize: 11, color: 'var(--fg-3)' }}>// nav · 모노스페이스 · 좌측 인덱스 · 우측 메타</span>
      </div>
    </div>
  );
};

window.ComponentProjectCard = function ComponentProjectCard() {
  return (
    <div style={{ width: 760, padding: 32, background: 'var(--bg-0)' }}>
      <div className="eyebrow" style={{ marginBottom: 6 }}>components / project card</div>
      <h3 style={{ fontSize: 20, margin: '0 0 20px', fontWeight: 500 }}>Project card</h3>
      <article className="card" style={{ overflow: 'hidden' }}>
        <div className="placeholder-hatch" style={{ height: 200 }}>[ project thumbnail · 1600×900 ]</div>
        <div style={{ padding: 20, borderTop: '1px solid var(--line-1)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
            <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>P-03</span>
            <span className="tag accent"><span className="tag-dot" style={{ background: 'var(--accent)' }} />Live</span>
            <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginLeft: 'auto' }}>2025.10</span>
          </div>
          <h4 style={{ margin: '0 0 6px', fontSize: 18, letterSpacing: '-0.01em' }}>Homelab Console</h4>
          <p style={{ margin: '0 0 14px', fontSize: 14, color: 'var(--fg-2)', lineHeight: 1.55 }}>
            홈서버 상태와 컨테이너를 한눈에 확인하는 대시보드. WebSocket으로 실시간 메트릭을 푸시합니다.
          </p>
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            <span className="tag">Next.js</span>
            <span className="tag">FastAPI</span>
            <span className="tag">WebSocket</span>
          </div>
        </div>
      </article>
    </div>
  );
};

window.ComponentTimeline = function ComponentTimeline() {
  const items = [
    { y: '2024 — present', t: 'Senior Engineer', org: 'Acme Corp.', d: '내부 도구 플랫폼 리드. Next.js 기반 어드민과 권한 시스템 설계.', tags: ['Next.js', 'NestJS'] },
    { y: '2022 — 2024', t: 'Software Engineer', org: 'Foo Studio', d: '커머스 백엔드와 결제 모듈 담당. 트래픽 30배 스케일업 운영 안정화.', tags: ['Python', 'PostgreSQL'] },
    { y: '2020 — 2022', t: 'Full-stack Engineer', org: 'Bar Inc.', d: '관리자 페이지와 내부 BI 대시보드. 디자인 시스템 v1 구축.', tags: ['React', 'TypeScript'] },
  ];
  return (
    <div style={{ width: 760, padding: 32, background: 'var(--bg-0)' }}>
      <div className="eyebrow" style={{ marginBottom: 6 }}>components / timeline</div>
      <h3 style={{ fontSize: 20, margin: '0 0 20px', fontWeight: 500 }}>Timeline item</h3>
      <div style={{ position: 'relative', paddingLeft: 24 }}>
        <div style={{ position: 'absolute', left: 5, top: 6, bottom: 6, width: 1, background: 'var(--line-2)' }} />
        {items.map((it, i) => (
          <div key={i} style={{ position: 'relative', marginBottom: 28 }}>
            <span style={{ position: 'absolute', left: -24, top: 6, width: 11, height: 11, borderRadius: 2, background: 'var(--bg-0)', border: `1px solid ${i===0?'var(--accent)':'var(--line-3)'}`, boxShadow: i===0 ? '0 0 0 3px var(--accent-soft)' : 'none' }} />
            <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 4 }}>{it.y}</div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginBottom: 4 }}>
              <h4 style={{ margin: 0, fontSize: 16, fontWeight: 500 }}>{it.t}</h4>
              <span style={{ color: 'var(--fg-3)' }}>·</span>
              <span style={{ color: 'var(--fg-2)', fontSize: 14 }}>{it.org}</span>
            </div>
            <p style={{ margin: '0 0 8px', color: 'var(--fg-1)', fontSize: 14, lineHeight: 1.55 }}>{it.d}</p>
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
              {it.tags.map(t => <span key={t} className="tag">{t}</span>)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
