import * as React from 'react';
export interface ListCellListCellProps {
  className?: string;
  style?: React.CSSProperties;
  disable?: boolean;
  verticalPadding?: "none" | "sm" | "md" | "lg";
  label?: string;
  description?: boolean;
  text?: string;
  leadingContent?: boolean;
  instance?: React.ReactNode;
  trailingContent?: boolean;
  instance2?: React.ReactNode;
  chevron?: boolean;
  divider?: boolean;
  interaction?: boolean;
  selected?: boolean;
  verticalAlign?: "center" | "top";
  textEllipsis?: boolean;
  fillWidth?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const ListCellListCell: React.FC<ListCellListCellProps>;
export default ListCellListCell;
