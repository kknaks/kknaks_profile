"use client";

import { useState } from "react";
import type { LayerRowsResponse, LayerTable, RowValue } from "@/lib/ontology/types";
import { formatCount, rangeLabel } from "@/lib/ontology/encoding";
import { LayerBadge, StateNote } from "../primitives";

/**
 * 데이터 표(디자인 02 · 06).
 *
 * - 헤더는 `1–N / total` 을 **항상** 표시한다 — 조용히 잘리지 않는다(U-14).
 * - 마스킹 바의 **개수·이름은 `masked_fields` 파생**이고, 언마스킹 UI 는 없다.
 * - 컬럼을 다 보이지 않을 때는 「N개 컬럼 중 M개 표시」를 밝힌다.
 */

const VISIBLE_COLUMN_CAP = 10;

export function TablePanel({
  rows,
  table,
  selectedColumn,
  onSelectColumn,
}: {
  rows: LayerRowsResponse;
  table: LayerTable | undefined;
  selectedColumn: string | null;
  onSelectColumn: (column: string) => void;
}) {
  const [expandColumns, setExpandColumns] = useState(false);
  const [selectedRow, setSelectedRow] = useState<number | null>(null);

  const columns = expandColumns ? rows.columns : rows.columns.slice(0, VISIBLE_COLUMN_CAP);
  const truncated = rows.columns.length > columns.length;
  const partial = rows.columns.length > VISIBLE_COLUMN_CAP;

  return (
    <section
      style={{
        flex: 1,
        minWidth: 0,
        borderRadius: 12,
        border: "1px solid var(--ont-border-card)",
        background: "var(--ont-surface)",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <header
        style={{
          height: 56,
          flexShrink: 0,
          display: "flex",
          alignItems: "center",
          gap: 10,
          padding: "0 16px",
          borderBottom: "1px solid var(--ont-border)",
        }}
      >
        <LayerBadge layer={rows.layer} />
        <span style={{ fontSize: 15, fontWeight: 700 }}>{rows.table}</span>
        <span className="ont-mono" style={{ fontSize: 12, color: "var(--ont-muted)" }}>
          {rows.view}
          {table ? ` · ${table.note_ref}` : ""}
        </span>
        <span className="ont-mono" style={{ marginLeft: "auto", fontSize: 12, color: "var(--ont-muted)" }}>
          {rows.columns.length === 0
            ? `총 ${formatCount(rows.total)}건`
            : rangeLabel(rows.offset, rows.returned, rows.total)}
        </span>
      </header>

      {rows.masked_fields.length > 0 ? (
        <div
          style={{
            height: 36,
            flexShrink: 0,
            display: "flex",
            alignItems: "center",
            padding: "0 16px",
            background: "var(--ont-alert-fill)",
            borderBottom: "1px solid var(--ont-alert-border)",
            fontSize: 12,
            color: "var(--ont-alert-text)",
          }}
        >
          <strong>{rows.masked_fields.length}개 컬럼이 마스킹</strong>
          <span>
            됩니다 — {rows.masked_fields.join(" · ")}. 언마스킹 기능은 제공하지 않습니다.
          </span>
        </div>
      ) : (
        <div
          style={{
            height: 36,
            flexShrink: 0,
            display: "flex",
            alignItems: "center",
            padding: "0 16px",
            background: "var(--ont-canvas)",
            borderBottom: "1px solid var(--ont-border)",
            fontSize: 12,
            color: "var(--ont-label)",
          }}
        >
          <strong>실명·전화·생년월일은 이 계층으로 올라오지 않습니다.</strong>
          <span>&nbsp;차트번호(chart_no)는 계층 추적용으로 유지됩니다.</span>
        </div>
      )}

      {partial && (
        <div
          style={{
            flexShrink: 0,
            display: "flex",
            alignItems: "center",
            gap: 10,
            padding: "8px 16px",
            borderBottom: "1px solid var(--ont-border)",
            fontSize: 12,
            color: "var(--ont-muted)",
          }}
        >
          <span>
            {rows.columns.length}개 컬럼 중 {columns.length}개 표시
          </span>
          <button
            type="button"
            onClick={() => setExpandColumns((prev) => !prev)}
            style={{
              height: 24,
              padding: "0 10px",
              borderRadius: 6,
              border: "1px solid var(--ont-border-card)",
              background: "var(--ont-surface)",
              fontSize: 12,
              color: "var(--ont-body)",
            }}
          >
            {expandColumns ? "접기" : "전체 컬럼 보기"}
          </button>
        </div>
      )}

      {rows.columns.length === 0 ? (
        // 사유는 **테이블 목록 응답**이 갖는다(SPEC-003 AC-18b) — 빈 컬럼을 침묵으로 두지 않는다.
        <StateNote>{table?.columns_note ?? "표시할 컬럼이 없습니다."}</StateNote>
      ) : rows.rows.length === 0 ? (
        <StateNote>해당 조건의 행이 없습니다.</StateNote>
      ) : (
        <div style={{ flex: 1, minHeight: 0, overflow: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", tableLayout: "auto" }}>
            <thead>
              <tr>
                {columns.map((column) => (
                  <th
                    key={column}
                    onClick={() => onSelectColumn(column)}
                    className="ont-mono"
                    style={{
                      position: "sticky",
                      top: 0,
                      zIndex: 1,
                      height: 40,
                      padding: "0 12px",
                      textAlign: "left",
                      whiteSpace: "nowrap",
                      background: "var(--ont-canvas)",
                      borderBottom: "1px solid var(--ont-border)",
                      fontSize: 12,
                      fontWeight: 600,
                      color: selectedColumn === column ? "var(--ont-ink)" : "var(--ont-body)",
                      cursor: "pointer",
                    }}
                  >
                    {rows.masked_fields.includes(column) && (
                      <svg width="10" height="10" viewBox="0 0 12 12" style={{ marginRight: 4 }} aria-hidden>
                        <rect x="2.5" y="5" width="7" height="5.5" rx="1" stroke="var(--ont-placeholder)" strokeWidth="1.6" fill="none" />
                        <path d="M4 5V3.6a2 2 0 0 1 4 0V5" stroke="var(--ont-placeholder)" strokeWidth="1.6" fill="none" />
                      </svg>
                    )}
                    {column}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.rows.map((row, index) => (
                <tr
                  key={index}
                  onClick={() => setSelectedRow(index)}
                  style={{
                    height: 44,
                    cursor: "pointer",
                    background: selectedRow === index ? "var(--ont-row-selected)" : undefined,
                  }}
                >
                  {columns.map((column) => (
                    <Cell
                      key={column}
                      value={row[column]}
                      masked={rows.masked_fields.includes(column)}
                    />
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function Cell({ value, masked }: { value: RowValue; masked: boolean }) {
  const numeric = typeof value === "number";
  return (
    <td
      className="ont-mono"
      style={{
        height: 44,
        padding: "0 12px",
        borderBottom: "1px solid var(--ont-row-divider)",
        fontSize: 13,
        color: "var(--ont-ink)",
        textAlign: numeric ? "right" : "left",
        whiteSpace: "nowrap",
      }}
    >
      {masked ? (
        <span
          style={{
            background: "var(--ont-hover)",
            color: "var(--ont-label)",
            padding: "2px 6px",
            borderRadius: 4,
          }}
        >
          {String(value ?? "—")}
        </span>
      ) : numeric ? (
        formatCount(value)
      ) : (
        String(value ?? "—")
      )}
    </td>
  );
}
