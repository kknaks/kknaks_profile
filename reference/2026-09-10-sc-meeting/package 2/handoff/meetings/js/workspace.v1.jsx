/* 「회의」 한 화면 (4칸) — 사이드바 | 회의 목록 | 회의 상세 | 첨부·스크립트.
   업무 탭과 같은 틀이다. 목록과 상세를 페이지로 나누지 않는다.
   공용 틀은 ../../shell/js/scax-ui.jsx 가 먼저 싣는다. */
const { AgentBubble } = window;
const { Icon, Button, IconButton, Badge, SegmentedControl, Empty, StatusNote, Skeleton, AppShell, SideNav, AppHeader, AppBody, StateSwitch, Field, TextField, DateField, Composer, AutoComplete, Checklist } = window;

const MEETING_ALL = [].concat(MEETING_UPCOMING, MEETING_PAST);

/* ---- 2칸: 회의 목록 ---- */
function MeetingCard({ row, selected, onSelect, onRemove }) {
  const st = MEETING_STATUS[row.status];
  return (
    <li>
      <div role="button" tabIndex={0} className={`scax-meeting-card${selected ? ' scax-meeting-card--selected' : ''}`} onClick={() => onSelect(row.id)}>
        <div className="scax-meeting-card__top">
          <span className="scax-meeting-card__when">{row.when}</span>
          <span className="scax-meeting-card__state">
            {row.relation === 'shared' ? <span className="scax-badge scax-badge--neutral">{MEETING_COPY.sharedTag}</span> : null}
            <span className={`scax-badge scax-badge--${st.tone}`}>{st.label}</span>
          </span>
        </div>
        <p className={`scax-meeting-card__title${row.title ? '' : ' scax-meeting-card__title--untitled'}`}>{row.title || MEETING_COPY.noTitle}</p>
        <div className="scax-meeting-card__meta">
          {row.place ? <span className="scax-meeting-card__meta-item">{row.place}</span> : null}
          {row.place ? <span className="scax-meeting-card__meta-sep" /> : null}
          <span className="scax-meeting-card__meta-item">참석 {row.attendees}명</span>
        </div>
        {/* 카드를 누르면 오른쪽이 그 회의로 바뀐다 — 여는 단추를 따로 두지 않는다 */}
        {row.status === 'scheduled' ? (
          <div className="scax-meeting-card__actions">
            <button type="button" className="scax-button scax-button--outlined-neutral scax-button--sm" onClick={(e) => e.stopPropagation()}>수정</button>
            <button type="button" className="scax-button scax-button--outlined-neutral scax-button--sm" onClick={(e) => { e.stopPropagation(); onRemove(row); }}>{MEETING_COPY.remove}</button>
          </div>
        ) : null}
      </div>
    </li>
  );
}

function MeetingListRail({ state, selected, onSelect, onRemove, statusOf }) {
  let body;
  if (state === 'loading') {
    body = <div className="scax-skeleton-stack">{[0, 1, 2].map((i) => <Skeleton key={i} variant="card" />)}</div>;
  } else if (state === 'error') {
    body = <StatusNote title={MEETING_COPY.listError} action={<Button size="sm" variant="outlined" tone="neutral" label="다시 시도" />} />;
  } else if (state === 'empty') {
    body = <Empty icon="persons" title={MEETING_COPY.listEmpty} />;
  } else {
    body = (
      <React.Fragment>
        {[[MEETING_COPY.upcoming, MEETING_UPCOMING, true], [MEETING_COPY.past, MEETING_PAST, false]].map(([label, rows, counted]) => (
          <section className="scax-meeting-section" key={label}>
            <div className="scax-meeting-section__head">
              {label}
              {counted ? <span className="scax-meeting-section__count">{rows.length}</span> : null}
            </div>
            <ul className="scax-meeting-section__list">
              {rows.map((r) => <MeetingCard key={r.id} row={statusOf && statusOf(r) !== r.status ? Object.assign({}, r, { status: statusOf(r) }) : r} selected={selected === r.id} onSelect={onSelect} onRemove={onRemove} />)}
            </ul>
          </section>
        ))}
        <div className="scax-meeting-section__more"><Button size="sm" variant="outlined" tone="neutral" label={MEETING_COPY.more} /></div>
      </React.Fragment>
    );
  }
  return (
    <section className="scax-meeting-list">
      <div className="scax-meeting-list__body">{body}</div>
    </section>
  );
}

