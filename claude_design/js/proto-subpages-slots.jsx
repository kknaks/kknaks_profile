/* global React */

/* =========================================================
   Sub-page: About — slot edition
   ========================================================= */
window.ProtoAbout = function ProtoAbout({ lang }) {
  const Slot = window.Slot;
  return (
    <div>
      <header className="pad-x m-pad-h" style={{ padding: '56px 80px 32px', borderBottom: '1px solid var(--line-1)' }}>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12 }}>
          01 / About · <Slot k="about.subtitle" />
        </div>
        <div className="about-id" style={{ display: 'flex', alignItems: 'center', gap: 24, flexWrap: 'wrap' }}>
          <div style={{
            width: 88, height: 88, borderRadius: '50%',
            background: 'var(--bg-2)', border: '1px solid var(--line-2)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexShrink: 0, overflow: 'hidden',
          }}>
            <span style={{
              fontFamily: 'var(--font-mono)', fontSize: 9, lineHeight: 1.3, color: 'var(--accent)',
              padding: '4px 6px', textAlign: 'center',
              background: 'rgba(106, 230, 168, 0.08)', border: '1px dashed var(--accent)', borderRadius: 4,
            }}>
              {`{{user.\navatarUrl}}`}
            </span>
          </div>
          <div style={{ minWidth: 0 }}>
            <h1 className="m-h1" style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.025em', margin: 0, fontWeight: 600 }}>
              <Slot k="user.handle" /> <span className="about-id-sub" style={{ color: 'var(--fg-3)', fontSize: 28, fontWeight: 400 }}>· <Slot k="user.name" /></span>
            </h1>
            <div className="mono" style={{ fontSize: 13, color: 'var(--fg-2)', marginTop: 8 }}>
              <Slot k="user.role" /> · <Slot k="user.years" /> · <Slot k="user.location" />
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

      <div className="pad-x m-stack" style={{ padding: '48px 80px', display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: 64 }}>
        <div>
          <p style={{ fontSize: 22, lineHeight: 1.55, letterSpacing: '-0.01em', color: 'var(--fg-0)', marginTop: 0, fontWeight: 500 }}>
            <Slot k="user.tagline" hint="한 줄짜리 캐치프레이즈" />
          </p>
          <p style={{ fontSize: 16, lineHeight: 1.7, color: 'var(--fg-1)', marginTop: 24 }}>
            <Slot k="user.intro" />
          </p>
          <p style={{ fontSize: 15, lineHeight: 1.7, color: 'var(--fg-1)' }}>
            <Slot k="user.intro2" hint="(선택) 두 번째 문단 — 비워둬도 됨" />
          </p>

          <div className="m-stack" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginTop: 36 }}>
            {[0, 1, 2, 3].map(i => (
              <div key={i} style={{ padding: 18, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6 }}>
                <div className="mono" style={{ fontSize: 11, color: 'var(--accent)', marginBottom: 8 }}>// <Slot k={`user.cards[${i}].title`} /></div>
                <div style={{ fontSize: 14, color: 'var(--fg-1)', lineHeight: 1.6 }}><Slot k={`user.cards[${i}].body`} /></div>
              </div>
            ))}
          </div>
        </div>

        <aside>
          <dl style={{ margin: 0, fontSize: 13 }}>
            {[
              ['name',     'user.name'],
              ['role',     'user.role'],
              ['location', 'user.location'],
              ['focus',    'user.focus'],
              ['email',    'user.email'],
              ['github',   'user.github'],
            ].map(([k, slotK]) => (
              <div key={k} style={{ display: 'grid', gridTemplateColumns: '90px 1fr', padding: '10px 0', borderTop: '1px solid var(--line-1)' }}>
                <dt className="mono" style={{ color: 'var(--fg-3)' }}>{k}</dt>
                <dd style={{ margin: 0, color: 'var(--fg-1)' }}><Slot k={slotK} /></dd>
              </div>
            ))}
          </dl>

          <div style={{ marginTop: 24, padding: 16, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6 }}>
            <div className="mono" style={{ fontSize: 11, color: 'var(--accent)', marginBottom: 8 }}>// stack</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              <Slot k="user.stack[]" hint="배열 — 각 원소가 <span class=tag>로 렌더됨" />
            </div>
          </div>
        </aside>
      </div>

      {/* 잔디 — 본문 4카드 아래 풀폭 */}
      <div className="pad-x" style={{ padding: '8px 80px 64px' }}>
        <ContribGrassSlot />
      </div>
    </div>
  );
};

