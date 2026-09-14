import * as React from 'react';
export interface ProductInfoCardProps {
  className?: string;
  style?: React.CSSProperties;
  showDescription?: boolean;
  body?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const ProductInfoCard: React.FC<ProductInfoCardProps>;
export default ProductInfoCard;
