import * as React from 'react';
export interface AutoCompleteResourceItemCellProps {
  className?: string;
  style?: React.CSSProperties;
  variant?: "normal" | "search" | "avatar" | "thumbnail" | "checkbox";
  focused?: boolean;
}
export declare const AutoCompleteResourceItemCell: React.FC<AutoCompleteResourceItemCellProps>;
export default AutoCompleteResourceItemCell;
