import * as React from 'react';
export interface InteractionStrongProps {
  className?: string;
  style?: React.CSSProperties;
  state?: "normal" | "hovered" | "focused" | "pressed";
}
export declare const InteractionStrong: React.FC<InteractionStrongProps>;
export default InteractionStrong;
