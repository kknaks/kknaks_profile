import * as React from 'react';
export interface Button3Props {
  className?: string;
  style?: React.CSSProperties;
  label?: string;
  variant?: "primary" | "neutral" | "subtle";
  hasIconStart?: boolean;
  iconStart?: React.ReactNode;
  hasIconEnd?: boolean;
  iconEnd?: React.ReactNode;
  state?: "default" | "hover" | "disabled";
  size?: "md" | "sm";
}
export declare const Button3: React.FC<Button3Props>;
export default Button3;
