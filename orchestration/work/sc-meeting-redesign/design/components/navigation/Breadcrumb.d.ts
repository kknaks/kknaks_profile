import * as React from 'react';
export interface BreadcrumbProps {
  className?: string;
  style?: React.CSSProperties;
  prop?: string;
  prop2?: string;
  /** Text content; defaults to "이전 페이지". */
  text1?: string;
  /** Text content; defaults to "현재 페이지". */
  text2?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const Breadcrumb: React.FC<BreadcrumbProps>;
export default Breadcrumb;
