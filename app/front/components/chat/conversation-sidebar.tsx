"use client";

import Link from "next/link";
import { sameId, type ChatId, type Conversation } from "@/lib/chat";

/**
 * 대화 사이드바 (§2 U-4) — `＋ 새 대화` · 「대화」 라벨 · 이 세션의 대화 목록
 * (최신순) · `← 홈으로`. 현재 대화는 배경 강조.
 *
 * 대화 전환은 **페이지 이동이 아니라 스레드 교체**다. 모바일(≤720px)에서는
 * 숨긴다 — 드로어는 후속(OQ-1).
 */
export function ConversationSidebar({
  conversations,
  currentId,
  onNew,
  onSelect,
}: {
  conversations: Conversation[];
  currentId: ChatId | null;
  onNew: () => void;
  onSelect: (conversation: Conversation) => void;
}) {
  return (
    <aside className="chat-side">
      <button type="button" className="newchat" onClick={onNew}>
        ＋ 새 대화
      </button>
      <div className="caps-label">대화</div>
      <div className="convlist">
        {conversations.map((c) => (
          <button
            key={String(c.id)}
            type="button"
            className={sameId(c.id, currentId) ? "active" : undefined}
            title={c.title}
            onClick={() => onSelect(c)}
          >
            {c.title}
          </button>
        ))}
      </div>
      <Link className="homelink" href="/">
        ← 홈으로
      </Link>
    </aside>
  );
}
