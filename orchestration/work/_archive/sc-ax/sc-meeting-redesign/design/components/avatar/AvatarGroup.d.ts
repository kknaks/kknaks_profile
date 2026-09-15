import * as React from 'react';
export interface AvatarGroupProps {
  className?: string;
  style?: React.CSSProperties;
  showOverflow?: boolean;
  spacing?: "overlap" | "spaced";
  number?: string;
  avatars2?: string;
  avatars?: string;
}
export declare const AvatarGroup: React.FC<AvatarGroupProps>;
export default AvatarGroup;
