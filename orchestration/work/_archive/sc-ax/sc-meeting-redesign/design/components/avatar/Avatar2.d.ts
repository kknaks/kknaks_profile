import * as React from 'react';
export interface Avatar2Props {
  className?: string;
  style?: React.CSSProperties;
  initials?: string;
  type?: "initial" | "image";
  size?: "lg" | "sm" | "md";
  shape?: "circle" | "square";
}
export declare const Avatar2: React.FC<Avatar2Props>;
export default Avatar2;
