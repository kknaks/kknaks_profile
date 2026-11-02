import * as React from 'react';
export interface CheckboxFieldProps {
  className?: string;
  style?: React.CSSProperties;
  label?: string;
  hasDescription?: boolean;
  state?: "default" | "disabled";
  description?: string;
  valueType?: "unchecked" | "checked" | "indeterminate";
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const CheckboxField: React.FC<CheckboxFieldProps>;
export default CheckboxField;
