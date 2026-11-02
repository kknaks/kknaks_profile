import * as React from 'react';
export interface TooltipTooltipProps {
  className?: string;
  style?: React.CSSProperties;
  label?: string;
  shortcut?: boolean;
  text?: string;
  size?: "sm" | "md";
  labelOnlyDesktop?: string;
  position?: "bottom" | "top" | "left" | "right";
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const TooltipTooltip: React.FC<TooltipTooltipProps>;
export default TooltipTooltip;
