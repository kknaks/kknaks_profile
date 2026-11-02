import * as React from 'react';
export interface MODCreateTaskProps {
  className?: string;
  style?: React.CSSProperties;
  state?: "normal" | "detailed" | "state3";
  /** Text content; defaults to "업무 만들기". */
  text1?: string;
  /** Text content; defaults to "추가 정보 입력". */
  text2?: string;
  /** Text content; defaults to "파일 첨부". */
  text3?: string;
  /** Text content; defaults to "첨부할 파일을 끌어다 놓거나 추가하세요". */
  text4?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
}
export declare const MODCreateTask: React.FC<MODCreateTaskProps>;
export default MODCreateTask;
