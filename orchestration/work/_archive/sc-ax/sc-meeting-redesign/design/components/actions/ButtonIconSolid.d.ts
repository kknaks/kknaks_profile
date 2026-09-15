import * as React from 'react';
export interface ButtonIconSolidProps {
  className?: string;
  style?: React.CSSProperties;
  size?: "sm" | "md" | "custom";
  disable?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
}
export declare const ButtonIconSolid: React.FC<ButtonIconSolidProps>;
export default ButtonIconSolid;
