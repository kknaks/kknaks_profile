import * as React from 'react';
export interface FramedStyleResourceSlotProps {
  className?: string;
  style?: React.CSSProperties;
  type?: "custom" | "checkbox" | "radio";
}
export declare const FramedStyleResourceSlot: React.FC<FramedStyleResourceSlotProps>;
export default FramedStyleResourceSlot;