/* =========================================================
   ContribGrass — slot edition
   53주×7일 격자 자체는 시각 데모, 데이터는 activity[] 슬롯.
   ========================================================= */
function ContribGrassSlot() {
  const Slot = window.Slot;
  const [selected, setSelected] = React.useState(null); // {wi, di} or null
  // 시각 데모용 결정론 mock — 격자 모양만 보여주기 위함
  const weeks = React.useMemo(() => {
    let s = 20260501;
    const rnd = () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
    const w = [];
    for (let wi = 0; wi < 53; wi++) {
      const wk = [];
      for (let di = 0; di < 7; di++) {
        const future = wi === 52 && di > 4;
        const r = rnd();
        const recencyBoost = wi / 53;
        const weekdayBoost = (di >= 1 && di <= 5) ? 1 : 0.4;
        const c = future ? 0 : Math.max(0, Math.round(r * 6 * weekdayBoost * (0.4 + recencyBoost) - 1.2));
        wk.push({ count: c, future });
      }
      w.push(wk);
    }
    return w;
  }, []);

  const levelColor = (count) => {
    if (count <= 0) return 'var(--bg-2)';
    if (count <= 2) return 'oklch(0.42 0.14 152 / 0.45)';
    if (count <= 4) return 'oklch(0.55 0.17 152 / 0.7)';
    if (count <= 7) return 'oklch(0.68 0.19 152 / 0.85)';
    return 'oklch(0.78 0.21 152)';
  };
  const GAP = 3;
  const dayLabels = ['', 'Mon', '', 'Wed', '', 'Fri', ''];

  return (
    <div className="grass-wrap" style={{ marginTop: 8, padding: 20, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6, display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) 260px', gap: 28, alignItems: 'start' }}>
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
            <Slot k="activity.totalCount" /> 회 · <Slot k="activity.since" /> ~ <Slot k="activity.until" />
          </div>
        </div>
        <div className="mono" style={{ fontSize: 10, color: 'var(--fg-3)', marginBottom: 12 }}>
          AI가 분류한 커밋 · 노트 · 학습 · 배포 활동 (격자 구조 데모, 데이터는 <span style={{ color: 'var(--accent)' }}>{'{{activity[]}}'}</span>)
        </div>

        <div className="grass-board-scroll" style={{ paddingBottom: 4 }}>
          <div className="grass-board-inner" style={{ width: '100%' }}>
            <div className="grass-cells-row" style={{ display: 'grid', gridTemplateColumns: `18px repeat(53, 1fr)`, columnGap: GAP, width: '100%' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: GAP }}>
                {dayLabels.map((dl, i) => (
                  <span key={i} className="mono" style={{ fontSize: 9, color: 'var(--fg-3)', minHeight: 11, display: 'flex', alignItems: 'center' }}>{dl}</span>
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
                        onClick={() => !cell.future && cell.count > 0 && setSelected({ wi, di })}
                        style={{
                          width: '100%', aspectRatio: '1 / 1',
                          background: cell.future ? 'transparent' : levelColor(cell.count),
                          border: cell.future ? 'none' : '1px solid oklch(1 0 0 / 0.04)',
                          borderRadius: 1.5,
                          cursor: cell.future || cell.count === 0 ? 'default' : 'pointer',
                          outline: isSel ? '1px solid var(--accent)' : 'none',
                          outlineOffset: 1,
                        }}
                      />
                    );
                  })}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 12, fontSize: 10 }}>
          <span className="mono" style={{ color: 'var(--fg-3)' }}>적음</span>
          {[0, 1, 3, 5, 9].map(c => (
            <span key={c} style={{ width: 11, height: 11, background: levelColor(c), border: '1px solid oklch(1 0 0 / 0.04)', borderRadius: 1.5 }} />
          ))}
          <span className="mono" style={{ color: 'var(--fg-3)' }}>많음</span>
        </div>
      </div>

      {/* 우측 — 클릭 전: 안내 / 클릭 후: 그날 상세 (슬롯) */}
      <div style={{ minWidth: 0, borderLeft: '1px solid var(--line-1)', paddingLeft: 24, alignSelf: 'stretch' }}>
        {selected ? (
          <div>
            <div className="mono" style={{ fontSize: 11, color: 'var(--accent)', marginBottom: 4 }}>
              // <Slot k={`activity[${selected.wi * 7 + selected.di}].kind`} hint="enum: commit|note|study|ship" />
            </div>
            <div className="mono" style={{ fontSize: 10, color: 'var(--fg-3)', marginBottom: 14 }}>
              <Slot k={`activity[${selected.wi * 7 + selected.di}].date`} /> · <Slot k={`activity[${selected.wi * 7 + selected.di}].count`} /> 회
            </div>
            <div style={{ fontSize: 14, color: 'var(--fg-0)', lineHeight: 1.55, fontWeight: 500, marginBottom: 12 }}>
              <Slot k={`activity[${selected.wi * 7 + selected.di}].summary`} hint="AI가 가공한 그날 한 줄 요약" />
            </div>
          </div>
        ) : (
          <div>
            <div className="mono" style={{ fontSize: 11, color: 'var(--accent)', marginBottom: 4 }}>// activity</div>
            <div className="mono" style={{ fontSize: 10, color: 'var(--fg-3)', marginBottom: 14 }}>
              <Slot k="activity.totalCount" /> 회 · 지난 1년
            </div>
            <p style={{ margin: 0, fontSize: 12, lineHeight: 1.65, color: 'var(--fg-2)' }}>
              잔디는 그날 AI가 가공한 활동 기록이에요. 셀을 클릭하면 그날 뭐를 했는지 볼 수 있어요.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   Sub-page: Career — slot edition
   ========================================================= */
window.ProtoCareer = function ProtoCareer({ lang }) {
  const Slot = window.Slot;
  // 페이지에선 4개 표시. 길이는 백엔드가 보내주는 배열 길이로.
  const N = 4;
  return (
    <div>
      <header className="pad-x m-pad-h" style={{ padding: '56px 80px 32px', borderBottom: '1px solid var(--line-1)' }}>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12 }}>
          02 / Career · <Slot k="career.subtitle" />
        </div>
        <h1 className="m-h1" style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.025em', margin: 0, fontWeight: 600 }}>Career</h1>
      </header>
      <div className="pad-x" style={{ padding: '48px 80px' }}>
        <div className="m-stack" style={{ display: 'grid', gridTemplateColumns: '180px 1fr', gap: 48 }}>
          <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.12em' }}>
            <div>// <Slot k="career.totalYears" /><br/>// <Slot k="career.totalRoles" /></div>
            <div style={{ marginTop: 16, color: 'var(--fg-2)' }}>
              focus<br/>
              <span style={{ color: 'var(--fg-0)' }}><Slot k="career.focus" hint="여러 줄. 줄바꿈은 \\n으로 (프론트가 split)" /></span>
            </div>
          </div>
          <div style={{ position: 'relative', paddingLeft: 28 }}>
            <div style={{ position: 'absolute', left: 5, top: 8, bottom: 8, width: 1, background: 'var(--line-2)' }} />
            {Array.from({ length: N }).map((_, i) => (
              <div key={i} style={{ position: 'relative', marginBottom: 36 }}>
                <span style={{ position: 'absolute', left: -28, top: 8, width: 11, height: 11, borderRadius: 2, background: 'var(--bg-0)', border: `1px solid ${i===0 ? 'var(--accent)' : 'var(--line-3)'}`, boxShadow: i===0 ? '0 0 0 3px var(--accent-soft)' : 'none' }} />
                <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 6 }}>
                  <Slot k={`career[${i}].period`} />
                  {i===0 && <span style={{ color: 'var(--accent)', marginLeft: 8 }}>● now</span>}
                </div>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginBottom: 6 }}>
                  <h3 style={{ margin: 0, fontSize: 20, letterSpacing: '-0.01em' }}><Slot k={`career[${i}].title`} /></h3>
                  <span style={{ color: 'var(--fg-3)' }}>·</span>
                  <span style={{ color: 'var(--fg-1)', fontSize: 16 }}><Slot k={`career[${i}].org`} /></span>
                  <span className="mono" style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--fg-3)' }}><Slot k={`career[${i}].location`} /></span>
                </div>
                <p style={{ margin: '0 0 10px', color: 'var(--fg-1)', fontSize: 14, lineHeight: 1.6, maxWidth: 640 }}>
                  <Slot k={`career[${i}].summary`} hint="2~3 문장 — bullet이 아니라 paragraph" />
                </p>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                  <Slot k={`career[${i}].stack[]`} hint="배열 — 각 원소가 tag로 렌더" />
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
   Sub-page: Projects — slot edition
   ========================================================= */
