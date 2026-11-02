import { redirect } from "next/navigation";

/** 기본 진입은 모니터링이다(SPEC-004 §4 라우트 표 · AC-1). */
export default function OntologyIndexPage() {
  redirect("/ontology/monitoring");
}
