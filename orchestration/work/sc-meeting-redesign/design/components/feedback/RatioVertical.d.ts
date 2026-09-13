import * as React from 'react';
export interface RatioVerticalProps {
  className?: string;
  style?: React.CSSProperties;
  ratio?: "1:1" | "1:2" | "2:3" | "3:4";
}
export declare const RatioVertical: React.FC<RatioVerticalProps>;
export default RatioVertical;
