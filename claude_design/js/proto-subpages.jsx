/* global React */

/* =========================================================
   Contribution Grass — AI가 가공한 활동 히트맵
   53주 × 7일. 단순 커밋이 아니라 "내가 뭘 했는지" 요약.
   ========================================================= */
function ContribGrass({ lang, T }) {
  // 결정론적 mock 생성 (시드 기반 — 새로고침해도 그대로)
  const { weeks, total, byKind } = React.useMemo(() => {
    const KINDS = [
      { k: 'commit', ko: '커밋',   en: 'commits' },
      { k: 'note',   ko: '노트',   en: 'notes' },
      { k: 'study',  ko: '학습',   en: 'study' },
      { k: 'ship',   ko: '배포',   en: 'deploys' },
    ];
    // mulberry32 시드
    let s = 20260501;
    const rnd = () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };

    const today = new Date(2026, 4, 1); // 2026-05-01 (현재 날짜 기준 고정)
    const dayMs = 86400000;
    // 53주 전 같은 요일까지 거슬러 — 일요일 시작 격자
    const end = new Date(today);
    const endDow = end.getDay();
    // 마지막 칸이 today가 되도록, 53*7 - (6 - endDow) 일 전이 시작
    const totalDays = 53 * 7;
    const start = new Date(end.getTime() - (totalDays - 1 - (6 - endDow)) * dayMs);
    // start를 일요일로 정렬
    start.setDate(start.getDate() - start.getDay());

    const cells = [];
    let runningTotal = 0;
    const kindCount = { commit: 0, note: 0, study: 0, ship: 0 };
    for (let i = 0; i < totalDays; i++) {
      const d = new Date(start.getTime() + i * dayMs);
      const future = d > today;
      const dow = d.getDay();
      // 패턴: 평일 활동 ↑, 주말 ↓, 최근 6개월 ↑
      const monthsAgo = (today.getFullYear() - d.getFullYear()) * 12 + (today.getMonth() - d.getMonth());
      const recencyBoost = Math.max(0, 1 - monthsAgo / 14);
      const weekdayBoost = (dow >= 1 && dow <= 5) ? 1 : 0.45;
      const r = rnd();
      let count = 0;
      if (!future) {
        const base = r * 6 * weekdayBoost * (0.4 + recencyBoost);
        count = Math.max(0, Math.round(base - 1.2));
        // 가끔 spike
        if (rnd() < 0.04) count += Math.round(rnd() * 6);
      }
      // 활동 종류 (AI 분류)
      const kindIdx = future ? -1 : count === 0 ? -1 : Math.floor(rnd() * KINDS.length);
      const kind = kindIdx >= 0 ? KINDS[kindIdx].k : null;
      if (count > 0 && kind) kindCount[kind] += count;
      runningTotal += count;
      cells.push({ d, count, kind, future });
    }
    // 53주 × 7일 격자로 변환
    const w = [];
    for (let i = 0; i < 53; i++) {
      w.push(cells.slice(i * 7, i * 7 + 7));
    }
    return { weeks: w, total: runningTotal, byKind: kindCount };
  }, []);

  const [hover, setHover] = React.useState(null);
  const wrapRef = React.useRef(null);

  // 명도 5단계 — 터미널 그린 기반
  const levelColor = (count) => {
    if (count <= 0) return 'var(--bg-2)';
    if (count <= 2) return 'oklch(0.42 0.14 152 / 0.45)';
    if (count <= 4) return 'oklch(0.55 0.17 152 / 0.7)';
    if (count <= 7) return 'oklch(0.68 0.19 152 / 0.85)';
    return 'oklch(0.78 0.21 152)';
  };

  const fmtDate = (d) => {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    return `${y}.${m}.${dd}`;
  };

  // AI 요약 mock — 활동 종류별 한 줄
  const aiSummary = (cell) => {
    if (!cell || cell.future || cell.count === 0) return null;
    const ko = {
      commit: ['리팩토링 위주', 'API 엔드포인트 추가', '버그 픽스', '인프라 정리'],
      note:   ['CS 노트 작성', '논문 정리', '회고 기록', '학습 요약'],
      study:  ['알고리즘 풀이', '강의 시청', '책 읽고 정리', '튜토리얼 따라함'],
      ship:   ['배포 작업', '도메인 연결', '모니터링 셋업', '환경 변수 정리'],
    };
    const en = {
      commit: ['mostly refactor', 'new API endpoints', 'bug fixes', 'infra cleanup'],
      note:   ['CS note', 'paper summary', 'retro entry', 'learning log'],
      study:  ['algorithm practice', 'watched lecture', 'book notes', 'followed tutorial'],
      ship:   ['deploy work', 'domain wiring', 'monitoring setup', 'env cleanup'],
    };
    const map = lang === 'en' ? en : ko;
    // 시드를 날짜+kind에서 — 호버할 때마다 안 바뀌게
    const seed = cell.d.getDate() * 7 + cell.d.getMonth();
    return map[cell.kind][seed % map[cell.kind].length];
  };

  // 월 라벨 — 각 주의 첫째날이 새 달의 첫주면 표시
  const monthLabels = weeks.map((wk, wi) => {
    const first = wk[0];
    if (!first) return null;
    const isFirstWeekOfMonth = first.d.getDate() <= 7;
    if (!isFirstWeekOfMonth) return null;
    const monthsKo = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'];
    const monthsEn = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const arr = lang === 'en' ? monthsEn : monthsKo;
    return { wi, label: arr[first.d.getMonth()] };
  }).filter(Boolean);

  const dayLabelsKo = ['', '월', '', '수', '', '금', ''];
  const dayLabelsEn = ['', 'Mon', '', 'Wed', '', 'Fri', ''];
  const dayLabels = lang === 'en' ? dayLabelsEn : dayLabelsKo;

  // 셀 사이즈 — 본문 풀폭에 맞춤
  const CELL = 11;
  const GAP = 3;

  // 우측 패널에 쓰일 선택된 셀 (클릭)
  const [selected, setSelected] = React.useState(null);
  // 기본 선택: 오늘 (마지막 주의 마지막 날)
  React.useEffect(() => {
    if (selected) return;
    for (let wi = weeks.length - 1; wi >= 0; wi--) {
      for (let di = 6; di >= 0; di--) {
        const c = weeks[wi][di];
        if (c && !c.future) { setSelected({ cell: c, wi, di }); return; }
      }
    }
  }, [weeks, selected]);

  return (
    <div ref={wrapRef} className="grass-wrap" style={{ marginTop: 24, padding: 20, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6, position: 'relative', display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) 260px', gap: 28, alignItems: 'start' }}>
      <style>{`
        @media (max-width: 768px) {
          .grass-wrap { grid-template-columns: 1fr !important; }
          .grass-board-scroll { overflow-x: auto !important; overflow-y: hidden; }
          .grass-board-inner { min-width: max-content !important; width: auto !important; }
          .grass-cells-row { width: auto !important; }
          .grass-cell { width: 11px !important; height: 11px !important; flex: 0 0 auto !important; }
        }
      `}</style>
      <div style={{ minWidth: 0 }}>
      <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: 4 }}>
        <div className="mono" style={{ fontSize: 11, color: 'var(--accent)' }}>// activity</div>
        <div className="mono" style={{ fontSize: 10, color: 'var(--fg-3)' }}>
          {total} {T('회 · 지난 1년', 'events · past year')}
        </div>
      </div>
      <div className="mono" style={{ fontSize: 10, color: 'var(--fg-3)', marginBottom: 12, lineHeight: 1.4 }}>
        {T('AI가 분류한 커밋 · 노트 · 학습 · 배포 활동', 'AI-classified commits · notes · study · deploys')}
      </div>

      {/* 격자 — 풍용으로 자동 fit, 모바일은 가로스크롤 */}
      <div className="grass-board-scroll" style={{ paddingBottom: 4 }}>
        <div className="grass-board-inner" style={{ width: '100%' }}>
          {/* 월 라벨 row */}
          <div className="mono" style={{ display: 'grid', gridTemplateColumns: `18px repeat(${weeks.length}, 1fr)`, columnGap: GAP, fontSize: 9, color: 'var(--fg-3)', marginBottom: 4, height: 12, lineHeight: '12px' }}>
            <span />
            {weeks.map((wk, wi) => {
              const ml = monthLabels.find(m => m.wi === wi);
              return <span key={wi} style={{ whiteSpace: 'nowrap' }}>{ml ? ml.label : ''}</span>;
            })}
          </div>
          {/* 격자 + 요일 라벨 */}
          <div className="grass-cells-row" style={{ display: 'grid', gridTemplateColumns: `18px repeat(${weeks.length}, 1fr)`, columnGap: GAP, width: '100%' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: GAP }}>
              {dayLabels.map((dl, i) => (
                <span key={i} className="mono" style={{ fontSize: 9, color: 'var(--fg-3)', height: 0, paddingTop: 0, lineHeight: '11px', display: 'flex', alignItems: 'center', minHeight: 11 }}>{dl}</span>
              ))}
            </div>
            {weeks.map((wk, wi) => (
              <div key={wi} style={{ display: 'flex', flexDirection: 'column', gap: GAP, minWidth: 0 }}>
                {wk.map((cell, di) => {
                  const isSel = selected && selected.wi === wi && selected.di === di;
                  return (
                    <div
                      key={di}
                      className="grass-cell"
                      onMouseEnter={() => setHover({ cell, wi, di })}
                      onMouseLeave={() => setHover(null)}
                      onClick={() => !cell.future && cell.count > 0 && setSelected({ cell, wi, di })}
                      style={{
                        width: '100%', aspectRatio: '1 / 1',
                        background: cell.future ? 'transparent' : levelColor(cell.count),
                        border: cell.future ? 'none' : '1px solid oklch(1 0 0 / 0.04)',
                        borderRadius: 1.5,
                        cursor: cell.future || cell.count === 0 ? 'default' : 'pointer',
                        outline: isSel ? '1px solid var(--accent)' : (hover && hover.wi === wi && hover.di === di ? '1px solid var(--fg-2)' : 'none'),
                        outlineOffset: 1,
                        transition: 'outline 80ms',
                      }}
                    />
                  );
                })}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 범례 */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 12, fontSize: 10 }}>
        <span className="mono" style={{ color: 'var(--fg-3)' }}>{T('적음', 'less')}</span>
        {[0, 1, 3, 5, 9].map(c => (
          <span key={c} style={{ width: 11, height: 11, background: levelColor(c), border: '1px solid oklch(1 0 0 / 0.04)', borderRadius: 1.5 }} />
        ))}
        <span className="mono" style={{ color: 'var(--fg-3)' }}>{T('많음', 'more')}</span>
      </div>

      </div>

      {/* 우측 — 선택한 날의 상세. 클릭 안 하면 아래의 간략 안내 */}
      <div style={{ minWidth: 0, borderLeft: '1px solid var(--line-1)', paddingLeft: 24, alignSelf: 'stretch' }}>
        {selected && selected.cell && !selected.cell.future && selected.cell.count > 0 ? (
          <div>
            <div className="mono" style={{ fontSize: 11, color: 'var(--accent)', marginBottom: 4 }}>// {selected.cell.kind}</div>
            <div className="mono" style={{ fontSize: 10, color: 'var(--fg-3)', marginBottom: 14 }}>
              {fmtDate(selected.cell.d)} · {selected.cell.count} {T('회', 'events')}
            </div>
            <div style={{ fontSize: 14, color: 'var(--fg-0)', lineHeight: 1.55, fontWeight: 500, marginBottom: 12 }}>
              {aiSummary(selected.cell)}
            </div>
            <p style={{ margin: 0, fontSize: 12, lineHeight: 1.65, color: 'var(--fg-2)' }}>
              {T(
                'AI가 그날 작성한 노트·커밋·세션을 모아 한 줄로 요약하고, 관련 링크를 표시해요.',
                'AI summarises the day\'s notes/commits/sessions into one line and surfaces related links.'
              )}
            </p>
          </div>
        ) : (
          <div>
            <div className="mono" style={{ fontSize: 11, color: 'var(--accent)', marginBottom: 4 }}>// summary</div>
            <div className="mono" style={{ fontSize: 10, color: 'var(--fg-3)', marginBottom: 14 }}>
              {total} {T('회 · 지난 1년', 'events · past year')}
            </div>
            <p style={{ margin: 0, fontSize: 12, lineHeight: 1.65, color: 'var(--fg-2)' }}>
              {T(
                '잔디는 그날 AI가 가공한 활동 기록이에요. 셀을 클릭하면 그날 뭐를 했는지 볼 수 있어요.',
                'Each cell is an AI-curated record of that day\'s activity. Click a cell to see what happened.'
              )}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   Sub-page: About
   ========================================================= */
window.ProtoAbout = function ProtoAbout({ lang }) {
  const T = (ko, en) => lang === 'en' ? en : ko;
  return (
    <div>
      <header className="pad-x m-pad-h" style={{ padding: '56px 80px 32px', borderBottom: '1px solid var(--line-1)' }}>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12 }}>
          01 / About · {T('만드는 사람', 'who builds it')}
        </div>
        <div className="about-id" style={{ display: 'flex', alignItems: 'center', gap: 24, flexWrap: 'wrap' }}>
          {/* 원형 이모지/아바타 자리 — 헤더 옆 */}
          <div style={{
            width: 88, height: 88, borderRadius: '50%',
            background: 'var(--bg-2)', border: '1px solid var(--line-2)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 40, flexShrink: 0,
          }}>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--fg-3)' }}>:)</span>
          </div>
          <div style={{ minWidth: 0 }}>
            <h1 className="m-h1" style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.025em', margin: 0, fontWeight: 600 }}>
              kknaks <span className="about-id-sub" style={{ color: 'var(--fg-3)', fontSize: 28, fontWeight: 400 }}>· 이건학</span>
            </h1>
            <div className="mono" style={{ fontSize: 13, color: 'var(--fg-2)', marginTop: 8 }}>
              backend engineer · 1년차 · seoul, kr
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
      <div className="pad-x m-stack" style={{ padding: '48px 80px', display: 'grid', gridTemplateColumns: 'minmax(0, 1.5fr) minmax(0, 1fr)', gap: 64 }}>
        <div style={{ minWidth: 0 }}>
          <p style={{ fontSize: 22, lineHeight: 1.55, letterSpacing: '-0.01em', color: 'var(--fg-0)', marginTop: 0, fontWeight: 500 }}>
            {T(
              '호기심으로 시작해서, 도전으로 만들고, 개발로 풀어냅니다.',
              'Curious enough to start, brave enough to build, stubborn enough to ship.'
            )}
          </p>
          <p style={{ fontSize: 16, lineHeight: 1.7, color: 'var(--fg-1)', marginTop: 24 }}>
            {T(
              '저는 새로운 것을 도전하고, 무언가를 만드는 일을 좋아하는 개발자입니다. 배우고 싶은 것이 생기면 작게라도 직접 만들어 보면서 손에 익히는 편입니다.',
              'I\'m a developer who likes trying new things and building stuff. When I want to learn something, I\'d rather build a small version of it than just read about it.'
            )}
          </p>
          <p style={{ fontSize: 15, lineHeight: 1.7, color: 'var(--fg-1)' }}>
            {T(
              '지금은 AI 회사에서 백엔드 엔지니어로 일하고 있고, 그 외에는 앱과 웹사이트를 만들면서 풀스택의 폭을 넓히고 있습니다.',
              'Currently a backend engineer at an AI company, while building apps and websites on the side to broaden into full-stack.'
            )}
          </p>

          <div className="m-stack" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginTop: 36 }}>
            {[
              { h: T('지금 일하는 곳', 'Working on'),
                p: T('AI 회사 · 백엔드 엔지니어. 데이터·모델 서빙 인프라.', 'AI company · backend engineer. Data + model-serving infra.') },
              { h: T('만들고 있는 것', 'Building'),
                p: T('홈서버 위에서 돌아가는 작은 앱과 웹사이트들.', 'Small apps and sites running on my home server.') },
              { h: T('관심 있는 기술', 'Curious about'),
                p: 'AI · Python · Infra · self-hosting' },
              { h: T('일하는 방식', 'How I work'),
                p: T('일단 만들고, 직접 써보고, 부족한 부분을 채운다.', 'Ship a tiny version, use it, then fill in what\'s missing.') },
            ].map(b => (
              <div key={b.h} style={{ padding: 18, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6 }}>
                <div className="mono" style={{ fontSize: 11, color: 'var(--accent)', marginBottom: 8 }}>// {b.h}</div>
                <div style={{ fontSize: 14, color: 'var(--fg-1)', lineHeight: 1.6 }}>{b.p}</div>
              </div>
            ))}
          </div>
        </div>

        <aside>
          <dl style={{ margin: 0, fontSize: 13 }}>
            {[
              ['name',     '이건학 (kknaks)'],
              ['role',     'Backend Engineer'],
              ['location', 'Seoul, KR'],
              ['focus',    'AI · Python · Infra'],
              ['email',    'kknaks@gmail.com'],
              ['github',   'github.com/kknaks'],
            ].map(([k, v]) => (
              <div key={k} style={{ display: 'grid', gridTemplateColumns: '90px 1fr', padding: '10px 0', borderTop: '1px solid var(--line-1)' }}>
                <dt className="mono" style={{ color: 'var(--fg-3)' }}>{k}</dt>
                <dd style={{ margin: 0, color: 'var(--fg-1)' }}>{v}</dd>
              </div>
            ))}
            <div style={{ display: 'grid', gridTemplateColumns: '90px 1fr', padding: '10px 0', borderTop: '1px solid var(--line-1)', borderBottom: '1px solid var(--line-1)' }}>
              <dt className="mono" style={{ color: 'var(--fg-3)' }}>links</dt>
              <dd style={{ margin: 0, color: 'var(--fg-3)', fontFamily: 'var(--font-mono)', fontSize: 12 }}>// soon — from db</dd>
            </div>
          </dl>

          <div style={{ marginTop: 24, padding: 16, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6 }}>
            <div className="mono" style={{ fontSize: 11, color: 'var(--accent)', marginBottom: 8 }}>// stack</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              {['Python', 'FastAPI', 'PostgreSQL', 'Docker', 'Next.js', 'TypeScript'].map(s => (
                <span key={s} className="tag">{s}</span>
              ))}
            </div>
          </div>
        </aside>
      </div>
      {/* 잔디 — 본문 4카드 아래 풀폭 */}
      <div className="pad-x" style={{ padding: '8px 80px 64px' }}>
        <ContribGrass lang={lang} T={T} />
      </div>
    </div>
  );
};

