import * as React from 'react';
export interface CardGridContentListProps {
  className?: string;
  style?: React.CSSProperties;
  cards?: string;
  platform?: "desktop" | "mobile";
}
export declare const CardGridContentList: React.FC<CardGridContentListProps>;
export default CardGridContentList;
