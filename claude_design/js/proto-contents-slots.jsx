/* global React */
const { useState: _cuS, useEffect: _cuE } = React;

/* =========================================================
   Contents — slot edition
   - List: contents[i].* (collection)
   - Detail: contents.detail.* (single record fetched by id)
   - 단, list view에 N=5 카드를 보여주려면 contents[0]~[4]를 미리 받음
   ========================================================= */

const N_CONTENTS = 5;

function ContentsList({ lang, setRoute }) {
  const Slot = window.Slot;

  return (
    <div>
      <header className="pad-x m-pad-h" style={{ padding: '56px 80px 32px', borderBottom: '1px solid var(--line-1)' }}>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12 }}>
          05 / Contents · <Slot k="contents.subtitle" />
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 16, flexWrap: 'wrap' }}>
          <h1 className="m-h1" style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.025em', margin: 0, fontWeight: 600 }}>Contents</h1>
          <span className="mono" style={{ fontSize: 12, color: 'var(--fg-3)' }}>// study log · video + 교안</span>
        </div>
        <p style={{ margin: '20px 0 0', fontSize: 15, color: 'var(--fg-1)', maxWidth: 640, lineHeight: 1.6 }}>
          <Slot k="contents.intro" hint="페이지 상단 1~2 문장 설명" />
        </p>
      </header>

      {/* Latest — large card */}
      <section className="pad-x" style={{ padding: '48px 80px 24px' }}>
        <div className="caps" style={{ marginBottom: 16 }}>latest</div>
        <article className="card m-stack"
          style={{ overflow: 'hidden', cursor: 'pointer', display: 'grid', gridTemplateColumns: '1.15fr 1fr' }}
          onClick={() => setRoute('contents/_latest')}
        >
          <YouTubeFramePlaceholder idKey="contents[0].youtubeId" titleKey="contents[0].title" />
          <div style={{ padding: '28px 32px', borderLeft: '1px solid var(--line-1)', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
              <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}><Slot k="contents[0].id" /></span>
              <span className="tag" style={{ color: 'var(--accent)', background: 'var(--accent-soft)', borderColor: 'var(--accent-line)' }}>
                <span className="tag-dot" style={{ background: 'var(--accent)' }} /><Slot k="contents[0].day" />
              </span>
              <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginLeft: 'auto' }}><Slot k="contents[0].date" /></span>
            </div>
            <h2 style={{ margin: '0 0 12px', fontSize: 26, lineHeight: 1.25, letterSpacing: '-0.015em', fontWeight: 600 }}>
              <Slot k="contents[0].title" />
            </h2>
            <p style={{ margin: '0 0 18px', color: 'var(--fg-1)', fontSize: 14, lineHeight: 1.65 }}>
              <Slot k="contents[0].summary" />
            </p>
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 18 }}>
              <Slot k="contents[0].tags[]" hint="['#AI', '#VectorDB', ...]" />
            </div>
            <div style={{ marginTop: 'auto', display: 'flex', alignItems: 'center', gap: 12 }}>
              <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>▶ <Slot k="contents[0].duration" /></span>
              <span className="mono" style={{ fontSize: 11, color: 'var(--accent)', marginLeft: 'auto' }}>open sheet →</span>
            </div>
          </div>
        </article>
      </section>

      {/* Rest — list */}
      <section className="pad-x" style={{ padding: '24px 80px 64px' }}>
        <div className="caps" style={{ marginBottom: 16 }}>previous</div>
        <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
          {[1,2,3,4].map(i => (
            <li key={i}
              style={{
                display: 'grid',
                gridTemplateColumns: '76px 88px 1fr 200px 80px',
                gap: 20,
                padding: '18px 12px',
                borderTop: '1px solid var(--line-1)',
                alignItems: 'center',
                cursor: 'pointer',
                transition: 'background 120ms',
              }}
            >
              <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}><Slot k={`contents[${i}].id`} /></span>
              <span className="mono" style={{ fontSize: 11, color: 'var(--fg-2)' }}><Slot k={`contents[${i}].day`} /></span>
              <div>
                <div style={{ fontSize: 15, color: 'var(--fg-0)', marginBottom: 4 }}><Slot k={`contents[${i}].title`} /></div>
                <div style={{ fontSize: 13, color: 'var(--fg-2)', lineHeight: 1.5 }}><Slot k={`contents[${i}].summary`} /></div>
              </div>
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                <Slot k={`contents[${i}].tags[]`} />
              </div>
              <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textAlign: 'right' }}><Slot k={`contents[${i}].date`} /></span>
            </li>
          ))}
        </ul>
        <div style={{ marginTop: 24, padding: '12px 0', borderTop: '1px solid var(--line-1)' }}>
          <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>
            // pagination — total <Slot k="contents.totalCount" /> episodes
          </span>
        </div>
      </section>
    </div>
  );
}

