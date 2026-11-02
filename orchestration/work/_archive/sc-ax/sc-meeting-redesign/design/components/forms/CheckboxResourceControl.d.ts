import * as React from 'react';
export interface CheckboxResourceControlProps {
  className?: string;
  style?: React.CSSProperties;
  size?: "sm" | "normal";
  state?: "unchecked" | "checked" | "indeterminate";
  disable?: boolean;
  tight?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
}
export declare const CheckboxResourceControl: React.FC<CheckboxResourceControlProps>;
export default CheckboxResourceControl;
