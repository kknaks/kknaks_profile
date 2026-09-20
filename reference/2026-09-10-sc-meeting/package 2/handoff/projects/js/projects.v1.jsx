/* 「프로젝트」 화면 — 좌 레일: 프로젝트 셀렉터 + 업무 카드(업무 탭 카드 그대로, 공용 WORK_TASKS).
   자료함은 나중에 「자료」 탭으로 간다. 본문은 진행 라인(요약 + 간트 + 의존선). */
const { Icon, Badge, Select, Empty, AppShell, SideNav, AppHeader, AppBody } = window;

const GANTT = { day: 34, row: 40, label: 200, days: 30, today: 17 };

/* 업무 카드 — 캘린더 ItemCard 와 같은 꼴(배지 · 제목 · when + meta). */
function ProjectTaskCard({ row, selected, onSelect }) {
  return (
    <article className={`scax-inbox-card${selected ? ' scax-inbox-card--selected' : ''}`} role="button" tabIndex={0} onClick={() => onSelect(row.id)}>
      <div className="scax-inbox-card__content">
        <div className="scax-inbox-card__top">
          <Badge tone={row.badgeTone}>{row.badge}</Badge>
        </div>
        <h3 className="scax-inbox-card__title">{row.title}</h3>
        <div className="scax-inbox-card__meta">
          <span className="scax-inbox-card__meta-who">{row.when}</span>
          {row.meta.map((m) => (
            <React.Fragment key={m}>
              <span className="scax-inbox-card__meta-sep" />
              <span>{m}</span>
            </React.Fragment>
          ))}
        </div>
      </div>
    </article>
  );
}

function ProjectRail({ project, onProject, tasks, taskId, onTask }) {
  return (
    <section className="scax-gutter-list">
      <header className="scax-gutter-list__header">
        <h2 className="scax-gutter-list__title">
          <Icon name="square-check" size={24} />
          업무
          <Badge variant="count">{tasks.length}</Badge>
        </h2>
        <Select ariaLabel="프로젝트 선택" value={project} options={PROJECT_OPTIONS} onChange={onProject} />
      </header>
      <div className="scax-gutter-list__body">
        {tasks.map((r) => <ProjectTaskCard key={r.id} row={r} selected={r.id === taskId} onSelect={onTask} />)}
      </div>
    </section>
  );
}

/* ---- 본문 ① 요약 스트립 ---- */
function ProjectSummary({ s }) {
  const cells = [
    { label: '전체 업무', value: s.total, tone: 'ink' },
    { label: '진행 중', value: s.progress, tone: 'accent' },
    { label: '지연', value: s.blocked, tone: 'danger' },
    { label: '완료', value: s.done, tone: 'positive' },
  ];
  return (
    <section className="scax-pj-summary">
      {cells.map((c) => (
        <div className="scax-pj-summary__cell" key={c.label} data-tone={c.tone}>
          <span className="scax-pj-summary__label">{c.label}</span>
          <span className="scax-pj-summary__value">{c.value}</span>
        </div>
      ))}
      <div className="scax-pj-summary__cell scax-pj-summary__cell--wide">
        <span className="scax-pj-summary__label">전체 진행률</span>
        <span className="scax-pj-summary__meter">
          <span className="scax-pj-summary__track"><span className="scax-pj-summary__fill" style={{ width: `${s.percent}%` }} /></span>
          <span className="scax-pj-summary__pct">{s.percent}%</span>
        </span>
      </div>
    </section>
  );
}

/* ---- 본문 ② 진행 라인(간트) + ③ 의존선 ---- */
function ganttGeom(rows) {
  const x = (day) => GANTT.label + (day - 1) * GANTT.day;
  const pos = {};
  rows.forEach((r, i) => {
    pos[r.id] = { x1: x(r.from), x2: x(r.to + 1), y: i * GANTT.row + GANTT.row / 2, i };
  });
  return { x, pos, width: GANTT.label + GANTT.days * GANTT.day, height: rows.length * GANTT.row };
}

function DepLines({ rows, geom, taskId }) {
  const seg = [];
  rows.forEach((r) => {
    r.deps.forEach((d) => {
      const a = geom.pos[d];
      const b = geom.pos[r.id];
      if (!a || !b) return;
      const mx = Math.max(a.x2 + 10, b.x1 - 10);
      seg.push({ key: `${d}-${r.id}`, on: taskId === r.id || taskId === d, d: `M ${a.x2} ${a.y} H ${mx} V ${b.y} H ${b.x1 - 5}` });
    });
  });
  return (
    <svg className="scax-pj-gantt__links" width={geom.width} height={geom.height} aria-hidden="true">
      <defs>
        <marker id="pj-arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
          <path d="M0 0 L6 3 L0 6 z" fill="currentColor" />
        </marker>
      </defs>
      {seg.map((s) => <path key={s.key} className={`scax-pj-gantt__link${s.on ? ' scax-pj-gantt__link--on' : ''}`} d={s.d} markerEnd="url(#pj-arrow)" />)}
    </svg>
  );
}

