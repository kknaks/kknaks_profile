import { Suspense } from "react";
import { MonitoringView } from "@/components/ontology/monitoring/monitoring-view";

/**
 * `/ontology/monitoring` — 기본 진입 화면(SPEC-004 U-4~U-7).
 * `?edge=` 를 `useSearchParams` 로 읽으므로 Suspense 경계가 필요하다.
 */
export default function MonitoringPage() {
  return (
    <Suspense fallback={null}>
      <MonitoringView />
    </Suspense>
  );
}
