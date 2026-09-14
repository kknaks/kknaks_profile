import * as React from 'react';
export interface IconNormalLineHorizontalProps {
  className?: string;
  style?: React.CSSProperties;
  name?: "lineHorizontal" | "lineHorizontalThick";
  thick?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const IconNormalLineHorizontal: React.FC<IconNormalLineHorizontalProps>;
export default IconNormalLineHorizontal;
