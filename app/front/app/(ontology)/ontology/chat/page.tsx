import { Suspense } from "react";
import { ChatView } from "@/components/ontology/chat/chat-view";

/**
 * `/ontology/chat` — 데모 채팅(SPEC-004 U-8~U-12).
 *
 * **기존 포트폴리오 `/chat` 은 건드리지 않는다.** `?q=` 프리필 패턴만 같이 쓴다.
 */
export default function OntologyChatPage() {
  return (
    <Suspense fallback={null}>
      <ChatView />
    </Suspense>
  );
}
