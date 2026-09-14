import * as React from 'react';
export interface CategoryResourceChipNormalSmallProps {
  className?: string;
  style?: React.CSSProperties;
  instance?: React.ReactNode;
  leadingContent?: boolean;
  trailingContent?: boolean;
  instance2?: React.ReactNode;
  active?: boolean;
  text?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const CategoryResourceChipNormalSmall: React.FC<CategoryResourceChipNormalSmallProps>;
export default CategoryResourceChipNormalSmall;
