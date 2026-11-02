import * as React from 'react';
export interface InboxTaskProps {
  className?: string;
  style?: React.CSSProperties;
  reply?: boolean;
  state?: "active" | "normal" | "reply";
  prop?: string;
  prop2?: string;
  /** Text content; defaults to "8월 매출 자료 오늘까지 보내주세요.". */
  text1?: string;
  /** Text content; defaults to "데모에서 업무·회의·자료가 채팅에서 안전하게\n이어지는 경험을 검증한다. 여섯줄까지 말줄임 없이 노출해주세요.". */
  text2?: string;
  /** Text content; defaults to "홍길동". */
  text3?: string;
  /** Text content; defaults to "2026.10.10". */
  text4?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon3?: React.ReactNode;
}
export declare const InboxTask: React.FC<InboxTaskProps>;
export default InboxTask;
