/* global React */
const { useState: useS, useEffect: useE, useRef: useR, useMemo: useM } = React;

/* =========================================================
   Notes — slot edition
   - 그래프 노드/엣지 데이터: 백엔드가 미리 계산해서 내려줌
   - 노트 본문: 클릭 시 별도 fetch
   - 시각화는 mock 그래프(고정 18노드)로 유지 — 실제 데이터 형식은 SLOTS.md 참고
   ========================================================= */

// 그래프 시각화용 placeholder 데이터 — 실 운영 시 GET /api/notes/graph 로 받음
const PLACEHOLDER_NODES = [
  { id: 'n1',  group: 'ai',    x: 0.30, y: 0.30 },
  { id: 'n2',  group: 'ai',    x: 0.42, y: 0.22 },
  { id: 'n3',  group: 'ai',    x: 0.20, y: 0.42 },
  { id: 'n4',  group: 'ai',    x: 0.35, y: 0.45 },
  { id: 'n5',  group: 'py',    x: 0.65, y: 0.28 },
  { id: 'n6',  group: 'py',    x: 0.78, y: 0.32 },
  { id: 'n7',  group: 'py',    x: 0.70, y: 0.45 },
  { id: 'n8',  group: 'py',    x: 0.83, y: 0.50 },
  { id: 'n9',  group: 'infra', x: 0.55, y: 0.65 },
  { id: 'n10', group: 'infra', x: 0.68, y: 0.72 },
  { id: 'n11', group: 'infra', x: 0.45, y: 0.75 },
  { id: 'n12', group: 'infra', x: 0.60, y: 0.85 },
  { id: 'n13', group: 'cs',    x: 0.18, y: 0.62 },
  { id: 'n14', group: 'cs',    x: 0.28, y: 0.78 },
  { id: 'n15', group: 'cs',    x: 0.10, y: 0.78 },
  { id: 'n16', group: 'daily', x: 0.85, y: 0.78 },
  { id: 'n17', group: 'daily', x: 0.92, y: 0.65 },
  { id: 'n18', group: 'daily', x: 0.50, y: 0.50 }, // bridge
];
const PLACEHOLDER_EDGES = [
  ['n1','n2'],['n1','n3'],['n2','n4'],['n3','n4'],['n4','n18'],
  ['n5','n6'],['n5','n7'],['n6','n8'],['n7','n8'],['n7','n18'],
  ['n9','n10'],['n9','n11'],['n10','n12'],['n11','n12'],['n9','n18'],
  ['n13','n14'],['n13','n15'],['n14','n15'],['n13','n18'],
  ['n16','n17'],['n16','n18'],
];
const GROUP_COLOR = {
  ai:    'var(--accent)',
  py:    '#7aa2f7',
  infra: '#e0af68',
  cs:    '#bb9af7',
  daily: 'var(--fg-3)',
};

