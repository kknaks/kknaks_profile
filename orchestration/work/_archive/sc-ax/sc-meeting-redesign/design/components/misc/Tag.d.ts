import * as React from 'react';
export interface TagProps {
  className?: string;
  style?: React.CSSProperties;
  scheme?: "brand" | "neutral" | "positive" | "danger" | "warning";
  state?: "default" | "hover";
  label?: string;
  removable?: boolean;
  variant?: "primary" | "secondary";
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const Tag: React.FC<TagProps>;
export default Tag;
