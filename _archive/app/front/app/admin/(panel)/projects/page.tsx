import { ProductRegistry } from "@/components/admin/product-registry";

/* 제품 레지스트리 — KDEV-SPEC-014 / WORK-018 P4.
 *
 * 인증 게이트와 로그아웃은 `(panel)/layout.tsx` 셸이 담당한다.
 */
export default function AdminProjectsPage() {
  return (
    <div style={{ padding: "28px 32px", maxWidth: 1100, margin: "0 auto" }}>
      <header style={{ marginBottom: 20 }}>
        <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>프로젝트</h1>
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
          제품 · 레포 레지스트리 — 무엇을 긁고 어느 제품에 잇는지
        </p>
      </header>

      <ProductRegistry />
    </div>
  );
}
