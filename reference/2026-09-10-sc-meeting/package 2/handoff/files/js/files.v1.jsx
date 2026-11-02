/* 「자료」 화면 — 좌 레일(프로젝트 셀렉터 + 자료 트리 + 만들기/업로드)만. 본문은 아직 비어 있다.
   폴더/문서 만들기: 머리의 「+」 또는 트리에서 마우스 우클릭. 만든 직후 이름 입력 칸에 커서가 깜빡인다.
   공용 틀은 ../../shell/js/scax-ui.jsx, 트리 데이터는 ../../projects/js/data.js 의 PROJECT_FILE_TREE. */
const { Icon, Select, Button, IconButton, Popover, Empty, StatusNote, AppShell, SideNav, AppHeader, AppBody } = window;

/* 트리에서 한 건 집어내기 — 본부·우 레일이 같은 것을 보게. */
function findNode(list, id) {
  for (let i = 0; i < list.length; i += 1) {
    const n = list[i];
    if (n.id === id) return n;
    if (n.children) { const hit = findNode(n.children, id); if (hit) return hit; }
  }
  return null;
}

/* 이름 입력 — 새로 만들거나 이름을 바꿀 때만 뜬다. 뜨는 즉시 커서가 들어간다. */
function NameField({ value, onDone, onCancel }) {
  const ref = React.useRef(null);
  React.useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.focus();
    const dot = value.lastIndexOf('.');
    el.setSelectionRange(0, dot > 0 ? dot : value.length);
  }, []);
  return (
    <input
      ref={ref}
      className="scax-file-tree__input"
      defaultValue={value}
      onKeyDown={(e) => {
        if (e.key === 'Enter') onDone(e.target.value);
        if (e.key === 'Escape') onCancel();
        e.stopPropagation();
      }}
      onBlur={(e) => onDone(e.target.value)}
      onClick={(e) => e.stopPropagation()}
      aria-label="이름"
    />
  );
}

function FileTreeNode({ node, depth, openIds, onToggle, selected, onSelect, folderId, onFolder, editingId, onRename, onCancel, onMenu }) {
  const isFolder = !!node.children;
  const open = openIds.indexOf(node.id) >= 0;
  const pad = { paddingLeft: `calc(var(--scax-space-300) + ${depth} * var(--scax-space-500))` };
  const editing = node.id === editingId;
  const context = (e) => { e.preventDefault(); e.stopPropagation(); onMenu(e.clientX, e.clientY, node, isFolder); };
  return (
    <li>
      {isFolder ? (
        <button
          type="button"
          className={`scax-file-tree__row scax-file-tree__row--folder${node.id === folderId ? ' scax-file-tree__row--selected' : ''}`}
          style={pad}
          aria-expanded={open}
          onClick={() => { onToggle(node.id); onFolder(node.id); }}
          onContextMenu={context}
        >
          <Icon name={open ? 'chevron-down' : 'chevron-right'} size={12} />
          <Icon name="folder" size={16} />
          {editing
            ? <NameField value={node.name} onDone={(v) => onRename(node.id, v)} onCancel={onCancel} />
            : <span className="scax-file-tree__name">{node.name}</span>}
          {editing ? null : <span className="scax-file-tree__count">{node.children.length}</span>}
        </button>
      ) : (
        <button
          type="button"
          className={`scax-file-tree__row${node.id === selected ? ' scax-file-tree__row--selected' : ''}`}
          style={pad}
          onClick={() => onSelect(node.id)}
          onContextMenu={context}
        >
          <span className="scax-file-tree__twig" />
          <Icon name="document" size={16} />
          {editing
            ? <NameField value={node.name} onDone={(v) => onRename(node.id, v)} onCancel={onCancel} />
            : <span className="scax-file-tree__name">{node.name}</span>}
          {editing ? null : <span className="scax-file-tree__meta">{node.meta}</span>}
        </button>
      )}
      {isFolder && open ? (
        <ul className="scax-file-tree__list">
          {node.children.map((c) => (
            <FileTreeNode
              key={c.id} node={c} depth={depth + 1} openIds={openIds} onToggle={onToggle}
              selected={selected} onSelect={onSelect} folderId={folderId} onFolder={onFolder}
              editingId={editingId} onRename={onRename} onCancel={onCancel} onMenu={onMenu}
            />
          ))}
        </ul>
      ) : null}
    </li>
  );
}

