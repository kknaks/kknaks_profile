import * as React from 'react';
export interface ButtonGroupProps {
  className?: string;
  style?: React.CSSProperties;
  buttonStart?: boolean;
  align?: "justify" | "start" | "end" | "center" | "stack";
  buttonEnd?: boolean;
}
export declare const ButtonGroup: React.FC<ButtonGroupProps>;
export default ButtonGroup;
