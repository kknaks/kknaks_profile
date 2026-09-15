import { Icon } from '../icon/Icon.jsx';

/* 「신규」 SideNav — 페이지 틀의 왼쪽 기둥. 소스 kit 의 `Navigation` 은 고정 마크업이라
   접기/펴기·활성 표시·이동을 다루지 못한다. 그 자리를 대신하는 부품이다.
   href 가 있는 항목만 이동한다 — 없으면 자리는 지키되 눌리지 않는다.
   접으면 아이콘만 남고 hover 에서 라벨 툴팁이 뜬다 (규칙은 components/shell/shell.css). */
export function SideNav({ user, items = [], utilityItems = [], activeId, collapsed, onCollapse, logo = 'LOGO', version = 'v1.0' }) {
  const item = (it) => (
    <a
      key={it.id}
      className={`scax-nav-item${it.id === activeId ? ' scax-nav-item--active' : ''}`}
      aria-current={it.id === activeId ? 'page' : undefined}
      aria-disabled={it.href ? undefined : 'true'}
      data-label={it.label}
      href={it.href || undefined}
    >
      <span className="scax-nav-item__glyph">
        <Icon name={it.icon} size={20} />
        {it.dot ? <span className="scax-nav-item__dot" /> : null}
      </span>
      {collapsed ? null : <span className="scax-nav-item__label">{it.label}</span>}
    </a>
  );
  return (
    <nav className={`scax-side-nav${collapsed ? ' scax-side-nav--collapsed' : ''}`} aria-label="주 메뉴">
      {/* 접으면 이 줄이 세로로 서고, 접기 단추가 아바타 위로 올라간다 (디자이너 확정) */}
      <div className="scax-side-nav__identity">
        <button type="button" className="scax-side-nav__collapse" aria-label={collapsed ? '메뉴 펴기' : '메뉴 접기'} aria-expanded={!collapsed} onClick={onCollapse}>
          <Icon name="left-side" size={20} />
        </button>
        {user ? <img className="scax-side-nav__avatar" src={user.avatar} alt="" /> : null}
        {user && !collapsed ? (
          <span className="scax-side-nav__who">
            <span className="scax-side-nav__name">{user.name}</span>
            <span className="scax-side-nav__role">{user.role}</span>
          </span>
        ) : null}
      </div>
      {utilityItems.length ? <div className="scax-side-nav__group">{utilityItems.map(item)}</div> : null}
      {utilityItems.length ? <div className="scax-side-nav__divider" /> : null}
      <div className="scax-side-nav__group">{items.map(item)}</div>
      <div className="scax-side-nav__spacer" />
      <div className="scax-side-nav__footer">
        <span className="scax-side-nav__logo">{collapsed ? logo.slice(0, 1) : logo}</span>
        {collapsed ? null : <span className="scax-side-nav__version">{version}</span>}
      </div>
    </nav>
  );
}
export default SideNav;