/* 「+」 — 최상위(또는 고른 폴더) 에 만든다. */
function CreateMenu({ onCreate }) {
  const [open, setOpen] = React.useState(false);
  const close = React.useCallback(() => setOpen(false), []);
  const pick = (kind) => { onCreate(kind); close(); };
  return (
    <span className="scax-file-create">
      <IconButton name="plus" size={20} label="새로 만들기" onClick={() => setOpen((v) => !v)} />
      <Popover open={open} onClose={close} placement="below-start">
        <button type="button" role="option" className="scax-popover__option" onClick={() => pick('folder')}>
          <Icon name="folder" size={16} />
          새 폴더
        </button>
        <button type="button" role="option" className="scax-popover__option" onClick={() => pick('md')}>
          <Icon name="document" size={16} />
          새 문서 (.md)
        </button>
      </Popover>
    </span>
  );
}

/* 우클릭 메뉴 — 커서 자리에 뜬다. 레일이 잘라내지 않도록 fixed 로 띄운다. */
function ContextMenu({ menu, onClose, onCreate, onRename }) {
  React.useEffect(() => {
    if (!menu) return undefined;
    const off = () => onClose();
    const key = (e) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('mousedown', off);
    document.addEventListener('keydown', key);
    window.addEventListener('blur', off);
    return () => { document.removeEventListener('mousedown', off); document.removeEventListener('keydown', key); window.removeEventListener('blur', off); };
  }, [menu, onClose]);
  if (!menu) return null;
  const target = menu.isFolder ? menu.node.name : '이 폴더';
  return (
    <div className="scax-context-menu" style={{ left: menu.x, top: menu.y }} role="menu" onMouseDown={(e) => e.stopPropagation()}>
      <span className="scax-context-menu__where">{target}</span>
      <button type="button" role="menuitem" className="scax-context-menu__item" onClick={() => { onCreate('folder', menu); onClose(); }}>
        <Icon name="folder" size={16} />
        폴더 만들기
      </button>
      <button type="button" role="menuitem" className="scax-context-menu__item" onClick={() => { onCreate('md', menu); onClose(); }}>
        <Icon name="document" size={16} />
        문서 만들기 (.md)
      </button>
      <span className="scax-context-menu__sep" />
      <button type="button" role="menuitem" className="scax-context-menu__item" onClick={() => { onRename(menu.node.id); onClose(); }}>
        <Icon name="pencil" size={16} />
        이름 바꾸기
      </button>
    </div>
  );
}

/* ---- 본부: 마크다운만 그린다 ---- */
function FileView({ node }) {
  if (!node) {
    return (
      <div className="scax-file-main">
        <Empty icon="document" title="볼 문서를 선택하세요" desc="자료함에서 .md 문서를 골르면 여기에 그려줍니다." />
      </div>
    );
  }
  const isMd = /\.md$/i.test(node.name);
  if (!isMd) {
    return (
      <div className="scax-file-main">
        <StatusNote
          tone="neutral"
          title="문서 보기는 .md 만 지원합니다"
          desc={`${node.name} 은 미리보기를 지원하지 않는 형식입니다. 내려받아 여십시오.`}
          action={<Button variant="outlined" tone="neutral" label="내려받기" />}
        />
      </div>
    );
  }
  const src = FILE_DOCS[node.id];
  const toc = src ? mdOutline(src) : [];
  return (
    <div className="scax-file-main">
      {src ? (
        <div className="scax-file-doc">
          <article className="scax-md">{renderMarkdown(src)}</article>
          {toc.length > 1 ? (
            <nav className="scax-md-toc" aria-label="목차">
              <span className="scax-md-toc__head">목차</span>
              <ul className="scax-md-toc__list">
                {toc.map((h) => (
                  <li key={h.id} className={`scax-md-toc__item scax-md-toc__item--l${h.level}`}>
                    <a className="scax-md-toc__link" href={`#${h.id}`}>{h.text}</a>
                  </li>
                ))}
              </ul>
            </nav>
          ) : null}
        </div>
      ) : <Empty icon="document" title="빈 문서입니다" desc="아직 내용이 없습니다." />}
    </div>
  );
}

