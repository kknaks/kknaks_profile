"use client";

/**
 * 어드민 「채팅」 — 대화 열람 · 인사이트 (KDEV-SPEC-017 §2 U-8 / KDEV-WORK-025 P2).
 * 시각 정본: `21-html/admin-chat-mockup.html`.
 *
 * 화면은 둘이다 — **목록**(총계 줄 + 위젯 3종 + 대화 표) 과 **상세**(읽기 전용
 * 스레드). 시안처럼 한 페이지에서 갈아 끼운다. 상세로 들어가는 문은 둘 —
 * 최근 질문 피드의 행, 그리고 대화 표의 행.
 *
 * 데이터는 정적 로드다 — 폴링·WS 없음(WORK-025 Scope 「WS 갱신 제외」).
 * 인증 게이트는 `(panel)/layout.tsx` 가 이미 서 있고, 여기서는 조회 실패만 적는다.
 */

import { useEffect, useState } from "react";
import { AuthError } from "@/lib/api";
import {
  ADMIN_CHAT_PAGE_SIZE,
  adminChatApi,
  type AdminChatInsights,
  type AdminConversationDetail,
  type AdminConversationPage,
} from "@/lib/admin-chat";
import type { ChatId } from "@/lib/chat";
import {
  DailyQuestionsCard,
  RecentQuestionsCard,
  TopSourcesCard,
} from "@/components/admin/chat-widgets";
import { ChatConversationTable } from "@/components/admin/chat-conversation-table";
import { ChatDetailView } from "@/components/admin/chat-detail";

function errText(e: unknown): string {
  return e instanceof AuthError ? `${e.status} — ${e.message}` : String(e);
}

export default function AdminChatsPage() {
  const [insights, setInsights] = useState<AdminChatInsights | null>(null);
  const [list, setList] = useState<AdminConversationPage | null>(null);
  const [page, setPage] = useState(1);
  const [loadError, setLoadError] = useState<string | null>(null);

  // 상세 — 열린 대화의 id. null 이면 목록이다(시안의 `body.detail` 토글 자리).
  const [openId, setOpenId] = useState<ChatId | null>(null);
  const [detail, setDetail] = useState<AdminConversationDetail | null>(null);
  const [detailError, setDetailError] = useState<string | null>(null);

  // 인사이트 — 한 번만. 총계 줄과 위젯 3종이 이 한 응답을 나눠 쓴다.
  useEffect(() => {
    let alive = true;
    adminChatApi
      .insights()
      .then((d) => alive && setInsights(d))
      .catch((e) => alive && setLoadError(errText(e)));
    return () => {
      alive = false;
    };
  }, []);

  // 목록 — 쪽이 바뀌면 다시.
  useEffect(() => {
    let alive = true;
    adminChatApi
      .conversations(page, ADMIN_CHAT_PAGE_SIZE)
      .then((p) => {
        if (!alive) return;
        setList(p);
        setLoadError(null);
      })
      .catch((e) => alive && setLoadError(errText(e)));
    return () => {
      alive = false;
    };
  }, [page]);

  // 상세 — 연 대화가 바뀌면 다시. 늦게 온 응답이 다른 대화를 덮지 않게 가드한다.
  useEffect(() => {
    if (openId == null) return;
    let alive = true;
    setDetail(null);
    setDetailError(null);
    adminChatApi
      .conversation(openId)
      .then((d) => alive && setDetail(d))
      .catch((e) => alive && setDetailError(errText(e)));
    return () => {
      alive = false;
    };
  }, [openId]);

  function openDetail(id: ChatId) {
    setOpenId(id);
    // 시안의 `window.scrollTo(0,0)` — 스크롤 주체는 어드민 셸의 본문이다.
    document.querySelector(".admin-scroll")?.scrollTo(0, 0);
  }

  function closeDetail() {
    setOpenId(null);
    setDetail(null);
    document.querySelector(".admin-scroll")?.scrollTo(0, 0);
  }

  /* ── 상세 ─────────────────────────────────────────────────────────── */
  if (openId != null) {
    return (
      <div className="achat-wrap">
        {detailError ? (
          <>
            <button type="button" className="achat-back" onClick={closeDetail}>
              ← 목록으로
            </button>
            <p
              className="mono"
              style={{ fontSize: 12, color: "var(--danger)", marginTop: 14 }}
            >
              대화를 불러오지 못했습니다 — {detailError}
            </p>
          </>
        ) : detail ? (
          <ChatDetailView detail={detail} onBack={closeDetail} />
        ) : (
          <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
            불러오는 중…
          </p>
        )}
      </div>
    );
  }

  /* ── 목록 + 인사이트 ──────────────────────────────────────────────── */
  const totals = insights?.totals;

  return (
    <div className="achat-wrap">
      <div className="achat-head">
        <span className="crumb">admin /</span>
        <h1>채팅</h1>
        {totals && (
          <span className="count">
            대화 {totals.conversations} · 질문 {totals.questions} · 최근 7일 +
            {totals.last7d}
          </span>
        )}
      </div>

      {loadError && (
        <p className="mono" style={{ fontSize: 12, color: "var(--danger)", marginBottom: 12 }}>
          불러오지 못했습니다 — {loadError}
        </p>
      )}

      <div className="achat-widgets">
        <RecentQuestionsCard
          items={insights?.recentQuestions ?? []}
          onOpen={openDetail}
        />
        <DailyQuestionsCard
          daily={insights?.daily ?? []}
          totalQuestions={totals?.questions ?? 0}
        />
        <TopSourcesCard items={insights?.topSources ?? []} />
      </div>

      <ChatConversationTable
        items={list?.items ?? []}
        total={list?.total ?? 0}
        page={list?.page ?? page}
        size={list?.size ?? ADMIN_CHAT_PAGE_SIZE}
        onPage={setPage}
        onOpen={openDetail}
      />
    </div>
  );
}
