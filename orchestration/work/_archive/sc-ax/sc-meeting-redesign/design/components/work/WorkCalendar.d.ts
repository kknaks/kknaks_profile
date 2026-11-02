import * as React from 'react';
export interface WorkCalendarProps {
  className?: string;
  style?: React.CSSProperties;
  empty?: boolean;
  type?: "월간" | "주간" | "오늘";
  task?: boolean;
  /** Text content; defaults to "캘린더". */
  text1?: string;
  /** Text content; defaults to "2026년 9월". */
  text2?: string;
  /** Text content; defaults to "월". */
  text3?: string;
  /** Text content; defaults to "화". */
  text4?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon4?: React.ReactNode;
}
export declare const WorkCalendar: React.FC<WorkCalendarProps>;
export default WorkCalendar;
