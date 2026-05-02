/* global React */
const { useState, useEffect, useRef } = React;

/* =========================================================
   Shared layout primitives — slot edition
   - 정적 UI 라벨(About/Career/Projects/Notes/Contents)은 박아둠
   - 사용자가 채울 텍스트만 {{slot}}으로 교체
   ========================================================= */

window.useI18n = function useI18n() {
  const [lang, setLang] = useState(() => {
    try { return localStorage.getItem('kknaks_lang') || 'ko'; } catch { return 'ko'; }
  });
  const set = (l) => { setLang(l); try { localStorage.setItem('kknaks_lang', l); } catch {} };
  return [lang, set];
};

/* Slot — visualizes an unfilled backend field.
   key: 'user.intro', 'career[].title' 등
   block: true 면 한 줄을 통째로 차지 */
window.Slot = function Slot({ k, block, hint }) {
  return (
    <span className={'slot' + (block ? ' block' : '')} data-slot={k} title={hint || k}>
      {'{{' + k + '}}'}
    </span>
  );
};

window.TopNav = function TopNav({ route, setRoute, lang, setLang }) {
  const items = [
    { id: 'about',    label: 'About'    },
    { id: 'career',   label: 'Career'   },
    { id: 'projects', label: 'Projects' },
    { id: 'notes',    label: 'Notes'    },
    { id: 'contents', label: 'Contents' },
  ];
  const [menuOpen, setMenuOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(() => typeof window !== 'undefined' && window.innerWidth <= 720);
  useEffect(() => {
    const onResize = () => setIsMobile(window.innerWidth <= 720);
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []);
  const go = (id) => { setRoute(id); setMenuOpen(false); };

  return (
    <div style={{
      position: 'sticky', top: 0, zIndex: 20,
      padding: '14px 32px', display: 'flex', alignItems: 'center', gap: 24,
      borderBottom: '1px solid var(--line-1)',
      background: 'rgba(10,11,13,0.75)', backdropFilter: 'blur(10px)',
    }} className="topnav-wrap pad-x">
      <button onClick={() => go('home')}
        className="mono"
        style={{ background: 'transparent', border: 'none', color: 'var(--fg-0)', fontSize: 13, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 8, padding: 0 }}>
        <span style={{ width: 8, height: 8, background: 'var(--accent)', borderRadius: 2 }} />
        kknaks<span style={{ color: 'var(--fg-3)' }}>.dev</span>
      </button>

      <nav className="m-hide" style={{ display: 'flex', gap: 4, marginLeft: 16 }}>
        {items.map((i, idx) => {
          const active = route === i.id;
          return (
            <button key={i.id} onClick={() => go(i.id)} style={{
              fontFamily: 'var(--font-mono)', fontSize: 12, padding: '6px 10px',
              background: 'transparent', border: 'none', cursor: 'pointer',
              color: active ? 'var(--fg-0)' : 'var(--fg-2)',
              borderBottom: active ? '1px solid var(--accent)' : '1px solid transparent',
              borderRadius: 0, transition: 'color 120ms',
            }}>
              <span style={{ color: 'var(--fg-3)' }}>0{idx+1} </span>{i.label}
            </button>
          );
        })}
      </nav>

      <div style={{ marginLeft: 'auto', display: 'flex', gap: 10, alignItems: 'center' }}>
        <span className="mono m-hide" style={{ fontSize: 11, color: 'var(--fg-3)', display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--accent)', boxShadow: '0 0 0 3px var(--accent-soft)' }} />
          online
        </span>
        <div style={{ display: 'flex', border: '1px solid var(--line-2)', borderRadius: 4, overflow: 'hidden' }}>
          {['ko','en'].map(l => (
            <button key={l} onClick={() => setLang(l)} style={{
              fontFamily: 'var(--font-mono)', fontSize: 11, padding: '4px 8px',
              background: lang===l ? 'var(--bg-3)' : 'transparent',
              color: lang===l ? 'var(--fg-0)' : 'var(--fg-3)',
              border: 'none', cursor: 'pointer',
            }}>{l.toUpperCase()}</button>
          ))}
        </div>
        {isMobile && (
        <button aria-label="menu" onClick={() => setMenuOpen(o => !o)} style={{
          display: 'flex', width: 36, height: 32,
          background: menuOpen ? 'var(--bg-3)' : 'transparent',
          border: '1px solid var(--line-2)', borderRadius: 4,
          cursor: 'pointer', padding: 0,
          flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 4,
        }}>
          <span style={{ display: 'block', width: 16, height: 1, background: 'var(--fg-0)', transform: menuOpen ? 'translateY(2.5px) rotate(45deg)' : 'none', transition: 'transform 160ms' }} />
          <span style={{ display: 'block', width: 16, height: 1, background: 'var(--fg-0)', opacity: menuOpen ? 0 : 1, transition: 'opacity 120ms' }} />
          <span style={{ display: 'block', width: 16, height: 1, background: 'var(--fg-0)', transform: menuOpen ? 'translateY(-2.5px) rotate(-45deg)' : 'none', transition: 'transform 160ms' }} />
        </button>
        )}
      </div>

      {menuOpen && isMobile && (
        <div style={{
          position: 'absolute', top: '100%', left: 0, right: 0,
          background: 'var(--bg-1)', borderBottom: '1px solid var(--line-1)',
          padding: '8px 0', boxShadow: 'var(--shadow-pop)',
        }}>
          {items.map((i, idx) => {
            const active = route === i.id;
            return (
              <button key={i.id} onClick={() => go(i.id)} style={{
                fontFamily: 'var(--font-mono)', fontSize: 14,
                padding: '14px 20px',
                background: active ? 'var(--bg-2)' : 'transparent',
                border: 'none', cursor: 'pointer',
                color: active ? 'var(--fg-0)' : 'var(--fg-1)',
                borderLeft: active ? '2px solid var(--accent)' : '2px solid transparent',
                textAlign: 'left',
                display: 'flex', alignItems: 'center', gap: 12,
              }}>
                <span style={{ color: 'var(--fg-3)' }}>0{idx+1}</span>
                <span>{i.label}</span>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};

window.PageFooter = function PageFooter({ lang }) {
  const Slot = window.Slot;
  return (
    <footer style={{ borderTop: '1px solid var(--line-1)', padding: '40px 32px 24px', marginTop: 80 }} className="pad-x">
      <div className="m-stack" style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr 1fr 1fr', gap: 32 }}>
        <div>
          <div className="mono" style={{ fontSize: 13, marginBottom: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{ width: 8, height: 8, background: 'var(--accent)', borderRadius: 2 }} />
            kknaks<span style={{ color: 'var(--fg-3)' }}>.dev</span>
          </div>
          <p style={{ margin: 0, fontSize: 13, color: 'var(--fg-2)', lineHeight: 1.6, maxWidth: 320 }}>
            <Slot k="site.footerTagline" />
          </p>
        </div>
        <div>
          <div className="caps" style={{ marginBottom: 10 }}>Contact</div>
          <a href="#" style={{ display: 'block', fontSize: 13, color: 'var(--fg-1)', padding: '4px 0', fontFamily: 'var(--font-mono)' }}><Slot k="user.email" /></a>
          <a href="#" style={{ display: 'block', fontSize: 13, color: 'var(--fg-1)', padding: '4px 0', fontFamily: 'var(--font-mono)' }}><Slot k="user.github" /></a>
          <a href="#" style={{ display: 'block', fontSize: 13, color: 'var(--fg-1)', padding: '4px 0', fontFamily: 'var(--font-mono)' }}><Slot k="user.linkedin" /></a>
        </div>
        <div>
          <div className="caps" style={{ marginBottom: 10 }}>Files</div>
          <a href="#" style={{ display: 'block', fontSize: 13, color: 'var(--fg-1)', padding: '4px 0' }}><Slot k="files.resumeLabel" /> ↓</a>
          <a href="#" style={{ display: 'block', fontSize: 13, color: 'var(--fg-1)', padding: '4px 0' }}><Slot k="files.portfolioLabel" /></a>
        </div>
        <div>
          <div className="caps" style={{ marginBottom: 10 }}>Now</div>
          <div className="mono" style={{ fontSize: 12, color: 'var(--fg-2)', lineHeight: 1.7 }}>
            <div><Slot k="site.location" /></div>
            <div><Slot k="site.version" /></div>
            <div style={{ color: 'var(--accent)' }}>● uptime <Slot k="site.uptime" /></div>
          </div>
        </div>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', borderTop: '1px solid var(--line-1)', marginTop: 32, paddingTop: 16 }} className="mono">
        <span style={{ fontSize: 11, color: 'var(--fg-3)' }}>© <Slot k="site.year" /> kknaks · all systems nominal</span>
        <span style={{ fontSize: 11, color: 'var(--fg-3)' }}>built with next.js + python</span>
      </div>
    </footer>
  );
};
