/**
 * Sheet — A4 시트 wrapper (corner crosshairs + meta footer).
 * 원본: claude_design/.../print/components.jsx#Sheet
 */

import type { CSSProperties, ReactNode } from "react";

export type SheetOrientation = "portrait" | "landscape";

export interface SheetProps {
  orientation?: SheetOrientation;
  children?: ReactNode;
  meta?: string;
  pageNum?: number;
  totalPages?: number;
  style?: CSSProperties;
}

export function Sheet({
  orientation = "portrait",
  children,
  meta,
  pageNum,
  totalPages,
  style,
}: SheetProps) {
  return (
    <div className={`sheet ${orientation}`} style={style}>
      <span className="cross" style={{ top: 12, left: 12 }} />
      <span className="cross" style={{ top: 12, right: 12, transform: "scaleX(-1)" }} />
      <span className="cross" style={{ bottom: 12, left: 12, transform: "scaleY(-1)" }} />
      <span className="cross" style={{ bottom: 12, right: 12, transform: "scale(-1, -1)" }} />
      {children}
      {(meta || pageNum) && (
        <div className="sheet-meta">
          <span>{meta}</span>
          {pageNum && <span>{pageNum} / {totalPages}</span>}
        </div>
      )}
    </div>
  );
}
