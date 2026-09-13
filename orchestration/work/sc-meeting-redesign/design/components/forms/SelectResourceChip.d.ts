import * as React from 'react';
export interface SelectResourceChipProps {
  className?: string;
  style?: React.CSSProperties;
  state?: "normal" | "negative";
  disable?: boolean;
}
export declare const SelectResourceChip: React.FC<SelectResourceChipProps>;
export default SelectResourceChip;
