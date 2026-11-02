import * as React from 'react';
export interface SegmentedControlSegmentedControlProps {
  className?: string;
  style?: React.CSSProperties;
  segment3?: boolean;
  segment4?: boolean;
  segment6?: boolean;
  segment5?: boolean;
  variant?: "solid" | "outlined";
  size?: "sm" | "md" | "lg";
  icon?: boolean;
}
export declare const SegmentedControlSegmentedControl: React.FC<SegmentedControlSegmentedControlProps>;
export default SegmentedControlSegmentedControl;
