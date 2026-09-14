import * as React from 'react';
export interface IconNormalChevronDownProps {
  className?: string;
  style?: React.CSSProperties;
  name?: "chevronDown" | "chevronDownThick" | "chevronDownSmall" | "chevronDownThickSmall";
  thick?: boolean;
  small?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const IconNormalChevronDown: React.FC<IconNormalChevronDownProps>;
export default IconNormalChevronDown;
