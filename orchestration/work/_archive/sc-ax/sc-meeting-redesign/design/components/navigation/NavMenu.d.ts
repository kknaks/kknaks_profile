import * as React from 'react';
export interface NavMenuProps {
  className?: string;
  style?: React.CSSProperties;
  text?: string;
  state?: "active" | "default" | "hover";
  pushBadge?: boolean;
  /** Text content; defaults to "메뉴 명". */
  text1?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const NavMenu: React.FC<NavMenuProps>;
export default NavMenu;
