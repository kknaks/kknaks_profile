/* 「캘린더」 화면 — [사이드바][목록][월별·주별 캘린더] 3분할.
   테이블 둘을 본다 (data.js):
     CAL_TASKS    업무   — 날짜 단위 (시작~마감 / 마감만 / 기한 없음)
     CAL_SCHEDULE 스케쥴 — 시간 단위 (회의, 그리고 업무의 「그날 몇 시」 배정)
   공용 틀은 ../../shell/js/scax-ui.jsx, 주별 뷰는 ./week.jsx. */
const { AppShell, SideNav, AppHeader, AppBody, Badge, Button, Icon, IconButton, SegmentedControl, GutterList, Empty, TaskCreateModal } = window;

const CAL_DOW = ['일', '월', '화', '수', '목', '금', '토'];
const CAL_VIEWS = [{ value: 'week', label: '주' }, { value: 'month', label: '월' }];
const CAL_TODAY = new Date(2026, 8, 15);
const CAL_CELL_LIMIT = 4;

const tFrom = (t) => t.from || t.due;
const tTo = (t) => t.to || t.due;
const tUndated = (t) => !t.from && !t.due;

/* 해당 월이 걸친 주(일요일 시작)를 모두 채운 날짜 배열 */
function monthDays(year, month) {
  const f = new Date(year, month, 1);
  const s = new Date(year, month, 1 - f.getDay());
  const days = [];
  for (let i = 0; i < 42; i += 1) {
    const d = new Date(s.getFullYear(), s.getMonth(), s.getDate() + i);
    days.push({ date: d, out: d.getMonth() !== month });
  }
  while (days.length > 35 && days[days.length - 1].out && days[days.length - 7].out) days.length -= 7;
  return days;
}

/* 업무·스케쥴을 캘린더가 그릴 한 가지 꼴로 모은다 */
function calEntries(tasks, schedule, tab) {
  const list = [];
  if (tab !== 'meeting') {
    tasks.filter((t) => tFrom(t)).forEach((t) => list.push({ key: `t${t.id}`, id: t.id, kind: 'task', title: t.title, f: tFrom(t), t: tTo(t), task: t }));
  }
  schedule
    .filter((s) => (tab === 'all' ? true : tab === 'meeting' ? s.kind === 'meeting' : s.kind === 'task'))
    .forEach((s) => list.push({ key: `s${s.id}`, id: s.id, kind: s.kind, title: s.title, f: s.day, t: s.day, time: s.start, slot: s }));
  return list;
}

