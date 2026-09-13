import * as React from 'react';
/** 내비 한 줄. `href` 가 없으면 비활성으로 서고 이동하지 않는다. */
export interface NavItem {
  id: string;
  label: string;
  /** `Icon` 의 glyph 이름. */
  icon: string;
  href?: string;
  /** 안 읽은 것이 있으면 글리프 오른쪽 위에 점이 선다. */
  dot?: boolean;
}
/**
 * Left nav rail: identity block, utility group, main group, logo footer.
 *
 * **Intentional addition.** 소스 kit 의 `Navigation` 은 변형별 고정 마크업이라
 * 접기/펴기·활성 표시·페이지 이동을 다루지 못한다. 페이지 틀의 기둥으로 새로 만든 부품이다.
 */
export interface SideNavProps {
  user?: { name: string; role?: string; avatar?: string };
  /** 주 메뉴. */
  items?: NavItem[];
  /** 구분선 위에 서는 알림·설정 같은 항목. */
  utilityItems?: NavItem[];
  activeId?: string;
  /** 접힘(65px). 아이콘만 남고 hover 에서 라벨 툴팁이 뜬다. */
  collapsed?: boolean;
  onCollapse?: () => void;
  /** 바닥의 워드마크. 접히면 첫 글자만 선다. */
  logo?: string;
  version?: string;
}
export declare const SideNav: React.FC<SideNavProps>;
export default SideNav;
