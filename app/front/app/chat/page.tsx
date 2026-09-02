import type { Metadata } from "next";
import { Suspense } from "react";
import { ChatView } from "@/components/chat/chat-view";

export const metadata: Metadata = {
  title: "Ask · kknaks.dev",
  description: "이력 데이터(career · projects · problem)를 근거로 대답하는 채팅",
};

/**
 * `/chat` — 채용담당자 채팅 (KDEV-SPEC-017 §2 U-3~U-6).
 *
 * 표면 전체가 방문자 상호작용이라 본체는 클라이언트 컴포넌트다. `?q=`(홈 히어로가
 * 넘긴 첫 질문)를 `useSearchParams` 로 읽으므로 Suspense 경계가 필요하다.
 */
export default function ChatPage() {
  return (
    <Suspense fallback={null}>
      <ChatView />
    </Suspense>
  );
}
