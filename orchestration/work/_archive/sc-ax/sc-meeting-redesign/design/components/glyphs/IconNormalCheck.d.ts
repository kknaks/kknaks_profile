import * as React from 'react';
export interface IconNormalCheckProps {
  className?: string;
  style?: React.CSSProperties;
  name?: "check" | "checkThick";
  thick?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const IconNormalCheck: React.FC<IconNormalCheckProps>;
export default IconNormalCheck;
