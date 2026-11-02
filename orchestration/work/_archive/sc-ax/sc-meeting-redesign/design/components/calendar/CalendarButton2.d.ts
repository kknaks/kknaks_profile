import * as React from 'react';
export interface CalendarButton2Props {
  className?: string;
  style?: React.CSSProperties;
  dot?: boolean;
  state?: "default" | "disabled" | "today" | "blank";
  selected?: boolean;
  date?: string;
  /** Text content; defaults to "1". */
  text1?: string;
}
export declare const CalendarButton2: React.FC<CalendarButton2Props>;
export default CalendarButton2;