window.ProtoNotes = function ProtoNotes({ lang }) {
  const Slot = window.Slot;
  const [activeIdx, setActive] = useS(null);
  const [query, setQuery] = useS('');

  const wrapRef = useR();
  const [size, setSize] = useS({ w: 900, h: 620 });
  useE(() => {
    const measure = () => {
      if (!wrapRef.current) return;
      const r = wrapRef.current.getBoundingClientRect();
      setSize({ w: Math.max(360, Math.floor(r.width)), h: Math.max(420, Math.floor(r.height)) });
    };
    measure();
    const ro = new ResizeObserver(measure);
    if (wrapRef.current) ro.observe(wrapRef.current);
    return () => ro.disconnect();
  }, [activeIdx]);

  useE(() => {
    const h = (e) => { if (e.key === 'Escape') setActive(null); };
    window.addEventListener('keydown', h);
    return () => window.removeEventListener('keydown', h);
  }, []);

  return (
    <div>
      <header className="pad-x m-pad-h" style={{ padding: '56px 80px 32px', borderBottom: '1px solid var(--line-1)' }}>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12 }}>
          04 / Notes · <Slot k="notes.subtitle" />
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 16, flexWrap: 'wrap' }}>
          <h1 className="m-h1" style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.025em', margin: 0, fontWeight: 600 }}>
            Notes
          </h1>
          <span className="mono" style={{ fontSize: 12, color: 'var(--fg-3)' }}>
            <Slot k="notes.totalCount" /> notes · auto-synced
          </span>
          <span className="tag accent" style={{ marginLeft: 'auto' }}>
            <span className="tag-dot" style={{ background: 'var(--accent)' }} />vault → live
          </span>
        </div>

        <div style={{ marginTop: 24, display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'wrap' }}>
          <input value={query} onChange={e => setQuery(e.target.value)}
            placeholder="search — title or #tag"
            style={{
              padding: '8px 12px', fontFamily: 'var(--font-mono)', fontSize: 12,
              background: 'var(--bg-1)', border: '1px solid var(--line-2)', color: 'var(--fg-0)',
              borderRadius: 4, outline: 'none', minWidth: 280,
            }} />
          <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap' }}>
            {/* 클러스터 라벨은 DB에서 — clusters[] = [{ id, label }, ...].
                color는 프론트가 id로 매핑(GROUP_COLOR). */}
            {Array.from({ length: 5 }).map((_, i) => (
              <span key={i} className="mono" style={{ display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: 11, color: 'var(--fg-3)' }}>
                <span style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--fg-3)', outline: '1px dashed var(--accent)' }} />
                <Slot k={`notes.clusters[${i}].label`} hint="'AI' / 'Python' / 'Infra' 같은 클러스터 표시명" />
              </span>
            ))}
          </div>
          <span className="mono" style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--fg-3)' }}>
            click node → open note
          </span>
        </div>
      </header>

      <div className="pad-x m-hide" style={{ padding: '24px 80px 0' }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: activeIdx !== null ? '1.2fr 1fr' : '1fr',
          gap: 0,
          height: 640,
          border: '1px solid var(--line-1)',
          borderRadius: 6,
          background: 'var(--bg-0)',
          overflow: 'hidden',
          transition: 'grid-template-columns 320ms cubic-bezier(.2,.8,.2,1)',
        }}>
          <div ref={wrapRef} style={{ position: 'relative', overflow: 'hidden' }}>
            {/* Static placeholder graph — slot annotation overlaid */}
            <svg width={size.w} height={size.h} style={{ display: 'block' }}>
              {PLACEHOLDER_EDGES.map(([s,t], i) => {
                const a = PLACEHOLDER_NODES.find(n => n.id === s);
                const b = PLACEHOLDER_NODES.find(n => n.id === t);
                return <line key={i} x1={a.x*size.w} y1={a.y*size.h} x2={b.x*size.w} y2={b.y*size.h} stroke="var(--line-2)" strokeWidth={1} />;
              })}
              {PLACEHOLDER_NODES.map((n, i) => (
                <g key={n.id} style={{ cursor: 'pointer' }} onClick={() => setActive(i)}>
                  <circle cx={n.x*size.w} cy={n.y*size.h} r={activeIdx===i ? 8 : 5} fill={GROUP_COLOR[n.group]}
                    stroke={activeIdx===i ? 'var(--bg-0)' : 'transparent'} strokeWidth={2} />
                </g>
              ))}
            </svg>
            <div style={{
              position: 'absolute', top: 12, left: 12,
              background: 'var(--bg-1)', border: '1px solid var(--line-2)', borderRadius: 4,
              padding: '8px 10px', fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--fg-2)',
              lineHeight: 1.7, maxWidth: 260,
            }}>
              <div style={{ color: 'var(--accent)', marginBottom: 4 }}>// graph data</div>
              <div>nodes: <Slot k="notes.graph.nodes[]" hint="[{id, title, group, links[]}, ...]" /></div>
              <div style={{ marginTop: 4 }}>edges: <Slot k="notes.graph.edges[]" hint="[{source, target}, ...] — links에서 파생 가능" /></div>
            </div>
            <div className="mono" style={{
              position: 'absolute', bottom: 10, left: 12, fontSize: 10, color: 'var(--fg-3)',
              pointerEvents: 'none',
            }}>
              <Slot k="notes.totalCount" /> nodes · <Slot k="notes.edgeCount" /> edges
            </div>
          </div>

          {activeIdx !== null && (
            <div style={{ height: '100%', display: 'flex', flexDirection: 'column', background: 'var(--bg-1)', borderLeft: '1px solid var(--line-1)' }}>
              <div style={{ padding: '14px 24px', borderBottom: '1px solid var(--line-1)', display: 'flex', alignItems: 'center', gap: 12 }}>
                <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>
                  <Slot k="notes.detail.id" />.md
                </span>
                <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginLeft: 'auto' }}>
                  <Slot k="notes.detail.date" />
                </span>
                <button onClick={() => setActive(null)} className="mono" style={{
                  background: 'transparent', border: '1px solid var(--line-2)', color: 'var(--fg-2)',
                  padding: '3px 8px', borderRadius: 3, fontSize: 11, cursor: 'pointer',
                }}>esc ✕</button>
              </div>
              <div style={{ padding: '20px 28px 30px', overflowY: 'auto', flex: 1 }}>
                <h1 style={{ fontSize: 28, letterSpacing: '-0.02em', margin: '0 0 10px', fontWeight: 600 }}>
                  <Slot k="notes.detail.title" />
                </h1>
                <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 20 }}>
                  <Slot k="notes.detail.tags[]" hint="['#ai', '#rag', ...]" />
                </div>
                <div style={{ color: 'var(--fg-1)', fontSize: 13.5, lineHeight: 1.75 }}>
                  <Slot k="notes.detail.body" hint="마크다운 본문 — 코드/링크/리스트 포함. 프론트가 렌더" block />
                </div>
                <div style={{ marginTop: 24 }}>
                  <div className="caps" style={{ marginBottom: 8 }}>backlinks</div>
                  <div className="mono" style={{ fontSize: 12, color: 'var(--fg-2)' }}>
                    <Slot k="notes.detail.backlinks[]" hint="[{id, title}, ...] — 이 노트를 가리키는 다른 노트들" />
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Mobile list */}
      <div className="m-only pad-x" style={{ padding: '24px 20px 48px' }}>
        <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
          {[0,1,2,3,4,5].map(i => (
            <li key={i}
                style={{ padding: '14px 4px', borderTop: '1px solid var(--line-1)', cursor: 'pointer' }}>
              <div style={{ fontSize: 15, color: 'var(--fg-0)', marginBottom: 4 }}>
                <Slot k={`notes.recent[${i}].title`} />
              </div>
              <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                <span><Slot k={`notes.recent[${i}].path`} /></span>
                <span>· <Slot k={`notes.recent[${i}].date`} /></span>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