function ContentsDetail({ lang, id, setRoute }) {
  const Slot = window.Slot;

  return (
    <div>
      <header className="pad-x m-pad-h" style={{ padding: '40px 80px 32px', borderBottom: '1px solid var(--line-1)' }}>
        <button className="mono" onClick={() => setRoute('contents')}
          style={{ background: 'transparent', border: 'none', color: 'var(--fg-3)', fontSize: 12, cursor: 'pointer', padding: 0, marginBottom: 20 }}>
          ← all contents
        </button>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 12, display: 'flex', gap: 12 }}>
          <span><Slot k="contents.detail.id" /></span>
          <span style={{ color: 'var(--accent)' }}>● <Slot k="contents.detail.day" /></span>
          <span><Slot k="contents.detail.date" /></span>
        </div>
        <h1 className="m-h1" style={{ fontSize: 40, lineHeight: 1.15, letterSpacing: '-0.02em', margin: 0, fontWeight: 600, maxWidth: 900 }}>
          <Slot k="contents.detail.title" />
        </h1>
        <p style={{ margin: '16px 0 0', color: 'var(--fg-1)', fontSize: 15, lineHeight: 1.65, maxWidth: 760 }}>
          <Slot k="contents.detail.summary" />
        </p>
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 20 }}>
          <Slot k="contents.detail.tags[]" />
        </div>
      </header>

      <div className="pad-x m-stack" style={{ padding: '48px 80px 24px', display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: 56, alignItems: 'start' }}>
        <div>
          <SectionHeader idx="01" label="video" title="Video" />
          <YouTubeFramePlaceholder idKey="contents.detail.youtubeId" titleKey="contents.detail.title" />
          <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginTop: 10, display: 'flex', justifyContent: 'space-between' }}>
            <span>▶ <Slot k="contents.detail.duration" /></span>
            <span>youtu.be/<Slot k="contents.detail.youtubeId" /></span>
          </div>
        </div>

        <aside>
          <SectionHeader idx="02" label="concept" title="Concept" />
          <div className="card" style={{ padding: 24 }}>
            <ul style={{ margin: 0, padding: 0, listStyle: 'none' }}>
              {[0,1,2,3].map(i => (
                <li key={i} style={{ display: 'grid', gridTemplateColumns: '24px 1fr', gap: 8, padding: '10px 0', borderTop: i === 0 ? 'none' : '1px solid var(--line-1)' }}>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', paddingTop: 3 }}>{String(i+1).padStart(2,'0')}</span>
                  <span style={{ fontSize: 14, lineHeight: 1.6, color: 'var(--fg-1)' }}>
                    <Slot k={`contents.detail.concept[${i}]`} hint="개념 설명 한 줄. 배열 길이는 가변" />
                  </span>
                </li>
              ))}
            </ul>
            <div className="mono" style={{ marginTop: 12, paddingTop: 10, borderTop: '1px solid var(--line-1)', fontSize: 11, color: 'var(--fg-3)' }}>
              // length: <Slot k="contents.detail.concept[]" hint="배열 — 위 4개 슬롯과 같은 데이터, 가변 길이용" />
            </div>
          </div>
          <div style={{ marginTop: 16, padding: '16px 20px', border: '1px solid var(--line-1)', borderRadius: 6, background: 'var(--bg-1)' }}>
            <div className="caps" style={{ marginBottom: 8 }}>speaker</div>
            <div className="mono" style={{ fontSize: 13, color: 'var(--fg-0)' }}><Slot k="contents.detail.speaker" /></div>
          </div>
        </aside>
      </div>

      <section className="pad-x" style={{ padding: '32px 80px 32px' }}>
        <SectionHeader idx="03" label="applied" title="Applied example" />
        <ol style={{ margin: 0, padding: 0, listStyle: 'none' }}>
          {[0,1,2].map(i => (
            <li key={i} style={{ display: 'grid', gridTemplateColumns: '60px 1fr', gap: 20, padding: '18px 0', borderTop: '1px solid var(--line-1)' }}>
              <span className="mono" style={{ fontSize: 11, color: 'var(--accent)', paddingTop: 4 }}>03.{String(i+1).padStart(2,'0')}</span>
              <span style={{ fontSize: 16, lineHeight: 1.65, color: 'var(--fg-0)', maxWidth: 880 }}>
                <Slot k={`contents.detail.example[${i}]`} hint="적용 예시 한 줄. 배열 가변" />
              </span>
            </li>
          ))}
          <li style={{ borderTop: '1px solid var(--line-1)', padding: '12px 0' }}>
            <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>
              // length: <Slot k="contents.detail.example[]" hint="배열 — 위 슬롯과 동일 데이터, 가변 길이용" />
            </span>
          </li>
        </ol>
      </section>

      <nav className="pad-x m-stack" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, padding: '32px 80px 64px', borderTop: '1px solid var(--line-1)' }}>
        <button className="card" style={{ padding: '20px 24px', textAlign: 'left', cursor: 'pointer', background: 'var(--bg-1)', border: '1px solid var(--line-1)' }}>
          <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 6 }}>← newer</div>
          <div style={{ fontSize: 14, color: 'var(--fg-0)' }}><Slot k="contents.detail.newer.title" /></div>
        </button>
        <button className="card" style={{ padding: '20px 24px', textAlign: 'right', cursor: 'pointer', background: 'var(--bg-1)', border: '1px solid var(--line-1)' }}>
          <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginBottom: 6 }}>older →</div>
          <div style={{ fontSize: 14, color: 'var(--fg-0)' }}><Slot k="contents.detail.older.title" /></div>
        </button>
      </nav>
    </div>
  );
}

