import * as React from 'react';
export interface SelectFieldProps {
  className?: string;
  style?: React.CSSProperties;
  state?: "default" | "error" | "disabled";
  value?: string;
  open?: boolean;
  hasLabel?: boolean;
  hasError?: boolean;
  error?: string;
  label?: string;
  hasDescription?: boolean;
  description?: string;
  valueType?: "default" | "placeholder";
  /** Text content; defaults to "Hello World". */
  text1?: string;
  /** Text content; defaults to "Option 2". */
  text2?: string;
  /** Text content; defaults to "Option 3". */
  text3?: string;
  /** Text content; defaults to "Option 4". */
  text4?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const SelectField: React.FC<SelectFieldProps>;
export default SelectField;
