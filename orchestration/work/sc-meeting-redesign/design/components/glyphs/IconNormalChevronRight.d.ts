import * as React from 'react';
export interface IconNormalChevronRightProps {
  className?: string;
  style?: React.CSSProperties;
  name?: "chevronRight" | "chevronRightThick" | "chevronRightTight" | "chevronRightTightThick" | "chevronRightSmall" | "chevronRightThickSmall" | "chevronRightTightSmall" | "chevronRightTightThickSmall";
  tight?: boolean;
  thick?: boolean;
  small?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const IconNormalChevronRight: React.FC<IconNormalChevronRightProps>;
export default IconNormalChevronRight;
