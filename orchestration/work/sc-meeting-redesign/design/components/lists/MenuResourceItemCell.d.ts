import * as React from 'react';
export interface MenuResourceItemCellProps {
  className?: string;
  style?: React.CSSProperties;
  variant?: "normal" | "radio" | "checkbox";
  disable?: boolean;
  verticalPadding?: "8px" | "12px";
  caption?: boolean;
  active?: boolean;
}
export declare const MenuResourceItemCell: React.FC<MenuResourceItemCellProps>;
export default MenuResourceItemCell;
