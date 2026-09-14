import * as React from 'react';
export interface CategoryResourceChipNormalLargeProps {
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
export declare const CategoryResourceChipNormalLarge: React.FC<CategoryResourceChipNormalLargeProps>;
export default CategoryResourceChipNormalLarge;
