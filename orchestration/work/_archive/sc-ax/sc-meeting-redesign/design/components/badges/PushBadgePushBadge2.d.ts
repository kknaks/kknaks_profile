import * as React from 'react';
export interface PushBadgePushBadge2Props {
  className?: string;
  style?: React.CSSProperties;
  number?: string;
  variant?: "dot" | "number" | "new";
  size?: "xs" | "sm" | "md";
  /** Text content; defaults to "N". */
  text1?: string;
}
export declare const PushBadgePushBadge2: React.FC<PushBadgePushBadge2Props>;
export default PushBadgePushBadge2;
