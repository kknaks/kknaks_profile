import * as React from 'react';
export interface IconNormalBlankProps {
  className?: string;
  style?: React.CSSProperties;
  name?: "blank";
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const IconNormalBlank: React.FC<IconNormalBlankProps>;
export default IconNormalBlank;
