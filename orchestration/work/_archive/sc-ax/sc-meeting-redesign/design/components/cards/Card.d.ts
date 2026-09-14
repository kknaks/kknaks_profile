import * as React from 'react';
export interface CardProps {
  className?: string;
  style?: React.CSSProperties;
  assetType?: "icon" | "image";
  asset?: boolean;
  icon?: React.ReactNode;
  button?: boolean;
  heading?: string;
  body2?: string;
  body?: string;
  variant?: "stroke" | "default";
  direction?: "horizontal" | "vertical";
}
export declare const Card: React.FC<CardProps>;
export default Card;
