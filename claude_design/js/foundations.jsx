/* global React */
const { useState, useEffect, useRef } = React;

/* =========================================================
   FOUNDATIONS
   ========================================================= */

const SwatchRow = ({ items }) => (
  <div style={{ display: 'grid', gridTemplateColumns: `repeat(${items.length}, 1fr)`, gap: 1, background: 'var(--line-1)', border: '1px solid var(--line-1)', borderRadius: 6, overflow: 'hidden' }}>
    {items.map((it, i) => (
      <div key={i} style={{ background: it.bg, padding: '20px 14px', minHeight: 84 }}>
        <div style={{ width: 40, height: 40, background: it.value, border: '1px solid var(--line-2)', borderRadius: 4, marginBottom: 12 }} />
        <div className="mono" style={{ fontSize: 11, color: 'var(--fg-1)' }}>{it.name}</div>
        <div className="mono" style={{ fontSize: 10, color: 'var(--fg-3)' }}>{it.value}</div>
      </div>
    ))}
  </div>
);

window.FoundationColors = function FoundationColors() {
  return (
    <div style={{ width: 1100, padding: 40, background: 'var(--bg-0)' }}>
      <div className="eyebrow" style={{ marginBottom: 8 }}>foundations / color</div>
      <h2 style={{ fontSize: 28, margin: '0 0 24px', letterSpacing: '-0.02em' }}>Color system</h2>

      <div className="caps" style={{ marginBottom: 8 }}>Surface</div>
      <SwatchRow items={[
        { name: 'bg-0', value: '#0a0b0d', bg: 'var(--bg-1)' },
        { name: 'bg-1', value: '#101216', bg: 'var(--bg-1)' },
        { name: 'bg-2', value: '#14171c', bg: 'var(--bg-1)' },
        { name: 'bg-3', value: '#1a1e24', bg: 'var(--bg-1)' },
        { name: 'bg-4', value: '#232830', bg: 'var(--bg-1)' },
      ]} />

      <div className="caps" style={{ marginTop: 24, marginBottom: 8 }}>Foreground</div>
      <SwatchRow items={[
        { name: 'fg-0', value: '#f4f5f7', bg: 'var(--bg-1)' },
        { name: 'fg-1', value: '#c8ccd3', bg: 'var(--bg-1)' },
        { name: 'fg-2', value: '#8b919b', bg: 'var(--bg-1)' },
        { name: 'fg-3', value: '#5a606b', bg: 'var(--bg-1)' },
        { name: 'fg-4', value: '#3a3f48', bg: 'var(--bg-1)' },
      ]} />

      <div className="caps" style={{ marginTop: 24, marginBottom: 8 }}>Accent &amp; status</div>
      <SwatchRow items={[
        { name: 'accent', value: 'oklch(0.78 0.14 145)', bg: 'var(--bg-1)' },
        { name: 'accent-soft', value: 'oklch(.78 .14 145 / .14)', bg: 'var(--bg-1)' },
        { name: 'info', value: 'oklch(.78 .10 230)', bg: 'var(--bg-1)' },
        { name: 'warn', value: 'oklch(.82 .13 80)', bg: 'var(--bg-1)' },
        { name: 'danger', value: 'oklch(.72 .16 25)', bg: 'var(--bg-1)' },
      ]} />

      <div style={{ marginTop: 28, padding: 20, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 8 }}>
        <div className="mono" style={{ color: 'var(--fg-2)', fontSize: 12, marginBottom: 8 }}>// principles</div>
        <ul style={{ margin: 0, paddingLeft: 18, color: 'var(--fg-1)', lineHeight: 1.7, fontSize: 14 }}>
          <li>다크 베이스 + 단일 액센트(터미널 그린). 채도 낮게.</li>
          <li>경계는 색이 아닌 1px 라인 + 미세한 표면 차이로.</li>
          <li>액센트는 인터랙션·강조에만. 본문은 fg-0 / fg-1.</li>
        </ul>
      </div>
    </div>
  );
};

