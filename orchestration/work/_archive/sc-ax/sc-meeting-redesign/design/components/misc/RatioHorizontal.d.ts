import * as React from 'react';
export interface RatioHorizontalProps {
  className?: string;
  style?: React.CSSProperties;
  aspectRatio?: "1:1" | "5:4" | "4:3" | "3:2" | "16:10" | "1.618:1" | "16:9" | "2:1" | "21:9" | "4:5" | "3:4" | "2:3" | "10:16" | "1:1.618" | "9:16" | "1:2" | "9:21";
}
export declare const RatioHorizontal: React.FC<RatioHorizontalProps>;
export default RatioHorizontal;
