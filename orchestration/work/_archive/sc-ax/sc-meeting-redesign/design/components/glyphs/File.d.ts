import * as React from 'react';
export interface FileProps {
  className?: string;
  style?: React.CSSProperties;
  prop?: boolean;
  state?: "default" | "hover" | "delete";
  fileName?: string;
  /** Text content; defaults to "Document File.html". */
  text1?: string;
  /** Text content; defaults to "1.2 MB". */
  text2?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
}
export declare const File: React.FC<FileProps>;
export default File;
