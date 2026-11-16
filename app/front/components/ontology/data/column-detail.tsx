"use client";

import Link from "next/link";
import type { Layer, LineageColumn, LayerTable } from "@/lib/ontology/types";
import { LAYER_LABEL, dataHref, parseTableRef } from "@/lib/ontology/encoding";
import { LayerBadge, SectionLabel, StateNote } from "../primitives";

/**
 * 우측 컬럼 — 「이 원본이 가는 곳 / 이 테이블이 이어지는 곳」 + 컬럼 상세(U-15).
 *
 * 목록은 `flows_to[]` 에서, 역추적은 `lineage.source_columns` 에서 만든다 —
 * **매핑을 화면에 손으로 두지 않는다.** 미확정 값(`is_provisional`)은 `—` + 「미확정」
 * 으로 적고 0 으로 채우지 않는다.
 */

export function FlowsPanel({ layer, table }: { layer: Layer; table: LayerTable | undefined }) {
  const title = layer === "bronze" ? "이 원본이 가는 곳" : "이 테이블이 이어지는 곳";
  const flows = table?.flows_to ?? [];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
      <SectionLabel>{title}</SectionLabel>
      {flows.length === 0 ? (
        <StateNote>이 테이블에서 이어지는 계층이 응답에 없습니다.</StateNote>
      ) : (
        flows.map((flow) => (
          <Link
            key={`${flow.layer}:${flow.table}`}
            href={dataHref({ layer: flow.layer, table: flow.table, column: null })}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              height: 36,
              padding: "0 10px",
              borderRadius: 8,
              border: "1px solid var(--ont-border)",
              background: "var(--ont-surface)",
            }}
          >
            <LayerBadge layer={flow.layer} size="sm" />
            <span className="ont-mono" style={{ fontSize: 12, color: "var(--ont-ink)" }}>
              {flow.table}
            </span>
            {flow.note && (
              <span style={{ marginLeft: "auto", fontSize: 11, color: "var(--ont-muted)" }}>{flow.note}</span>
            )}
          </Link>
        ))
      )}
    </div>
  );
}

export function ColumnDetail({
  layer,
  table,
  column,
  lineage,
}: {
  layer: Layer;
  table: string;
  column: string | null;
  lineage: LineageColumn | null;
}) {
  if (!column) {
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: 10, flex: 1, minHeight: 0 }}>
        <SectionLabel>컬럼 상세</SectionLabel>
        <StateNote>표의 컬럼 헤더를 누르면 변환 규칙·계산식과 근거 기록이 표시됩니다.</StateNote>
      </div>
    );
  }

  if (!lineage) {
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: 10, flex: 1, minHeight: 0 }}>
        <SectionLabel>컬럼 상세</SectionLabel>
        <StateNote>
          <span className="ont-mono">{column}</span> 의 컬럼 상세가 응답에 없습니다 — 화면이 지어내지
          않습니다.
        </StateNote>
      </div>
    );
  }

  const question = `${table}.${column} 은 어떤 규칙으로 만들어졌어?`;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12, flex: 1, minHeight: 0, overflow: "auto" }}>
      <SectionLabel>컬럼 상세</SectionLabel>

      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <LayerBadge layer={layer} size="sm" />
        <span className="ont-mono" style={{ fontSize: 13, fontWeight: 600 }}>
          {column}
        </span>
        {lineage.is_provisional && (
          <span style={{ fontSize: 11, color: "var(--ont-placeholder)" }}>— 미확정</span>
        )}
      </div>

      {layer === "gold" ? (
        <>
          <Field label="계산식" value={lineage.formula ?? "—"} mono />
          <Field label="게이트" value={lineage.gate ?? "—"} />
        </>
      ) : (
        <>
          <Field label="원본 값" value={lineage.note ?? "—"} />
          <Field label="실버 규칙" value={lineage.rule_id ? `${lineage.rule_id}` : "—"} mono />
        </>
      )}

      {layer !== "gold" && lineage.gate && <Field label="게이트" value={lineage.gate} />}
      {layer === "gold" && lineage.note && <Field label="설명" value={lineage.note} />}

      {lineage.source_columns.length > 0 && (
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          <span style={{ fontSize: 12, color: "var(--ont-muted)" }}>출처 — 한 계층 아래로</span>
          {lineage.source_columns.map((ref) => (
            <RefLink key={ref} refString={ref} />
          ))}
        </div>
      )}

      {lineage.downstream.length > 0 && (
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          <span style={{ fontSize: 12, color: "var(--ont-muted)" }}>쓰이는 곳</span>
          {lineage.downstream.map((item) => (
            <Link
              key={`${item.layer}:${item.table}:${item.column}`}
              href={dataHref({ layer: item.layer, table: item.table, column: null })}
              className="ont-mono"
              style={refLinkStyle}
            >
              {LAYER_LABEL[item.layer]} · {item.table}.{item.column}
            </Link>
          ))}
        </div>
      )}

      {lineage.status_thresholds && (
        <Field
          label="상태 경계"
          value={Object.entries(lineage.status_thresholds)
            .map(([key, value]) => `${key} ${value}`)
            .join(" · ")}
          mono
        />
      )}

      <Field label="근거 기록" value={lineage.note_ref} />

      <Link
        href={`/ontology/chat?q=${encodeURIComponent(question)}`}
        style={{
          height: 30,
          display: "inline-flex",
          alignItems: "center",
          alignSelf: "flex-start",
          padding: "0 12px",
          borderRadius: 8,
          border: "1px solid var(--ont-border-card)",
          fontSize: 13,
          color: "var(--ont-body)",
        }}
      >
        이 값 물어보기
      </Link>
    </div>
  );
}

const refLinkStyle = {
  display: "block",
  fontSize: 12,
  lineHeight: 1.7,
  color: "var(--ont-primary-deep)",
  textDecoration: "underline",
} as const;

function RefLink({ refString }: { refString: string }) {
  const parsed = parseTableRef(refString);
  if (!parsed) {
    return (
      <span className="ont-mono" style={{ fontSize: 12, color: "var(--ont-body)" }}>
        {refString}
      </span>
    );
  }
  return (
    <Link href={dataHref(parsed)} className="ont-mono" style={refLinkStyle}>
      {LAYER_LABEL[parsed.layer]} · {parsed.table}
      {parsed.column ? `.${parsed.column}` : ""}
    </Link>
  );
}

function Field({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 3 }}>
      <span style={{ fontSize: 12, color: "var(--ont-muted)" }}>{label}</span>
      <span
        className={mono ? "ont-mono" : undefined}
        style={{ fontSize: 12, lineHeight: 1.7, color: "var(--ont-ink)" }}
      >
        {value}
      </span>
    </div>
  );
}
