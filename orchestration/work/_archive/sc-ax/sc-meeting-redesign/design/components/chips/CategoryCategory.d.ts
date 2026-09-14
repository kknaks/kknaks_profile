import * as React from 'react';
export interface CategoryCategoryProps {
  className?: string;
  style?: React.CSSProperties;
  verticalPadding?: boolean;
  iconButton?: boolean;
  gradientLeading?: boolean;
  gradientTrailing?: boolean;
  tab6?: boolean;
  tab1?: boolean;
  variant?: "normal" | "alternative";
  tab7?: boolean;
  tab8?: boolean;
  tab5?: boolean;
  tab2?: boolean;
  size?: "md" | "sm" | "lg" | "xl";
  tab4?: boolean;
  tab3?: boolean;
  horizontalPadding?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon4?: React.ReactNode;
}
export declare const CategoryCategory: React.FC<CategoryCategoryProps>;
export default CategoryCategory;
