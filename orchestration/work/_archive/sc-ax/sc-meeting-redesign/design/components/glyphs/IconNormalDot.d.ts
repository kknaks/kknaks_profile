import * as React from 'react';
export interface IconNormalDotProps {
  className?: string;
  style?: React.CSSProperties;
  name?: "dot";
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const IconNormalDot: React.FC<IconNormalDotProps>;
export default IconNormalDot;
