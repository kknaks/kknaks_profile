import { Suspense } from "react";
import { DataView } from "@/components/ontology/data/data-view";

/**
 * `/ontology/data` — 계층 탐색·마스킹 표·컬럼 상세·역추적(SPEC-004 U-13~U-15).
 * `?tier=`·`?table=`·`?filters=` 를 읽으므로 Suspense 경계가 필요하다.
 */
export default function DataPage() {
  return (
    <Suspense fallback={null}>
      <DataView />
    </Suspense>
  );
}
