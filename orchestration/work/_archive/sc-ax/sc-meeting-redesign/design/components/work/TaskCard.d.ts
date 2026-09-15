import * as React from 'react';
export interface TaskCardProps {
  className?: string;
  style?: React.CSSProperties;
  prop?: boolean;
  property1?: "create" | "completion" | "edit";
  /** Text content; defaults to "SC AX 채팅 기반 데모 준비". */
  text1?: string;
  /** Text content; defaults to "데모에서 업무·회의·자료가 채팅에서 안전하게\n이어지는 경험을 검증한다.". */
  text2?: string;
  /** Text content; defaults to "담당자". */
  text3?: string;
  /** Text content; defaults to "홍길동". */
  text4?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
  /** Swappable nested instance; defaults to the design's. */
  icon4?: React.ReactNode;
}
export declare const TaskCard: React.FC<TaskCardProps>;
export default TaskCard;
