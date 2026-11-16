import { GateForm } from "@/components/ontology/gate-form";

/**
 * 접속 게이트 — 미들웨어가 세션 없는 요청을 이 라우트로 **rewrite** 한다.
 * URL 은 원래 가려던 라우트 그대로라 통과 즉시 그 화면으로 돌아온다(U-2).
 * 셸(헤더 탭)을 그리지 않는다 — 아직 아무 화면에도 들어오지 않은 상태다.
 */
export default function OntologyGatePage() {
  return <GateForm />;
}
