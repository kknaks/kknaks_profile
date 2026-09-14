import * as React from 'react';
export interface ButtonTextProps {
  className?: string;
  style?: React.CSSProperties;
  loading?: boolean;
  label?: string;
  variant?: "primary" | "assistive";
  leadingIcon?: boolean;
  size?: "sm" | "md";
  trailingIcon?: boolean;
  disable?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon4?: React.ReactNode;
}
export declare const ButtonText: React.FC<ButtonTextProps>;
export default ButtonText;
