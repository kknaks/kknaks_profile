import * as React from 'react';
export interface ReplyProps {
  className?: string;
  style?: React.CSSProperties;
  prop?: string;
  property1?: "mail" | "messenger";
  prop2?: string;
  prop3?: string;
  /** Text content; defaults to "메일로 답장". */
  text1?: string;
  /** Text content; defaults to "받는 사람". */
  text2?: string;
  /** Text content; defaults to "박민수 <park@thesc.co.kr>". */
  text3?: string;
  /** Text content; defaults to "제목". */
  text4?: string;
}
export declare const Reply: React.FC<ReplyProps>;
export default Reply;
