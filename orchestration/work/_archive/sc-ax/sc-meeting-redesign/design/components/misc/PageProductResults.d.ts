import * as React from 'react';
export interface PageProductResultsProps {
  className?: string;
  style?: React.CSSProperties;
  slot?: string;
  platform?: "desktop" | "mobile";
  cardGrid?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
}
export declare const PageProductResults: React.FC<PageProductResultsProps>;
export default PageProductResults;
