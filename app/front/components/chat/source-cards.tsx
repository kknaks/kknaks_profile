"use client";

import Link from "next/link";
import type { ChatSource } from "@/lib/chat";
import { opensInPanel, sourceTypeLabel } from "@/lib/chat-doc";

/**
 * 근거 카드 (§2 U-5) — `[유형 태그] 제목 →`.
 *
 * 누르면 어떻게 되는지가 **유형에 따라 갈린다**(spec v0.0.12 U-5):
 *
 *   company_product · career · problem  →  우측 문서 패널에서 그 자리에서 읽는다
 *   project · note                      →  전용 공개 페이지로 이동
 *
 * 셋을 패널로 여는 이유는 그 셋만 전용 페이지가 없어 url 이 `/career` 한 곳을
 * 가리키기 때문이다 — 눌러도 타임라인에 떨어질 뿐이라 채팅을 두고 읽는 편이 낫다.
 *
 * AI 가 **실제로 읽은** 문서만 온다(§3 S-9 — tool_result 폴딩). 프론트는 걸러내지
 * 않고 온 대로 그린다. 0건이면 아무것도 그리지 않는다.
 */
export function SourceCards({
  sources,
  onOpen,
}: {
  sources: ChatSource[];
  /** 패널로 여는 유형의 클릭. 없으면(패널이 없는 자리) 링크만 그린다. */
  onOpen?: (source: ChatSource) => void;
}) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="chat-sources">
      {sources.map((s) => {
        const inner = (
          <>
            <span className="tag-type">{sourceTypeLabel(s.type)}</span>
            {s.title}
            <span className="arrow">→</span>
          </>
        );
        const key = `${s.type}-${s.slug}`;

        if (onOpen && opensInPanel(s.type)) {
          return (
            <button key={key} type="button" onClick={() => onOpen(s)}>
              {inner}
            </button>
          );
        }
        // url 이 없는 유형은 링크를 걸지 않는다 — 카드만 그린다(BE ChatSourceItem.url: null).
        if (!s.url) return <span key={key}>{inner}</span>;
        return s.url.startsWith("http") ? (
          <a key={key} href={s.url} target="_blank" rel="noopener noreferrer">
            {inner}
          </a>
        ) : (
          <Link key={key} href={s.url}>
            {inner}
          </Link>
        );
      })}
    </div>
  );
}
