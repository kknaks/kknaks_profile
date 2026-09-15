import { Icon } from '../icon/Icon.jsx';
import { DatePicker } from './DatePicker.jsx';

const SIZES = { sm: 32, md: 39, lg: 47 };

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
const popStyle = { position: 'absolute', right: 0, top: 'calc(100% + 4px)', zIndex: 30, padding: 12, border: '1px solid var(--ax-line)', borderRadius: 'var(--ax-r-sm)', background: 'var(--ax-surface)', boxShadow: 'var(--ax-shadow-raised)' };

/**
 * DateField — typed `YYYY-MM-DD` entry plus a DatePicker popover on the
 * calendar button. Closes on outside click and Escape.
 */
export function DateField({ value = '', onChange, size = 'md', placeholder = 'YYYY-MM-DD', invalid, marks, min, max, ariaLabel = '날짜', style }) {
  const [open, setOpen] = React.useState(false);
  const ref = React.useRef(null);
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
          onChange={(e) => onChange(e.target.value)}
        />
        <button type="button" style={trailingStyle} aria-label="날짜 선택" aria-expanded={open} onClick={() => setOpen((v) => !v)}>
          <Icon name="calendar" size={20} />
        </button>
      </div>
      {open ? (
        <div style={popStyle}>
          <DatePicker value={value} marks={marks} min={min} max={max} onChange={(v) => { onChange(v); setOpen(false); }} />
        </div>
      ) : null}
    </div>
  );
}
export default DateField;
