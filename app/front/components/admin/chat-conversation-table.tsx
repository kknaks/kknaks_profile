"use client";

/**
 * 대화 목록 표 + 페이지네이션 (KDEV-SPEC-017 §2 U-8).
 * 시각 정본: `21-html/admin-chat-mockup.html` 의 `table` · `.pager`.
 *
 * 열은 시안 그대로 — 시작 질문(=제목) · 세션 · 메시지 수 · 시작 · 최근. 최신순은
 * 서버가 준 순서다(계약) — 여기서 다시 정렬하지 않는다. 행 클릭 = 읽기 전용 상세.
 */

import type { AdminConversationRow } from "@/lib/admin-chat";
import type { ChatId } from "@/lib/chat";

/** `2026-08-29T10:03:00+09:00` → `08-29 10:03`. 파싱 없이 자른다(커밋 화면 관례). */
function fmtStart(iso: string): string {
  return `${iso.slice(5, 7)}-${iso.slice(8, 10)} ${iso.slice(11, 16)}`;
}

/** 「최근」 칸은 시작과 같은 날이면 시각만(시안) — 아니면 날짜까지 보인다. */
function fmtLast(last: string, start: string): string {
  return last.slice(0, 10) === start.slice(0, 10) ? last.slice(11, 16) : fmtStart(last);
}

/** 페이지 번호 창 — 현재 쪽 둘레만 그리고 끝은 `… N` 으로 접는다(시안 `1 2 3 … 8`). */
function pageWindow(page: number, totalPages: number, span = 3): number[] {
  const start = Math.max(1, Math.min(page - Math.floor(span / 2), totalPages - span + 1));
  return Array.from({ length: Math.min(span, totalPages) }, (_, i) => start + i);
}

export function ChatConversationTable({
  items,
  total,
  page,
  size,
  onPage,
  onOpen,
}: {
  items: AdminConversationRow[];
  total: number;
  page: number;
  size: number;
  onPage: (page: number) => void;
  onOpen: (id: ChatId) => void;
}) {
  const totalPages = Math.max(1, Math.ceil(total / Math.max(1, size)));
  const win = pageWindow(page, totalPages);

  return (
    <div className="achat-tablecard">
      <table className="achat-table">
        <thead>
          <tr>
            <th>시작 질문</th>
            <th>세션</th>
            <th className="num">메시지</th>
            <th>시작</th>
            <th>최근</th>
          </tr>
        </thead>
        <tbody>
          {items.length === 0 ? (
            <tr style={{ cursor: "default" }}>
              <td colSpan={5}>
                <span className="achat-empty">대화가 없습니다</span>
              </td>
            </tr>
          ) : (
            items.map((c) => (
              <tr key={String(c.id)} onClick={() => onOpen(c.id)}>
                <td title={c.title}>{c.title}</td>
                <td className="sid">s#{String(c.sessionId)}</td>
                <td className="num">{c.messageCount}</td>
                <td className="tt">{fmtStart(c.createdAt)}</td>
                <td className="tt">{fmtLast(c.lastMessageAt, c.createdAt)}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>

      <div className="achat-pager">
        <span style={{ marginRight: "auto" }}>총 {total}건</span>
        <button type="button" onClick={() => onPage(page - 1)} disabled={page <= 1}>
          ◀
        </button>
        {win.map((p) => (
          <button
            key={p}
            type="button"
            className={p === page ? "on" : undefined}
            onClick={() => onPage(p)}
          >
            {p}
          </button>
        ))}
        {win[win.length - 1] < totalPages && <span>… {totalPages}</span>}
        <button
          type="button"
          onClick={() => onPage(page + 1)}
          disabled={page >= totalPages}
        >
          ▶
        </button>
      </div>
    </div>
  );
}
