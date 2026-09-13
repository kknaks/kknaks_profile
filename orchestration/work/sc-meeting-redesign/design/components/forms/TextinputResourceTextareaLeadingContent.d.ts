import * as React from 'react';
export interface TextinputResourceTextareaLeadingContentProps {
  className?: string;
  style?: React.CSSProperties;
  characterCount?: string;
  variant?: "character counter" | "button" | "normal icon button" | "icon" | "badge";
  characterLimit?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const TextinputResourceTextareaLeadingContent: React.FC<TextinputResourceTextareaLeadingContentProps>;
export default TextinputResourceTextareaLeadingContent;
