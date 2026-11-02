import * as React from 'react';
export interface ClockProps {
  className?: string;
  style?: React.CSSProperties;
  size?: "20" | "24" | "32" | "40" | "48" | "16";
}
export declare const Clock: React.FC<ClockProps>;
export default Clock;