function MonthGrid({ year, month, tab, tasks, schedule, selected, onSelect, onDropDay, onResizeTask }) {
  const days = monthDays(year, month);
  const [overDay, setOverDay] = React.useState(null);
  const [grab, setGrab] = React.useState(null);
  const entries = calEntries(tasks, schedule, tab);
  const isToday = (d) => d.toDateString() === CAL_TODAY.toDateString();

  React.useEffect(() => {
    if (!grab) return undefined;
    const move = (e) => {
      const el = document.elementFromPoint(e.clientX, e.clientY);
      const cell = el && el.closest ? el.closest('.scax-month__cell[data-day]') : null;
      if (cell) onResizeTask(grab.id, grab.edge, Number(cell.getAttribute('data-day')));
    };
    const up = () => setGrab(null);
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
    return () => { window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); };
  }, [grab, onResizeTask]);

  const handle = (id, edge) => (
    <span
      className={`scax-event__handle scax-event__handle--${edge}`}
      role="presentation"
      title={edge === 'start' ? '끌어서 시작일 정하기' : '끌어서 마감일 정하기'}
      onPointerDown={(e) => { e.stopPropagation(); e.preventDefault(); setGrab({ id, edge }); }}
      onClick={(e) => e.stopPropagation()}
    />
  );

  /* 주 단위로 줄을 나눠 둔다 — 같은 항목이 그 주 내내 같은 줄에 앉아야 띠가 이어진다 */
  const laneMap = {};
  for (let w = 0; w * 7 < days.length; w += 1) {
    const week = days.slice(w * 7, w * 7 + 7).filter((x) => !x.out).map((x) => x.date.getDate());
    if (!week.length) { laneMap[w] = []; continue; }
    const segs = entries
      .filter((e) => e.t >= week[0] && e.f <= week[week.length - 1])
      .sort((a, b) => a.f - b.f || (b.t - b.f) - (a.t - a.f));
    const lanes = [];
    segs.forEach((seg) => {
      const li = lanes.findIndex((lane) => lane.every((s) => s.t < seg.f || s.f > seg.t));
      if (li === -1) lanes.push([seg]); else lanes[li].push(seg);
    });
    laneMap[w] = lanes;
  }

  return (
    <section className="scax-month" aria-label={`${year}년 ${month + 1}월 달력`}>
      <div className="scax-month__head">
        {CAL_DOW.map((w, i) => <span key={w} className={`scax-month__dow${i === 0 ? ' scax-month__dow--sun' : ''}`}>{w}</span>)}
      </div>
      <div className="scax-month__grid">
        {days.map(({ date, out }, i) => {
          const day = date.getDate();
          const weekIdx = Math.floor(i / 7);
          const week = days.slice(weekIdx * 7, weekIdx * 7 + 7).filter((x) => !x.out).map((x) => x.date.getDate());
          const live = !out;
          const lanes = laneMap[weekIdx] || [];
          const visible = lanes.slice(0, CAL_CELL_LIMIT);
          const rest = lanes.slice(CAL_CELL_LIMIT).reduce((n, lane) => n + lane.filter((s) => day >= s.f && day <= s.t).length, 0);
          return (
            <div
              key={date.toISOString()}
              data-day={live ? day : undefined}
              className={`scax-month__cell${out ? ' scax-month__cell--out' : ''}${live && selected === day ? ' scax-month__cell--selected' : ''}${live && overDay === day ? ' scax-month__cell--drop' : ''}`}
              onClick={live ? () => onSelect(selected === day ? null : day) : undefined}
              onDragOver={live ? (e) => { e.preventDefault(); setOverDay(day); } : undefined}
              onDragLeave={live ? () => setOverDay((d) => (d === day ? null : d)) : undefined}
              onDrop={live ? (e) => { e.preventDefault(); setOverDay(null); onDropDay(e.dataTransfer.getData('text/plain'), day); } : undefined}
            >
              <div className="scax-month__daytop">
                <span className={`scax-month__date${date.getDay() === 0 && !out ? ' scax-month__date--sun' : ''}${isToday(date) ? ' scax-month__date--today' : ''}`}>{day}</span>
                {isToday(date) ? <span className="scax-month__today-label">오늘</span> : null}
              </div>
              {live ? visible.map((lane, li) => {
                const seg = lane.find((s) => day >= s.f && day <= s.t);
                if (!seg) return <span key={li} className="scax-event scax-event--ghost" aria-hidden="true" />;
                const head = day === seg.f;
                const tail = day === seg.t;
                const weekEnd = week[week.length - 1];
                const reach = Math.min(seg.t, weekEnd) - Math.max(seg.f, week[0]) + 1;
                const multi = seg.t > seg.f;
                const resizable = seg.kind === 'task' && seg.task;
                const cls = multi
                  ? `scax-event scax-event--bar scax-event--${seg.kind}${head ? ' scax-event--bar-head' : ''}${tail ? ' scax-event--bar-tail' : ''}`
                  : `scax-event scax-event--${seg.kind}`;
                return (
                  <span key={li} className={`${cls}${resizable ? ' scax-event--resizable' : ''}`}>
                    {head || day === week[0] ? (
                      <span className="scax-event__span-label" style={multi ? { width: `calc(${reach * 100}% - ${reach * 12}px)` } : undefined}>
                        {seg.time ? `${seg.time} ` : ''}{seg.title}
                      </span>
                    ) : null}
                    {resizable && head ? handle(seg.id, 'start') : null}
                    {resizable && tail ? handle(seg.id, 'end') : null}
                  </span>
                );
              }) : null}
              {live && rest > 0 ? <span className="scax-event scax-event--more">+{rest}건 더</span> : null}
            </div>
          );
        })}
      </div>
    </section>
  );
}

