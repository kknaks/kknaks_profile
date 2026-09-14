import * as React from 'react';
export interface IconNormalChevronUpProps {
  className?: string;
  style?: React.CSSProperties;
  name?: "chevronUp" | "chevronUpThick" | "chevronUpSmall" | "chevronUpThickSmall";
  thick?: boolean;
  small?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const IconNormalChevronUp: React.FC<IconNormalChevronUpProps>;
export default IconNormalChevronUp;
