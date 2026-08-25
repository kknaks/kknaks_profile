"use client";

import { useMemo, useState } from "react";
import ReactMarkdown, { defaultUrlTransform } from "react-markdown";

import { api, assetUrl } from "@/lib/api";
import type { NoteDetail, NoteItem } from "@/lib/types";

/**
 * 공개 글 — 탐색기형 레이아웃. 왼쪽 = 디렉토리 트리, 오른쪽 = md 뷰.
 *
 * `folder` 는 컬럼이 아니다 — `detail_path` 의 note/ 이하 첫 디렉토리를 백엔드가
 * 파생해 내려준 것이고, 트리는 그 값으로 묶기만 한다(분류 SoT 는 원장 디렉토리).
 *
 * `/notes` 와 `/notes/[slug]` 가 같은 컴포넌트를 그린다 — 직접 URL 진입은
 * 서버가 `initialDetail` 로 채우고, 트리 클릭은 클라이언트에서 fetch 한 뒤
 * `history.replaceState` 로 URL 만 맞춘다. 서버 재렌더를 안 타는 이유는
 * 트리의 펼침 상태를 잃지 않기 위해서다.
 */
export function NotesExplorer({
  items,
  initialDetail,
}: {
  items: NoteItem[];
  initialDetail: NoteDetail | null;
}) {
  const [detail, setDetail] = useState<NoteDetail | null>(initialDetail);
  const [loadingSlug, setLoadingSlug] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [open, setOpen] = useState<Set<string>>(
    () => new Set(initialDetail ? [initialDetail.folder] : []),
  );

  // 폴더별 묶음 — items 는 이미 publishedOn DESC 라 폴더 안 순서도 그것을 따른다.
  const folders = useMemo(() => {
    const map = new Map<string, NoteItem[]>();
    for (const note of items) {
      const key = note.folder || "etc";
      const list = map.get(key);
      if (list) list.push(note);
      else map.set(key, [note]);
    }
    return [...map.entries()].sort(([a], [b]) => a.localeCompare(b));
  }, [items]);

  const toggle = (folder: string) =>
    setOpen((prev) => {
      const next = new Set(prev);
      if (next.has(folder)) next.delete(folder);
      else next.add(folder);
      return next;
    });

  const select = async (note: NoteItem) => {
    if (detail?.slug === note.slug || loadingSlug) return;
    setLoadingSlug(note.slug);
    setError(null);
    try {
      const data = await api.noteDetail(note.slug);
      setDetail(data["notes.detail"]);
      window.history.replaceState(null, "", `/notes/${note.slug}`);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoadingSlug(null);
    }
  };

  return (
    <div
      className="pad-x m-stack notes-explorer"
      style={{
        display: "grid",
        gridTemplateColumns: "300px minmax(0, 1fr)",
        gap: 48,
        padding: "40px 80px 80px",
        alignItems: "start",
      }}
    >
      <style>{`
        /* 태블릿만 — 모바일(≤720px)은 globals 의 m-stack 이 1열로 무너뜨린다.
           하한 없이 두면 이 규칙이 m-stack 을 이겨 모바일에서도 2열이 된다. */
        @media (max-width: 1024px) and (min-width: 721px) {
          .notes-explorer { grid-template-columns: 220px minmax(0, 1fr) !important; gap: 32px !important; }
        }
      `}</style>
      {/* ── 왼쪽: 디렉토리 트리 ── */}
      <nav aria-label="노트 디렉토리">
        <div
          className="mono"
          style={{ fontSize: 11, color: "var(--accent)", marginBottom: 14 }}
        >
          {"// directory"}
        </div>
        <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
          {folders.map(([folder, notes]) => {
            const isOpen = open.has(folder);
            return (
              <li key={folder} style={{ marginBottom: 4 }}>
                <button
                  type="button"
                  onClick={() => toggle(folder)}
                  className="mono"
                  style={{
                    display: "flex",
                    alignItems: "baseline",
                    gap: 8,
                    width: "100%",
                    padding: "7px 8px",
                    background: "none",
                    border: "none",
                    cursor: "pointer",
                    fontSize: 12,
                    color: isOpen ? "var(--fg-0)" : "var(--fg-2)",
                    textAlign: "left",
                  }}
                >
                  <span style={{ color: "var(--fg-3)", fontSize: 10 }}>
                    {isOpen ? "▾" : "▸"}
                  </span>
                  <span>{folder}/</span>
                  <span style={{ color: "var(--fg-4)", fontSize: 11 }}>
                    {notes.length}
                  </span>
                </button>
                {isOpen && (
                  <ul
                    style={{
                      listStyle: "none",
                      margin: "2px 0 8px",
                      padding: 0,
                      borderLeft: "1px solid var(--line-1)",
                      marginLeft: 12,
                    }}
                  >
                    {notes.map((note) => {
                      const selected = detail?.slug === note.slug;
                      return (
                        <li key={note.slug}>
                          <button
                            type="button"
                            onClick={() => select(note)}
                            style={{
                              display: "block",
                              width: "100%",
                              padding: "6px 12px",
                              background: "none",
                              border: "none",
                              borderLeft: selected
                                ? "2px solid var(--accent)"
                                : "2px solid transparent",
                              marginLeft: -1,
                              cursor: "pointer",
                              textAlign: "left",
                              fontSize: 13,
                              lineHeight: 1.45,
                              color: selected ? "var(--fg-0)" : "var(--fg-2)",
                              opacity: loadingSlug === note.slug ? 0.5 : 1,
                            }}
                          >
                            {note.title}
                          </button>
                        </li>
                      );
                    })}
                  </ul>
                )}
              </li>
            );
          })}
        </ul>
      </nav>

      {/* ── 오른쪽: 마크다운 뷰 ── */}
      <section style={{ minWidth: 0 }}>
        {error && (
          <p className="mono" style={{ fontSize: 12, color: "var(--danger)" }}>
            불러오기 실패: {error}
          </p>
        )}
        {detail ? (
          <article key={detail.slug}>
            <div
              className="mono"
              style={{
                display: "flex",
                alignItems: "baseline",
                gap: 12,
                flexWrap: "wrap",
                fontSize: 11,
                color: "var(--fg-3)",
                marginBottom: 10,
              }}
            >
              <span>
                {detail.folder}/{detail.slug}
              </span>
              {detail.publishedOn && <span>{detail.publishedOn}</span>}
            </div>
            <h2
              style={{
                margin: "0 0 8px",
                fontSize: 26,
                lineHeight: 1.25,
                letterSpacing: "-0.015em",
                fontWeight: 600,
              }}
            >
              {detail.title}
            </h2>
            {!!detail.tags?.length && (
              <div
                className="mono"
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: 8,
                  fontSize: 10,
                  color: "var(--fg-4)",
                }}
              >
                {detail.tags.map((tag) => (
                  <span key={tag}>#{tag}</span>
                ))}
              </div>
            )}
            <div
              style={{
                borderTop: "1px solid var(--line-1)",
                margin: "20px 0 24px",
              }}
            />
            {/* md 본문 타이포는 contents-body 한 곳이 정한다. 이미지 상대참조는
                원장(md) 디렉토리 기준 — para 를 서빙하는 백엔드 /api/assets 로 푼다. */}
            <article className="contents-body" style={{ maxWidth: 860 }}>
              <ReactMarkdown
                urlTransform={(url, key) =>
                  key === "src" && !/^(https?:|data:|\/)/.test(url)
                    ? assetUrl(
                        `para/resources/note/${detail.folder}/${url.replace(/^\.\//, "")}`,
                      )
                    : defaultUrlTransform(url)
                }
              >
                {detail.body}
              </ReactMarkdown>
            </article>
          </article>
        ) : (
          <div
            className="mono"
            style={{
              fontSize: 12,
              color: "var(--fg-3)",
              padding: "48px 0",
            }}
          >
            {"// 왼쪽 디렉토리에서 노트를 선택하세요"}
          </div>
        )}
      </section>
    </div>
  );
}
