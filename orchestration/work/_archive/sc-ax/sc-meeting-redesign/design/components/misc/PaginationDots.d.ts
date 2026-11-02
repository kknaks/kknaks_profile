import * as React from 'react';
export interface PaginationDotsProps {
  className?: string;
  style?: React.CSSProperties;
  dot?: boolean;
  dot2?: boolean;
  dot3?: boolean;
  variant?: "normal" | "white";
  dot4?: boolean;
  dot5?: boolean;
  size?: "sm" | "md";
  dot6?: boolean;
  dot7?: boolean;
  dot8?: boolean;
  dot9?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon4?: React.ReactNode;
}
export declare const PaginationDots: React.FC<PaginationDotsProps>;
export default PaginationDots;