/* 좌측 카드 — 「내 업무」 InboxCard 를 그대로 쓴다. 유형은 DS Badge tone 으로만 구분. */
function ItemCard({ card }) {
  return (
    <article
      className={`scax-inbox-card${card.draggable ? ' scax-inbox-card--draggable' : ''}`}
      draggable={card.draggable}
      onDragStart={card.draggable ? (e) => { window.__calDragId = card.id; e.dataTransfer.setData('text/plain', card.id); } : undefined}
      title={card.draggable ? '캘린더로 끌어다 기한·시간 지정' : undefined}
    >
      <div className="scax-inbox-card__content">
        <div className="scax-inbox-card__top">
          <Badge tone={card.kind === 'meeting' ? 'neutral' : 'accent'}>{card.kind === 'meeting' ? '회의' : '업무'}</Badge>
        </div>
        <h3 className="scax-inbox-card__title">{card.title}</h3>
        <div className="scax-inbox-card__meta">
          <span className="scax-inbox-card__meta-who">{card.when}</span>
          {card.meta.map((m) => (
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

function ItemRail({ cards, tab, onTab, selected, onClearDay }) {
  return (
    <GutterList title="일정" count={cards.length} headerEnd={<SegmentedControl ariaLabel="일정 구분" value={tab} options={window.CAL_TABS || []} onChange={onTab} />}>
      {selected ? (
        <div className="scax-cal-rail__scope">
          <span>9월 {selected}일</span>
          <Button variant="text" tone="neutral" size="sm" label="전체 보기" onClick={onClearDay} />
        </div>
      ) : null}
      {cards.length ? cards.map((c) => <ItemCard key={c.key} card={c} />) : <Empty icon="calendar" title="해당 일정이 없습니다" desc="다른 구분이나 날짜를 골라 보세요." />}
      {cards.length ? <div className="scax-cal-rail__more"><Button variant="outlined" tone="neutral" size="sm" label="더보기" /></div> : null}
    </GutterList>
  );
}

function CalendarPage() {
  const [navId, setNavId] = React.useState('calendar');
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [createOpen, setCreateOpen] = React.useState(false);
  const [view, setView] = React.useState('week');
  const [tab, setTab] = React.useState('all');
  const [selected, setSelected] = React.useState(null);
  const [weekAnchor, setWeekAnchor] = React.useState(CAL_TODAY.getDate());
  const [cursor, setCursor] = React.useState({ year: CAL_TODAY.getFullYear(), month: CAL_TODAY.getMonth() });
  const [tasks, setTasks] = React.useState(() => (window.CAL_TASKS || []).map((t) => Object.assign({}, t)));
  const [schedule, setSchedule] = React.useState(() => (window.CAL_SCHEDULE || []).map((s) => Object.assign({}, s)));

  /* 업무를 날짜 칸으로 옮기면 기간 길이를 그대로 지킨다 */
  const moveTask = React.useCallback((id, day) => setTasks((list) => list.map((t) => {
    if (t.id !== id) return t;
    if (t.from && t.to) return Object.assign({}, t, { from: day, to: day + (t.to - t.from) });
    if (t.due) return Object.assign({}, t, { due: day });
    return Object.assign({}, t, { from: day, to: day });
  })), []);

  /* 좌우 손잡이 — 마감만 있던 업무는 이때 시작~마감 기간이 생긴다 */
  const resizeTask = React.useCallback((id, edge, day) => setTasks((list) => list.map((t) => {
    if (t.id !== id) return t;
    const from = tFrom(t);
    const to = tTo(t);
    const next = edge === 'start' ? { from: Math.min(day, to), to } : { from, to: Math.max(day, from) };
    return Object.assign({}, t, next, { due: undefined });
  })), []);

  /* 업무를 시간 칸에 떨어뜨리면 스케쥴 한 줄이 생긴다 — 업무의 기간은 그대로 남는다 */
  const addSlot = React.useCallback((taskId, day, start, end) => setSchedule((list) => {
    const task = (window.CAL_TASKS || []).concat(tasks).find((t) => t.id === taskId);
    const keep = list.filter((s) => !(s.taskId === taskId && s.day === day));
    return keep.concat([{ id: `sx${taskId}-${day}`, kind: 'task', taskId, title: task ? task.title : '업무', day, start, end, owner: task && task.owner }]);
  }), [tasks]);

  /* 시간 블록을 세로로 끌어 시각 조정 (30분 단위) */
  const resizeSlot = React.useCallback((id, edge, time) => setSchedule((list) => list.map((s) => {
    if (s.id !== id) return s;
    if (edge === 'start') return Object.assign({}, s, { start: time < s.end ? time : s.start });
    return Object.assign({}, s, { end: time > s.start ? time : s.end });
  })), []);

  const shift = (n) => {
    setSelected(null);
    if (view === 'week') { setWeekAnchor((a) => a + n * 7); return; }
    setCursor((c) => {
      const d = new Date(c.year, c.month + n, 1);
      return { year: d.getFullYear(), month: d.getMonth() };
    });
  };

  const weekNo = Math.ceil((weekAnchor + new Date(cursor.year, cursor.month, 1).getDay()) / 7);
  const weekRange = view === 'week' && window.weekDates
    ? (() => { const ds = window.weekDates(new Date(cursor.year, cursor.month, weekAnchor)); return [ds[0].getDate(), ds[6].getDate()]; })()
    : null;

  /* 좌측 목록 — 업무(기간) + 스케쥴(시간)을 같은 카드 꼴로 */
  const inScope = (f, t) => {
    if (weekRange && (t < weekRange[0] || f > weekRange[1])) return false;
    if (selected && (selected < f || selected > t)) return false;
    return true;
  };
  const cards = [];
  if (tab !== 'meeting') {
    tasks.forEach((t) => {
      const dated = Boolean(tFrom(t));
      if (dated && !inScope(tFrom(t), tTo(t))) return;
      if (!dated && selected) return;
      const slots = schedule.filter((s) => s.taskId === t.id).map((s) => `${s.day}일 ${s.start}`);
      cards.push({
        key: `t${t.id}`,
        id: t.id,
        kind: 'task',
        title: t.title,
        when: t.from ? `9월 ${t.from}일 ~ ${t.to}일` : t.due ? `9월 ${t.due}일 마감` : '기한 없음',
        meta: slots.concat([t.owner]).filter(Boolean),
        sort: dated ? tFrom(t) : 99,
        draggable: true,
      });
    });
  }
  schedule
    .filter((s) => (tab === 'all' ? s.kind === 'meeting' : tab === 'meeting' ? s.kind === 'meeting' : false))
    .filter((s) => inScope(s.day, s.day))
    .forEach((s) => cards.push({
      key: `s${s.id}`,
      id: s.id,
      kind: 'meeting',
      title: s.title,
      when: `9월 ${s.day}일 ${s.start}–${s.end}`,
      meta: [s.place, s.repeat, s.owner].filter(Boolean),
      sort: s.day,
      draggable: false,
    }));
  cards.sort((a, b) => a.sort - b.sort);

  return (
    <React.Fragment>
      <AppShell nav={<SideNav user={{ name: '유하람님', role: '기획자', avatar: './assets/avatar-person.png' }} activeId={navId} onSelect={setNavId} collapsed={navCollapsed} onCollapse={() => setNavCollapsed((v) => !v)} />}>
        <AppHeader title="캘린더" actions={<Button variant="solid" tone="primary" label="업무 만들기" onClick={() => setCreateOpen(true)} />} />
        <AppBody railLeft={<ItemRail cards={cards} tab={tab} onTab={setTab} selected={selected} onClearDay={() => setSelected(null)} />}>
          <div className="scax-cal-main">
            <div className="scax-cal-toolbar">
              <span className="scax-cal-toolbar__year">{cursor.year}년{view === 'week' ? ` ${cursor.month + 1}월` : ''}</span>
              <div className="scax-cal-toolbar__nav">
                <IconButton name="chevron-right" size={20} label={view === 'week' ? '이전 주' : '이전 달'} className="scax-cal-toolbar__prev" onClick={() => shift(-1)} />
                <h2 className="scax-cal-toolbar__month">{view === 'week' ? `${weekNo}주차` : `${cursor.month + 1}월`}</h2>
                <IconButton name="chevron-right" size={20} label={view === 'week' ? '다음 주' : '다음 달'} onClick={() => shift(1)} />
              </div>
              <span className="scax-cal-toolbar__spacer" />
              <SegmentedControl ariaLabel="기간 보기" value={view} options={CAL_VIEWS} onChange={setView} />
            </div>
            {view === 'week'
              ? (
                <window.WeekGrid
                  anchor={new Date(cursor.year, cursor.month, weekAnchor)}
                  tasks={tasks}
                  schedule={schedule}
                  tab={tab}
                  today={CAL_TODAY}
                  selected={selected}
                  onSelect={setSelected}
                  onSchedule={addSlot}
                  onResizeTask={resizeTask}
                  onMoveTask={moveTask}
                  onResizeSlot={resizeSlot}
                />
              )
              : (
                <MonthGrid
                  year={cursor.year}
                  month={cursor.month}
                  tab={tab}
                  tasks={tasks}
                  schedule={schedule}
                  selected={selected}
                  onSelect={setSelected}
                  onDropDay={moveTask}
                  onResizeTask={resizeTask}
                />
              )}
          </div>
        </AppBody>
      </AppShell>
      <TaskCreateModal open={createOpen} onClose={() => setCreateOpen(false)} />
    </React.Fragment>
  );
}

const scaxCalendarRoot = ReactDOM.createRoot(document.getElementById('root'));
scaxCalendarRoot.render(<CalendarPage />);
