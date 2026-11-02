import * as React from 'react';
export interface ButtonButtonProps {
  className?: string;
  style?: React.CSSProperties;
  loading?: boolean;
  label?: string;
  leadingIcon?: boolean;
  variant?: "solid" | "outlined";
  disable?: boolean;
  color?: "primary" | "assistive";
  trailingIcon?: boolean;
  iconOnly?: boolean;
  size?: "sm" | "md" | "lg";
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon4?: React.ReactNode;
}
export declare const ButtonButton: React.FC<ButtonButtonProps>;
export default ButtonButton;