/* ---- 우 레일: 파일 메타데이타 ---- */
function FileMetaRail({ node }) {
  if (!node) {
    return <section className="scax-pj-side"><Empty icon="document" title="자료를 선택하세요" desc="고른 자료의 메타데이타가 여기에 나옵니다." /></section>;
  }
  const isFolder = !!node.children;
  const m = FILE_META[node.id] || {};
  const kind = isFolder ? '폴더' : /\.md$/i.test(node.name) ? 'Markdown (.md)' : node.name.slice(node.name.lastIndexOf('.') + 1).toUpperCase();
  const facts = [
    ['종료', kind],
    isFolder ? ['항목', `${node.children.length}개`] : null,
    ['경로', m.path ? `자료함 / ${m.path}` : '자료함'],
    ['작성', m.author || (node.meta ? node.meta.split(' · ')[1] : null) || '—'],
    ['만든 날', m.created || '—'],
    ['수정', m.updated || '—'],
    isFolder ? null : ['크기', m.size || '—'],
    isFolder ? null : ['분량', m.words ? `${m.words} 단어` : '—'],
    isFolder ? null : ['버전', m.version || 'v1'],
  ].filter(Boolean);
  return (
    <section className="scax-pj-side">
      <header className="scax-pj-side__head">
        <h2 className="scax-pj-side__title">{node.name}</h2>
      </header>
      <div className="scax-pj-side__body">
        <section className="scax-pj-side__block">
          <h3 className="scax-pj-side__block-title">메타데이타</h3>
          <dl className="scax-pj-facts">
            {facts.map(([kk, v]) => (
              <React.Fragment key={kk}>
                <dt className="scax-pj-facts__key">{kk}</dt>
                <dd className="scax-pj-facts__val">{v}</dd>
              </React.Fragment>
            ))}
          </dl>
        </section>
        {m.tags && m.tags.length ? (
          <section className="scax-pj-side__block">
            <h3 className="scax-pj-side__block-title">태그</h3>
            <div className="scax-file-tags">
              {m.tags.map((t) => <span className="scax-badge scax-badge--neutral" key={t}>{t}</span>)}
            </div>
          </section>
        ) : null}
        {m.task ? (
          <section className="scax-pj-side__block">
            <h3 className="scax-pj-side__block-title">연결된 업무</h3>
            <a className="scax-file-link" href="./Projects.html">
              <Icon name="square-check" size={16} />
              <span className="scax-file-link__text">{m.task}</span>
              <Icon name="chevron-right" size={12} />
            </a>
          </section>
        ) : null}
      </div>
    </section>
  );
}

function FileRail({ project, onProject, tree, openIds, onToggle, fileId, onFile, folderId, onFolder, onCreate, editingId, onRename, onCancel, onMenu }) {
  return (
    <section className="scax-gutter-list" onContextMenu={(e) => { e.preventDefault(); onMenu(e.clientX, e.clientY, null, false); }}>
      <header className="scax-gutter-list__header">
        <h2 className="scax-gutter-list__title">
          <Icon name="folder" size={24} />
          자료함
        </h2>
        <Select ariaLabel="프로젝트 선택" value={project} options={PROJECT_OPTIONS} onChange={onProject} />
        <CreateMenu onCreate={onCreate} />
      </header>
      <div className="scax-gutter-list__body">
        <ul className="scax-file-tree__list scax-file-tree__list--root">
          {tree.map((n) => (
            <FileTreeNode
              key={n.id} node={n} depth={0} openIds={openIds} onToggle={onToggle}
              selected={fileId} onSelect={onFile} folderId={folderId} onFolder={onFolder}
              editingId={editingId} onRename={onRename} onCancel={onCancel} onMenu={onMenu}
            />
          ))}
        </ul>
      </div>
      <footer className="scax-file-upload">
        <div className="scax-dropzone">
          <div className="scax-dropzone__head">
            <Icon name="paperclip" size={20} />
            <span className="scax-dropzone__hint">파일을 여기로 끌어다 놓거나</span>
            <Button variant="outlined" tone="neutral" size="sm" iconBefore="plus" label="업로드" />
          </div>
        </div>
      </footer>
    </section>
  );
}