function ProjectGantt({ rows, taskId, onTask }) {
  const [open, setOpen] = React.useState(rows.filter((r) => r.children.length).map((r) => r.id));
  const toggle = (id) => setOpen((l) => (l.indexOf(id) >= 0 ? l.filter((x) => x !== id) : l.concat([id])));
  /* 폈친 후에만 자리를 줌 — 상위 다음에 하위가 뒤따람다 */
  const flat = [];
  rows.forEach((r) => {
    flat.push(Object.assign({}, r, { depth: 0, hasKids: r.children.length > 0, open: open.indexOf(r.id) >= 0 }));
    if (r.children.length && open.indexOf(r.id) >= 0) r.children.forEach((c) => flat.push(Object.assign({}, c, { depth: 1, hasKids: false })));
  });
  const geom = ganttGeom(flat);
  const days = Array.from({ length: GANTT.days }, (_, i) => i + 1);
  return (
    <section className="scax-pj-gantt">
      <header className="scax-pj-gantt__head">
        <h2 className="scax-pj-gantt__title">진행 라인</h2>
        <span className="scax-pj-gantt__legend">2026년 9월 · 화살표는 선행 → 후행</span>
      </header>
      <div className="scax-pj-gantt__scroll">
        <div className="scax-pj-gantt__canvas" style={{ width: geom.width }}>
          <div className="scax-pj-gantt__axis" style={{ paddingLeft: GANTT.label }}>
            {days.map((d) => <span className={`scax-pj-gantt__day${d === GANTT.today ? ' scax-pj-gantt__day--today' : ''}`} style={{ width: GANTT.day }} key={d}>{d}</span>)}
          </div>
          <div className="scax-pj-gantt__plot" style={{ height: geom.height }}>
            <div className="scax-pj-gantt__grid" style={{ left: GANTT.label, backgroundSize: `${GANTT.day}px ${GANTT.row}px` }} />
            <span className="scax-pj-gantt__now" style={{ left: geom.x(GANTT.today) }} />
            <DepLines rows={flat} geom={geom} taskId={taskId} />
            {flat.map((r, i) => (
              <div className={`scax-pj-gantt__row${r.depth ? ' scax-pj-gantt__row--child' : ''}`} style={{ top: i * GANTT.row, height: GANTT.row }} key={r.id}>
                <div className="scax-pj-gantt__name-cell" style={{ width: GANTT.label, paddingLeft: r.depth ? 'var(--scax-space-600)' : 0 }}>
                  {r.hasKids ? (
                    <button type="button" className="scax-pj-gantt__twisty" aria-expanded={r.open} aria-label={r.open ? '하위 업무 접기' : '하위 업무 펼기'} onClick={() => toggle(r.id)}>
                      <Icon name={r.open ? 'chevron-down' : 'chevron-right'} size={12} />
                    </button>
                  ) : <span className="scax-pj-gantt__twisty scax-pj-gantt__twisty--blank" />}
                  <button type="button" className={`scax-pj-gantt__name${r.id === taskId ? ' scax-pj-gantt__name--on' : ''}`} onClick={() => onTask(r.id)}>
                    <span className="scax-pj-gantt__name-text">{r.title}</span>
                    <span className="scax-pj-gantt__name-owner">{r.owner}{r.hasKids ? ` · 하위 ${r.children.length}` : ''}</span>
                  </button>
                </div>
                <button
                  type="button"
                  className={`scax-pj-gantt__bar scax-pj-gantt__bar--${r.status}${r.depth ? ' scax-pj-gantt__bar--child' : ''}${r.hasKids ? ' scax-pj-gantt__bar--parent' : ''}${r.id === taskId ? ' scax-pj-gantt__bar--on' : ''}`}
                  style={{ left: geom.pos[r.id].x1, width: geom.pos[r.id].x2 - geom.pos[r.id].x1 }}
                  onClick={() => onTask(r.id)}
                  title={`${r.title} · 9월 ${r.from}–${r.to}일 · ${r.progress}%`}
                >
                  <span className="scax-pj-gantt__bar-fill" style={{ width: `${r.progress}%` }} />
                  <span className="scax-pj-gantt__bar-pct">{r.progress}%</span>
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

/* ---- 우 레일: 업무 메타 · 체크리스트 · 하위 업무 ---- */
function ProjectDetailRail({ detail, onTask }) {
  if (!detail) {
    return (
      <section className="scax-pj-side">
        <Empty icon="square-check" title="업무를 선택하세요" desc="진행 라인이나 업무 목록에서 골라 상자를 열어 봅니다." />
      </section>
    );
  }
  const { row, parent, status, when, requester, group, prev, next, checklist, children } = detail;
  const doneCount = checklist.filter((c) => c.done).length;
  const facts = [
    ['상태', <span className={`scax-badge scax-badge--${status.tone}`} key="s">{status.label}</span>],
    ['기간', when],
    ['담당', row.owner],
    requester ? ['요잴', requester] : null,
    ['분류', group],
    parent ? ['상위 업무', parent.title] : null,
  ].filter(Boolean);
  return (
    <section className="scax-pj-side">
      <header className="scax-pj-side__head">
        <h2 className="scax-pj-side__title">{row.title}</h2>
        <div className="scax-pj-side__meter">
          <span className="scax-pj-side__track"><span className="scax-pj-side__fill" style={{ width: `${row.progress}%` }} /></span>
          <span className="scax-pj-side__pct">{row.progress}%</span>
        </div>
      </header>
      <div className="scax-pj-side__body">
        <section className="scax-pj-side__block">
          <h3 className="scax-pj-side__block-title">메타 정보</h3>
          <dl className="scax-pj-facts">
            {facts.map(([k, v]) => (
              <React.Fragment key={k}>
                <dt className="scax-pj-facts__key">{k}</dt>
                <dd className="scax-pj-facts__val">{v}</dd>
              </React.Fragment>
            ))}
          </dl>
        </section>
        <section className="scax-pj-side__block">
          <h3 className="scax-pj-side__block-title">관계</h3>
          {[['선행', prev, 'arrow-up'], ['후행', next, 'arrow-down']].map(([label, list, icon]) => (
            <div className="scax-pj-rel" key={label}>
              <span className="scax-pj-rel__head">
                <Icon name={icon} size={14} />
                {label}
                <span className="scax-pj-side__count">{list.length}</span>
              </span>
              {list.length ? (
                <ul className="scax-pj-rel__list">
                  {list.map((n) => (
                    <li key={n.id}>
                      <button type="button" className="scax-pj-rel__item" onClick={() => onTask(n.id)}>
                        <span className="scax-pj-rel__dot" data-tone={(PROJECT_STATUS_BADGE[n.status] || PROJECT_STATUS_BADGE.progress).tone} />
                        <span className="scax-pj-rel__name">{n.title}</span>
                        <Icon name="chevron-right" size={12} />
                      </button>
                    </li>
                  ))}
                </ul>
              ) : <p className="scax-pj-side__none">없음</p>}
            </div>
          ))}
        </section>
        <section className="scax-pj-side__block">
          <h3 className="scax-pj-side__block-title">
            체크리스트
            {checklist.length ? <span className="scax-pj-side__count">{doneCount}/{checklist.length}</span> : null}
          </h3>
          {checklist.length ? (
            <ul className="scax-pj-check">
              {checklist.map((c) => (
                <li className={`scax-pj-check__item${c.done ? ' scax-pj-check__item--done' : ''}`} key={c.id}>
                  <span className="scax-pj-check__box">{c.done ? <Icon name="check" size={12} /> : null}</span>
                  <span className="scax-pj-check__text">{c.text}</span>
                </li>
              ))}
            </ul>
          ) : <p className="scax-pj-side__none">등록된 항목이 없습니다.</p>}
        </section>
        <section className="scax-pj-side__block">
          <h3 className="scax-pj-side__block-title">
            하위 업무
            {children.length ? <span className="scax-pj-side__count">{children.length}</span> : null}
          </h3>
          {children.length ? (
            <ul className="scax-pj-sub">
              {children.map((c) => {
                const st = PROJECT_STATUS_BADGE[c.status] || PROJECT_STATUS_BADGE.progress;
                return (
                  <li key={c.id}>
                    <button type="button" className="scax-pj-sub__row" onClick={() => onTask(c.id)}>
                      <span className="scax-pj-sub__top">
                        <span className="scax-pj-sub__name">{c.title}</span>
                        <span className={`scax-badge scax-badge--${st.tone}`}>{st.label}</span>
                      </span>
                      <span className="scax-pj-sub__meta">
                        9월 {c.from === c.to ? `${c.from}일` : `${c.from}–${c.to}일`} · {c.owner} · {c.progress}%
                      </span>
                    </button>
                  </li>
                );
              })}
            </ul>
          ) : <p className="scax-pj-side__none">하위 업무가 없습니다.</p>}
        </section>
      </div>
    </section>
  );
}

function ProjectsPage() {
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [project, setProject] = React.useState(PROJECT_OPTIONS[0].value);
  const [taskId, setTaskId] = React.useState('');
  const tasks = projectTasks(project);
  const timeline = projectTimeline(project);
  const summary = projectSummary(project);
  const detail = projectTaskDetail(project, taskId);
  return (
    <AppShell nav={<SideNav user={{ name: '유하람님', role: '기획자', avatar: './assets/avatar-person.png' }} activeId="project" collapsed={navCollapsed} onCollapse={() => setNavCollapsed((v) => !v)} />}>
      <AppHeader title="프로젝트" />
      <AppBody
        railLeft={<ProjectRail project={project} onProject={setProject} tasks={tasks} taskId={taskId} onTask={setTaskId} />}
        railRight={<ProjectDetailRail detail={detail} onTask={setTaskId} />}
      >
        <div className="scax-pj-view">
          <ProjectSummary s={summary} />
          <ProjectGantt rows={timeline} taskId={taskId} onTask={setTaskId} />
        </div>
      </AppBody>
    </AppShell>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<ProjectsPage />);
