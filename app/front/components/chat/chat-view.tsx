"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import {
  ChatApiError,
  chatApi,
  hasPendingAssistant,
  sameId,
  useConversationPolling,
  type ChatId,
  type ChatMessage,
  type ChatSource,
  type Conversation,
  type ConversationDetail,
} from "@/lib/chat";
import { resolveChatDoc, type ChatDoc } from "@/lib/chat-doc";
import { AskBox } from "@/components/chat/ask-box";
import { ChatIntro } from "@/components/chat/chat-intro";
import { ChatThread } from "@/components/chat/chat-thread";
import { ChatDocPanel } from "@/components/chat/doc-panel";
import { ConversationSidebar } from "@/components/chat/conversation-sidebar";

/** §4 Case Matrix 의 프론트 출력 문구. spec 문구 그대로 — 바꾸지 않는다. */
const MSG_TOO_LONG = "질문은 1,000자까지 입력할 수 있습니다";
/** 계약에 없는 실패(네트워크 등)의 안내 — Case Matrix 밖이라 FE 가 정한 문구다. */
const MSG_SEND_FAILED = "질문을 보내지 못했습니다. 잠시 후 다시 시도해 주세요.";
/** 패널을 열었는데 번들을 못 읽었을 때. 매칭 실패는 이 문구가 아니라 페이지 이동이다. */
const MSG_DOC_FAILED = "근거 문서를 불러오지 못했습니다.";

/**
 * 「하단 근처」의 폭(px) — §2 U-5 스크롤 계약의 bottom-stick 판정.
 * 이 안에 있으면 새 내용을 따라가고, 벗어나 있으면(위를 읽는 중) 밀지 않는다.
 */
const BOTTOM_STICK_PX = 80;

/**
 * `/chat` 본체 (§2 U-3~U-6).
 *
 * 상태는 셋이다 — **빈 상태**(대화 없음) · **대화**(스레드 + 컴포저) ·
 * 그 위의 사이드바(대화가 하나라도 있으면). 대화 전환은 페이지 이동이 아니라
 * 스레드 교체다.
 *
 * 폴링은 `pending` assistant 가 있는 동안만 2초 간격으로 돌고 `done`/`failed`
 * 에서 멈춘다(§4). 대화를 옮기거나 화면을 떠나면 인터벌을 걷는다.
 */
