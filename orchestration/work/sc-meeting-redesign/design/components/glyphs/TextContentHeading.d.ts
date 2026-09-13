import * as React from 'react';
export interface TextContentHeadingProps {
  className?: string;
  style?: React.CSSProperties;
  hasSubheading?: boolean;
  align?: "start" | "center";
  heading?: string;
  subheading?: string;
}
export declare const TextContentHeading: React.FC<TextContentHeadingProps>;
export default TextContentHeading;
