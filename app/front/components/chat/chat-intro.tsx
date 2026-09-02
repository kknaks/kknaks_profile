"use client";

import { AskBox } from "@/components/chat/ask-box";

/**
 * 인사말 + 입력창 한 화면 — 홈 히어로(U-1)와 `/chat` 빈 상태(U-3)가 같은 구성이다.
 * 다른 건 `scroll ↓` 큐뿐 — 빈 상태에는 스크롤 섹션이 없으니 큐도 없다.
 *
 * 문구는 spec §2 U-1 그대로다. 임의로 바꾸지 않는다.
 */
export function ChatIntro({
  onSubmit,
  scrollCueHref,
}: {
  onSubmit: (question: string) => void | boolean | Promise<void | boolean>;
  /** 주면 하단에 `scroll ↓` 큐가 붙는다(홈 전용). */
  scrollCueHref?: string;
}) {
  return (
    <section className="chat-hero">
      <div className="chat-greet">
        <div className="eyebrow-line">// ask kknaks · v0.2.0</div>
        <h1>
          안녕하세요, <span className="em">이건학</span>입니다.
          <br />
          무엇이든 물어보세요.
        </h1>
        <p>제 커리어·프로젝트·문제 해결 기록이 직접 대답합니다.</p>
      </div>

      <AskBox
        showBar
        autoFocus
        placeholder="이 사람, FastAPI 실무 경험 있나요?"
        onSubmit={onSubmit}
      />

      <div className="chat-hint">
        답변은 실제 이력 데이터(<span className="k">career · projects · problem</span>)를
        근거로 생성됩니다
      </div>

      {scrollCueHref && (
        <div className="chat-scroll-cue">
          <a href={scrollCueHref}>
            scroll<span className="arr">↓</span>
          </a>
        </div>
      )}
    </section>
  );
}
