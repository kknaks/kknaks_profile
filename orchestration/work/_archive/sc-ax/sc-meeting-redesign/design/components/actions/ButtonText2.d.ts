import * as React from 'react';
export interface ButtonText2Props {
  className?: string;
  style?: React.CSSProperties;
  loading?: boolean;
  label?: string;
  leadingIcon?: boolean;
  variant?: "primary" | "assistive";
  size?: "sm" | "md";
  disable?: boolean;
  trailingIcon?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon4?: React.ReactNode;
}
export declare const ButtonText2: React.FC<ButtonText2Props>;
export default ButtonText2;
