"use client";

import { useEffect, useState } from "react";
import {
  QueueError,
  queueApi,
  type ConceptPayload,
  type ConceptResult,
  type Gate,
  type DailyCollection,
  type DailyDraft,
  type DailyPayload,
  type GatePayload,
  type NotePayload,
  type RouteResult,
} from "@/lib/api";

/* 게이트 카드 — KDEV-SPEC-008 U-3 / SPEC-009 U-4.
 *
 * 카드에 **인라인 입력창을 두지 않는다.** 버튼은 `피드백`·`승인` 둘뿐이고, 피드백은
 * 모달에서 받는다. 카드 안에 입력창이 있으면 "적다 말고 승인"이 쉬워진다.
 *
 * 승인된 게이트는 접는다. 지금 봐야 할 것 하나만 펼쳐져 있어야 한다.
 *
 * **두 가지 "진행 중"을 섞지 않는다** (KDEV-WORK-016 P3).
 *
 *     busy            내 요청이 나가 있는 짧은 순간. 응답은 1초 안에 온다.
 *     generating      서버가 AI 로 제안을 만드는 중. 30~60초. 폴링이 감지한다.
 *
 * 섞으면 "버튼이 안 먹은 것"과 "AI 가 도는 것"이 같은 모양이 되어, 사람이 다시 누른다.
 */

const STAGE_LABEL: Record<string, string> = {
  route: "목적지",
  source_note: "자료 노트",
  concept: "개념",
  derived: "교안",
  daily: "잔디",
};

const STATUS_LABEL: Record<string, { text: string; tone: "wait" | "ok" | "bad" | "idle" }> = {
  not_started: { text: "대기", tone: "idle" },
  generating: { text: "생성 중", tone: "wait" },
  review_pending: { text: "검토 대기", tone: "wait" },
  feedback_pending: { text: "피드백 반영 대기", tone: "wait" },
  regenerating: { text: "재생성 중", tone: "wait" },
  approved: { text: "승인됨", tone: "ok" },
  failed: { text: "실패", tone: "bad" },
  cancelled: { text: "무효화됨", tone: "idle" },
};

const TONE: Record<string, string> = {
  wait: "var(--accent)",
  ok: "#3fb950",
  bad: "#f85149",
  idle: "var(--fg-3)",
};

const box = {
  border: "1px solid var(--line-2)",
  borderRadius: 6,
  background: "var(--bg-1)",
};

/** 서버가 지금 만들고 있는 게이트 — 화면은 폴링하고 조작은 잠근다. */
export function gateInFlight(gate: { status: string }): boolean {
  return gate.status === "generating" || gate.status === "regenerating";
}

function Badge({ status }: { status: string }) {
  const meta = STATUS_LABEL[status] ?? { text: status, tone: "idle" as const };
  return (
    <span
      className="mono"
      style={{
        fontSize: 10,
        letterSpacing: "0.06em",
        color: TONE[meta.tone],
        border: `1px solid ${TONE[meta.tone]}`,
        borderRadius: 3,
        padding: "1px 6px",
      }}
    >
      {meta.text}
    </span>
  );
}

function emptyRoute(): RouteResult {
  return {
    destinations: {
      reference: { enabled: false },
      concept: { enabled: false },
      derived: { enabled: false },
    },
    exclusive: null,
  };
}

