/* global React */

/* =========================================================
   PAGE LEVEL SCREENS
   ========================================================= */

const PageHeader = ({ idx, title, kicker }) => (
  <header style={{ padding: '40px 64px 24px', borderBottom: '1px solid var(--line-1)' }}>
    <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12 }}>
      {idx} · {kicker}
    </div>
    <h1 style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.025em', margin: 0, fontWeight: 600 }}>{title}</h1>
  </header>
);

/* ---- About page ---- */
window.PageAbout = function PageAbout() {
  return (
    <div style={{ width: 1100, background: 'var(--bg-0)' }}>
      <PageHeader idx="01 / About" kicker="who" title="만드는 사람,\nkknaks" />
      <div style={{ padding: '40px 64px', display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: 64 }}>
        <div>
          <p style={{ fontSize: 18, lineHeight: 1.65, color: 'var(--fg-0)', marginTop: 0 }}>
            저는 작은 도구를 직접 만들고 직접 운영하는 풀스택 엔지니어입니다.
            서비스의 한 끝에서 다른 끝까지 — 데이터 모델부터 배포 파이프라인, UI의 한 픽셀까지 — 책임지는 일을 좋아합니다.
          </p>
          <p style={{ fontSize: 15, lineHeight: 1.7, color: 'var(--fg-1)', marginBottom: 24 }}>
            낮에는 회사에서 내부 도구 플랫폼을 만들고, 밤에는 홈서버 위에서 작은 사이드 프로젝트들을 돌립니다.
            제가 만든 것을 매일 쓰는 일이 가장 빠른 피드백 루프라고 믿습니다.
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginTop: 32 }}>
            {[
              { h: '믿는 것', p: '작게 만들고, 자주 배포하고, 직접 쓴다.' },
              { h: '피하는 것', p: '추상화 먼저. 도구로 시작해서 빌드한 적 없는 시스템.' },
              { h: '잘하는 것', p: '복잡한 도메인을 단순한 인터페이스로 옮기는 것.' },
              { h: '배우는 것', p: 'RSC · 분산 시스템 · 디자인 시스템 운영.' },
            ].map(b => (
              <div key={b.h} style={{ padding: 16, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6 }}>
                <div className="mono" style={{ fontSize: 11, color: 'var(--accent)', marginBottom: 8 }}>// {b.h}</div>
                <div style={{ fontSize: 14, color: 'var(--fg-1)', lineHeight: 1.6 }}>{b.p}</div>
              </div>
            ))}
          </div>
        </div>
        <aside>
          <div className="placeholder-hatch" style={{ aspectRatio: '4/5', borderRadius: 6, marginBottom: 24 }}>[ portrait · 800×1000 ]</div>
          <dl style={{ margin: 0, fontSize: 13 }}>
            {[
              ['location', 'Seoul, KR'],
              ['role', 'Full-stack Engineer'],
              ['focus', 'Internal tools · Self-hosting'],
              ['email', 'hello@kknaks.dev'],
              ['github', '@kknaks'],
            ].map(([k, v]) => (
              <div key={k} style={{ display: 'grid', gridTemplateColumns: '90px 1fr', padding: '8px 0', borderTop: '1px solid var(--line-1)' }}>
                <dt className="mono" style={{ color: 'var(--fg-3)' }}>{k}</dt>
                <dd style={{ margin: 0, color: 'var(--fg-1)' }}>{v}</dd>
              </div>
            ))}
          </dl>
        </aside>
      </div>
    </div>
  );
};