window.FoundationType = function FoundationType() {
  const Row = ({ label, sample, style }) => (
    <div style={{ display: 'grid', gridTemplateColumns: '160px 1fr', alignItems: 'baseline', gap: 24, padding: '14px 0', borderTop: '1px solid var(--line-1)' }}>
      <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)' }}>{label}</div>
      <div style={style}>{sample}</div>
    </div>
  );
  return (
    <div style={{ width: 1100, padding: 40, background: 'var(--bg-0)' }}>
      <div className="eyebrow" style={{ marginBottom: 8 }}>foundations / typography</div>
      <h2 style={{ fontSize: 28, margin: '0 0 24px', letterSpacing: '-0.02em' }}>Typography</h2>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
        <div>
          <div className="caps" style={{ marginBottom: 4 }}>Sans · Inter / Pretendard</div>
          <Row label="display / 56" style={{ fontSize: 56, lineHeight: 1.05, letterSpacing: '-0.02em', fontWeight: 600 }} sample="안녕하세요" />
          <Row label="h1 / 40" style={{ fontSize: 40, lineHeight: 1.1, letterSpacing: '-0.02em', fontWeight: 600 }} sample="개발자 KKnaks" />
          <Row label="h2 / 28" style={{ fontSize: 28, lineHeight: 1.2, fontWeight: 600 }} sample="이력 · Career" />
          <Row label="h3 / 20" style={{ fontSize: 20, lineHeight: 1.3, fontWeight: 500 }} sample="프로젝트 제목" />
          <Row label="body / 15" style={{ fontSize: 15, lineHeight: 1.55 }} sample="홈서버 위에 Python 백엔드를 두고, Next.js로 정적 프론트를 띄웁니다." />
          <Row label="small / 13" style={{ fontSize: 13, color: 'var(--fg-1)' }} sample="작은 메타 정보, 캡션, 라벨" />
        </div>
        <div>
          <div className="caps" style={{ marginBottom: 4 }}>Mono · JetBrains Mono</div>
          <Row label="mono / 12" style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--fg-1)', letterSpacing: '0.02em' }} sample="$ ssh kknaks@homelab" />
          <Row label="mono caps" style={{ fontFamily: 'var(--font-mono)', fontSize: 11, textTransform: 'uppercase', letterSpacing: '0.12em', color: 'var(--fg-2)' }} sample="// section · 03" />
          <Row label="tag" style={{ fontFamily: 'var(--font-mono)', fontSize: 12 }} sample={
            <span style={{ display: 'inline-flex', gap: 6 }}>
              <span className="tag">Next.js</span>
              <span className="tag">Python</span>
              <span className="tag accent">Production</span>
            </span>
          } />
          <Row label="hint" style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--fg-3)' }} sample="// kknaks.dev v0.1.0" />
          <div className="caps" style={{ marginTop: 24, marginBottom: 4 }}>Pairing rule</div>
          <ul style={{ margin: 0, paddingLeft: 18, color: 'var(--fg-1)', lineHeight: 1.7, fontSize: 14 }}>
            <li>Sans = 본문/제목</li>
            <li>Mono = 라벨/태그/메타/코드</li>
            <li>한 화면에 두 패밀리만</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

window.FoundationSpacing = function FoundationSpacing() {
  const tokens = [
    { name: 's-1', v: 4 }, { name: 's-2', v: 8 }, { name: 's-3', v: 12 },
    { name: 's-4', v: 16 }, { name: 's-5', v: 20 }, { name: 's-6', v: 24 },
    { name: 's-8', v: 32 }, { name: 's-10', v: 40 }, { name: 's-12', v: 48 },
  ];
  return (
    <div style={{ width: 1100, padding: 40, background: 'var(--bg-0)' }}>
      <div className="eyebrow" style={{ marginBottom: 8 }}>foundations / spacing &amp; radii</div>
      <h2 style={{ fontSize: 28, margin: '0 0 24px', letterSpacing: '-0.02em' }}>Spacing &amp; radii</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12 }}>
        {tokens.map(t => (
          <div key={t.name} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: 12, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: 6 }}>
            <div style={{ width: t.v, height: t.v, background: 'var(--accent)', borderRadius: 2 }} />
            <div className="mono" style={{ fontSize: 12, color: 'var(--fg-1)' }}>{t.name}</div>
            <div className="mono" style={{ fontSize: 11, color: 'var(--fg-3)', marginLeft: 'auto' }}>{t.v}px</div>
          </div>
        ))}
      </div>

      <div className="caps" style={{ marginTop: 28, marginBottom: 8 }}>Radii</div>
      <div style={{ display: 'flex', gap: 16 }}>
        {[{n:'r-1',v:2},{n:'r-2',v:4},{n:'r-3',v:6},{n:'r-4',v:10}].map(r => (
          <div key={r.n} style={{ flex: 1, padding: 16, background: 'var(--bg-1)', border: '1px solid var(--line-1)', borderRadius: r.v, textAlign: 'center' }}>
            <div className="mono" style={{ fontSize: 11, color: 'var(--fg-1)' }}>{r.n}</div>
            <div className="mono" style={{ fontSize: 10, color: 'var(--fg-3)' }}>{r.v}px</div>
          </div>
        ))}
      </div>
    </div>
  );
};
