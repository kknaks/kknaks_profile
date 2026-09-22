import { NextResponse, type NextRequest } from "next/server";

/**
 * 접속 게이트 — **화면 가드**(SPEC-003 §5 「가드는 프론트 미들웨어와 백 API 양쪽」).
 *
 * 세션이 없으면 세 라우트 어디로 들어와도 게이트만 보인다. **redirect 가 아니라
 * rewrite** 라 URL 이 유지되고, 통과 후 새로고침만으로 원래 가려던 라우트로 돌아온다
 * (SPEC-004 U-2 · AC-6).
 *
 * matcher 가 `/ontology/*` 뿐이라 포트폴리오 라우트는 이 파일을 지나지 않는다.
 */

const GATE_PATH = "/ontology/gate";
const DEFAULT_PATH = "/ontology/monitoring";

/** 화면 가드용 마커. API 가드는 백엔드가 자기 세션 쿠키로 한다. */
const GATE_COOKIE = "ontology_demo_gate";
const BACKEND_SESSION_COOKIE = "ontology_demo_sid";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const authorized =
    request.cookies.has(GATE_COOKIE) || request.cookies.has(BACKEND_SESSION_COOKIE);

  if (pathname === GATE_PATH) {
    // 세션이 있으면 게이트가 나타나지 않는다.
    return authorized ? NextResponse.redirect(new URL(DEFAULT_PATH, request.url)) : NextResponse.next();
  }

  if (!authorized) {
    return NextResponse.rewrite(new URL(GATE_PATH, request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/ontology/:path*"],
};
