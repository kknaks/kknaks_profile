import * as React from 'react';
export interface TabItemProps {
  className?: string;
  style?: React.CSSProperties;
  state?: "selected" | "default" | "hover" | "focus" | "disabled";
  iconRight?: boolean;
  text?: boolean;
  iconLeft?: boolean;
  /** Text content; defaults to "Label". */
  text1?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const TabItem: React.FC<TabItemProps>;
export default TabItem;
