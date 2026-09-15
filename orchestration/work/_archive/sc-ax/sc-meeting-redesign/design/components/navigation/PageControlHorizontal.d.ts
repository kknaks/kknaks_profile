import * as React from 'react';
export interface PageControlHorizontalProps {
  className?: string;
  style?: React.CSSProperties;
  dot6?: boolean;
  dot1?: boolean;
  dot7?: boolean;
  dot8?: boolean;
  dot5?: boolean;
  dot2?: boolean;
  dot4?: boolean;
  dot3?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon4?: React.ReactNode;
}
export declare const PageControlHorizontal: React.FC<PageControlHorizontalProps>;
export default PageControlHorizontal;
