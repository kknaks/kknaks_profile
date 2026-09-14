import * as React from 'react';
export interface AutoCompleteAutoCompleteProps {
  className?: string;
  style?: React.CSSProperties;
  directInput?: boolean;
  title?: boolean;
  variant?: "normal" | "search" | "avatar" | "checkbox" | "thumbnail";
  directInputPosition?: "bottom" | "top";
  scrollBar?: boolean;
}
export declare const AutoCompleteAutoComplete: React.FC<AutoCompleteAutoCompleteProps>;
export default AutoCompleteAutoComplete;
