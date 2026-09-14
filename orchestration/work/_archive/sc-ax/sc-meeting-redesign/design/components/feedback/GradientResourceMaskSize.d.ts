import * as React from 'react';
export interface GradientResourceMaskSizeProps {
  className?: string;
  style?: React.CSSProperties;
  size?: "xs" | "sm" | "md" | "lg" | "xl";
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const GradientResourceMaskSize: React.FC<GradientResourceMaskSizeProps>;
export default GradientResourceMaskSize;