/* =========================================================
   Sub-page: Career — full timeline
   ========================================================= */
window.ProtoCareer = function ProtoCareer({ lang }) {
  const T = (ko, en) => lang === 'en' ? en : ko;
  const items = [
    { y: '2025.06 — present', t: 'Backend Engineer', org: 'Stealth AI Co.', loc: T('서울 · 하이브리드', 'Seoul · hybrid'), d: T('LLM 기반 B2B 제품의 백엔드. RAG 파이프라인 설계, 임베딩·검색 서버 운영, 사내 어드민 신규 구축.', 'Backend for an LLM-based B2B product. Designed the RAG pipeline, ran embedding/retrieval services, built the internal admin from scratch.'), tags: ['Python', 'FastAPI', 'Postgres', 'pgvector', 'Docker'], active: true },
    { y: '2025.01 — 2025.05', t: T('백엔드 부트캠프', 'Backend Bootcamp'), org: 'SSAFY 12기', loc: T('서울', 'Seoul'), d: T('자율 프로젝트로 팀 4명과 가계부 앱 백엔드를 만들었음. 결제 모듈과 OCR 영수증 인식까지. 우수상 수상.', 'Built a team-of-4 budgeting app backend during the self-directed track — payments + receipt OCR. Awarded top project.'), tags: ['Spring Boot', 'JPA', 'MySQL', 'AWS'] },
    { y: '2024.07 — 2024.12', t: T('개인 학습', 'Self-study'), org: T('독학', 'self-directed'), loc: '—', d: T('전공 외에서 개발로 전환. CS 기초(컴퓨터구조·OS·네트워크) 다시 보고, 알고리즘 + 토이 프로젝트 5개. Notes에 다 기록.', 'Pivot into engineering. Re-did CS fundamentals (architecture/OS/networks), algorithms, 5 toy projects. All logged in Notes.'), tags: [T('CS 기초', 'CS basics'), 'Python', 'Algorithms'] },
    { y: '— 2024.06', t: T('학사 졸업', 'B.S. graduated'), org: T('OO대학교 · 비전공', 'Univ. — non-CS major'), loc: T('서울', 'Seoul'), d: T('비전공 출신. 졸업 직전에 만든 작은 사이드 토이가 의외로 잘 되어 개발로 진로 전환.', 'Non-CS undergrad. A small toy I built right before graduation worked surprisingly well — that pulled me toward engineering.'), tags: [] },
  ];
  return (
    <div>
      <header className="pad-x m-pad-h" style={{ padding: '56px 80px 32px', borderBottom: '1px solid var(--line-1)' }}>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12 }}>
          02 / Career · {T('언제 · 어디서', 'when · where')}
        </div>
        <h1 className="m-h1" style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.025em', margin: 0, fontWeight: 600 }}>Career</h1>
      </header>
      <div className="pad-x" style={{ padding: '48px 80px' }}>
        <div className="m-stack" style={{ display: 'grid', gridTemplateColumns: '180px 1fr', gap: 48 }}>
          <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.12em' }}>
            <div>// 1 yr<br/>// 1 role</div>
            <div style={{ marginTop: 16, color: 'var(--fg-2)' }}>focus<br/><span style={{ color: 'var(--fg-0)' }}>backend · AI</span><br/><span style={{ color: 'var(--fg-0)' }}>RAG · infra</span></div>
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

