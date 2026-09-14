import * as React from 'react';
export interface NavigationProps {
  className?: string;
  style?: React.CSSProperties;
  size?: "max" | "min";
  /** Text content; defaults to "유하람님". */
  text1?: string;
  /** Text content; defaults to "기획자". */
  text2?: string;
  /** Text content; defaults to "LOGO". */
  text3?: string;
  /** Text content; defaults to "v1.0". */
  text4?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
}
export declare const Navigation: React.FC<NavigationProps>;
export default Navigation;
