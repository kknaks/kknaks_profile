import * as React from 'react';
export interface CalendarProps {
  className?: string;
  style?: React.CSSProperties;
  /** Text content; defaults to "Su". */
  text1?: string;
  /** Text content; defaults to "Mo". */
  text2?: string;
  /** Text content; defaults to "Tu". */
  text3?: string;
  /** Text content; defaults to "We". */
  text4?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon4?: React.ReactNode;
}
export declare const Calendar: React.FC<CalendarProps>;
export default Calendar;