/* ---- Career page ---- */
window.PageCareer = function PageCareer() {
  const items = [
    { y: '2024 — present', t: 'Senior Engineer', org: 'Acme Corp.', loc: 'Seoul', d: '내부 도구 플랫폼 리드. 권한 시스템과 어드민 표준화. 디자인 시스템과 함께 12개 어드민을 통합.', tags: ['Next.js', 'NestJS', 'Postgres'], active: true },
    { y: '2022 — 2024', t: 'Software Engineer', org: 'Foo Studio', loc: 'Seoul', d: '커머스 백엔드. 결제·정산 모듈 운영. 트래픽 30배 스케일업과 SLO 정의.', tags: ['Python', 'FastAPI', 'Redis'] },
    { y: '2020 — 2022', t: 'Full-stack Engineer', org: 'Bar Inc.', loc: 'Seoul', d: '관리자 페이지와 내부 BI 대시보드. 디자인 시스템 v1을 0→1로 구축.', tags: ['React', 'TypeScript'] },
    { y: '2019', t: 'Engineering Intern', org: 'Baz Lab.', loc: 'Seoul', d: '리서치 데이터 파이프라인 + 어노테이션 도구.', tags: ['Python', 'Django'] },
  ];
  return (
    <div style={{ width: 1100, background: 'var(--bg-0)' }}>
      <PageHeader idx="02 / Career" kicker="when · where" title="이력" />
      <div style={{ padding: '40px 64px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '180px 1fr', gap: 48 }}>
          <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.12em', position: 'sticky', top: 24 }}>
            <div style={{ marginBottom: 8 }}>// 4 yrs<br />// 4 roles</div>
            <div style={{ marginTop: 16, color: 'var(--fg-2)' }}>focus<br /><span style={{ color: 'var(--fg-0)' }}>internal tools</span><br /><span style={{ color: 'var(--fg-0)' }}>commerce backend</span></div>
          </div>
          <div style={{ position: 'relative', paddingLeft: 28 }}>
            <div style={{ position: 'absolute', left: 5, top: 8, bottom: 8, width: 1, background: 'var(--line-2)' }} />
            {items.map((it, i) => (
              <div key={i} style={{ position: 'relative', marginBottom: 36 }}>
                <span style={{ position: 'absolute', left: -28, top: 8, width: 11, height: 11, borderRadius: 2, background: 'var(--bg-0)', border: `1px solid ${it.active ? 'var(--accent)' : 'var(--line-3)'}`, boxShadow: it.active ? '0 0 0 3px var(--accent-soft)' : 'none' }} />
                <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 6 }}>{it.y}{it.active && <span style={{ color: 'var(--accent)', marginLeft: 8 }}>● now</span>}</div>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginBottom: 6 }}>
                  <h3 style={{ margin: 0, fontSize: 20, letterSpacing: '-0.01em' }}>{it.t}</h3>
                  <span style={{ color: 'var(--fg-3)' }}>·</span>
                  <span style={{ color: 'var(--fg-1)', fontSize: 16 }}>{it.org}</span>
                  <span className="mono" style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--fg-3)' }}>{it.loc}</span>
                </div>
                <p style={{ margin: '0 0 10px', color: 'var(--fg-1)', fontSize: 14, lineHeight: 1.6, maxWidth: 640 }}>{it.d}</p>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                  {it.tags.map(t => <span key={t} className="tag">{t}</span>)}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

/* ---- Projects page (cards grid) ---- */
window.PageProjects = function PageProjects() {
  const data = [
    { id: 'P-01', t: 'Homelab Console', d: '홈서버 메트릭과 컨테이너 상태를 실시간으로 보는 대시보드.', tags: ['Next.js', 'FastAPI', 'WebSocket'], status: 'live', date: '2026' },
    { id: 'P-02', t: 'Inbox Zero', d: '내가 안 읽는 뉴스레터를 자동으로 요약하는 봇.', tags: ['Python', 'OpenAI'], status: 'live', date: '2025' },
    { id: 'P-03', t: 'Tide', d: '취미용 가계부. 영수증 OCR + 월간 요약.', tags: ['Next.js', 'Postgres'], status: 'wip', date: '2025' },
    { id: 'P-04', t: 'Static Tail', d: 'Tailscale 위에서만 접근 가능한 정적 사이트 생성기.', tags: ['Go', 'Tailscale'], status: 'archived', date: '2024' },
  ];
  const StatusTag = ({ s }) => {
    const map = { live: { c: 'var(--accent)', l: 'live' }, wip: { c: 'var(--info)', l: 'wip' }, archived: { c: 'var(--fg-3)', l: 'archived' } };
    return <span className="tag" style={s==='live' ? { color: 'var(--accent)', background: 'var(--accent-soft)', borderColor: 'var(--accent-line)' } : {}}><span className="tag-dot" style={{ background: map[s].c }} />{map[s].l}</span>;
  };
  return (
    <div style={{ width: 1100, background: 'var(--bg-0)' }}>
      <PageHeader idx="03 / Projects" kicker="solo · personal" title="혼자 만든 것들" />
      <div style={{ padding: '32px 64px 48px' }}>
        <div style={{ display: 'flex', gap: 8, marginBottom: 24, alignItems: 'center' }}>
          <span className="caps">filter</span>
          <button className="btn" style={{ padding: '4px 10px', fontSize: 11 }}>All <span style={{ color: 'var(--fg-3)', marginLeft: 4 }}>12</span></button>
          <button className="btn ghost" style={{ padding: '4px 10px', fontSize: 11 }}>Web</button>
          <button className="btn ghost" style={{ padding: '4px 10px', fontSize: 11 }}>CLI</button>
          <button className="btn ghost" style={{ padding: '4px 10px', fontSize: 11 }}>Bot</button>
          <span className="mono" style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--fg-3)' }}>sorted by date ↓</span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          {data.map(p => (
            <article key={p.id} className="card" style={{ overflow: 'hidden' }}>
              <div className="placeholder-hatch" style={{ aspectRatio: '16/9' }}>[ {p.t} · 1600×900 ]</div>
              <div style={{ padding: 20, borderTop: '1px solid var(--line-1)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>{p.id}</span>
                  <StatusTag s={p.status} />
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginLeft: 'auto' }}>{p.date}</span>
                </div>
                <h3 style={{ margin: '0 0 6px', fontSize: 18, letterSpacing: '-0.01em' }}>{p.t}</h3>
                <p style={{ margin: '0 0 12px', fontSize: 13, color: 'var(--fg-2)', lineHeight: 1.55 }}>{p.d}</p>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                  {p.tags.map(t => <span key={t} className="tag">{t}</span>)}
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </div>
  );
};

/* ---- Products page (case study list) ---- */
window.PageProducts = function PageProducts() {
  const data = [
    { id: '01', t: 'Acme Admin Platform', co: 'Acme Corp.', role: 'Lead engineer', y: '2024 — present', d: '12개의 분산된 어드민을 한 플랫폼으로 통합. 역할 기반 접근 제어와 감사 로그 도입.', metric: ['12개 어드민 통합', '권한 변경 30s → 즉시', '온콜 인입 -42%'] },
    { id: '02', t: 'Foo Commerce Pay', co: 'Foo Studio', role: 'Backend engineer', y: '2022 — 2024', d: '결제·정산 모듈 신규 구축. 멀티 PG와 정기 결제, 부분 환불 흐름.', metric: ['트래픽 30× scale', '결제 실패율 -1.8pt', 'p99 380ms → 140ms'] },
    { id: '03', t: 'Bar BI Studio', co: 'Bar Inc.', role: 'Full-stack', y: '2020 — 2022', d: '내부 BI 대시보드 0→1. 디자인 시스템 v1과 컴포넌트 라이브러리 정립.', metric: ['200+ 차트 템플릿', 'DS v1 — 38개 컴포넌트', '레포트 작성 -65%'] },
  ];
  return (
    <div style={{ width: 1100, background: 'var(--bg-0)' }}>
      <PageHeader idx="04 / Products" kicker="company · shipped" title="회사에서 만든 것들" />
      <div style={{ padding: '32px 64px 48px' }}>
        {data.map((p, i) => (
          <article key={p.id} style={{ display: 'grid', gridTemplateColumns: '60px 1fr 1.2fr', gap: 32, padding: '32px 0', borderTop: '1px solid var(--line-1)' }}>
            <div className="mono" style={{ fontSize: 12, color: 'var(--fg-3)' }}>{p.id}</div>
            <div>
              <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 8 }}>{p.y} · {p.co}</div>
              <h3 style={{ margin: '0 0 6px', fontSize: 26, letterSpacing: '-0.02em' }}>{p.t}</h3>
              <div style={{ fontSize: 13, color: 'var(--fg-2)', marginBottom: 12 }}>역할 · {p.role}</div>
              <p style={{ margin: 0, fontSize: 14, color: 'var(--fg-1)', lineHeight: 1.65, maxWidth: 420 }}>{p.d}</p>
            </div>
            <div>
              <div className="caps" style={{ marginBottom: 12 }}>Impact</div>
              <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
                {p.metric.map(m => (
                  <li key={m} style={{ display: 'flex', alignItems: 'baseline', gap: 12, padding: '10px 0', borderTop: '1px solid var(--line-1)', fontSize: 14, color: 'var(--fg-1)' }}>
                    <span style={{ width: 6, height: 6, background: 'var(--accent)', borderRadius: 1, transform: 'translateY(-2px)' }} />
                    {m}
                  </li>
                ))}
              </ul>
              <button className="btn ghost" style={{ marginTop: 16, padding: '6px 10px', fontSize: 12 }}>케이스 스터디 읽기 <span className="arrow">→</span></button>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
};
