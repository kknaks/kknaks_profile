import * as React from 'react';
export interface SelectResourceBackgroundProps {
  className?: string;
  style?: React.CSSProperties;
  platform?: "web/ios" | "android";
}
export declare const SelectResourceBackground: React.FC<SelectResourceBackgroundProps>;
export default SelectResourceBackground;
