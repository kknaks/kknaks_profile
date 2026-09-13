import * as React from 'react';
export interface TaskTableProps {
  className?: string;
  style?: React.CSSProperties;
  type?: "my" | "request" | "done";
  /** Text content; defaults to "제목/종류". */
  text1?: string;
  /** Text content; defaults to "요청자". */
  text2?: string;
  /** Text content; defaults to "기한". */
  text3?: string;
  /** Text content; defaults to "상태". */
  text4?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon1?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon4?: React.ReactNode;
}
export declare const TaskTable: React.FC<TaskTableProps>;
export default TaskTable;
