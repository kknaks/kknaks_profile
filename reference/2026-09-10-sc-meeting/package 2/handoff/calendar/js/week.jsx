/* 「캘린더」 주별 뷰.
   위 칸(머리 + 종일)은 고정, 아래 시간 격자는 0시~24시 스크롤 영역이며 기본 8시에 맞춰 열린다.
   종일 = 업무(CAL_TASKS, 날짜 단위) · 시간 = 스케쥴(CAL_SCHEDULE, 시간 단위).
   날짜 열은 위·아래 두 구역 모두 같은 data-day 를 달고 같이 선택된다. */
const WEEK_DOW = ['일', '월', '화', '수', '목', '금', '토'];
const WEEK_ROW = 56;   /* 1시간 높이(px) */
const WEEK_OPEN = 8;   /* 처음 보여줄 시각 */
const WEEK_LANES = 3;
const WEEK_SNAP = 30;
const WEEK_SPAN = 24 * 60;

function weekDates(anchor) {
  const s = new Date(anchor.getFullYear(), anchor.getMonth(), anchor.getDate() - anchor.getDay());
  return Array.from({ length: 7 }, (_, i) => new Date(s.getFullYear(), s.getMonth(), s.getDate() + i));
}

const wkMin = (t) => { const [h, m] = String(t).split(':').map(Number); return h * 60 + (m || 0); };
const wkClock = (min) => `${String(Math.floor(min / 60)).padStart(2, '0')}:${String(min % 60).padStart(2, '0')}`;
const wkLabel = (h) => (h === 0 ? '오전 12시' : h < 12 ? `오전 ${h}시` : h === 12 ? '오후 12시' : `오후 ${h - 12}시`);
const taskFrom = (t) => t.from || t.due;
const taskTo = (t) => t.to || t.due;

/* 종일 줄 배치 — 같은 업무는 그 주 내내 같은 줄에 앉는다 */
function alldayLanes(tasks, first, last) {
  const segs = tasks
    .filter((t) => taskFrom(t) && taskTo(t) >= first && taskFrom(t) <= last)
    .map((t) => ({ t, f: Math.max(taskFrom(t), first), to: Math.min(taskTo(t), last) }))
    .sort((a, b) => a.f - b.f || (b.to - b.f) - (a.to - a.f));
  const lanes = [];
  segs.forEach((seg) => {
    const li = lanes.findIndex((lane) => lane.every((s) => s.to < seg.f || s.f > seg.to));
    if (li === -1) lanes.push([seg]); else lanes[li].push(seg);
  });
  return lanes;
}

