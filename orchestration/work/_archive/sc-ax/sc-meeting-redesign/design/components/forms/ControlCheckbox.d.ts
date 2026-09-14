import * as React from 'react';
export interface ControlCheckboxProps {
  className?: string;
  style?: React.CSSProperties;
  label?: boolean;
  text?: string;
  size?: "sm" | "md";
  disable?: boolean;
  state?: "unchecked" | "checked" | "indeterminate";
  bold?: boolean;
  tight?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const ControlCheckbox: React.FC<ControlCheckboxProps>;
export default ControlCheckbox;
