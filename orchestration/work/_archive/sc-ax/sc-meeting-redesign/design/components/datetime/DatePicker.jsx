import { Icon } from '../icon/Icon.jsx';

const MONTH_LABEL = (y, m) => `${y}년 ${m + 1}월`;
const HEADS = ['월', '화', '수', '목', '금', '토', '일'];

/* Monday-first matrix of Date-or-null for the given month. */
function monthMatrix(year, month) {
  const first = new Date(year, month, 1);
  const lead = (first.getDay() + 6) % 7;
  const days = new Date(year, month + 1, 0).getDate();
  const cells = [];
  for (let i = 0; i < lead; i += 1) cells.push(null);
  for (let d = 1; d <= days; d += 1) cells.push(new Date(year, month, d));
  while (cells.length % 7) cells.push(null);
  return cells;
}

const iso = (d) => [d.getFullYear(), String(d.getMonth() + 1).padStart(2, '0'), String(d.getDate()).padStart(2, '0')].join('-');

const headStyle = { display: 'flex', alignItems: 'center', gap: 4, padding: '6px 0' };
const labelStyle = { flex: '1 1 auto', fontFamily: 'var(--font-ui)', fontSize: 14, lineHeight: 1.467, letterSpacing: '0.010em', fontWeight: 600, color: 'var(--ax-ink)' };
const navBtnStyle = { display: 'flex', alignItems: 'center', justifyContent: 'center', width: 28, height: 28, flexShrink: 0, border: 0, borderRadius: 'var(--ax-r-xs)', background: 'transparent', color: 'var(--ax-ink-assistive)', cursor: 'pointer' };
const gridStyle = { display: 'grid', gridTemplateColumns: 'repeat(7, minmax(0, 1fr))', rowGap: 4, alignItems: 'center', justifyItems: 'center' };
const headCellStyle = { paddingBottom: 6, fontFamily: 'var(--font-ui)', fontSize: 12, lineHeight: 1.334, letterSpacing: '0.025em', color: 'var(--ax-ink-assistive)' };

function dayStyle({ selected, muted, today }) {
  return {
    position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center',
    width: 32, height: 32, flexShrink: 0, border: 0, borderRadius: 'var(--ax-r-sm)',
    background: selected ? 'var(--ax-accent-08)' : 'transparent',
    color: selected ? 'var(--ax-accent)' : muted ? 'var(--ax-ink-disable)' : 'var(--ax-ink-neutral)',
    fontFamily: 'var(--font-ui)', fontSize: 14, lineHeight: 1, fontWeight: selected || today ? 600 : 500,
    cursor: muted ? 'default' : 'pointer',
  };
}

/**
 * DatePicker — month grid, Monday-first. Controlled: pass `value` (YYYY-MM-DD)
 * and handle `onChange`. `marks` draws the accent dot under a date.
 */
export function DatePicker({ value, onChange, marks = [], min, max, style }) {
  const base = value ? new Date(value) : new Date();
  const [view, setView] = React.useState({ y: base.getFullYear(), m: base.getMonth() });
  const cells = monthMatrix(view.y, view.m);
  const todayIso = iso(new Date());
  const step = (delta) => setView((v) => {
    const d = new Date(v.y, v.m + delta, 1);
    return { y: d.getFullYear(), m: d.getMonth() };
  });
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8, minWidth: 280, ...style }}>
      <div style={headStyle}>
        <span style={labelStyle}>{MONTH_LABEL(view.y, view.m)}</span>
        <button type="button" aria-label="이전 달" style={navBtnStyle} onClick={() => step(-1)}><Icon name="chevron-left-small" size={20} /></button>
        <button type="button" aria-label="다음 달" style={navBtnStyle} onClick={() => step(1)}><Icon name="chevron-right-small" size={20} /></button>
      </div>
      <div style={gridStyle}>
        {HEADS.map((h) => <span key={h} style={headCellStyle}>{h}</span>)}
        {cells.map((d, i) => {
          if (!d) return <span key={`b${i}`} style={{ width: 32, height: 32 }} />;
          const key = iso(d);
          const outOfRange = (min && key < min) || (max && key > max);
          return (
            <button
              key={key}
              type="button"
              disabled={outOfRange}
              aria-pressed={key === value}
              aria-current={key === todayIso ? 'date' : undefined}
              style={dayStyle({ selected: key === value, muted: outOfRange, today: key === todayIso })}
              onClick={() => onChange(key)}
            >
              {d.getDate()}
              {marks.indexOf(key) > -1 ? (
                <span style={{ position: 'absolute', left: '50%', bottom: 3, transform: 'translateX(-50%)', width: 3, height: 3, borderRadius: 'var(--ax-r-pill)', background: 'currentColor' }} />
              ) : null}
            </button>
          );
        })}
      </div>
    </div>
  );
}
export default DatePicker;