function SectionHeader({ idx, label, title }) {
  return (
    <div style={{ marginBottom: 18, display: 'flex', alignItems: 'baseline', gap: 12 }}>
      <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>{idx}</span>
      <h2 style={{ margin: 0, fontSize: 22, letterSpacing: '-0.015em', fontWeight: 600 }}>{title}</h2>
      <span className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>· {label}</span>
    </div>
  );
}

function YouTubeFramePlaceholder({ idKey, titleKey }) {
  const Slot = window.Slot;
  return (
    <div style={{ position: 'relative', aspectRatio: '16/9', background: '#000', overflow: 'hidden' }}>
      <div className="placeholder-hatch" style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 12 }}>
        <div style={{
          width: 64, height: 64, borderRadius: '50%',
          background: 'var(--accent)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          boxShadow: '0 0 0 6px rgba(0,0,0,0.4)',
        }}>
          <div style={{
            width: 0, height: 0,
            borderLeft: '18px solid var(--accent-ink)',
            borderTop: '12px solid transparent',
            borderBottom: '12px solid transparent',
            marginLeft: 5,
          }} />
        </div>
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-2)' }}>
          youtu.be/<Slot k={idKey} />
        </div>
      </div>
    </div>
  );
}

window.ProtoContents = function ProtoContents({ lang, subRoute, setRoute }) {
  if (subRoute) {
    return <ContentsDetail lang={lang} id={subRoute} setRoute={setRoute} />;
  }
  return <ContentsList lang={lang} setRoute={setRoute} />;
};
