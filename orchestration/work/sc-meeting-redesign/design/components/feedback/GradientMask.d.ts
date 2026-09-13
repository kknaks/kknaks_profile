import * as React from 'react';
export interface GradientMaskProps {
  className?: string;
  style?: React.CSSProperties;
  prop?: "null";
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const GradientMask: React.FC<GradientMaskProps>;
export default GradientMask;
