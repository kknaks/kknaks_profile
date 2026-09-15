import * as React from 'react';
export interface TextinputResourceTextfieldButtonProps {
  className?: string;
  style?: React.CSSProperties;
  label?: string;
  label2?: string;
  variant?: "normal" | "assistive";
  disable?: boolean;
  leadingIcon?: boolean;
  trailingIcon?: boolean;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
}
export declare const TextinputResourceTextfieldButton: React.FC<TextinputResourceTextfieldButtonProps>;
export default TextinputResourceTextfieldButton;
