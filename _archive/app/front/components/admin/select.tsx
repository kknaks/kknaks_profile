"use client";

import { useCallback, useEffect, useRef, useState } from "react";

/* 공용 셀렉트 — KDEV-WORK-018 P4.
 *
 * **네이티브 `<select>` 를 쓰지 않는다.** 옵션 목록 팝업은 OS 가 그리는 것이라
 * `background`·`color` 를 줘도 대부분 무시되고, macOS 에서는 `color-scheme: dark` 를
 * 걸어도 밝은 회색 목록이 그대로 뜬다. 어두운 화면에서 그 부분만 튄다.
 *
 * 팝업을 **`position: fixed` 로 띄운다.** 표가 `overflow-x: auto` 로 감싸여 있어
 * `absolute` 로 두면 셀 밖에서 잘린다. 트리거의 화면 좌표를 재서 그 아래에 붙인다.
 */

export type SelectOption = { value: string; label: string };

export function Select({
  value,
  options,
  onChange,
  placeholder = "선택",
  disabled = false,
  emptyLabel,
  width,
  ariaLabel,
}: {
  value: string;
  options: SelectOption[] | string[];
  onChange: (value: string) => void;
  placeholder?: string;
  disabled?: boolean;
  /** 빈 값을 고를 수 있게 한다. 문구를 주면 그 항목이 목록 맨 위에 붙는다. */
  emptyLabel?: string;
  width?: number | string;
  ariaLabel?: string;
}) {
  const [open, setOpen] = useState(false);
  const [rect, setRect] = useState<{ top: number; left: number; width: number } | null>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);

  const items: SelectOption[] = options.map((o) =>
    typeof o === "string" ? { value: o, label: o } : o,
  );
  const all = emptyLabel !== undefined ? [{ value: "", label: emptyLabel }, ...items] : items;
  const current = all.find((o) => o.value === value);

  const place = useCallback(() => {
    const el = triggerRef.current;
    if (!el) return;
    const r = el.getBoundingClientRect();
    setRect({ top: r.bottom + 4, left: r.left, width: r.width });
  }, []);

  useEffect(() => {
    if (!open) return;
    place();
    // 스크롤·리사이즈로 트리거가 움직이면 목록이 따라간다. 안 그러면 허공에 남는다.
    const sync = () => place();
    window.addEventListener("scroll", sync, true);
    window.addEventListener("resize", sync);
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => {
      window.removeEventListener("scroll", sync, true);
      window.removeEventListener("resize", sync);
      window.removeEventListener("keydown", onKey);
    };
  }, [open, place]);

  return (
    <>
      <button
        ref={triggerRef}
        type="button"
        disabled={disabled}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-label={ariaLabel}
        onClick={() => !disabled && setOpen((v) => !v)}
        style={{
          width: width ?? "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 8,
          padding: "7px 9px",
          fontSize: 12.5,
          background: "var(--bg-0)",
          border: `1px solid ${open ? "var(--accent)" : "var(--line-2)"}`,
          borderRadius: 5,
          color: current ? "var(--fg-0)" : "var(--fg-4)",
          cursor: disabled ? "default" : "pointer",
          opacity: disabled ? 0.5 : 1,
          textAlign: "left",
        }}
      >
        <span
          style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}
        >
          {current?.label ?? placeholder}
        </span>
        <Chevron open={open} />
      </button>

      {open && rect && (
        <>
          {/* 바깥 클릭으로 닫는다. 투명 오버레이가 그 역할을 한다 — document 리스너보다
              닫힘 시점이 분명하고, 안쪽 클릭이 새어 나가지 않는다. */}
          <div
            onClick={() => setOpen(false)}
            style={{ position: "fixed", inset: 0, zIndex: 40 }}
          />
          <ul
            role="listbox"
            style={{
              position: "fixed",
              top: rect.top,
              left: rect.left,
              minWidth: rect.width,
              maxHeight: 260,
              overflowY: "auto",
              margin: 0,
              padding: 4,
              listStyle: "none",
              background: "var(--bg-2)",
              border: "1px solid var(--line-3)",
              borderRadius: 6,
              boxShadow: "0 8px 24px rgba(0,0,0,0.5)",
              zIndex: 41,
            }}
          >
            {all.map((o) => {
              const selected = o.value === value;
              return (
                <li key={o.value || "__empty"} role="option" aria-selected={selected}>
                  <button
                    type="button"
                    onClick={() => {
                      onChange(o.value);
                      setOpen(false);
                    }}
                    style={{
                      width: "100%",
                      textAlign: "left",
                      padding: "7px 9px",
                      fontSize: 12.5,
                      background: selected ? "var(--bg-4)" : "transparent",
                      border: "none",
                      borderRadius: 4,
                      color: o.value ? "var(--fg-0)" : "var(--fg-4)",
                      cursor: "pointer",
                      display: "flex",
                      justifyContent: "space-between",
                      gap: 8,
                    }}
                    onMouseEnter={(e) => {
                      if (!selected) e.currentTarget.style.background = "var(--bg-3)";
                    }}
                    onMouseLeave={(e) => {
                      if (!selected) e.currentTarget.style.background = "transparent";
                    }}
                  >
                    <span>{o.label}</span>
                    {selected && <span style={{ color: "var(--accent)" }}>✓</span>}
                  </button>
                </li>
              );
            })}
          </ul>
        </>
      )}
    </>
  );
}

function Chevron({ open }: { open: boolean }) {
  return (
    <svg
      width="12"
      height="12"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      style={{
        flexShrink: 0,
        color: "var(--fg-3)",
        transform: open ? "rotate(180deg)" : undefined,
        transition: "transform 120ms",
      }}
    >
      <path d="m6 9 6 6 6-6" />
    </svg>
  );
}