function WeekGrid({ anchor, tasks, schedule, tab, today, selected, onSelect, onSchedule, onResizeTask, onMoveTask, onResizeSlot }) {
  const dates = weekDates(anchor);
  const first = dates[0].getDate();
  const last = dates[6].getDate();
  const shownTasks = tab === 'meeting' ? [] : tasks;
  const shownSlots = schedule.filter((s) => (tab === 'all' ? true : tab === 'meeting' ? s.kind === 'meeting' : s.kind === 'task'));
  const lanes = alldayLanes(shownTasks, first, last);
  const hours = Array.from({ length: 24 }, (_, i) => i);

  const scroller = React.useRef(null);
  const [dropAt, setDropAt] = React.useState(null);
  const [open, setOpen] = React.useState(false);
  const [grabTask, setGrabTask] = React.useState(null);
  const [grabSlot, setGrabSlot] = React.useState(null);

  const hidden = Math.max(0, lanes.length - WEEK_LANES);
  const laneRows = open ? lanes.length : Math.min(lanes.length, WEEK_LANES);
  const alldayH = (laneRows + (hidden ? 1 : 0)) * 22 + laneRows * 4 + 16;
  const px = (min) => (min / 60) * WEEK_ROW;

  /* 처음 열릴 때 8시가 보이게 */
  React.useEffect(() => {
    const go = () => { if (scroller.current) scroller.current.scrollTop = WEEK_OPEN * WEEK_ROW; };
    go();
    const id = window.requestAnimationFrame(go);
    return () => window.cancelAnimationFrame(id);
  }, []);

  /* 종일 띠 손잡이 — 포인터가 지나는 날짜 열을 읽어 시작·마감을 정한다 */
  React.useEffect(() => {
    if (!grabTask) return undefined;
    const move = (e) => {
      const el = document.elementFromPoint(e.clientX, e.clientY);
      const col = el && el.closest ? el.closest('[data-day]') : null;
      if (col) onResizeTask(grabTask.id, grabTask.edge, Number(col.getAttribute('data-day')));
    };
    const up = () => setGrabTask(null);
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
    return () => { window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); };
  }, [grabTask, onResizeTask]);

  /* 시간 블록 손잡이 — 세로로 끌어 30분 단위로 시작·종료 시각을 정한다 */
  React.useEffect(() => {
    if (!grabSlot) return undefined;
    const move = (e) => {
      const box = grabSlot.el.getBoundingClientRect();
      const raw = ((e.clientY - box.top) / WEEK_ROW) * 60;
      const snapped = Math.max(0, Math.min(WEEK_SPAN, Math.round(raw / WEEK_SNAP) * WEEK_SNAP));
      onResizeSlot(grabSlot.id, grabSlot.edge, wkClock(snapped));
    };
    const up = () => setGrabSlot(null);
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
    return () => { window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); };
  }, [grabSlot, onResizeSlot]);

  const minAt = (e) => {
    const box = e.currentTarget.getBoundingClientRect();
    const raw = ((e.clientY - box.top) / WEEK_ROW) * 60;
    return Math.max(0, Math.min(WEEK_SPAN - 60, Math.round(raw / WEEK_SNAP) * WEEK_SNAP));
  };

  /* 업무는 「그 업무의 기간 안」 에만 시간으로 넣을 수 있다 */
  const canDrop = (day) => {
    const t = tasks.find((x) => x.id === window.__calDragId);
    if (!t || !taskFrom(t)) return false;
    return day >= taskFrom(t) && day <= taskTo(t);
  };

  const taskHandle = (t, edge) => (
    <span
      className={`scax-event__handle scax-event__handle--${edge}`}
      role="presentation"
      title={edge === 'start' ? '끌어서 시작일 정하기' : '끌어서 마감일 정하기'}
      onPointerDown={(e) => { e.stopPropagation(); e.preventDefault(); setGrabTask({ id: t.id, edge }); }}
      onClick={(e) => e.stopPropagation()}
    />
  );

  const slotHandle = (s, edge) => (
    <span
      className={`scax-week__slot-handle scax-week__slot-handle--${edge}`}
      role="presentation"
      title={edge === 'start' ? '끌어서 시작 시각 정하기' : '끌어서 종료 시각 정하기'}
      onPointerDown={(e) => {
        e.stopPropagation();
        e.preventDefault();
        setGrabSlot({ id: s.id, edge, el: e.currentTarget.closest('.scax-week__hours') });
      }}
      onClick={(e) => e.stopPropagation()}
    />
  );

  return (
    <section className="scax-week" aria-label="주별 달력">
      {/* 고정 머리 — 요일·날짜 + 종일 */}
      <div className="scax-week__top">
        <div className="scax-week__ruler-top">
          <div className="scax-week__ruler-head" />
          <div className="scax-week__ruler-allday" style={{ height: alldayH }}>
            <span>종일</span>
            {hidden ? (
              <button type="button" className="scax-week__fold" onClick={() => setOpen((v) => !v)}>
                {open ? '접기' : `${hidden}건 펴기`}
              </button>
            ) : null}
          </div>
        </div>
        <div className="scax-week__days">
          {dates.map((d) => {
            const day = d.getDate();
            const on = d.toDateString() === today.toDateString();
            const picked = selected === day;
            const cellLanes = (open ? lanes : lanes.slice(0, WEEK_LANES)).map((lane) => lane.find((s) => day >= s.f && day <= s.to) || null);
            return (
              <div
                key={d.toISOString()}
                data-day={day}
                className={`scax-week__day${picked ? ' scax-week__day--picked' : ''}`}
                onClick={() => onSelect(picked ? null : day)}
              >
                <div className="scax-week__day-head">
                  <span className={`scax-week__day-dow${d.getDay() === 0 ? ' scax-week__day-dow--sun' : ''}`}>{WEEK_DOW[d.getDay()]}</span>
                  <span className={`scax-week__day-date${on ? ' scax-week__day-date--today' : ''}`}>{day}</span>
                </div>
                <div
                  className="scax-week__day-allday"
                  style={{ height: alldayH }}
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) => { e.preventDefault(); onMoveTask(e.dataTransfer.getData('text/plain'), day); }}
                >
                  {cellLanes.map((seg, li) => (seg ? (
                    <span
                      key={li}
                      className={`scax-event scax-event--task scax-week__band${day === seg.f ? ' scax-week__band--head' : ''}${day === seg.to ? ' scax-week__band--tail' : ''} scax-event--resizable`}
                      draggable
                      onDragStart={(e) => { window.__calDragId = seg.t.id; e.dataTransfer.setData('text/plain', seg.t.id); }}
                    >
                      {day === seg.f || day === first ? <span className="scax-event__label">{seg.t.title}</span> : null}
                      {day === seg.f && taskFrom(seg.t) >= first ? taskHandle(seg.t, 'start') : null}
                      {day === seg.to && taskTo(seg.t) <= last ? taskHandle(seg.t, 'end') : null}
                    </span>
                  ) : <span key={li} className="scax-week__band scax-week__band--empty" aria-hidden="true" />))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 시간 격자 — 0시~24시 스크롤 */}
      <div className="scax-week__scroll" ref={scroller}>
        <div className="scax-week__ruler-hours">
          {hours.map((h) => <span key={h} className="scax-week__ruler-hour" style={{ height: WEEK_ROW }}>{wkLabel(h)}</span>)}
        </div>
        <div className="scax-week__days">
          {dates.map((d) => {
            const day = d.getDate();
            const picked = selected === day;
            const slots = shownSlots.filter((s) => s.day === day);
            return (
              <div
                key={d.toISOString()}
                data-day={day}
                className={`scax-week__hours${picked ? ' scax-week__hours--picked' : ''}`}
                style={{ height: 24 * WEEK_ROW }}
                onClick={() => onSelect(picked ? null : day)}
                onDragOver={(e) => { if (!canDrop(day)) return; e.preventDefault(); setDropAt({ day, min: minAt(e) }); }}
                onDragLeave={() => setDropAt((p) => (p && p.day === day ? null : p))}
                onDrop={(e) => {
                  if (!canDrop(day)) return;
                  e.preventDefault();
                  const min = minAt(e);
                  setDropAt(null);
                  onSchedule(e.dataTransfer.getData('text/plain'), day, wkClock(min), wkClock(min + 60));
                }}
              >
                {dropAt && dropAt.day === day ? (
                  <span className="scax-week__ghost" style={{ top: px(dropAt.min), height: px(60) - 2 }}>
                    {wkClock(dropAt.min)} – {wkClock(dropAt.min + 60)}
                  </span>
                ) : null}
                {slots.map((s) => {
                  const a = wkMin(s.start);
                  const b = wkMin(s.end);
                  return (
                    <span
                      key={s.id}
                      className={`scax-event scax-event--${s.kind} scax-week__slot`}
                      style={{ top: px(a), height: Math.max(px(30), px(b - a)) - 2 }}
                    >
                      <span className="scax-week__slot-title">{s.title}</span>
                      <span className="scax-week__slot-time">{s.start} – {s.end}</span>
                      {slotHandle(s, 'start')}
                      {slotHandle(s, 'end')}
                    </span>
                  );
                })}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

Object.assign(window, { WeekGrid, weekDates });
