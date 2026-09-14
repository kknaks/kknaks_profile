import * as React from 'react';
export interface ContentBadgeContentBadgeProps {
  className?: string;
  style?: React.CSSProperties;
  variant?: "solid" | "outlined";
  size?: "md" | "sm" | "xs";
  color?: "neutral" | "accent";
  trailingIcon?: boolean;
  leadingIcon?: boolean;
  text?: string;
}
export declare const ContentBadgeContentBadge: React.FC<ContentBadgeContentBadgeProps>;
export default ContentBadgeContentBadge;
