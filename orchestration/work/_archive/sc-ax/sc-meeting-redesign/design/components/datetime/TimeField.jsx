import { Icon } from '../icon/Icon.jsx';

const SIZES = { sm: 32, md: 39, lg: 47 };
const pad = (n) => String(n).padStart(2, '0');

/* Options every `step` minutes across the working range. */
function slots(step, from, to) {
  const out = [];
  for (let m = from; m <= to; m += step) out.push(`${pad(Math.floor(m / 60))}:${pad(m % 60)}`);
  return out;
}

function shellStyle(size, open, invalid) {
  return {
    display: 'flex', alignItems: 'center', gap: 8, minHeight: SIZES[size] + 9,
    padding: '0 12px 0 16px', boxSizing: 'border-box',
    border: `1px solid ${invalid ? 'var(--ax-danger)' : open ? 'var(--ax-accent)' : 'var(--ax-line)'}`,
    borderRadius: 'var(--ax-r-sm)', background: 'var(--ax-surface)',
    boxShadow: open ? '0 0 0 3px var(--ax-accent-20)' : 'none',
  };
}
const inputStyle = { flex: '1 1 auto', minWidth: 0, border: 0, outline: 0, background: 'transparent', color: 'var(--ax-ink)', fontFamily: 'var(--font-ui)', fontSize: 14, lineHeight: 1.467, letterSpacing: '0.010em' };
const trailingStyle = { display: 'flex', alignItems: 'center', justifyContent: 'center', width: 28, height: 28, flexShrink: 0, border: 0, borderRadius: 'var(--ax-r-xs)', background: 'transparent', color: 'var(--ax-ink-assistive)', cursor: 'pointer' };
const listStyle = { position: 'absolute', left: 0, right: 0, top: 'calc(100% + 4px)', zIndex: 30, maxHeight: 220, margin: 0, padding: 4, listStyle: 'none', overflowY: 'auto', border: '1px solid var(--ax-line)', borderRadius: 'var(--ax-r-sm)', background: 'var(--ax-surface)', boxShadow: 'var(--ax-shadow-raised)' };

function optionStyle(selected) {
  return {
    display: 'flex', alignItems: 'center', gap: 8, width: '100%', padding: '8px 12px',
    border: 0, borderRadius: 'var(--ax-r-xs)', background: 'transparent',
    color: selected ? 'var(--ax-accent)' : 'var(--ax-ink-neutral)',
    fontFamily: 'var(--font-ui)', fontSize: 14, lineHeight: 1.467, fontWeight: selected ? 600 : 400,
    textAlign: 'left', cursor: 'pointer',
  };
}

/**
 * TimeField — `HH:MM` entry with a slot list. `step` / `from` / `to` are
 * minutes, so a working-hours field is `from={540} to={1080}` (09:00–18:00).
 */
export function TimeField({ value = '', onChange, size = 'md', step = 30, from = 0, to = 1410, placeholder = 'HH:MM', invalid, ariaLabel = '시간', style }) {
  const [open, setOpen] = React.useState(false);
  const ref = React.useRef(null);
  const options = slots(step, from, to);
  React.useEffect(() => {
    if (!open) return undefined;
    const onDown = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
    const onKey = (e) => { if (e.key === 'Escape') setOpen(false); };
    document.addEventListener('mousedown', onDown);
    document.addEventListener('keydown', onKey);
    return () => { document.removeEventListener('mousedown', onDown); document.removeEventListener('keydown', onKey); };
  }, [open]);
  return (
    <div ref={ref} style={{ position: 'relative', ...style }}>
      <div style={shellStyle(size, open, invalid)}>
        <input
          style={inputStyle}
          value={value}
          placeholder={placeholder}
          aria-label={ariaLabel}
          inputMode="numeric"
          role="combobox"
          aria-expanded={open}
          onFocus={() => setOpen(true)}
          onChange={(e) => onChange(e.target.value)}
        />
        <button type="button" style={trailingStyle} aria-label="시간 선택" aria-expanded={open} onClick={() => setOpen((v) => !v)}>
          <Icon name="clock" size={20} />
        </button>
      </div>
      {open ? (
        <ul style={listStyle} role="listbox">
          {options.map((o) => (
            <li key={o}>
              <button type="button" role="option" aria-selected={o === value} style={optionStyle(o === value)} onMouseDown={() => { onChange(o); setOpen(false); }}>
                {o}
                {o === value ? <Icon name="check" size={16} style={{ marginLeft: 'auto' }} /> : null}
              </button>
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}
export default TimeField;
