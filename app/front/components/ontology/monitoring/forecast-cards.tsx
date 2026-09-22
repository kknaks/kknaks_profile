"use client";

import type { ForecastItem } from "@/lib/ontology/types";
import { stateTone } from "@/lib/ontology/encoding";
import { StatusDot } from "../primitives";

/**
 * 다음 위험(예보) — **제목·본문·근거·lag·신뢰도는 전부 `/api/forecast` 응답값이다.**
 * 화면이 수치를 만들지 않는다(SPEC-004 U-7 · 디자인 02).
 *
 * 카드 색은 `risk` 가 정한다. lag 배지는 정본 문자열 원형(`0d`·`2w`)을 그대로 쓴다 —
 * `2w` 를 `14d` 로 고치지 않는다.
 */
export function ForecastCards({ forecasts }: { forecasts: ForecastItem[] }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
      {forecasts.map((item) => (
        <ForecastCard key={item.edge.edge_id} item={item} />
      ))}
    </div>
  );
}

function ForecastCard({ item }: { item: ForecastItem }) {
  const tone = stateTone(item.risk);
  return (
    <article
      style={{
        borderRadius: 10,
        border: `1px solid ${tone.border}`,
        background: tone.softFill,
        padding: "14px 16px",
        display: "flex",
        flexDirection: "column",
        gap: 9,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <StatusDot state={item.risk} />
        <span style={{ fontSize: 14, fontWeight: 700, color: tone.text }}>{item.title}</span>
        {item.edge.lag && (
          <span
            className="ont-mono"
            style={{
              marginLeft: "auto",
              height: 20,
              display: "inline-flex",
              alignItems: "center",
              padding: "0 7px",
              borderRadius: 4,
              background: "var(--ont-surface)",
              border: `1px solid ${tone.border}`,
              fontSize: 11,
              color: "var(--ont-body)",
            }}
          >
            lag {item.edge.lag}
          </span>
        )}
      </div>

      <p style={{ margin: 0, fontSize: 13, lineHeight: 1.6, color: "var(--ont-body)" }}>{item.message}</p>

      <div className="ont-mono" style={{ fontSize: 11, color: "var(--ont-label)", lineHeight: 1.6 }}>
        {item.edge.evidence}
        {item.edge.confidence ? ` · 신뢰도 ${item.edge.confidence}` : ""}
        {item.note ? ` · ${item.note}` : ""}
      </div>
    </article>
  );
}
