"use client";

import { useRouter } from "next/navigation";
import { ChatIntro } from "@/components/chat/chat-intro";

/**
 * 홈 첫 화면 — 채팅 히어로(§2 U-1 · DEC-025 D1).
 *
 * 정확히 한 화면이고, 아래로 스크롤하면 기존 `LandingPreview` 섹션이 이어진다.
 * 질문을 보내면 `/chat?q=` 로 이동한다 — 대화 생성·전송은 `/chat` 이 한다
 * (§3 S-1: 새 대화가 생성되고 첫 질문이 즉시 전송된 상태로 시작).
 */
export function ChatHero() {
  const router = useRouter();

  return (
    <ChatIntro
      scrollCueHref="#about"
      onSubmit={(question) => {
        router.push(`/chat?q=${encodeURIComponent(question)}`);
      }}
    />
  );
}