/** 목적지 토글 — 승인 대상은 AI 제안이 아니라 **여기서 사람이 고친 결과**다. */
function RouteEditor({
  value,
  disabled,
  onChange,
}: {
  value: RouteResult;
  disabled: boolean;
  onChange: (next: RouteResult) => void;
}) {
  const d = value.destinations;
  const anyEnabled = d.reference.enabled || d.concept.enabled || d.derived.enabled;

  function toggle(key: "reference" | "concept" | "derived", enabled: boolean) {
    onChange({
      ...value,
      // 목적지를 켜면 exclusive 는 자동으로 풀린다 — 서버가 동시 설정을 거부한다.
      exclusive: enabled ? null : value.exclusive,
      destinations: { ...d, [key]: { ...d[key], enabled } },
    });
  }

  function setExclusive(next: RouteResult["exclusive"]) {
    onChange({
      ...value,
      exclusive: next,
      destinations: next
        ? {
            reference: { ...d.reference, enabled: false },
            concept: { enabled: false },
            derived: { enabled: false },
          }
        : d,
    });
  }

  const row = {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "8px 10px",
    borderTop: "1px solid var(--line-1)",
  } as const;

  return (
    <div style={{ ...box, marginTop: 10 }}>
      <div style={{ padding: "8px 10px", fontSize: 12, color: "var(--fg-2)" }}>
        만들 것
      </div>

      <label style={row}>
        <input
          type="checkbox"
          checked={d.reference.enabled}
          disabled={disabled}
          onChange={(e) => toggle("reference", e.target.checked)}
        />
        <span style={{ fontSize: 13, color: "var(--fg-1)", flex: 1 }}>
          자료 노트 <span style={{ color: "var(--fg-3)" }}>reference/</span>
        </span>
      </label>

      <label style={row}>
        <input
          type="checkbox"
          checked={d.concept.enabled}
          disabled={disabled}
          onChange={(e) => toggle("concept", e.target.checked)}
        />
        <span style={{ fontSize: 13, color: "var(--fg-1)", flex: 1 }}>
          개념 <span style={{ color: "var(--fg-3)" }}>permanent/concept/</span>
        </span>
      </label>

      <label style={row}>
        <input
          type="checkbox"
          checked={d.derived.enabled}
          disabled={disabled}
          onChange={(e) => toggle("derived", e.target.checked)}
        />
        <span style={{ fontSize: 13, color: "var(--fg-1)", flex: 1 }}>
          교안 <span style={{ color: "var(--fg-3)" }}>persona/contents/</span>
        </span>
      </label>

      <div style={{ ...row, gap: 8 }}>
        <span style={{ fontSize: 12, color: "var(--fg-3)", flex: 1 }}>
          아무것도 안 만든다면
        </span>
        {(
          [
            [null, "—"],
            ["inbox_hold", "보류"],
            ["discard", "폐기"],
          ] as const
        ).map(([key, label]) => (
          <button
            key={String(key)}
            type="button"
            disabled={disabled || (anyEnabled && key !== null)}
            onClick={() => setExclusive(key)}
            className="mono"
            style={{
              fontSize: 11,
              padding: "3px 9px",
              borderRadius: 4,
              cursor: disabled ? "default" : "pointer",
              border: `1px solid ${value.exclusive === key ? "var(--accent)" : "var(--line-2)"}`,
              background: value.exclusive === key ? "var(--accent-soft)" : "transparent",
              color: value.exclusive === key ? "var(--accent)" : "var(--fg-2)",
              opacity: anyEnabled && key !== null ? 0.4 : 1,
            }}
          >
            {label}
          </button>
        ))}
      </div>

      {value.exclusive === "discard" && (
        <div style={{ ...row, color: "#f85149", fontSize: 12 }}>
          승인하면 이 항목은 종료되고 아무 파일도 만들어지지 않습니다.
        </div>
      )}
    </div>
  );
}

function isNote(payload: GatePayload | null | undefined): payload is NotePayload {
  return !!payload && "filename_stem" in payload;
}

/** 노트 초안 미리보기 — 전문과 **저장될 경로**를 함께 보여준다.
 *
 * 경로를 감추면 "어디에 생기는지 모른 채 승인"하게 된다. AI 는 stem 만 내고
 * 디렉토리는 시스템이 조립하므로, 그 결과를 사람이 확인할 수 있어야 한다. */
function NotePreview({ payload }: { payload: NotePayload }) {
  const [expanded, setExpanded] = useState(false);
  const lines = payload.content.split("\n");
  const shown = expanded ? payload.content : lines.slice(0, 24).join("\n");

  return (
    <div style={{ marginTop: 10 }}>
      <div
        className="mono"
        style={{
          fontSize: 11,
          color: "var(--fg-2)",
          padding: "6px 10px",
          border: "1px solid var(--line-2)",
          borderRadius: "5px 5px 0 0",
          background: "var(--bg-0)",
          wordBreak: "break-all",
        }}
      >
        {payload.target_path ?? `${payload.filename_stem}.md`}
      </div>
      <pre
        style={{
          margin: 0,
          padding: 12,
          fontSize: 11.5,
          lineHeight: 1.6,
          color: "var(--fg-1)",
          background: "var(--bg-0)",
          border: "1px solid var(--line-2)",
          borderTop: "none",
          borderRadius: expanded || lines.length <= 24 ? "0 0 5px 5px" : 0,
          overflowX: "auto",
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
        }}
      >
        {shown}
      </pre>
      {lines.length > 24 && (
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className="mono"
          style={{
            width: "100%",
            fontSize: 10.5,
            padding: "5px 0",
            border: "1px solid var(--line-2)",
            borderTop: "none",
            borderRadius: "0 0 5px 5px",
            background: "var(--bg-1)",
            color: "var(--fg-3)",
            cursor: "pointer",
          }}
        >
          {expanded ? "접기" : `전문 보기 (${lines.length}줄)`}
        </button>
      )}
    </div>
  );
}

