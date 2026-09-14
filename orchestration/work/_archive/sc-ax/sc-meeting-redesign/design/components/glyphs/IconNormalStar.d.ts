import * as React from 'react';
export interface IconNormalStarProps {
  className?: string;
  style?: React.CSSProperties;
  name?: "star" | "starFill";
  fill?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const IconNormalStar: React.FC<IconNormalStarProps>;
export default IconNormalStar;
