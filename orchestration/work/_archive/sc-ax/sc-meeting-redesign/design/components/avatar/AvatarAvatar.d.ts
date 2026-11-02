import * as React from 'react';
export interface AvatarAvatarProps {
  className?: string;
  style?: React.CSSProperties;
  interaction?: boolean;
  pushBadge?: boolean;
  variant?: "person" | "company" | "academy";
  size?: "xs" | "sm" | "md" | "lg" | "xl";
  placeholder?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon4?: React.ReactNode;
}
export declare const AvatarAvatar: React.FC<AvatarAvatarProps>;
export default AvatarAvatar;