/* =========================================================
   Sub-page: Projects — grid w/ filter
   ========================================================= */
window.ProtoProjects = function ProtoProjects({ lang }) {
  const T = (ko, en) => lang === 'en' ? en : ko;
  const all = [
    { id: 'P-01', t: 'Homelab Console',   cat: 'web', d: T('홈서버 메트릭(CPU/메모리/디스크)과 컨테이너 상태를 한 화면에서 보는 대시보드.', 'Single-pane dashboard for homelab metrics (CPU/mem/disk) and container status.'), tags: ['Next.js', 'FastAPI', 'WebSocket'], status: 'wip',  date: '2026.04' },
    { id: 'P-02', t: 'Vault Sync',        cat: 'bot', d: T('옵시디언 vault를 git push 하면 자동으로 빌드 → 사이트에 반영하는 봇.',          'Bot that picks up obsidian vault git pushes and rebuilds the site.'),               tags: ['Python', 'GitHub Actions'], status: 'live', date: '2026.02' },
    { id: 'P-03', t: 'Receipt OCR',       cat: 'web', d: T('영수증 사진 → 항목/금액 자동 추출 가계부. 부트캠프 자율 프로젝트의 후속.',         'Receipts → line items/amounts. Follow-up to my bootcamp capstone.'),                  tags: ['FastAPI', 'Postgres', 'OCR'], status: 'wip', date: '2025.09' },
    { id: 'P-04', t: 'Daily Standup Bot', cat: 'bot', d: T('어제 작성한 노트와 GitHub 활동을 묶어 아침에 메일로 보내는 봇.',                  'Bundles yesterday\'s notes + GitHub activity into a morning email.'),                  tags: ['Python', 'OpenAI'], status: 'live', date: '2025.07' },
    { id: 'P-05', t: 'algoboard',         cat: 'cli', d: T('백준/프로그래머스 풀이 자동 정리 → vault에 마크다운으로 저장.',                  'Auto-collects BOJ/programmers solves into vault as markdown.'),                       tags: ['Python', 'CLI'], status: 'live', date: '2025.04' },
    { id: 'P-06', t: 'Tide (bootcamp)',   cat: 'web', d: T('SSAFY 12기 자율 프로젝트. 팀 4명, 가계부 앱. 우수상.',                          'SSAFY self-directed capstone. Team of 4, budgeting app. Top-project award.'),         tags: ['Spring Boot', 'JPA', 'MySQL'], status: 'archived', date: '2025.05' },
  ];
  const cats = [
    { id: 'all', l: T('전체', 'All') },
    { id: 'web', l: 'Web' },
    { id: 'cli', l: 'CLI' },
    { id: 'bot', l: 'Bot' },
  ];
  const [cat, setCat] = React.useState('all');
  const list = cat === 'all' ? all : all.filter(p => p.cat === cat);

  const StatusTag = ({ s }) => {
    const map = { live: { c: 'var(--accent)', l: 'live' }, wip: { c: 'var(--info)', l: 'wip' }, archived: { c: 'var(--fg-3)', l: 'archived' } };
    return <span className="tag" style={s==='live' ? { color: 'var(--accent)', background: 'var(--accent-soft)', borderColor: 'var(--accent-line)' } : {}}><span className="tag-dot" style={{ background: map[s].c }} />{map[s].l}</span>;
  };
  return (
    <div>
      <header className="pad-x m-pad-h" style={{ padding: '56px 80px 32px', borderBottom: '1px solid var(--line-1)' }}>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12 }}>
          03 / Projects · {T('혼자 만든 것들', 'solo work')}
        </div>
        <h1 className="m-h1" style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.025em', margin: 0, fontWeight: 600 }}>Projects</h1>
      </header>
      <div className="pad-x" style={{ padding: '32px 80px 64px' }}>
        <div style={{ display: 'flex', gap: 8, marginBottom: 24, alignItems: 'center', flexWrap: 'wrap' }}>
          <span className="caps">filter</span>
          {cats.map(c => (
            <button key={c.id} onClick={() => setCat(c.id)} className={cat===c.id ? 'btn' : 'btn ghost'} style={{ padding: '4px 10px', fontSize: 11 }}>
              {c.l} <span style={{ color: 'var(--fg-3)', marginLeft: 4 }}>{c.id==='all' ? all.length : all.filter(p=>p.cat===c.id).length}</span>
            </button>
          ))}
          <span className="mono" style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--fg-3)' }}>sorted by date ↓</span>
        </div>
        <div className="m-stack" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          {list.map(p => (
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

/* =========================================================
   Sub-page: Products — case studies
   ========================================================= */
window.ProtoProducts = function ProtoProducts({ lang }) {
  const T = (ko, en) => lang === 'en' ? en : ko;
  const data = [
    { id: '01', t: 'Acme Admin Platform', co: 'Acme Corp.', role: 'Lead engineer', y: '2024 — present',
      d: T('12개의 분산된 어드민을 한 플랫폼으로 통합. 역할 기반 접근 제어와 감사 로그 도입.', 'Unified 12 scattered admins onto one platform. Introduced RBAC + audit logging.'),
      metric: [T('12개 어드민 통합', 'Unified 12 admins'), T('권한 변경 30s → 즉시', 'Permission change 30s → instant'), T('온콜 인입 −42%', 'On-call −42%')] },
    { id: '02', t: 'Foo Commerce Pay', co: 'Foo Studio', role: 'Backend engineer', y: '2022 — 2024',
      d: T('결제·정산 모듈 신규 구축. 멀티 PG와 정기 결제, 부분 환불 흐름.', 'Built payments & settlement from scratch. Multi-PG, recurring, partial refunds.'),
      metric: [T('트래픽 30× 스케일', 'Traffic 30× scale'), T('결제 실패율 −1.8pt', 'Payment failure −1.8pt'), T('p99 380ms → 140ms', 'p99 380ms → 140ms')] },
    { id: '03', t: 'Bar BI Studio', co: 'Bar Inc.', role: 'Full-stack', y: '2020 — 2022',
      d: T('내부 BI 대시보드 0→1. 디자인 시스템 v1과 컴포넌트 라이브러리 정립.', 'Internal BI dashboard 0→1. Established design system v1 and component library.'),
      metric: [T('200+ 차트 템플릿', '200+ chart templates'), T('DS v1 — 38개 컴포넌트', 'DS v1 — 38 components'), T('레포트 작성 −65%', 'Report time −65%')] },
  ];
  return (
    <div>
      <header style={{ padding: '56px 80px 32px', borderBottom: '1px solid var(--line-1)' }}>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12 }}>
          04 / Products · {T('회사에서 출시', 'shipped at companies')}
        </div>
        <h1 style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.025em', margin: 0, fontWeight: 600 }}>{T('제품', 'Products')}</h1>
      </header>
      <div style={{ padding: '32px 80px 64px' }}>
        {data.map(p => (
          <article key={p.id} style={{ display: 'grid', gridTemplateColumns: '60px 1fr 1.2fr', gap: 32, padding: '32px 0', borderTop: '1px solid var(--line-1)' }}>
            <div className="mono" style={{ fontSize: 12, color: 'var(--fg-3)' }}>{p.id}</div>
            <div>
              <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 8 }}>{p.y} · {p.co}</div>
              <h3 style={{ margin: '0 0 6px', fontSize: 26, letterSpacing: '-0.02em' }}>{p.t}</h3>
              <div style={{ fontSize: 13, color: 'var(--fg-2)', marginBottom: 12 }}>{T('역할', 'role')} · {p.role}</div>
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
              <button className="btn ghost" style={{ marginTop: 16, padding: '6px 10px', fontSize: 12 }}>{T('케이스 스터디 읽기', 'Read case study')} <span className="arrow">→</span></button>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
};
