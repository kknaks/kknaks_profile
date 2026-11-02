import * as React from 'react';
export interface ButtonProps {
  className?: string;
  style?: React.CSSProperties;
  iconLeft?: boolean;
  size?: "giant" | "lg" | "md" | "sm" | "tiny";
  state?: "default" | "hover" | "focus" | "press" | "disabled";
  content?: "icons + text" | "only icons";
  style2?: "filled" | "outline" | "clear";
  iconRight?: boolean;
  /** Text content; defaults to "Button". */
  text1?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
}
export declare const Button: React.FC<ButtonProps>;
export default Button;
