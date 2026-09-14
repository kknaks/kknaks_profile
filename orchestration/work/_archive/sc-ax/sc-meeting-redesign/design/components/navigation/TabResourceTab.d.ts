import * as React from 'react';
export interface TabResourceTabProps {
  className?: string;
  style?: React.CSSProperties;
  text?: string;
  active?: boolean;
  disabled?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const TabResourceTab: React.FC<TabResourceTabProps>;
export default TabResourceTab;
