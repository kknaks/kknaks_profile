import * as React from 'react';
export interface ButtonIconNormalProps {
  className?: string;
  style?: React.CSSProperties;
  badge?: boolean;
  disable?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
}
export declare const ButtonIconNormal: React.FC<ButtonIconNormalProps>;
export default ButtonIconNormal;
