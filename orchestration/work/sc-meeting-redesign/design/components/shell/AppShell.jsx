/* 「신규」 AppShell · AppHeader · AppBody — 페이지 틀. 모든 화면이 이 셋을 쓴다.
   스타일은 components/shell/shell.css 가 가진다. */

export function AppShell({ nav, children }) {
  return (
    <div className="scax-app-shell">
      {nav}
      <div className="scax-app-main">{children}</div>
    </div>
  );
}

export function AppHeader({ breadcrumb, title, actions }) {
  return (
    <header className="scax-page-header">
      <div className="scax-page-header__lead">
        {breadcrumb && breadcrumb.length ? (
          <nav className="scax-breadcrumb" aria-label="위치">
            {breadcrumb.map((b, i) => [
              i > 0 ? <span key={`s${i}`} className="scax-breadcrumb__sep">/</span> : null,
              <span key={b} className={`scax-breadcrumb__item${i === breadcrumb.length - 1 ? ' scax-breadcrumb__item--current' : ''}`}>{b}</span>,
            ])}
          </nav>
        ) : null}
        <h1 className="scax-page-header__title">{title}</h1>
      </div>
      <div className="scax-page-header__actions">{actions}</div>
    </header>
  );
}

export function AppBody({ railLeft, railRight, children }) {
  return (
    <div className="scax-page-body">
      {railLeft ? <aside className="scax-page-body__rail scax-page-body__rail--left">{railLeft}</aside> : null}
      <main className="scax-page-body__content">{children}</main>
      {railRight ? <aside className="scax-page-body__rail scax-page-body__rail--right">{railRight}</aside> : null}
    </div>
  );
}
export default AppShell;
