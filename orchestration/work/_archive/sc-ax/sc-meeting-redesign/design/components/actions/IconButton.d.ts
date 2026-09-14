import * as React from 'react';
export interface IconButtonProps {
  className?: string;
  style?: React.CSSProperties;
  variant?: "primary" | "neutral" | "subtle";
  icon?: React.ReactNode;
  state?: "default" | "hover" | "disabled";
  size?: "md" | "sm";
}
export declare const IconButton: React.FC<IconButtonProps>;
export default IconButton;
