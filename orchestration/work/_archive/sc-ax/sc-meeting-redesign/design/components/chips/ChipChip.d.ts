import * as React from 'react';
export interface ChipChipProps {
  className?: string;
  style?: React.CSSProperties;
  instance?: React.ReactNode;
  text?: string;
  trailingContent?: boolean;
  instance2?: React.ReactNode;
  leadingContent?: boolean;
  size?: "xs" | "sm" | "md" | "lg";
  variant?: "solid" | "outlined";
  disable?: boolean;
  active?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const ChipChip: React.FC<ChipChipProps>;
export default ChipChip;
