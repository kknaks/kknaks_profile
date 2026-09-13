import * as React from 'react';
export interface DividerDividerProps {
  className?: string;
  style?: React.CSSProperties;
  variant?: "thick" | "normal";
  vertical?: boolean;
}
export declare const DividerDivider: React.FC<DividerDividerProps>;
export default DividerDivider;
