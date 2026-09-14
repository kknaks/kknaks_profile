import * as React from 'react';
export interface InteractionLightProps {
  className?: string;
  style?: React.CSSProperties;
  state?: "normal" | "hovered" | "focused" | "pressed";
}
export declare const InteractionLight: React.FC<InteractionLightProps>;
export default InteractionLight;
