import * as React from 'react';
export interface PushBadgePushBadgeProps {
  className?: string;
  style?: React.CSSProperties;
  number?: string;
  variant?: "dot" | "number" | "new";
  size?: "xs" | "sm" | "md";
  /** Text content; defaults to "N". */
  text1?: string;
}
export declare const PushBadgePushBadge: React.FC<PushBadgePushBadgeProps>;
export default PushBadgePushBadge;
