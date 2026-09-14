import * as React from 'react';
export interface InteractionNormalProps {
  className?: string;
  style?: React.CSSProperties;
  state?: "normal" | "hovered" | "focused" | "pressed";
}
export declare const InteractionNormal: React.FC<InteractionNormalProps>;
export default InteractionNormal;
