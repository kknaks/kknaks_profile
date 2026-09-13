import * as React from 'react';
export interface IconNormalClockProps {
  className?: string;
  style?: React.CSSProperties;
  name?: "clock" | "clockFill";
  fill?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const IconNormalClock: React.FC<IconNormalClockProps>;
export default IconNormalClock;