window.ProtoProjects = function ProtoProjects({ lang }) {
  const Slot = window.Slot;
  // 카테고리 — DB에서 받음. 'all'은 프론트가 합산.
  // categories[] = [{ id, label, count }, ...]
  const N_CATS = 4;  // all + 3 카테고리 (가변, 보통 3~5개)
  const [cat, setCat] = React.useState('all');
  const N = 6;

  return (
    <div>
      <header className="pad-x m-pad-h" style={{ padding: '56px 80px 32px', borderBottom: '1px solid var(--line-1)' }}>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12 }}>
          03 / Projects · <Slot k="projects.subtitle" />
        </div>
        <h1 className="m-h1" style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.025em', margin: 0, fontWeight: 600 }}>Projects</h1>
      </header>
      <div className="pad-x" style={{ padding: '32px 80px 64px' }}>
        <div style={{ display: 'flex', gap: 8, marginBottom: 24, alignItems: 'center', flexWrap: 'wrap' }}>
          <span className="caps">filter</span>
          <button onClick={() => setCat('all')} className={cat==='all' ? 'btn' : 'btn ghost'} style={{ padding: '4px 10px', fontSize: 11 }}>
            All <span style={{ color: 'var(--fg-3)', marginLeft: 4 }}><Slot k="projects.totalCount" /></span>
          </button>
          {Array.from({ length: 3 }).map((_, i) => (
            <button key={i} onClick={() => setCat(`cat${i}`)} className={cat===`cat${i}` ? 'btn' : 'btn ghost'} style={{ padding: '4px 10px', fontSize: 11 }}>
              <Slot k={`projects.categories[${i}].label`} hint="'Web' / 'CLI' / 'Bot' 같은 카테고리 라벨" />
              <span style={{ color: 'var(--fg-3)', marginLeft: 4 }}><Slot k={`projects.categories[${i}].count`} /></span>
            </button>
          ))}
          <span className="mono" style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--fg-3)' }}>sorted by date ↓</span>
        </div>
        <div className="m-stack" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          {Array.from({ length: N }).map((_, i) => (
            <article key={i} className="card" style={{ overflow: 'hidden' }}>
              <div className="placeholder-hatch" style={{ aspectRatio: '16/9' }}>
                [ projects[{i}].thumbnail · 1600×900 ]
              </div>
              <div style={{ padding: 20, borderTop: '1px solid var(--line-1)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}><Slot k={`projects[${i}].id`} /></span>
                  <span className="tag"><span className="tag-dot" style={{ background: 'var(--accent)' }} /><Slot k={`projects[${i}].status`} hint="'live' | 'wip' | 'archived'" /></span>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginLeft: 'auto' }}><Slot k={`projects[${i}].date`} /></span>
                </div>
                <h3 style={{ margin: '0 0 6px', fontSize: 18, letterSpacing: '-0.01em' }}><Slot k={`projects[${i}].title`} /></h3>
                <p style={{ margin: '0 0 12px', fontSize: 13, color: 'var(--fg-2)', lineHeight: 1.55 }}>
                  <Slot k={`projects[${i}].summary`} />
                </p>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                  <Slot k={`projects[${i}].stack[]`} />
                </div>
                <div style={{ marginTop: 10, display: 'flex', gap: 10 }}>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>repo: <Slot k={`projects[${i}].links.repo`} /></span>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>live: <Slot k={`projects[${i}].links.live`} /></span>
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </div>
  );
};
