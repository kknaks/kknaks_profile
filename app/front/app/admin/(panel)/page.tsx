import { redirect } from "next/navigation";

// /admin 의 첫 화면은 프로필이다 — 대시보드는 두지 않기로 했다.
export default function AdminIndexPage() {
  redirect("/admin/profile");
}
