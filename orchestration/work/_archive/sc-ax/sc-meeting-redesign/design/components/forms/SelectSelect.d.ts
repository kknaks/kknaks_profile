import * as React from 'react';
export interface SelectSelectProps {
  className?: string;
  style?: React.CSSProperties;
  heading?: boolean;
  description?: boolean;
  errorText?: string;
  text?: string;
  text2?: string;
  required?: boolean;
  placeholder?: string;
  value?: string;
  menu?: boolean;
  render?: "text" | "chip";
  negative?: boolean;
  active?: boolean;
  focus?: boolean;
  disable?: boolean;
  overflow?: boolean;
  leadingContent?: boolean;
}
export declare const SelectSelect: React.FC<SelectSelectProps>;
export default SelectSelect;
