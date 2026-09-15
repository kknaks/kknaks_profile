import * as React from 'react';
export interface SliderFieldProps {
  className?: string;
  style?: React.CSSProperties;
  hasLabel?: boolean;
  label?: string;
  state?: "default" | "disabled";
  hasDescription?: boolean;
  description?: string;
  /** Text content; defaults to "$". */
  text1?: string;
  /** Text content; defaults to "0-100". */
  text2?: string;
}
export declare const SliderField: React.FC<SliderFieldProps>;
export default SliderField;
