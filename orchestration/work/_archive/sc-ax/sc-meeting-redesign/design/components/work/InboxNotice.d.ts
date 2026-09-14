import * as React from 'react';
export interface InboxNoticeProps {
  className?: string;
  style?: React.CSSProperties;
  type?: "cc" | "notice";
  /** Text content; defaults to "[9월 정산 자료 취합]에 참조로 걸렸습니다". */
  text1?: string;
  /** Text content; defaults to "홍길동". */
  text2?: string;
  /** Text content; defaults to "2026.10.10". */
  text3?: string;
  /** Text content; defaults to "메일". */
  text4?: string;
  /** Swappable nested instance; defaults to the design's. */
  icon2?: React.ReactNode;
}
export declare const InboxNotice: React.FC<InboxNoticeProps>;
export default InboxNotice;
