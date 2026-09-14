import * as React from 'react';
export interface MenuMenuProps {
  className?: string;
  style?: React.CSSProperties;
  actionArea?: boolean;
  variant?: "normal" | "radio" | "checkbox";
  scrollBar?: boolean;
  cellPadding?: "8px" | "12px";
}
export declare const MenuMenu: React.FC<MenuMenuProps>;
export default MenuMenu;
