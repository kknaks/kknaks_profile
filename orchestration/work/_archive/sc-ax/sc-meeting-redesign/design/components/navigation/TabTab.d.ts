import * as React from 'react';
export interface TabTabProps {
  className?: string;
  style?: React.CSSProperties;
  trailingIconButton?: boolean;
  gradientLeading?: boolean;
  gradientTrailing?: boolean;
  tab6?: boolean;
  tab1?: boolean;
  tab7?: boolean;
  tab8?: boolean;
  tab5?: boolean;
  tab2?: boolean;
  resize?: "hug" | "fill";
  size?: "sm" | "md" | "lg";
  horizontalPadding?: boolean;
  tab4?: boolean;
  tab3?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon4?: React.ReactNode;
}
export declare const TabTab: React.FC<TabTabProps>;
export default TabTab;
