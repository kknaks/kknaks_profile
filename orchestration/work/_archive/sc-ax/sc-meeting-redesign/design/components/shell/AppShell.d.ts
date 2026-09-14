import * as React from 'react';
/**
 * Page frame. **Intentional addition** — the source file draws one screen, not a frame;
 * these three are the shared skeleton every SCAX screen composes.
 *
 * `AppShell` 은 내비 + 본문 기둥, `AppHeader` 는 브레드크럼 + 제목 + 액션(72px),
 * `AppBody` 는 왼쪽 레일 · 본문 · 오른쪽 레일 세 칸이다.
 */
export interface AppShellProps {
  /** `SideNav` 를 넣는다. */
  nav?: React.ReactNode;
  children?: React.ReactNode;
}
export interface AppHeaderProps {
  /** 더 이상 쓰지 않는다 — 머리는 제목 한 줄이다 (디자이너 확정). */
  breadcrumb?: string[];
  /** 그 탭의 이름. 왼쪽 끝에 선다. */
  title?: React.ReactNode;
  /** 오른쪽 끝의 단추 둘. 왼쪽이 outlined, 오른쪽이 solid. */
  actions?: React.ReactNode;
}
export interface AppBodyProps {
  railLeft?: React.ReactNode;
  railRight?: React.ReactNode;
  children?: React.ReactNode;
}
export declare const AppShell: React.FC<AppShellProps>;
export declare const AppHeader: React.FC<AppHeaderProps>;
export declare const AppBody: React.FC<AppBodyProps>;
export default AppShell;