let seq = 0;
const todayMeta = '09-17 · 유하람';

/* 트리를 한 번 훑어 노드를 갈아 끼운다 (불변). */
const mapTree = (list, fn) => list.map((n) => {
  const next = fn(n);
  return next.children ? Object.assign({}, next, { children: mapTree(next.children, fn) }) : next;
});
const dropNode = (list, id) => list
  .filter((n) => n.id !== id)
  .map((n) => (n.children ? Object.assign({}, n, { children: dropNode(n.children, id) }) : n));

function FilesPage() {
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [project, setProject] = React.useState(PROJECT_OPTIONS[0].value);
  const [tree, setTree] = React.useState(PROJECT_FILE_TREE);
  const [fileId, setFileId] = React.useState('');
  const [folderId, setFolderId] = React.useState('');
  const [openIds, setOpenIds] = React.useState(PROJECT_FILE_TREE.filter((n) => n.open).map((n) => n.id));
  const [editingId, setEditingId] = React.useState('');
  const [fresh, setFresh] = React.useState('');
  const [menu, setMenu] = React.useState(null);
  const toggle = (id) => setOpenIds((l) => (l.indexOf(id) >= 0 ? l.filter((x) => x !== id) : l.concat([id])));
  const current = fileId ? findNode(tree, fileId) : folderId ? findNode(tree, folderId) : null;

  /* 지금은 폴더와 .md 문서만 만든다. 만든 자리를 펴고 이름 입력에 커서를 둔다. */
  const create = (kind, ctx) => {
    seq += 1;
    const id = `n-${seq}`;
    const node = kind === 'folder' ? { id, name: '새 폴더', children: [] } : { id, name: '새 문서.md', meta: todayMeta };
    /* 우클릭한 곳이 폴더면 그 안, 파일이면 최상위, 빈 곳이면 고른 폴더 또는 최상위 */
    const into = ctx && ctx.node ? (ctx.isFolder ? ctx.node.id : '') : folderId;
    setTree((t) => (into ? mapTree(t, (n) => (n.id === into && n.children ? Object.assign({}, n, { children: n.children.concat([node]) }) : n)) : t.concat([node])));
    setOpenIds((l) => {
      const next = into && l.indexOf(into) < 0 ? l.concat([into]) : l;
      return kind === 'folder' ? next.concat([id]) : next;
    });
    if (kind === 'folder') setFolderId(id); else { setFileId(id); setFolderId(''); }
    setEditingId(id);
    setFresh(id);
  };

  const rename = (id, name) => {
    const clean = (name || '').trim();
    if (!clean) {
      /* 새로 만든 것을 이름 없이 빠져나가면 없던 일로 */
      if (fresh === id) setTree((t) => dropNode(t, id));
      setEditingId('');
      setFresh('');
      return;
    }
    setTree((t) => mapTree(t, (n) => (n.id === id ? Object.assign({}, n, { name: clean }) : n)));
    setEditingId('');
    setFresh('');
  };
  const cancelEdit = () => {
    if (fresh) setTree((t) => dropNode(t, fresh));
    setEditingId('');
    setFresh('');
  };

  return (
    <React.Fragment>
      <AppShell nav={<SideNav user={{ name: '유하람님', role: '기획자', avatar: './assets/avatar-person.png' }} activeId="files" collapsed={navCollapsed} onCollapse={() => setNavCollapsed((v) => !v)} />}>
        <AppHeader title="자료" />
        <AppBody
          railLeft={(
            <FileRail
              project={project} onProject={setProject} tree={tree} openIds={openIds} onToggle={toggle}
              fileId={fileId} onFile={setFileId} folderId={folderId} onFolder={(id) => { setFolderId(id); setFileId(''); }}
              onCreate={(kind) => create(kind, null)} editingId={editingId} onRename={rename} onCancel={cancelEdit}
              onMenu={(x, y, node, isFolder) => setMenu({ x, y, node, isFolder })}
            />
          )}
          railRight={<FileMetaRail node={current} />}
        >
          <FileView node={fileId ? current : null} />
        </AppBody>
      </AppShell>
      <ContextMenu menu={menu} onClose={() => setMenu(null)} onCreate={create} onRename={setEditingId} />
    </React.Fragment>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<FilesPage />);
