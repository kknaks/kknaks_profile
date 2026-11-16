"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { ontologyApi, parseFilters } from "@/lib/ontology/client";
import type {
  Layer,
  LayerRowsResponse,
  LayerTable,
  LineageResponse,
  SourceGroup,
} from "@/lib/ontology/types";
import { LAYER_LABEL, LAYER_NOTE_REF, formatCount, layerTone } from "@/lib/ontology/encoding";
import { OntologyShell, ScreenBody, ScreenTitle } from "../shell";
import { Panel, StateNote } from "../primitives";
import { TablePanel } from "./table-panel";
import { ColumnDetail, FlowsPanel } from "./column-detail";

/**
 * 데이터 — 「모든 수치는 내려갈 수 있다」를 화면으로 증명하는 자리(U-13~U-15).
 *
 * - 계층은 **브론즈·실버·골드 3종만**. 온톨로지 계층은 이 화면에 없다(AC-18).
 * - 탭 카운트·칩 목록은 `/api/layers/{layer}/tables` 파생이다. 하드코딩 0건(AC-17).
 * - 선택 테이블은 **인덱스가 아니라 이름**으로 식별한다 — 목록 순서가 바뀌어도
 *   조용히 어긋나지 않는다.
 */

const LAYERS: Layer[] = ["bronze", "silver", "gold"];

/** 브론즈 1단 원천 축 라벨 — 화면 카피이고, 테이블 목록 자체는 응답이 준다. */
const SOURCE_GROUP_LABEL: Record<SourceGroup, string> = {
  vegas: "vegas 예약 원장",
  review: "리뷰 원본 CSV",
  nexus: "nexus 시술 카탈로그",
};