function isConcepts(payload: GatePayload | null | undefined): payload is ConceptPayload {
  return !!payload && "concepts" in payload;
}

/** 보충 diff — **사라지는 줄**을 눈에 띄게 한다.
 *
 * 보충은 덧붙이기가 아니라 다시 쓰기다. 무엇이 빠지는지가 승인 판단의 핵심이라
 * 삭제 줄을 색으로 구분한다. */
function Diff({ text }: { text: string }) {
  return (
    <pre
      style={{
        margin: "8px 0 0",
        padding: 10,
        fontSize: 11,
        lineHeight: 1.55,
        background: "var(--bg-0)",
        border: "1px solid var(--line-2)",
        borderRadius: 5,
        overflowX: "auto",
        maxHeight: 320,
      }}
    >
      {text.split("\n").map((line, i) => {
        const removed = line.startsWith("-") && !line.startsWith("---");
        const added = line.startsWith("+") && !line.startsWith("+++");
        return (
          <div
            key={i}
            style={{
              color: removed ? "#f85149" : added ? "#3fb950" : "var(--fg-3)",
              background: removed ? "rgba(248,81,73,0.08)" : "transparent",
              whiteSpace: "pre-wrap",
              wordBreak: "break-all",
            }}
          >
            {line || " "}
          </div>
        );
      })}
    </pre>
  );
}

/** 개념 묶음 — **개별 승인하지 않는다.**
 *
 * 개념 수만큼 승인 횟수가 늘면 마찰이 폭발한다(SPEC-008). 원하지 않는 개념만
 * 제외 토글로 빼고 게이트 하나로 승인한다. */
