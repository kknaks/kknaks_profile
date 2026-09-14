import * as React from 'react';
export interface TextinputTextareaProps {
  className?: string;
  style?: React.CSSProperties;
  value?: string;
  description?: boolean;
  text?: string;
  bottom?: boolean;
  leadingContent?: boolean;
  extra2?: boolean;
  extra1?: boolean;
  trailingContent?: boolean;
  extra12?: boolean;
  extra22?: boolean;
  scroll?: boolean;
  heading?: boolean;
  required?: boolean;
  text2?: string;
  placeholder?: string;
  status?: "normal" | "negative";
  resize?: "normal" | "limit" | "fixed";
  active?: boolean;
  focus?: boolean;
  disable?: boolean;
}
export declare const TextinputTextarea: React.FC<TextinputTextareaProps>;
export default TextinputTextarea;
