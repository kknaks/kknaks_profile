import * as React from 'react';
export interface AvatarBlockProps {
  className?: string;
  style?: React.CSSProperties;
  title?: string;
  description?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const AvatarBlock: React.FC<AvatarBlockProps>;
export default AvatarBlock;