function ConceptList({
  concepts,
  disabled,
  onChange,
}: {
  concepts: ConceptResult[];
  disabled: boolean;
  onChange: (next: ConceptResult[]) => void;
}) {
  const [openStem, setOpenStem] = useState<string | null>(null);

  if (concepts.length === 0) {
    return (
      <p style={{ fontSize: 12.5, color: "var(--fg-3)", marginTop: 10 }}>
        뽑을 개념이 없다고 판단했습니다. 억지로 만들지 않습니다.
      </p>
    );
  }

  return (
    <div style={{ marginTop: 10 }}>
      {concepts.map((c) => {
        const open = openStem === c.stem;
        const supplement = c.mode === "supplement";
        return (
          <div
            key={c.stem}
            style={{
              ...box,
              marginBottom: 8,
              opacity: c.excluded ? 0.45 : 1,
            }}
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                padding: "9px 10px",
              }}
            >
              <input
                type="checkbox"
                checked={!c.excluded}
                disabled={disabled}
                title={c.excluded ? "발행에서 제외됨" : "발행에 포함"}
                onChange={(e) =>
                  onChange(
                    concepts.map((x) =>
                      x.stem === c.stem ? { ...x, excluded: !e.target.checked } : x,
                    ),
                  )
                }
              />
              <span
                className="mono"
                style={{
                  fontSize: 10,
                  padding: "1px 6px",
                  borderRadius: 3,
                  border: `1px solid ${supplement ? "var(--accent)" : "#3fb950"}`,
                  color: supplement ? "var(--accent)" : "#3fb950",
                }}
              >
                {supplement ? "보충" : "신규"}
              </span>
              <span
                className="mono"
                style={{ fontSize: 12, color: "var(--fg-1)", flex: 1, wordBreak: "break-all" }}
              >
                {c.stem}
              </span>
              <button
                type="button"
                onClick={() => setOpenStem(open ? null : c.stem)}
                className="mono"
                style={{
                  fontSize: 10.5,
                  padding: "3px 8px",
                  border: "1px solid var(--line-2)",
                  borderRadius: 4,
                  background: "transparent",
                  color: "var(--fg-2)",
                  cursor: "pointer",
                }}
              >
                {open ? "접기" : supplement ? "변경 보기" : "전문 보기"}
              </button>
            </div>

            {supplement && c.matched_by && (
              <div
                style={{
                  padding: "0 10px 8px 38px",
                  fontSize: 11.5,
                  color: "var(--fg-3)",
                }}
              >
                기존 <b style={{ color: "var(--fg-2)" }}>{c.stem}</b> 와 같은 개념으로 봤습니다
                {" — "}
                <span className="mono">{c.matched_by}</span> 로 일치
              </div>
            )}

            {open && (
              <div style={{ padding: "0 10px 10px" }}>
                <div className="mono" style={{ fontSize: 10.5, color: "var(--fg-4)" }}>
                  {c.target_path}
                </div>
                {supplement && c.diff ? (
                  <Diff text={c.diff} />
                ) : (
                  <pre
                    style={{
                      margin: "8px 0 0",
                      padding: 10,
                      fontSize: 11,
                      lineHeight: 1.6,
                      background: "var(--bg-0)",
                      border: "1px solid var(--line-2)",
                      borderRadius: 5,
                      overflowX: "auto",
                      maxHeight: 320,
                      whiteSpace: "pre-wrap",
                      wordBreak: "break-word",
                    }}
                  >
                    {c.content}
                  </pre>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

function isDaily(payload: GatePayload | null | undefined): payload is DailyPayload {
  return !!payload && typeof payload === "object" && "daily" in payload;
}

/** 본문을 **줄 단위**로 쪼갠다. 섹션 제목(`## …`)은 토글 대상이 아니다. */
type CareerLine = { text: string; heading: boolean; keep: boolean; added: boolean };

function splitCareer(content: string, previous: string): CareerLine[] {
  const before = new Set(
    previous
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean),
  );
  return content.split("\n").map((raw) => {
    const text = raw.trimEnd();
    const heading = text.trimStart().startsWith("#");
    return {
      text,
      heading,
      keep: true,
      // 기존 문서에 없던 줄만 표시한다 — career 는 대개 조금씩만 바뀌므로
      // 좌우 비교는 과하고, 바뀐 곳만 눈에 띄면 된다.
      added: !heading && !!text.trim() && !before.has(text.trim()),
    };
  });
}

function joinCareer(lines: CareerLine[]): string {
  return lines
    .filter((l) => l.keep)
    .map((l) => l.text)
    .join("\n");
}

/**
 * 조사 진행 표시 — 승인 전에 **자료가 온전한지**를 먼저 보여준다.
 *
 * 편집 대상이 아니다. `counts` 와 같은 이유로 **표시만** 한다 — 코드가 센 값이라
 * 화면이 고칠 수 있으면 안 된다. 전부 온전하면 한 줄로 접히고, 빠진 것이 있을 때만
 * 눈에 띈다. 늘 경고를 띄우면 아무도 안 본다.
 */
function CollectionStatus({ collection }: { collection: DailyCollection }) {
  const truncated = Object.entries(collection.truncated ?? {});
  const careerMissing = collection.career_missing ?? [];
  const clean =
    collection.done === collection.total &&
    collection.missing.length === 0 &&
    collection.failed.length === 0 &&
    truncated.length === 0 &&
    careerMissing.length === 0;

  return (
    <section
      style={{
        padding: "6px 8px",
        borderRadius: 4,
        border: `1px solid ${clean ? "var(--line-2)" : "var(--warn, #b45309)"}`,
        background: "var(--bg-2)",
      }}
    >
      <p className="mono" style={{ fontSize: 11, color: "var(--fg-3)", margin: 0 }}>
        조사 {collection.done}/{collection.total}
        {clean && " · 빠진 레포 없음"}
      </p>

      {collection.failed.length > 0 && (
        <p className="mono" style={{ fontSize: 11, color: "var(--fg-4)", margin: "4px 0 0" }}>
          조사 못 함 {collection.failed.length}건 —{" "}
          {collection.failed
            .map((f) => `${f.repo ?? "?"}${f.code ? ` (${f.code})` : ""}`)
            .join(", ")}
        </p>
      )}

      {collection.missing.length > 0 && (
        <p className="mono" style={{ fontSize: 11, color: "var(--fg-4)", margin: "4px 0 0" }}>
          결과 안 돌아옴 {collection.missing.length}건 — {collection.missing.join(", ")}
        </p>
      )}

      {truncated.length > 0 && (
        <p className="mono" style={{ fontSize: 11, color: "var(--fg-4)", margin: "4px 0 0" }}>
          입력 상한 적용 — {truncated.map(([repo]) => repo).join(", ")} (일부 diff 생략)
        </p>
      )}

      {careerMissing.length > 0 && (
        <p className="mono" style={{ fontSize: 11, color: "var(--warn, #b45309)", margin: "4px 0 0" }}>
          career 대상 없음 — {careerMissing.join(", ")} (레지스트리의 `detail` 을 확인하세요).
          이 레포들의 오늘 작업은 **어느 career 에도 실리지 않습니다.**
        </p>
      )}

      {!clean && (
        <p style={{ fontSize: 11, color: "var(--fg-4)", margin: "4px 0 0" }}>
          서술이 얕다면 그날 일이 적어서가 아니라 자료가 빠져서일 수 있습니다.
        </p>
      )}
    </section>
  );
}

function DailyReview({
  payload,
  draft,
  disabled,
  previousCareer,
  onChange,
}: {
  payload: DailyPayload;
  draft: DailyPayload;
  disabled: boolean;
  previousCareer: string;
  onChange: (next: DailyPayload) => void;
}) {
  const [careerLines, setCareerLines] = useState<CareerLine[]>(() =>
    splitCareer(payload.career.content ?? "", previousCareer),
  );
  const [showPrevious, setShowPrevious] = useState(false);

  useEffect(() => {
    setCareerLines(splitCareer(payload.career.content ?? "", previousCareer));
  }, [payload.career.content, previousCareer]);

  function setDaily(patch: Partial<DailyDraft>) {
    onChange({ ...draft, daily: { ...draft.daily, ...patch } });
  }

  function setLines(next: CareerLine[]) {
    setCareerLines(next);
    onChange({
      ...draft,
      career: { ...draft.career, content: joinCareer(next) },
    });
  }

  const counts = draft.daily.counts ?? {};
  const total = (counts.commit ?? 0) + (counts.note ?? 0) + (counts.study ?? 0);

  return (
    <div style={{ marginTop: 10, display: "grid", gap: 14 }}>
      {/* --- 조사 상태 (편집 불가) ------------------------------------------ */}
      {payload.collection && <CollectionStatus collection={payload.collection} />}

      {/* --- daily --------------------------------------------------------- */}
      <section>
        <h4 className="mono" style={{ fontSize: 12, color: "var(--fg-3)", margin: "0 0 6px" }}>
          daily · {draft.daily.date}
        </h4>
        <p className="mono" style={{ fontSize: 11, color: "var(--fg-4)", margin: "0 0 8px" }}>
          commit {counts.commit ?? 0} · note {counts.note ?? 0} · study {counts.study ?? 0}
          {"  "}(합계 {total} — 코드가 센 값이라 고칠 수 없습니다)
        </p>

        {(["ko", "en"] as const).map((lang) => (
          <div key={lang} style={{ marginBottom: 8 }}>
            <p className="mono" style={{ fontSize: 11, color: "var(--fg-4)", margin: "0 0 4px" }}>
              요약 ({lang})
            </p>
            {(draft.daily.summary?.[lang] ?? []).length === 0 && (
              <p style={{ fontSize: 12, color: "var(--fg-4)" }}>줄이 없습니다.</p>
            )}
            {(draft.daily.summary?.[lang] ?? []).map((line, i) => (
              <div key={i} style={{ display: "flex", gap: 6, marginBottom: 4 }}>
                <input
                  value={line}
                  disabled={disabled}
                  onChange={(e) => {
                    const next = [...(draft.daily.summary?.[lang] ?? [])];
                    next[i] = e.target.value;
                    setDaily({ summary: { ...draft.daily.summary, [lang]: next } });
                  }}
                  className="mono"
                  style={{
                    flex: 1,
                    fontSize: 12,
                    padding: "4px 6px",
                    background: "var(--bg-2)",
                    border: "1px solid var(--line-2)",
                    borderRadius: 4,
                    color: "var(--fg-1)",
                  }}
                />
                <button
                  type="button"
                  disabled={disabled}
                  title="이 줄을 지웁니다"
                  onClick={() => {
                    const next = (draft.daily.summary?.[lang] ?? []).filter((_, j) => j !== i);
                    setDaily({ summary: { ...draft.daily.summary, [lang]: next } });
                  }}
                  style={{ ...btn("ghost"), padding: "2px 8px", fontSize: 12 }}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        ))}

        <p className="mono" style={{ fontSize: 11, color: "var(--fg-4)", margin: "8px 0 4px" }}>
          본문 (사이트에 노출되지 않습니다 — career·concept 의 입력입니다)
        </p>
        <textarea
          value={draft.daily.body ?? ""}
          disabled={disabled}
          onChange={(e) => setDaily({ body: e.target.value })}
          rows={8}
          className="mono"
          style={{
            width: "100%",
            fontSize: 12,
            padding: 8,
            background: "var(--bg-2)",
            border: "1px solid var(--line-2)",
            borderRadius: 4,
            color: "var(--fg-1)",
            resize: "vertical",
          }}
        />
      </section>

      {/* --- career -------------------------------------------------------- */}
      <section>
        <h4 className="mono" style={{ fontSize: 12, color: "var(--fg-3)", margin: "0 0 6px" }}>
          career{draft.career.stem ? ` · ${draft.career.stem}` : ""}
        </h4>
        {!payload.career.changed ? (
          <p style={{ fontSize: 12.5, color: "var(--fg-3)" }}>
            갱신할 것이 없다고 판단했습니다. 매일 갱신하되 대개 변경 없음이 정상입니다.
          </p>
        ) : (
          <>
            <p className="mono" style={{ fontSize: 11, color: "var(--fg-4)", margin: "0 0 6px" }}>
              체크를 풀면 그 줄은 발행되지 않습니다. 노란 표시가 이번에 바뀐 줄입니다.
            </p>
            <div style={{ ...box, padding: 8 }}>
              {careerLines.map((line, i) => (
                <label
                  key={i}
                  style={{
                    display: "flex",
                    gap: 8,
                    alignItems: "flex-start",
                    padding: "2px 0",
                    opacity: line.keep ? 1 : 0.4,
                  }}
                >
                  {line.heading || !line.text.trim() ? (
                    <span style={{ width: 13 }} />
                  ) : (
                    <input
                      type="checkbox"
                      checked={line.keep}
                      disabled={disabled}
                      onChange={(e) =>
                        setLines(
                          careerLines.map((l, j) =>
                            j === i ? { ...l, keep: e.target.checked } : l,
                          ),
                        )
                      }
                      style={{ marginTop: 3 }}
                    />
                  )}
                  <span
                    className="mono"
                    style={{
                      fontSize: 12,
                      whiteSpace: "pre-wrap",
                      color: line.heading ? "var(--fg-2)" : "var(--fg-1)",
                      fontWeight: line.heading ? 600 : 400,
                      textDecoration: line.keep ? "none" : "line-through",
                      borderLeft: line.added ? "2px solid var(--accent)" : "2px solid transparent",
                      paddingLeft: 6,
                    }}
                  >
                    {line.text || " "}
                  </span>
                </label>
              ))}
            </div>
            {previousCareer && (
              <>
                <button
                  type="button"
                  onClick={() => setShowPrevious((v) => !v)}
                  style={{ ...btn("ghost"), marginTop: 6, fontSize: 11.5 }}
                >
                  {showPrevious ? "기존 본문 접기" : "기존 본문 펼치기"}
                </button>
                {showPrevious && (
                  <pre
                    className="mono"
                    style={{
                      ...box,
                      padding: 8,
                      marginTop: 6,
                      fontSize: 11.5,
                      whiteSpace: "pre-wrap",
                      color: "var(--fg-3)",
                    }}
                  >
                    {previousCareer}
                  </pre>
                )}
              </>
            )}
          </>
        )}
      </section>

      {/* --- concept ------------------------------------------------------- */}
      <section>
        <h4 className="mono" style={{ fontSize: 12, color: "var(--fg-3)", margin: "0 0 6px" }}>
          concept
        </h4>
        <ConceptList
          concepts={draft.concepts ?? []}
          disabled={disabled}
          onChange={(next) => onChange({ ...draft, concepts: next })}
        />
      </section>
    </div>
  );
}

function FeedbackModal({
  onClose,
  onSubmit,
}: {
  onClose: () => void;
  onSubmit: (body: string) => Promise<void>;
}) {
  const [body, setBody] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    setBusy(true);
    setError(null);
    try {
      await onSubmit(body);
      onClose();
    } catch (e) {
      setError(e instanceof Error ? e.message : "재생성에 실패했습니다.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.55)",
        display: "grid",
        placeItems: "center",
        zIndex: 50,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{ ...box, width: 520, maxWidth: "92vw", padding: 18 }}
      >
        <h3 style={{ margin: 0, fontSize: 15, color: "var(--fg-0)" }}>피드백</h3>
        <p style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
          어떻게 고쳐야 하는지 적으면 새 버전을 만듭니다. 지금 버전은 그대로 남습니다.
        </p>
        <textarea
          autoFocus
          value={body}
          onChange={(e) => setBody(e.target.value)}
          rows={5}
          placeholder="예) 개념을 하나로 합쳐 달라 / 교안은 필요 없다"
          style={{
            width: "100%",
            marginTop: 10,
            padding: 10,
            fontSize: 13,
            background: "var(--bg-0)",
            color: "var(--fg-1)",
            border: "1px solid var(--line-2)",
            borderRadius: 5,
            resize: "vertical",
          }}
        />
        {error && (
          <p style={{ color: "#f85149", fontSize: 12, marginTop: 8 }}>{error}</p>
        )}
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end", marginTop: 12 }}>
          <button type="button" onClick={onClose} style={btn("ghost")}>
            취소
          </button>
          <button type="button" onClick={submit} disabled={busy} style={btn("primary")}>
            {busy ? "재생성 중…" : "재생성"}
          </button>
        </div>
      </div>
    </div>
  );
}

/** 진행 중 표시 — 눌린 줄 모르면 다시 누르게 되고, 그러면 요청이 겹친다. */
export function Spinner() {
  return <span className="kk-spinner" aria-hidden />;
}

export function btn(kind: "primary" | "ghost" | "danger") {
  const base = {
    fontSize: 12,
    padding: "6px 14px",
    borderRadius: 5,
    cursor: "pointer",
    border: "1px solid var(--line-2)",
    background: "transparent",
    color: "var(--fg-1)",
  };
  if (kind === "primary")
    return { ...base, border: "1px solid var(--accent)", color: "var(--accent)" };
  if (kind === "danger") return { ...base, border: "1px solid #f85149", color: "#f85149" };
  return base;
}

export function GateCard({
  gate,
  itemId,
  onChanged,
}: {
  gate: Gate;
  itemId: number;
  onChanged: () => void;
}) {
  const active =
    gate.revisions.find((r) => r.id === gate.active_revision_id) ??
    gate.revisions[gate.revisions.length - 1];
  const approved = gate.status === "approved";
  const [open, setOpen] = useState(!approved);
  const [draft, setDraft] = useState<RouteResult>(() =>
    active?.payload && !isNote(active.payload) && !isConcepts(active.payload)
      ? active.payload
      : emptyRoute(),
  );
  const [concepts, setConcepts] = useState<ConceptResult[]>(
    isConcepts(active?.payload) ? active.payload.concepts : [],
  );
  // 잔디는 게이트 하나가 목적지 셋을 내므로 초안 전체를 들고 편집한다.
  const [daily, setDaily] = useState<DailyPayload | null>(
    isDaily(active?.payload) ? active.payload : null,
  );
  const [feedbackOpen, setFeedbackOpen] = useState(false);
  // 무엇을 보내는 중인지 담는다. boolean 이면 화면이 "왜 멈춰 있는지"를 말하지 못한다.
  // 요청 자체는 1초 안에 끝난다 — 오래 걸리는 것은 그 뒤 서버가 만드는 시간이고,
  // 그건 `generating` 배지와 폴링이 말한다.
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setDraft(
      active?.payload && !isNote(active.payload) && !isConcepts(active.payload)
        ? active.payload
        : emptyRoute(),
    );
    setConcepts(isConcepts(active?.payload) ? active.payload.concepts : []);
    setDaily(isDaily(active?.payload) ? active.payload : null);
    setOpen(gate.status !== "approved");
  }, [active?.id, active?.payload, gate.status]);

  const canAct = gate.status === "review_pending" || gate.status === "feedback_pending";
  const inFlight = gateInFlight(gate);
  // 진행 중이면 손을 못 대게 한다 — 지금 만들어지는 것을 앞질러 조작하면
  // 사람이 보지 않은 내용이 확정되거나 중복 실행이 쌓인다.
  const locked = !!busy || inFlight;

  async function run(label: string, fn: () => Promise<unknown>) {
    if (busy) return; // 이미 도는 요청이 있으면 무시 — 중복 실행 차단
    setBusy(label);
    setError(null);
    try {
      await fn();
      onChanged();
    } catch (e) {
      setError(
        e instanceof QueueError
          ? e.code === "STALE_REVISION"
            ? "최신 상태를 다시 확인해 주세요."
            : e.message
          : "요청에 실패했습니다.",
      );
    } finally {
      setBusy(null);
    }
  }

  const failedNote =
    gate.status === "failed"
      ? "제안을 만들지 못했습니다. 재시도하면 새 실행으로 다시 만듭니다."
      : null;

  return (
    <div style={{ ...box, marginTop: 12 }}>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        style={{
          width: "100%",
          display: "flex",
          alignItems: "center",
          gap: 10,
          padding: "10px 12px",
          background: "transparent",
          border: "none",
          cursor: "pointer",
          textAlign: "left",
        }}
      >
        <span className="mono" style={{ fontSize: 11, color: "var(--fg-4)" }}>
          {gate.stage_no}
        </span>
        <span style={{ fontSize: 14, color: "var(--fg-0)", flex: 1 }}>
          {STAGE_LABEL[gate.stage_name] ?? gate.stage_name}
        </span>
        {active && (
          <span className="mono" style={{ fontSize: 10, color: "var(--fg-4)" }}>
            v{active.version}
          </span>
        )}
        <Badge status={gate.status} />
      </button>

      {open && (
        <div style={{ padding: "0 12px 12px" }}>
          {failedNote && (
            <p style={{ fontSize: 12, color: "#f85149", margin: "4px 0 10px" }}>{failedNote}</p>
          )}

          {!isNote(active?.payload) && !isConcepts(active?.payload) && active?.payload?.rationale && (
            <p
              style={{
                fontSize: 12.5,
                color: "var(--fg-2)",
                lineHeight: 1.6,
                margin: 0,
                whiteSpace: "pre-wrap",
              }}
            >
              {active.payload.rationale}
            </p>
          )}

          {gate.stage_name === "route" &&
            active?.payload &&
            !isNote(active.payload) &&
            !isConcepts(active.payload) && (
            <RouteEditor value={draft} disabled={!canAct || locked} onChange={setDraft} />
            )}

          {isNote(active?.payload) && <NotePreview payload={active.payload} />}

          {isConcepts(active?.payload) && (
            <ConceptList
              concepts={concepts}
              disabled={!canAct || locked}
              onChange={setConcepts}
            />
          )}

          {isDaily(active?.payload) && daily && (
            <DailyReview
              payload={active.payload}
              draft={daily}
              disabled={!canAct || locked}
              previousCareer={active.payload.career.previous_content ?? ""}
              onChange={setDaily}
            />
          )}

          {gate.revisions.length > 1 && (
            <p className="mono" style={{ fontSize: 10.5, color: "var(--fg-4)", marginTop: 8 }}>
              이전 버전 {gate.revisions.length - 1}개는 읽기 전용으로 남아 있습니다.
            </p>
          )}

          {inFlight && (
            <p className="mono" style={{ fontSize: 12, color: "var(--accent)", marginTop: 8 }}>
              <Spinner />
              {gate.status === "regenerating" ? "새 제안을" : "제안을"} 만드는 중입니다 (30~60초).
              끝나면 이 카드가 저절로 열립니다 — 창을 닫아도 계속 진행됩니다.
            </p>
          )}
          {busy && !inFlight && (
            <p className="mono" style={{ fontSize: 12, color: "var(--accent)", marginTop: 8 }}>
              <Spinner />
              {busy} 요청을 보내는 중…
            </p>
          )}
          {error && <p style={{ color: "#f85149", fontSize: 12, marginTop: 8 }}>{error}</p>}

          <div style={{ display: "flex", gap: 8, justifyContent: "flex-end", marginTop: 12 }}>
            {gate.stage_name === "route" && approved && (
              <button
                type="button"
                disabled={locked}
                title="뒤 단계가 무효화됩니다. 기록은 남고 수집·요약은 다시 돌지 않습니다."
                onClick={() => {
                  if (
                    window.confirm(
                      "목적지를 다시 정합니다.\n뒤 단계의 승인이 무효화됩니다 (기록은 남습니다).",
                    )
                  ) {
                    run("재오픈", () => queueApi.reopenRoute(itemId));
                  }
                }}
                style={btn("ghost")}
              >
                {busy === "재오픈" ? <><Spinner />재오픈 중…</> : "이 목적지가 아님"}
              </button>
            )}
            {gate.status === "failed" && (
              <button
                type="button"
                disabled={locked}
                onClick={() => run("재시도", () => queueApi.retryGate(gate.id))}
                style={btn("ghost")}
              >
                {busy === "재시도" ? <><Spinner />재시도 중…</> : "재시도"}
              </button>
            )}
            {canAct && (
              <>
                <button
                  type="button"
                  disabled={locked}
                  onClick={() => setFeedbackOpen(true)}
                  style={btn("ghost")}
                >
                  피드백
                </button>
                <button
                  type="button"
                  disabled={locked}
                  onClick={() =>
                    run("승인", () =>
                      queueApi.approve(
                        gate.id,
                        gate.stage_name === "route"
                          ? draft
                          : isConcepts(active?.payload)
                            ? { concepts }
                            : // 승인 대상은 AI 제안 원본이 아니라 **사람이 고친 것**이다.
                              isDaily(active?.payload) && daily
                              ? daily
                              : null,
                        active?.id ?? null,
                      ),
                    )
                  }
                  style={btn(draft.exclusive === "discard" ? "danger" : "primary")}
                >
                  {busy === "승인" ? (
                    <>
                      <Spinner />
                      승인 중…
                    </>
                  ) : draft.exclusive === "discard" ? (
                    "폐기 승인"
                  ) : (
                    "승인"
                  )}
                </button>
              </>
            )}
          </div>
        </div>
      )}

      {feedbackOpen && (
        <FeedbackModal
          onClose={() => setFeedbackOpen(false)}
          onSubmit={async (body) => {
            await queueApi.feedback(gate.id, body);
            await queueApi.regenerate(gate.id);
            onChanged();
          }}
        />
      )}
    </div>
  );
}
