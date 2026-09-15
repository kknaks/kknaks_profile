import * as React from 'react';
export interface SelectResourceLeadingContentProps {
  className?: string;
  style?: React.CSSProperties;
  variant?: "custom" | "icon" | "icon button";
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const SelectResourceLeadingContent: React.FC<SelectResourceLeadingContentProps>;
export default SelectResourceLeadingContent;
