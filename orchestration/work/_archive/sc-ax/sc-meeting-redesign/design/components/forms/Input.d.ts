import * as React from 'react';
export interface InputProps {
  className?: string;
  style?: React.CSSProperties;
  state?: "default" | "filled" | "hover" | "focus" | "disabled" | "success" | "info" | "warning" | "error";
  size?: "lg" | "md";
  style2?: "outline" | "filled";
  helperText?: boolean;
  label?: boolean;
  leftIcon?: boolean;
  rightIcon?: boolean;
  /** Text content; defaults to "Label". */
  text1?: string;
  /** Text content; defaults to "Placeholder". */
  text2?: string;
  /** Text content; defaults to "Helper Text". */
  text3?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
}
export declare const Input: React.FC<InputProps>;
export default Input;
