import * as React from 'react';
export interface TextinputResourceTextfieldTrailingContentProps {
  className?: string;
  style?: React.CSSProperties;
  text?: string;
  time?: string;
  variant?: "custom" | "badge" | "icon button" | "text" | "icon" | "timer";
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
}
export declare const TextinputResourceTextfieldTrailingContent: React.FC<TextinputResourceTextfieldTrailingContentProps>;
export default TextinputResourceTextfieldTrailingContent;