export function ChatView() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [current, setCurrent] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [notice, setNotice] = useState<string | null>(null);
  const [loadingThread, setLoadingThread] = useState(false);

  const currentId: ChatId | null = current?.id ?? null;
  const pending = hasPendingAssistant(messages);

  // 늦게 온 응답이 새 스레드를 덮지 않게 — 요청마다 번호를 매겨 마지막 것만 반영한다.
  const openSeq = useRef(0);
  const currentIdRef = useRef<ChatId | null>(null);
  currentIdRef.current = currentId;

  const refreshList = useCallback(() => {
    chatApi
      .listConversations()
      .then(setConversations)
      // 목록 실패는 조용히 넘긴다 — 쿠키가 없으면 원래 빈 목록이다(§3 S-2).
      .catch(() => undefined);
  }, []);

  /** 404 — 없는 대화이거나 남의 세션이다. 빈 상태로 돌아간다(§4 Case Matrix). */
  const goEmpty = useCallback(() => {
    openSeq.current += 1;
    setCurrent(null);
    setMessages([]);
    setNotice(null);
  }, []);

  const applyDetail = useCallback((detail: ConversationDetail) => {
    setCurrent(detail.conversation);
    setMessages(detail.messages);
  }, []);

  const handleSendError = useCallback(
    (err: unknown) => {
      if (err instanceof ChatApiError) {
        if (err.status === 422) {
          setNotice(MSG_TOO_LONG);
          return;
        }
        if (err.status === 404) {
          goEmpty();
          refreshList();
          return;
        }
        if (err.status === 409) {
          // 잠금으로 선차단하지만, 다른 탭에서 먼저 보냈을 수 있다 — 현재 상태를 다시 읽는다.
          const id = currentIdRef.current;
          if (id != null) {
            chatApi
              .getConversation(id)
              .then((detail) => applyDetail(detail))
              .catch(() => undefined);
          }
          return;
        }
      }
      setNotice(MSG_SEND_FAILED);
    },
    [applyDetail, goEmpty, refreshList],
  );

  /** 새 대화 + 첫 질문(§3 S-1 · S-4). */
  const startConversation = useCallback(
    async (question: string): Promise<boolean> => {
      setNotice(null);
      const seq = ++openSeq.current;
      try {
        const detail = await chatApi.createConversation(question);
        if (seq !== openSeq.current) return true;
        applyDetail(detail);
        setConversations((prev) => [
          detail.conversation,
          ...prev.filter((c) => !sameId(c.id, detail.conversation.id)),
        ]);
        return true;
      } catch (err) {
        handleSendError(err);
        return false;
      }
    },
    [applyDetail, handleSendError],
  );

  /** 같은 대화에 이어서 질문(§3 S-3). */
  const continueConversation = useCallback(
    async (id: ChatId, question: string): Promise<boolean> => {
      setNotice(null);
      try {
        const { messages: added } = await chatApi.sendMessage(id, question);
        if (!sameId(id, currentIdRef.current)) return true;
        setMessages((prev) => [...prev, ...added]);
        return true;
      } catch (err) {
        handleSendError(err);
        return false;
      }
    },
    [handleSendError],
  );

  // ── 스크롤 (§2 U-5 스크롤 계약) ──────────────────────────────────────
  // 문서가 아니라 **스레드 컨테이너**의 scrollTop 을 다룬다. 페이지는 스크롤하지
  // 않으므로(globals.css `body:has(.chat-stage)`) 네비·사이드바·컴포저는 고정이다.
  const scrollRef = useRef<HTMLDivElement | null>(null);
  /** 하단에 붙어 있나 — true 인 동안만 새 내용을 따라간다. */
  const stickRef = useRef(true);

  const stickToBottom = useCallback(() => {
    stickRef.current = true;
  }, []);

  /**
   * 사용자가 손으로 올리면 붙임을 뗀다. 따라가는 스크롤은 `scrollTop` 대입이라
   * 한 프레임에 끝난다 — smooth 였다면 애니메이션 도중의 스크롤 이벤트가
   * 「하단 아님」으로 읽혀 답변이 자라는 동안 붙임이 풀렸다.
   */
  const handleThreadScroll = useCallback(() => {
    const el = scrollRef.current;
    if (!el) return;
    stickRef.current =
      el.scrollHeight - el.scrollTop - el.clientHeight <= BOTTOM_STICK_PX;
  }, []);

  const send = useCallback(
    (question: string) => {
      // 자기 행동의 결과는 위치와 무관하게 보여야 한다 — 보낼 때는 하단으로.
      stickToBottom();
      return currentId == null
        ? startConversation(question)
        : continueConversation(currentId, question);
    },
    [currentId, startConversation, continueConversation, stickToBottom],
  );

  /**
   * 실패한 답변의 「다시 시도」(§3 S-8 3항) — 전용 retry 엔드포인트를 부른다.
   * **그 자리의 failed 메시지가 pending 으로 돌아온다** — 새 줄을 만들지 않으므로
   * 스레드에 같은 질문이 두 번 보이지 않는다.
   */
  const retry = useCallback(
    async (messageId: ChatId) => {
      const id = currentIdRef.current;
      if (id == null) return;
      setNotice(null);
      try {
        const { message } = await chatApi.retryMessage(id, messageId);
        if (!sameId(id, currentIdRef.current)) return;
        setMessages((prev) =>
          prev.map((m) => (sameId(m.id, messageId) ? message : m)),
        );
      } catch (err) {
        handleSendError(err);
      }
    },
    [handleSendError],
  );

  const openConversation = useCallback(
    async (conversation: Conversation) => {
      if (sameId(conversation.id, currentIdRef.current)) return;
      const seq = ++openSeq.current;
      setNotice(null);
      setCurrent(conversation); // 사이드바 강조는 즉시
      setMessages([]);
      setLoadingThread(true);
      try {
        const detail = await chatApi.getConversation(conversation.id);
        if (seq !== openSeq.current) return;
        applyDetail(detail);
      } catch (err) {
        if (seq !== openSeq.current) return;
        if (err instanceof ChatApiError && err.status === 404) {
          goEmpty();
          refreshList();
        } else {
          setNotice(MSG_SEND_FAILED);
        }
      } finally {
        if (seq === openSeq.current) setLoadingThread(false);
      }
    },
    [applyDetail, goEmpty, refreshList],
  );

  // ── 첫 진입 — 목록 로드 + `?q=` 자동 전송(§3 S-1 의 4항) ──────────────
  const booted = useRef(false);
  useEffect(() => {
    if (booted.current) return;
    booted.current = true;

    refreshList();

    const q = searchParams.get("q")?.trim();
    if (q) {
      // 쿼리를 먼저 지운다 — 새로고침에 같은 질문이 다시 나가지 않게.
      router.replace("/chat");
      void startConversation(q);
    }
  }, [refreshList, router, searchParams, startConversation]);

  // ── 2초 폴링 — pending 동안만 ────────────────────────────────────────
  useConversationPolling({
    conversationId: currentId,
    active: pending,
    onTick: (detail) => {
      // 대화를 옮긴 뒤 도착한 응답은 버린다.
      if (!sameId(detail.conversation.id, currentIdRef.current)) return;
      applyDetail(detail);
    },
    onError: (err) => {
      if (err instanceof ChatApiError && err.status === 404) {
        goEmpty();
        refreshList();
      }
    },
  });

  // ── 모바일 대화 드로어 (§2 U-4, spec v0.0.13) ───────────────────────
  // ≤720px 에서만 쓰이지만 상태는 폭과 무관하게 둔다 — 넓은 화면에서는 CSS 가
  // 사이드바를 제자리에 세우므로 `nav-open` 이 붙어도 보이는 것이 달라지지 않는다.
  const [navOpen, setNavOpen] = useState(false);
  const closeNav = useCallback(() => setNavOpen(false), []);

  // ── 문서 패널 (§2 U-5, spec v0.0.12) ────────────────────────────────
  // 근거 카드를 누르면 3열의 셋째 칸이 열린다. 다른 카드를 누르면 **교체**된다 —
  // 패널을 여러 장 쌓지 않는다. 스레드는 그대로 보이고 자기 스크롤을 지킨다.
  const [doc, setDoc] = useState<ChatDoc | null>(null);
  const [docOpen, setDocOpen] = useState(false);
  const [docLoading, setDocLoading] = useState(false);
  const [docError, setDocError] = useState<string | null>(null);
  // 늦게 온 문서가 나중에 연 문서를 덮지 않게 — 스레드와 같은 번호 매기기.
  const docSeq = useRef(0);

  const closeDoc = useCallback(() => {
    docSeq.current += 1;
    setDocOpen(false);
    setDoc(null);
    setDocError(null);
    setDocLoading(false);
  }, []);

  const openSource = useCallback(
    async (source: ChatSource) => {
      const seq = ++docSeq.current;
      closeNav(); // 모바일에서 두 드로어가 겹치지 않게
      setDocOpen(true);
      setDoc(null);
      setDocError(null);
      setDocLoading(true);
      try {
        const resolved = await resolveChatDoc(source);
        if (seq !== docSeq.current) return;
        if (!resolved) {
          // 번들에서 못 찾았다 — 패널 대신 기존 url 이동으로 접는다(U-5 폴백).
          closeDoc();
          if (source.url) router.push(source.url);
          return;
        }
        setDoc(resolved);
      } catch {
        if (seq !== docSeq.current) return;
        setDocError(MSG_DOC_FAILED);
      } finally {
        if (seq === docSeq.current) setDocLoading(false);
      }
    },
    [closeDoc, closeNav, router],
  );

  // 대화를 옮기면 열려 있던 문서는 닫는다 — 다른 대화의 근거를 들고 있을 이유가 없다.
  useEffect(() => {
    closeDoc();
  }, [currentId, closeDoc]);

  // 대화를 열면 하단부터 — 붙임을 되돌린다.
  useEffect(() => {
    stickRef.current = true;
  }, [currentId]);

  // 새 내용(질문 추가 · 답변 도착 · 폴링으로 자라는 부분 텍스트)마다 돌지만,
  // **하단에 붙어 있을 때만** 따라간다. 위를 읽는 중이면 밀지 않는다.
  useEffect(() => {
    const el = scrollRef.current;
    if (!el || !stickRef.current) return;
    el.scrollTop = el.scrollHeight;
  }, [messages]);

  const showSidebar = conversations.length > 0;
  const inConversation = current != null;

  return (
    <main
      className={`chat-stage page-fade${docOpen ? " doc-open" : ""}${
        navOpen ? " nav-open" : ""
      }`}
    >
      {showSidebar && (
        <>
          {/* 모바일 드로어 손잡이 — CSS 가 ≤720px 에서만 보인다(U-4). */}
          <button
            type="button"
            className="chat-navbtn"
            onClick={() => setNavOpen(true)}
            aria-label="대화 목록 열기"
            aria-expanded={navOpen}
          >
            <i />
            <i />
            <i />
          </button>
          <div className="chat-nav-scrim" onClick={closeNav} aria-hidden />
          <ConversationSidebar
            conversations={conversations}
            currentId={currentId}
            onNew={() => {
              goEmpty();
              closeNav();
            }}
            onSelect={(c) => {
              void openConversation(c);
              closeNav();
            }}
          />
        </>
      )}

      <div className="chat-main">
        {!inConversation ? (
          // U-3 빈 상태 — 히어로와 같은 구성이되 스크롤 큐가 없다.
          <div className="chat-scroll">
            <ChatIntro onSubmit={send} />
            {notice && (
              <div style={{ display: "flex", justifyContent: "center" }}>
                <div className="chat-error">{notice}</div>
              </div>
            )}
          </div>
        ) : (
          <>
            {/* 이 페이지에서 유일하게 스크롤하는 자리(§2 U-5 스크롤 계약). */}
            <div
              className="chat-scroll"
              ref={scrollRef}
              onScroll={handleThreadScroll}
            >
              <div className="chat-thread">
                {loadingThread && messages.length === 0 ? (
                  <div className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
                    불러오는 중…
                  </div>
                ) : (
                  <ChatThread
                    messages={messages}
                    onRetry={(id) => void retry(id)}
                    onOpenSource={(s) => void openSource(s)}
                  />
                )}
              </div>
            </div>

            {/* U-6 컴포저 — 답변 대기 중에는 전송이 잠긴다(직렬화 · 409 선차단). */}
            <div className="chat-composer">
              <AskBox
                placeholder={pending ? "답변을 기다리는 중…" : "이어서 물어보세요"}
                disabled={pending}
                onSubmit={send}
              />
              {notice && <div className="chat-error">{notice}</div>}
            </div>
          </>
        )}
      </div>

      {/* 3열의 셋째 칸. 좁은 화면에서는 CSS 가 오버레이로 바꾸고, 그때만 뒤를
          덮는 막이 보인다(넓은 화면에서는 `display: none`). */}
      {docOpen && (
        <>
          <div className="chat-doc-scrim" onClick={closeDoc} aria-hidden />
          <ChatDocPanel
            doc={doc}
            loading={docLoading}
            error={docError}
            onClose={closeDoc}
          />
        </>
      )}
    </main>
  );
}