/* ---- 3칸: 회의 상세 ---- */
function AgendaBlock({ agenda, index, concludeShown, todoActions, onPromote }) {
  return (
    <section className="scax-agenda-block">
      <div className="scax-agenda-block__head">
        <h3 className="scax-agenda-block__title">안건 {index + 1}. {agenda.title}</h3>
        {concludeShown ? (
          <span className={`scax-badge scax-badge--${agenda.concluded ? 'positive' : 'neutral'}`}>
            {agenda.concluded ? MEETING_COPY.concluded : MEETING_COPY.notConcluded}
          </span>
        ) : null}
      </div>
      <p className="scax-agenda-block__source">{MEETING_AGENDA_SOURCE[agenda.source]}</p>
      {agenda.lines && agenda.lines.length ? (
        <ul className="scax-agenda-block__lines">
          {agenda.lines.map((l) => (
            <li className="scax-note-line" key={l.id}>
              <span className="scax-note-line__text">{l.text}</span>
              {/* 그 줄이 딛는 구간의 시작 시각(mm:ss) — 누르면 스크립트의 그 자리가 열린다 */}
              {l.at && l.at.length ? (
                <span className="scax-note-line__evidence">
                  {l.at.map((t) => <button type="button" className="scax-time-chip" key={t}>{t}</button>)}
                </span>
              ) : null}
            </li>
          ))}
        </ul>
      ) : null}
      {agenda.todos && agenda.todos.length ? (
        <div className="scax-agenda-block__todos">
          <p className="scax-agenda-block__todos-label">{WS_COPY.todos}</p>
          <ul className="scax-agenda-block__todo-list">
            {agenda.todos.map((t) => (
              <li className="scax-agenda-block__todo" key={t.id}>
                <span className="scax-agenda-block__todo-what">{t.title}</span>
                <span className="scax-agenda-block__todo-due">{[t.who, t.due].filter(Boolean).join(' · ')}</span>
                {todoActions ? (
                  t.linked
                    ? <span className="scax-agenda-block__todo-state">{WS_COPY.requested}</span>
                    : (
                      <React.Fragment>
                        <Button size="sm" variant="outlined" tone="neutral" label={WS_COPY.promote} onClick={() => onPromote(t)} />
                        <IconButton name="close" size={20} label={WS_COPY.dropTodo} />
                      </React.Fragment>
                    )
                ) : null}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </section>
  );
}

function DetailPanel({ state, row, onPromote, focus, onToggleFocus, onStart, onEnd }) {
  const [leftTab, setLeftTab] = React.useState('memo');
  if (!row) return <div className="scax-detail-empty"><Empty icon="document-text" title={WS_COPY.panelEmpty} /></div>;
  const status = row.status;
  const live = status === 'in_progress';
  const settling = status === 'summarizing';
  const planned = status === 'scheduled';
  const settled = status === 'done';
  const failed = status === 'failed';
  const st = MEETING_STATUS[status];
  const purpose = WS_PURPOSE[row.id];
  const agendas = planned ? WS_AGENDAS_PLANNED : live ? WS_AGENDAS_LIVE[leftTab === 'ai' ? 'ai' : 'memo'] : WS_AGENDAS_DONE;

  let note;
  if (state === 'loading' || settling) {
    note = (
      <div className="scax-note__settling">
        {settling ? <p className="scax-note__meta">{WS_COPY.summarizingNow}</p> : null}
        <div className="scax-skeleton-stack">{[0, 1, 2].map((i) => <Skeleton key={i} variant="agenda" />)}</div>
      </div>
    );
  } else if (state === 'error') {
    note = <StatusNote title="회의록을 불러오지 못했습니다" desc="네트워크 상태를 확인한 뒤 다시 시도해 주세요." action={<Button size="sm" variant="outlined" tone="neutral" label={WS_COPY.retry} />} />;
  } else if (state === 'empty' || !agendas.length) {
    note = <Empty icon="document-text" title="아직 안건이 없습니다." />;
  } else {
    note = agendas.map((a, i) => (
      <AgendaBlock key={a.id} agenda={a} index={i} concludeShown={settled} todoActions={settled} onPromote={onPromote} />
    ));
  }

  return (
    <section className="scax-detail">
      {/* 진행 표시 — 회의가 도는 동안 위에 남는다 */}
      {live ? (
        <div className="scax-live-bar">
          <span className="scax-badge scax-badge--accent">{MEETING_STATUS.in_progress.label}</span>
          <span className="scax-live-bar__elapsed">00:52:07</span>
          <span className="scax-live-bar__who">{WS_COPY.startedBy('이건학')}</span>
        </div>
      ) : null}

      <header className="scax-detail__head">
        <div className="scax-detail__title-row">
          <h2 className="scax-detail__title">{row.title || MEETING_COPY.noTitle}</h2>
          {/* 상태 배지는 셋에만 — 정리 중 · 실패 · 취소 */}
          {settling || failed || status === 'cancelled' ? <Badge tone={st.tone}>{st.label}</Badge> : null}
          {/* 오른쪽 — 목록을 접고 회의에 집중하는 자리, 그리고 예정 회의를 여는 자리 */}
          <div className="scax-detail__head-actions">
            <IconButton name={focus ? 'collapse' : 'expand'} size={20} label={focus ? WS_COPY.exitFocus : WS_COPY.focus} onClick={onToggleFocus} />
            {/* 머리에 파란 면이 둘이면 눈이 갈린다 — 여기는 선 버튼으로 낮춘다 */}
            {planned ? <Button size="sm" variant="outlined" tone="neutral" iconBefore="play" label={WS_COPY.startMeeting} onClick={onStart} /> : null}
            {live ? <Button size="sm" variant="outlined" tone="danger" label={WS_COPY.endMeeting} onClick={onEnd} /> : null}
          </div>
        </div>
        <p className="scax-detail__facts">
          {row.when} · {row.place || '—'} · 참석 {row.attendees}명{settled ? ' · 00:52:07' : ''}
        </p>
      </header>

      {failed ? (
        <div className="scax-detail__note-bar" role="alert">
          <span>{WS_COPY.convertFailed}</span>
          <Button size="sm" variant="outlined" tone="neutral" label={WS_COPY.retry} />
        </div>
      ) : null}

      {/* 목적은 전체 폭 한 줄 — 안건 바를 대신한다 */}
      {purpose ? (
        <div className="scax-detail__purpose">
          <span className="scax-detail__purpose-label">{WS_COPY.purpose}</span>
          <span className="scax-detail__purpose-text">{purpose}</span>
        </div>
      ) : null}

      <div className="scax-note">
        {/* 머리는 셋 다 같은 줄이다 — 왼쪽은 늘 「AI 회의록」, 오른쪽 자리만 상태에 따라 채워진다
            예정: 빈칸 · 진행 중: [메모|AI 요약] · 완료: [수정] */}
        <header className="scax-note__head">
          <h3 className="scax-note__title">{WS_COPY.noteHead}</h3>
          {/* 마지막 저장 시각 — 완료 회의에만, 제목 옆에 선다 (오른쪽 자리는 조작 하나로 비워 둔다) */}
          {settled ? <span className="scax-note__meta">{WS_COPY.lastSaved('16:08')}</span> : null}
          {live ? <SegmentedControl ariaLabel="회의록 트랙" value={leftTab} options={[{ value: 'memo', label: WS_COPY.tabMemo }, { value: 'ai', label: WS_COPY.tabAi }]} onChange={setLeftTab} /> : null}
          {settled ? <Button size="sm" variant="outlined" tone="neutral" label={WS_COPY.edit} /> : null}
        </header>
        {/* 진행 중에만 메모/AI 요약이 갈린다 */}

        <div className="scax-note__body">
          {note}
          {planned ? (
            <div className="scax-add-agenda">
              <input className="scax-add-agenda__input" placeholder={WS_COPY.agendaPlaceholder} aria-label={WS_COPY.agendaPlaceholder} />
              <Button size="sm" variant="outlined" tone="neutral" label={WS_COPY.addAgenda} />
            </div>
          ) : null}
        </div>
        {/* 메모를 쓰는 사람은 회의를 만든 사람 하나다 */}
        {live ? (
          <footer className="scax-note__composer">
            <input className="scax-add-agenda__input" placeholder={WS_COPY.memoPlaceholder} aria-label={WS_COPY.memoPlaceholder} />
            <Button size="sm" variant="solid" tone="primary" label="기록" />
          </footer>
        ) : null}
      </div>
    </section>
  );
}

/* ---- 4칸: 첨부 · 스크립트 ---- */
/* 레일 머리는 늘 같은 폼이다 — 상태에 따라 탭을 없애지 않는다.
   예정 회의는 스크립트가 비어 있을 뿐이다. */
function SideRail({ row, onOpenMaterial }) {
  const planned = row && row.status === 'scheduled';
  const [tab, setTab] = React.useState('materials');
  const shown = tab;
  return (
    <section className="scax-side-rail">
      <header className="scax-side-rail__header">
        <SegmentedControl ariaLabel="자료와 스크립트" value={tab} options={[{ value: 'materials', label: WS_COPY.tabMaterials }, { value: 'script', label: WS_COPY.tabScript }]} onChange={setTab} />
      </header>
      <div className="scax-side-rail__body">
        {shown === 'script' ? (
          !planned && WS_SCRIPT.length ? WS_SCRIPT.map((s) => (
            <article className="scax-script-line" key={s.id}>
              <div className="scax-script-line__side">
                <span className="scax-script-line__who">{s.who}</span>
                <span className="scax-script-line__at">{s.at}</span>
              </div>
              <p className="scax-script-line__text">{s.text}</p>
            </article>
          )) : <Empty icon="message" title={WS_COPY.scriptEmpty} />
        ) : (
          <React.Fragment>
            {WS_MATERIALS.length ? (
              <ul className="scax-file-list">
                {WS_MATERIALS.map((f) => (
                  <li className="scax-file-row" key={f.id}>
                    <Icon name="document" size={20} />
                    <button type="button" className="scax-file-row__name scax-file-row__open" onClick={() => onOpenMaterial(f)}>{f.name}</button>
                    <span className="scax-file-row__size">{f.size}</span>
                  </li>
                ))}
              </ul>
            ) : <Empty icon="document" title={WS_COPY.materialsEmpty} />}
            {/* 첨부 단추는 상태와 무관하게 늘 선다 — 회의 중에도 자료를 붙인다 */}
            <Button size="sm" variant="outlined" tone="neutral" iconBefore="plus" label={WS_COPY.attach} block />
          </React.Fragment>
        )}
      </div>
    </section>
  );
}

/* 자료 미리보기 — 드로어. 탭 안에 미리보기를 깔지 않는다 */
function MaterialDrawer({ material, onClose }) {
  if (!material) return null;
  return (
    <div className="scax-drawer-overlay" onMouseDown={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <aside className="scax-drawer" role="dialog" aria-modal="true" aria-label={material.name}>
        <header className="scax-drawer__head">
          <h2 className="scax-drawer__title">{material.name}</h2>
          <IconButton name="close" size={24} label="닫기" onClick={onClose} />
        </header>
        <div className="scax-drawer__body">
          <div className="scax-drawer__preview">미리보기</div>
          <p className="scax-drawer__meta">{material.size} · {material.who}</p>
        </div>
      </aside>
    </div>
  );
}

/* 업무 요청 모달 (CreateWorkDrawer 의 내용을 그대로 옮겼다) — 후속업무 후보를 승격하는 자리.
   승격은 언제나 업무 요청이다 (D19·D24) — 「업무/요청」 토글을 두지 않는다.
   제목·설명·기한·체크리스트만 옮겨 담고 담당은 비워 연다 (D19-3). */
function WorkRequestModal({ todo, onClose }) {
  const [title, setTitle] = React.useState('');
  const [body, setBody] = React.useState('');
  const [due, setDue] = React.useState('');
  const [person, setPerson] = React.useState('');
  const [checks, setChecks] = React.useState([]);
  React.useEffect(() => {
    if (!todo) return;
    setTitle(todo.title || '');
    setBody('');
    setDue(todo.due || '');
    setPerson('');
    setChecks([]);
  }, [todo]);
  React.useEffect(() => {
    if (!todo) return undefined;
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [todo, onClose]);
  if (!todo) return null;
  return (
    <div className="scax-modal-overlay" onMouseDown={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="scax-modal scax-modal--md" role="dialog" aria-modal="true" aria-label="업무 요청">
        <header className="scax-modal__head">
          <h2 className="scax-modal__title">업무 요청</h2>
          <IconButton name="close" size={24} label="닫기" onClick={onClose} />
        </header>
        <p className="scax-modal__hint">동료가 수락해야 그 사람의 업무가 됩니다. 희망 기한을 함께 보낼 수 있습니다.</p>
        <div className="scax-modal__body">
          <Field label="요청할 업무" required>
            <TextField value={title} onChange={setTitle} placeholder="요청할 업무명을 입력하세요" clearable ariaLabel="요청할 업무" />
          </Field>
          {/* 사람과 기한은 짧은 값이라 한 줄에 나란히 선다 */}
          <div className="scax-field-row">
            <Field label="요청 받을 사람">
              <AutoComplete value={person} onChange={setPerson} options={window.PEOPLE_OPTIONS || ['홍길동', '박민수', '유하람']} placeholder="이름으로 찾기" />
            </Field>
            <Field label="희망 기한">
              <DateField value={due} onChange={setDue} ariaLabel="희망 기한" />
            </Field>
          </div>
          <Field label="설명">
            <Composer value={body} onChange={setBody} limit={200} ariaLabel="설명" />
          </Field>
          <Field label="체크리스트">
            <Checklist
              items={checks}
              onToggle={(id) => setChecks((l) => l.map((x) => (x.id === id ? Object.assign({}, x, { done: !x.done }) : x)))}
              onText={(id, text) => setChecks((l) => l.map((x) => (x.id === id ? Object.assign({}, x, { text }) : x)))}
              onAdd={() => setChecks((l) => l.concat([{ id: 'c' + Date.now(), text: '', done: false }]))}
              onRemove={(id) => setChecks((l) => l.filter((x) => x.id !== id))}
            />
          </Field>
        </div>
        <footer className="scax-modal__foot">
          <Button variant="outlined" tone="neutral" label="닫기" onClick={onClose} />
          <Button variant="solid" tone="primary" label="업무 요청 보내기" disabled={!title} onClick={onClose} />
        </footer>
      </div>
    </div>
  );
}

function MeetingWorkspacePage() {
  const [screenState, setScreenState] = React.useState('default');
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [selected, setSelected] = React.useState('m4');
  const [removing, setRemoving] = React.useState(null);
  const [material, setMaterial] = React.useState(null);
  const [promoting, setPromoting] = React.useState(null);
  /* 집중 모드 — 목록 칸을 접는다. 사이드바 | 회의록 | 첨부 만 남는다 */
  const [focus, setFocus] = React.useState(false);
  /* 시작한 회의 — 「회의 시작」을 누른 그 자리에서 예정이 진행 중으로 넘어간다 */
  const [started, setStarted] = React.useState([]);
  const [ended, setEnded] = React.useState([]);
  const found = screenState === 'default' || screenState === 'loading' || screenState === 'error'
    ? MEETING_ALL.find((m) => m.id === selected) || null
    : null;
  const statusOf = (m) => (ended.indexOf(m.id) >= 0 ? 'summarizing' : started.indexOf(m.id) >= 0 ? 'in_progress' : m.status);
  const row = found && statusOf(found) !== found.status ? Object.assign({}, found, { status: statusOf(found) }) : found;
  const startMeeting = () => {
    if (!found) return;
    setStarted((l) => (l.indexOf(found.id) >= 0 ? l : l.concat([found.id])));
    setFocus(true);
  };
  /* 「회의 종료」 — 묻지 않고 바로 끝낸다. 받아 적은 것을 정리하는 동안 「정리 중」에 머문다 */
  const endMeeting = () => {
    if (!found) return;
    setEnded((l) => (l.indexOf(found.id) >= 0 ? l : l.concat([found.id])));
    setFocus(false);
  };
  return (
    <React.Fragment>
      <AppShell nav={<SideNav user={{ name: '유하람님', role: '기획자', avatar: './assets/avatar-person.png' }} activeId="meeting" collapsed={navCollapsed} onCollapse={() => setNavCollapsed((v) => !v)} />}>
        <AppHeader
          title="회의"
          actions={(
            <React.Fragment>
              <Button variant="outlined" tone="primary" label="회의 생성" />
              <Button variant="solid" tone="primary" iconBefore="play" label="빠른 시작" />
            </React.Fragment>
          )}
        />
        <AppBody
          railLeft={focus ? null : <MeetingListRail state={screenState} selected={selected} onSelect={setSelected} onRemove={setRemoving} statusOf={statusOf} />}
          railRight={row ? <SideRail row={row} onOpenMaterial={setMaterial} /> : null}
        >
          <DetailPanel state={screenState} row={row} onPromote={setPromoting} focus={focus} onToggleFocus={() => setFocus((v) => !v)} onStart={startMeeting} onEnd={endMeeting} />
        </AppBody>
      </AppShell>
      <AgentBubble message={WS_COPY.agent} />
      <MaterialDrawer material={material} onClose={() => setMaterial(null)} />
      {/* 「업무 생성」은 업무 요청 모달을 연다 — 레거시 CreateWorkDrawer 의 내용 그대로다 */}
      <WorkRequestModal todo={promoting} onClose={() => setPromoting(null)} />
      {removing ? (
        <div className="scax-modal-overlay" onMouseDown={(e) => { if (e.target === e.currentTarget) setRemoving(null); }}>
          <div className="scax-modal scax-modal--sm" role="alertdialog" aria-modal="true" aria-label={MEETING_COPY.deleteTitle}>
            <header className="scax-modal__head">
              <h2 className="scax-modal__title">{MEETING_COPY.deleteTitle}</h2>
              <IconButton name="close" size={24} label="닫기" onClick={() => setRemoving(null)} />
            </header>
            <div className="scax-modal__body"><p className="scax-modal__text">{MEETING_COPY.deleteBody}</p></div>
            <footer className="scax-modal__foot"><Button variant="solid" tone="danger" label={MEETING_COPY.deleteMeeting} onClick={() => setRemoving(null)} /></footer>
          </div>
        </div>
      ) : null}
      <StateSwitch value={screenState} onChange={setScreenState} />
    </React.Fragment>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<MeetingWorkspacePage />);
