import * as React from 'react';
export interface RadioResourceControlProps {
  className?: string;
  style?: React.CSSProperties;
  size?: "sm" | "md";
  state?: "unchecked" | "checked";
  disable?: boolean;
  tight?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
}
export declare const RadioResourceControl: React.FC<RadioResourceControlProps>;
export default RadioResourceControl;
