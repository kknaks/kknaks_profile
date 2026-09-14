import * as React from 'react';
export interface SearchProps {
  className?: string;
  style?: React.CSSProperties;
  value?: string;
  state?: "default" | "disabled";
  valueType?: "filled" | "placeholder";
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const Search: React.FC<SearchProps>;
export default Search;
