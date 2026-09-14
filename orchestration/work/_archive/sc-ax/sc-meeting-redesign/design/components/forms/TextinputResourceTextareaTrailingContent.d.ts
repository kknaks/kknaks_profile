import * as React from 'react';
export interface TextinputResourceTextareaTrailingContentProps {
  className?: string;
  style?: React.CSSProperties;
  characterLimit?: string;
  variant?: "button" | "primary icon button" | "icon" | "character counter" | "badge" | "normal icon button";
  characterCount?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const TextinputResourceTextareaTrailingContent: React.FC<TextinputResourceTextareaTrailingContentProps>;
export default TextinputResourceTextareaTrailingContent;
