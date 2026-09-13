import * as React from 'react';
export interface PageControlItemProps {
  className?: string;
  style?: React.CSSProperties;
  state?: "default" | "disabled" | "disabled (reduced-1)" | "disabled (reduced-2)";
}
export declare const PageControlItem: React.FC<PageControlItemProps>;
export default PageControlItem;
