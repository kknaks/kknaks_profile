import * as React from 'react';
export interface AvatarProps {
  className?: string;
  style?: React.CSSProperties;
  size?: "xxxl giant" | "xxl giant" | "xl giant" | "giant" | "lg" | "md" | "sm" | "tiny";
  type?: "image" | "letter" | "icon";
  status?: boolean;
  /** Text content; defaults to "A". */
  text1?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const Avatar: React.FC<AvatarProps>;
export default Avatar;
