import * as React from 'react';
export interface AiChatSidebarProps {
  className?: string;
  style?: React.CSSProperties;
  property1?: "default" | "new";
  /** Text content; defaults to "데모 관련 업무 요청". */
  text1?: string;
  /** Text content; defaults to "1분 전". */
  text2?: string;
  /** Text content; defaults to "3". */
  text3?: string;
  /** Text content; defaults to "2026.09.09". */
  text4?: string;
}
export declare const AiChatSidebar: React.FC<AiChatSidebarProps>;
export default AiChatSidebar;
