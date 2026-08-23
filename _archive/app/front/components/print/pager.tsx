"use client";

/**
 * Pager — atom 배열을 받아 측정·그리디 패킹으로 자동 페이지 분할.
 *
 * 원본: claude_design/kknaks_profile_v2.0.0/print/pager.jsx (window 전역 IIFE)
 * 변경: TS + props 기반 (window 제거), Sheet 도 props 로 주입.
 *
 * 핵심 동작:
 *   1. MeasureNode 가 모든 atom + header(s) + footer 를 invisible 렌더 → useLayoutEffect 로 height 측정
 *   2. packPages 가 그리디로 페이지 안에 atom 들 채움 (available = sheetH - paddingY*2 - headerH - footerH)
 *   3. 실제 Sheet 들 렌더 (page 1 = full header, page 2+ = compact header)
 *
 * playwright headless chrome 에서도 useLayoutEffect 측정 동작 확인 — handoff §8.
 */

import {
  Fragment,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { Sheet, type SheetOrientation, type SheetProps } from "./sheet";

export interface PagerAtom {
  key: string;
  node: ReactNode;
}

export interface PagerProps {
  orientation?: SheetOrientation;
  contentWidth: number;     // sheet width in px (e.g. 794)
  contentHeight: number;    // sheet height in px (e.g. 1123)
  paddingX?: number;
  paddingY?: number;
  header?: ReactNode;        // page 1 only
  compactHeader?: ReactNode; // page 2+
  footer?: ReactNode;        // every page (in-flow, bottom)
  atoms: PagerAtom[];
  gap?: number;
  meta?: string;
  sheetProps?: Partial<SheetProps>;
  onReady?: () => void;      // 측정 완료 + 페이지 분할 끝나면 호출 (playwright 동기화)
}

interface Measurement {
  heights: number[];
  headerH: number;
  compactH: number;
  footerH: number;
}

function MeasureNode({
  width,
  atoms,
  header,
  compactHeader,
  footer,
  gap,
  onMeasured,
}: {
  width: number;
  atoms: PagerAtom[];
  header?: ReactNode;
  compactHeader?: ReactNode;
  footer?: ReactNode;
  gap: number;
  onMeasured: (m: Measurement) => void;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const compactRef = useRef<HTMLDivElement>(null);
  const footerRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (!ref.current) return;
    const atomEls = ref.current.querySelectorAll<HTMLElement>("[data-measure-atom]");
    const heights = Array.from(atomEls).map((el) =>
      Math.ceil(el.getBoundingClientRect().height),
    );
    const headerH = headerRef.current ? Math.ceil(headerRef.current.getBoundingClientRect().height) : 0;
    const compactH = compactRef.current ? Math.ceil(compactRef.current.getBoundingClientRect().height) : 0;
    const footerH = footerRef.current ? Math.ceil(footerRef.current.getBoundingClientRect().height) : 0;
    onMeasured({ heights, headerH, compactH, footerH });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [atoms, header, compactHeader, footer]);

  return (
    <div
      ref={ref}
      aria-hidden
      style={{
        position: "fixed",
        top: 0,
        left: -99999,
        width,
        visibility: "hidden",
        pointerEvents: "none",
      }}
    >
      {header && <div ref={headerRef}>{header}</div>}
      {compactHeader && <div ref={compactRef}>{compactHeader}</div>}
      <div style={{ display: "flex", flexDirection: "column", gap }}>
        {atoms.map((a, i) => (
          <div key={a.key ?? i} data-measure-atom>
            {a.node}
          </div>
        ))}
      </div>
      {footer && <div ref={footerRef}>{footer}</div>}
    </div>
  );
}

function packPages({
  heights,
  sheetInnerH,
  fullHeaderH,
  compactHeaderH,
  footerH,
  gap,
}: {
  heights: number[];
  sheetInnerH: number;
  fullHeaderH: number;
  compactHeaderH: number;
  footerH: number;
  gap: number;
}): number[][] {
  const pages: number[][] = [];
  let cur: number[] = [];
  let curH = 0;
  let pageIndex = 0;

  const headerForPage = (i: number) => (i === 0 ? fullHeaderH : compactHeaderH);
  const availableFor = (i: number) => sheetInnerH - headerForPage(i) - footerH;

  for (let i = 0; i < heights.length; i++) {
    const h = heights[i];
    const addH = cur.length === 0 ? h : curH + gap + h;
    if (addH <= availableFor(pageIndex)) {
      cur.push(i);
      curH = addH;
    } else {
      pages.push(cur);
      pageIndex++;
      cur = [i];
      curH = h;
      // 단일 atom 이 페이지보다 크면 그대로 박아 overflow 허용 (사용자가 수동 분할).
    }
  }
  if (cur.length) pages.push(cur);
  return pages;
}

export function Pager({
  orientation = "portrait",
  contentWidth,
  contentHeight,
  paddingX = 56,
  paddingY = 52,
  header,
  compactHeader,
  footer,
  atoms,
  gap = 14,
  meta,
  sheetProps,
  onReady,
}: PagerProps) {
  const [measurement, setMeasurement] = useState<Measurement | null>(null);

  const innerW = contentWidth - paddingX * 2;
  const innerH = contentHeight - paddingY * 2;

  const pages = useMemo(() => {
    if (!measurement) return null;
    return packPages({
      heights: measurement.heights,
      sheetInnerH: innerH,
      fullHeaderH: measurement.headerH,
      compactHeaderH: measurement.compactH || measurement.headerH,
      footerH: measurement.footerH,
      gap,
    });
  }, [measurement, innerH, gap]);

  useLayoutEffect(() => {
    if (pages && onReady) onReady();
  }, [pages, onReady]);

  return (
    <Fragment>
      <MeasureNode
        width={innerW}
        atoms={atoms}
        header={header}
        compactHeader={compactHeader}
        footer={footer}
        gap={gap}
        onMeasured={setMeasurement}
      />
      {pages &&
        pages.map((indices, pi) => (
          <Sheet
            key={pi}
            orientation={orientation}
            pageNum={pi + 1}
            totalPages={pages.length}
            meta={meta}
            {...sheetProps}
          >
            <div
              style={{
                padding: `${paddingY}px ${paddingX}px`,
                height: "100%",
                display: "flex",
                flexDirection: "column",
              }}
              data-pager-page={pi}
            >
              {pi === 0 ? header : compactHeader}
              <div style={{ display: "flex", flexDirection: "column", gap, marginTop: 0 }}>
                {indices.map((i) => (
                  <div key={atoms[i].key ?? i}>{atoms[i].node}</div>
                ))}
              </div>
              <div style={{ marginTop: "auto" }}>{footer}</div>
            </div>
          </Sheet>
        ))}
      {!pages && (
        <Sheet orientation={orientation} meta={meta} {...sheetProps}>
          <div
            style={{
              padding: `${paddingY}px ${paddingX}px`,
              color: "var(--fg-3)",
              fontFamily: "var(--font-mono)",
              fontSize: 11,
            }}
          >
            // measuring layout…
          </div>
        </Sheet>
      )}
    </Fragment>
  );
}
