import * as React from 'react';
export interface TextinputTextfieldProps {
  className?: string;
  style?: React.CSSProperties;
  heading?: boolean;
  menu?: boolean;
  text?: string;
  required?: boolean;
  leadingContent?: boolean;
  placeholder?: string;
  description?: boolean;
  label?: string;
  button?: boolean;
  text2?: string;
  errorText?: string;
  status?: "normal" | "positive" | "negative";
  active?: boolean;
  focus?: boolean;
  disable?: boolean;
  trailingButton?: boolean;
  successText?: string;
  extra?: boolean;
  trailingContent?: boolean;
}
export declare const TextinputTextfield: React.FC<TextinputTextfieldProps>;
export default TextinputTextfield;