export function DataView() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const tierParam = searchParams.get("tier");
  const tableParam = searchParams.get("table");
  const filtersParam = searchParams.get("filters");

  const layer: Layer = LAYERS.includes(tierParam as Layer) ? (tierParam as Layer) : "bronze";
  const filters = useMemo(() => parseFilters(filtersParam), [filtersParam]);

  const [tablesByLayer, setTablesByLayer] = useState<Record<string, LayerTable[]>>({});
  const [rows, setRows] = useState<LayerRowsResponse | null>(null);
  const [lineage, setLineage] = useState<LineageResponse | null>(null);
  const [selectedColumn, setSelectedColumn] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // 계층 탭 카운트를 위해 세 계층의 목록을 모두 받는다.
  useEffect(() => {
    let cancelled = false;
    Promise.all(LAYERS.map((item) => ontologyApi.layerTables(item)))
      .then((results) => {
        if (cancelled) return;
        setTablesByLayer(
          Object.fromEntries(results.map((res) => [res.layer, res.tables])) as Record<string, LayerTable[]>,
        );
      })
      .catch((err: Error) => {
        if (!cancelled) setError(err.message);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const tables = tablesByLayer[layer] ?? [];

  const groups = useMemo(() => {
    const map = new Map<string, LayerTable[]>();
    for (const table of tables) {
      const key = table.source_group ?? table.table;
      const list = map.get(key) ?? [];
      list.push(table);
      map.set(key, list);
    }
    return map;
  }, [tables]);

  const activeTable = tableParam && tables.some((t) => t.table === tableParam) ? tableParam : tables[0]?.table ?? null;

  const activeGroupKey = useMemo(() => {
    const hit = tables.find((t) => t.table === activeTable);
    return hit?.source_group ?? hit?.table ?? null;
  }, [tables, activeTable]);

  const navigate = useCallback(
    (nextLayer: Layer, nextTable: string | null, keepFilters = false) => {
      const params = new URLSearchParams({ tier: nextLayer });
      if (nextTable) params.set("table", nextTable);
      if (keepFilters && filtersParam) params.set("filters", filtersParam);
      router.push(`/ontology/data?${params.toString()}`);
    },
    [router, filtersParam],
  );

  // 행 조회 — 테이블·필터가 바뀔 때마다.
  useEffect(() => {
    if (!activeTable) return;
    let cancelled = false;
    setSelectedColumn(null);
    ontologyApi
      .layerRows(layer, activeTable, { limit: 50, offset: 0, filters })
      .then((res) => {
        if (!cancelled) setRows(res);
      })
      .catch((err: Error) => {
        if (!cancelled) {
          setRows(null);
          setError(err.message);
        }
      });
    ontologyApi
      .lineage(layer, activeTable)
      .then((res) => {
        if (!cancelled) setLineage(res);
      })
      .catch(() => {
        if (!cancelled) setLineage(null);
      });
    return () => {
      cancelled = true;
    };
  }, [layer, activeTable, filters]);

  const activeTableMeta = tables.find((t) => t.table === activeTable);
  const selectedLineage =
    (selectedColumn && lineage?.columns.find((col) => col.column === selectedColumn)) || null;

  return (
    <OntologyShell>
      <ScreenBody gap={20}>
        <ScreenTitle
          title="데이터"
          meta="브론즈 원본 → 실버 표준화 → 골드 KPI · 일 1회 배치"
          right={<MedallionStepper layer={layer} />}
        />

        {error && <StateNote tone="alert">데이터를 불러오지 못했습니다 — {error}</StateNote>}

        {/* 계층 탭 — 개수는 응답 파생 */}
        <div
          style={{
            height: 44,
            display: "flex",
            alignItems: "flex-end",
            gap: 24,
            paddingBottom: 12,
            borderBottom: "1px solid var(--ont-border-card)",
          }}
        >
          {LAYERS.map((item) => {
            const active = item === layer;
            const count = tablesByLayer[item]?.length;
            return (
              <button
                key={item}
                type="button"
                onClick={() => navigate(item, null)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 7,
                  padding: 0,
                  paddingBottom: 10,
                  marginBottom: -13,
                  border: "none",
                  borderBottom: active ? "2px solid var(--ont-ink)" : "2px solid transparent",
                  background: "transparent",
                  fontSize: 13,
                  fontWeight: active ? 700 : 400,
                  color: active ? "var(--ont-ink)" : "var(--ont-label)",
                }}
              >
                <span
                  style={{
                    width: 7,
                    height: 7,
                    borderRadius: "50%",
                    background: layerTone(item).dot,
                  }}
                />
                {LAYER_LABEL[item]}
                <span className="ont-mono" style={{ fontSize: 12, color: "var(--ont-muted)" }}>
                  {count ?? "—"}
                </span>
              </button>
            );
          })}
          <span style={{ marginLeft: "auto", fontSize: 12, color: "var(--ont-muted)" }}>
            근거 기록 · {LAYER_NOTE_REF[layer]}
          </span>
        </div>

        {/* 테이블 칩 — 브론즈는 원천 축 3칩(1단) → nexus 선택 시 2단 14칩 */}
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            {[...groups.entries()].map(([key, list]) => {
              const label = SOURCE_GROUP_LABEL[key as SourceGroup] ?? list[0].table;
              const meta =
                list.length > 1 ? `${list.length}개 테이블` : formatCount(list[0].row_count);
              return (
                <Chip
                  key={key}
                  active={key === activeGroupKey}
                  label={label}
                  meta={meta}
                  mono={list.length === 1}
                  onClick={() => navigate(layer, list[0].table)}
                />
              );
            })}
          </div>

          {activeGroupKey && (groups.get(activeGroupKey)?.length ?? 0) > 1 && (
            <div
              style={{
                display: "flex",
                gap: 8,
                flexWrap: "wrap",
                paddingLeft: 10,
                borderLeft: "2px solid var(--ont-bronze-border)",
              }}
            >
              {groups.get(activeGroupKey)!.map((table) => (
                <Chip
                  key={table.table}
                  active={table.table === activeTable}
                  label={table.table}
                  meta={formatCount(table.row_count)}
                  mono
                  onClick={() => navigate(layer, table.table)}
                />
              ))}
            </div>
          )}
        </div>

        {filters && filters.length > 0 && (
          <div style={{ fontSize: 12, color: "var(--ont-muted)" }}>
            필터 적용 중 —{" "}
            <span className="ont-mono">
              {filters.map((f) => `${f.field} ${f.op} ${JSON.stringify(f.value)}`).join(" · ")}
            </span>{" "}
            <button
              type="button"
              onClick={() => navigate(layer, activeTable)}
              style={{
                border: "none",
                background: "transparent",
                color: "var(--ont-primary-deep)",
                fontSize: 12,
                textDecoration: "underline",
              }}
            >
              필터 해제
            </button>
          </div>
        )}

        <div style={{ display: "flex", gap: 16, flex: 1, minHeight: 480 }}>
          {rows ? (
            <TablePanel
              layer={layer}
              rows={rows}
              table={activeTableMeta}
              selectedColumn={selectedColumn}
              onSelectColumn={setSelectedColumn}
            />
          ) : (
            <Panel style={{ flex: 1 }}>
              <StateNote>표를 불러오는 중입니다.</StateNote>
            </Panel>
          )}

          <Panel style={{ width: 420, flexShrink: 0, display: "flex", flexDirection: "column", gap: 16, minHeight: 0 }}>
            <FlowsPanel layer={layer} table={activeTableMeta} />
            <ColumnDetail
              layer={layer}
              table={activeTable ?? ""}
              column={selectedColumn}
              lineage={selectedLineage}
            />
          </Panel>
        </div>
      </ScreenBody>
    </OntologyShell>
  );
}

function Chip({
  active,
  label,
  meta,
  mono,
  onClick,
}: {
  active: boolean;
  label: string;
  meta: string;
  mono?: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      style={{
        height: 30,
        display: "inline-flex",
        alignItems: "center",
        gap: 8,
        padding: "0 12px",
        borderRadius: 8,
        border: `1px solid ${active ? "var(--ont-ink)" : "var(--ont-border-card)"}`,
        background: active ? "var(--ont-ink)" : "var(--ont-surface)",
        color: active ? "#fff" : "var(--ont-body)",
        fontSize: 13,
        fontWeight: active ? 600 : 400,
      }}
    >
      <span className={mono ? "ont-mono" : undefined} style={{ fontSize: mono ? 12 : 13 }}>
        {label}
      </span>
      <span className="ont-mono" style={{ fontSize: 12, color: active ? "var(--ont-placeholder)" : "var(--ont-muted)" }}>
        {meta}
      </span>
    </button>
  );
}

/** 메달리온 스테퍼 — 현재 계층만 채색한다(디자인 06). */
function MedallionStepper({ layer }: { layer: Layer }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      {LAYERS.map((item, index) => {
        const active = item === layer;
        const tone = layerTone(item);
        return (
          <span key={item} style={{ display: "flex", alignItems: "center", gap: 8 }}>
            {index > 0 && <span style={{ color: "var(--ont-border-card)" }}>→</span>}
            <span
              style={{
                height: 26,
                display: "inline-flex",
                alignItems: "center",
                gap: 6,
                padding: "0 10px",
                borderRadius: 6,
                background: active ? tone.fill : "transparent",
                border: `1px solid ${active ? tone.border : "var(--ont-border)"}`,
                color: active ? tone.text : "var(--ont-placeholder)",
                fontSize: 12,
                fontWeight: active ? 600 : 400,
              }}
            >
              {LAYER_LABEL[item]}
              {active && item === "bronze" ? " · 원본" : ""}
            </span>
          </span>
        );
      })}
    </div>
  );
}
