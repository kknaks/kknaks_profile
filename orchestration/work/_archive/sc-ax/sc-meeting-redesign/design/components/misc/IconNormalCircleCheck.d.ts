import * as React from 'react';
export interface IconNormalCircleCheckProps {
  className?: string;
  style?: React.CSSProperties;
  name?: "circleCheck" | "circleCheckFill";
  fill?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const IconNormalCircleCheck: React.FC<IconNormalCircleCheckProps>;
export default IconNormalCircleCheck;
