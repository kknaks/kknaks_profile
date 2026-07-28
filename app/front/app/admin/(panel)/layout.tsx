"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { AdminSidebar } from "@/components/admin/sidebar";
import { authApi, type AdminUser } from "@/lib/api";

// 관리자 셸 — (panel) 그룹의 모든 페이지에 인증 게이트 + 사이드바를 공유.
// 로그인(/admin/login)은 이 그룹 밖이라 사이드바가 붙지 않는다.
export default function AdminPanelLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [user, setUser] = useState<AdminUser | null>(null);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    authApi
      .me()
      .then(({ user }) => {
        setUser(user);
        setChecking(false);
      })
      .catch(() => router.replace("/admin/login"));
  }, [router]);

  async function onLogout() {
    try {
      await authApi.logout();
    } finally {
      router.replace("/admin/login");
    }
  }

  if (checking) {
    return (
      <div style={{ minHeight: "100vh", display: "grid", placeItems: "center" }}>
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
          확인 중…
        </p>
      </div>
    );
  }

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "var(--bg-0)" }}>
      <AdminSidebar user={user} onLogout={onLogout} />
      <main style={{ flex: 1, minWidth: 0 }}>{children}</main>
    </div>
  );
}
