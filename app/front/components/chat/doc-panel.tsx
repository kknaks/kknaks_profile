"use client";

import Link from "next/link";
import { DocBody } from "@/components/markdown/doc-body";
import { ProseBody } from "@/components/markdown/prose-body";
import { sourceTypeLabel, type ChatDoc } from "@/lib/chat-doc";

/**
 * 문서 패널 (§2 U-5, spec v0.0.12) — 근거 카드를 누르면 **채팅을 두고 옆에서**
 * 그 문서를 읽는다. 페이지를 떠나지 않는 것이 요점이다.
 *
 * `/chat` 3열의 셋째 칸이다. 컨테이너 폭·좁은 화면 오버레이 전환은 CSS 몫이고
 * (`globals.css` `.chat-doc`), 이 컴포넌트는 머리·본문·바닥만 그린다.
 *
 * **스크롤 계약(U-5)을 지킨다** — 본문 칸만 `overflow-y: auto` 다. 머리(닫기)와
 * 바닥(보조 링크)은 붙박이고, 문서가 길어도 페이지는 스크롤하지 않는다.
 */
export function ChatDocPanel({
  doc,
  loading,
  error,
  onClose,
}: {
  /** 로딩 중에는 null 일 수 있다 — 머리는 먼저 그린다. */
  doc: ChatDoc | null;
  loading: boolean;
  error: string | null;
  onClose: () => void;
}) {
  return (
    <aside className="chat-doc" aria-label="근거 문서">
      <header className="chat-doc-head">
        <div className="chat-doc-title">
          {doc && <span className="tag-type">{sourceTypeLabel(doc.type)}</span>}
          <span className="t">{doc?.title ?? "불러오는 중…"}</span>
        </div>
        {doc?.subtitle && <div className="chat-doc-sub mono">{doc.subtitle}</div>}
        <button
          type="button"
          className="chat-doc-close mono"
          onClick={onClose}
          aria-label="문서 닫기"
        >
          ✕
        </button>
      </header>

      <div className="chat-doc-body">
        {loading ? (
          <div className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
            불러오는 중…
          </div>
        ) : error ? (
          <div className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
            // {error}
          </div>
        ) : doc?.render === "md" ? (
          // 회사 제품 showcase — 원장 md 라 이미지·mermaid 가 산다.
          <DocBody body={doc.body} assetBase={doc.assetBase} />
        ) : doc?.body?.trim() ? (
          // career · problem 은 detail_path 없이 컬럼에 든 글이다.
          <ProseBody body={doc.body} />
        ) : (
          <div className="mono" style={{ fontSize: 13, color: "var(--fg-3)" }}>
            // {"상세 — 준비 중"}
          </div>
        )}
      </div>

      {/* 보조 링크 — 패널은 읽는 자리고, 원래 페이지로 가는 문은 남겨 둔다. */}
      {doc?.url && (
        <footer className="chat-doc-foot">
          <Link href={doc.url} className="mono">
            페이지에서 보기 →
          </Link>
        </footer>
      )}
    </aside>
  );
}
