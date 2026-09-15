import * as React from 'react';
export interface IconNormalCloseProps {
  className?: string;
  style?: React.CSSProperties;
  name?: "closeThick" | "close";
  thick?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const IconNormalClose: React.FC<IconNormalCloseProps>;
export default IconNormalClose;
