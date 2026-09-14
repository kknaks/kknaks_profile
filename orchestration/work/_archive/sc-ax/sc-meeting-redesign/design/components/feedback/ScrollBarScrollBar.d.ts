import * as React from 'react';
export interface ScrollBarScrollBarProps {
  className?: string;
  style?: React.CSSProperties;
  size?: "sm" | "md";
  percent?: "100%" | "75%" | "50%" | "25%";
  position?: "top" | "center" | "bottom";
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const ScrollBarScrollBar: React.FC<ScrollBarScrollBarProps>;
export default ScrollBarScrollBar;
