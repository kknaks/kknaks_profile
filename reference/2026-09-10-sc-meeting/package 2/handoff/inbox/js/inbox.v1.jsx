/* 「메시지함」 화면 — 좌 레일(쌓인 메시지 목록) + 본문(고른 것의 원문).
   역할은 수집한 메일·슬랙을 **조회**하고 **답장**하는 것이다 (2026-10-06 — 답장이 1단계에 들어왔다).
   답장 = 메일 답장·전체 답장 · 슬랙 메시지 · 슬랙 스레드 답글 · 첨부 파일 보내기(끌어다 놓기 + 첨부 창).
   그 밖의 행동 — 업무로 옮기기 · 확인완료 · 업무/참고 배지 · 리액션 추가 · hover 행동 막대 · 전달 · 새 메일 — 은 여전히 없다.
   레일 카드: 메일은 단건 카드, 슬랙·카톡은 대화방 카드 한 장(슬랙 채널 · DM · 그룹 DM / 카톡 1:1 · 단체방 하나 = 카드 하나, 마지막 3줄 미리보기).
   카톡(2026-10-06)은 조회 전용 — 슬랙과 같은 대화 모양이지만 입력창·스레드·답장이 없다. 첨부는 사진·앨범·파일 · 동영상/음성 표시 · 이모티콘 글자 · 만료됨.
   본문: 메일은 머리 표 + HTML 원문 틀 + 첨부 + 원문 아래 답장 작성 칸, 슬랙은 대화방처럼(날짜 구분 · 연속 메시지 묶음 ·
   서식 · 첨부 · 리액션) + 맨 아래 입력창. 「답글 N개」를 누르면 오른쪽 스레드 패널이 열려 3열이 된다(진짜 슬랙처럼).
   본문은 남은 폭을 다 쓴다(읽기 폭 제한 없음).
   첨부는 DS 부품을 쓴다 — 메일은 DropZone + FileList, 슬랙 입력창은 DropZone 의 `--over` 모양 + FileList.
   공용 틀은 ../../shell/js/scax-ui.jsx, 데이터는 ./data.js. 화면 네 상태 · 답장 상태는 화면 아래 DevSwitch(시안 전용)로 본다. */
const { Icon, Button, IconButton, Badge, SegmentedControl, GutterList, Empty, StatusNote, Skeleton, AppShell, SideNav, AppHeader, AppBody } = window;
/* DS 첨부 부품 — _ds_bundle.js 가 window.SCAX(= SCAX_DS) 로 싣는다 */
const { DropZone, FileList } = window.SCAX_DS || {};

const ME = 'me';
const MAIL_LIMIT = 25 * 1024 * 1024; /* Gmail 한 번에 25MB — 계약 사실 */

function fmtSize(bytes) {
  if (bytes >= 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
  return `${Math.max(1, Math.round(bytes / 1024))} KB`;
}
function extOf(name) { const m = /\.([a-z0-9]+)$/i.exec(name); return m ? m[1].toLowerCase() : 'file'; }

/* 고른 파일(File 또는 목데이터) → 한 줄 */
let fileSeq = 0;
function stage(list) {
  return list.map((f) => { fileSeq += 1; return { key: `f${fileSeq}`, name: f.name, bytes: f.size, type: extOf(f.name) }; });
}

/* DS FileList 줄 — 종류 글리프 · 이름 · 크기 · 못 붙은 이유 · 빼기 */
function fileRows(files, onRemove, limit) {
  return files.map((f) => ({
    key: f.key,
    name: f.name,
    size: fmtSize(f.bytes),
    icon: /^(png|jpe?g|gif|webp)$/.test(f.type) ? 'blank' : 'document',
    reason: limit && f.bytes > limit ? '25MB 를 넘어 붙지 않습니다' : null,
    onRemove: onRemove ? () => onRemove(f.key) : undefined,
    removeLabel: `${f.name} 빼기`,
  }));
}

/* 첨부 창 열기 — 숨은 <input type=file> 을 누른다 */
function useFilePicker(onFiles) {
  const ref = React.useRef(null);
  const input = <input ref={ref} type="file" multiple hidden aria-label="첨부할 파일 고르기" onChange={(e) => { if (e.target.files && e.target.files.length) onFiles(Array.from(e.target.files)); e.target.value = ''; }} />;
  return [input, () => ref.current && ref.current.click()];
}

const SOURCE_TABS = [
  { value: 'all', label: '전체' },
  { value: 'mail', label: '메일' },
  { value: 'slack', label: '슬랙' },
  { value: 'kakao', label: '카톡' },
];

const FILE_TYPE = {
  pdf: { label: 'PDF', mark: 'PDF' },
  md: { label: 'Markdown', mark: 'MD' },
  xlsx: { label: 'Excel 스프레드시트', mark: 'XLS' },
  docx: { label: 'Word 문서', mark: 'DOC' },
  zip: { label: 'ZIP 압축 파일', mark: 'ZIP' },
  png: { label: 'PNG 이미지', mark: 'IMG' },
  jpg: { label: 'JPEG 이미지', mark: 'IMG' },
};
const fileType = (t) => FILE_TYPE[t] || { label: t.toUpperCase(), mark: t.toUpperCase().slice(0, 3) };

const userOf = (id) => window.SLACK_USERS[id] || (window.KAKAO_USERS || {})[id] || { name: id, initial: '?', tone: 'a' };

/* ===== 서식 — 세그먼트 · 블록 ===== */

function segText(seg) {
  if (typeof seg === 'string') return seg;
  if (seg.b) return seg.b;
  if (seg.code) return seg.code;
  if (seg.mention) return `@${seg.mention}`;
  if (seg.link) return seg.link;
  if (seg.emoji) return seg.emoji;
  return '';
}

function itemSegs(item) { return Array.isArray(item) ? item : item.segs; }

/* 미리보기 한 줄 — 블록을 평문으로 */
function plainText(body) {
  return body.map((blk) => {
    if (blk.p) return blk.p.map(segText).join('');
    const items = blk.ol || blk.ul || [];
    return items.map((it) => itemSegs(it).map(segText).join('')).join(' · ');
  }).join(' ');
}

/* 레일 미리보기 한 줄 — 글이 없으면 첨부 종류로 */
function previewText(m) {
  const t = plainText(m.body);
  if (t) return t;
  if (m.album) return `사진 ${m.album.count}장`;
  if (m.photo || m.images) return '사진';
  if (m.video) return '동영상';
  if (m.voice) return '음성 메시지';
  if (m.emoticon) return '(이모티콘)';
  if (m.files || m.pdf) return '파일';
  return '첨부 파일';
}

function Segs({ segs }) {
  return segs.map((seg, i) => {
    if (typeof seg === 'string') return <React.Fragment key={i}>{seg}</React.Fragment>;
    if (seg.b) return <strong key={i}>{seg.b}</strong>;
    if (seg.code) return <code className="scax-msg-code" key={i}>{seg.code}</code>;
    if (seg.mention) return <span className="scax-msg-mention" key={i}>@{seg.mention}</span>;
    if (seg.link) return <a className="scax-msg-link" key={i} href={seg.href} target="_blank" rel="noreferrer">{seg.link}</a>;
    if (seg.emoji) return <span className="scax-msg-emoji" key={i}>{seg.emoji}</span>;
    return null;
  });
}

function ListItems({ items }) {
  return items.map((it, i) => (
    <li key={i}>
      <Segs segs={itemSegs(it)} />
      {!Array.isArray(it) && it.sub ? (
        <ul className="scax-msg-list scax-msg-list--sub">
          {it.sub.map((s, j) => <li key={j}><Segs segs={s} /></li>)}
        </ul>
      ) : null}
    </li>
  ));
}

function Blocks({ body }) {
  return body.map((blk, i) => {
    if (blk.p) return <p className="scax-msg-p" key={i}><Segs segs={blk.p} /></p>;
    if (blk.ol) return <ol className="scax-msg-list" key={i}><ListItems items={blk.ol} /></ol>;
    if (blk.ul) return <ul className="scax-msg-list" key={i}><ListItems items={blk.ul} /></ul>;
    return null;
  });
}

/* ===== 첨부 부품 — 메일·슬랙이 같이 쓴다 ===== */

function FileMark({ type, size = 'md' }) {
  return <span className={`scax-fmark scax-fmark--${type} scax-fmark--size-${size}`} aria-hidden="true">{fileType(type).mark}</span>;
}

/* 파일 카드 — 유형 색 아이콘 · 굵은 이름(말줄임) · 아래 유형명. 받기는 보이게만 둔다(조회에 속한다). */
function FileCard({ file }) {
  return (
    <div className="scax-fcard" title={file.name}>
      <FileMark type={file.type} />
      <span className="scax-fcard__text">
        <span className="scax-fcard__name">{file.name}</span>
        <span className="scax-fcard__type">{fileType(file.type).label}{file.size ? ` · ${file.size}` : ''}</span>
      </span>
      <IconButton name="arrow-down" size={18} label={`${file.name} 받기`} />
    </div>
  );
}

/* 접히는 머리 — 「3개의 첨부 파일 ▾」·「PDF ▾」·「파일명 ▾」 */
function FoldHead({ label, open, onToggle, end }) {
  return (
    <div className="scax-fold">
      <button type="button" className="scax-fold__toggle" aria-expanded={open} onClick={onToggle}>
        <span className="scax-fold__label">{label}</span>
        <Icon name={open ? 'chevron-down' : 'chevron-right'} size={16} />
      </button>
      {end ? <span className="scax-fold__sep" aria-hidden="true" /> : null}
      {end}
    </div>
  );
}

function FileGroup({ files }) {
  const [open, setOpen] = React.useState(true);
  return (
    <div className="scax-attach">
      <FoldHead
        label={`${files.length}개의 첨부 파일`}
        open={open}
        onToggle={() => setOpen((v) => !v)}
        end={<a className="scax-fold__action" href="#download-all" onClick={(e) => e.preventDefault()}><Icon name="arrow-down" size={16} />모두 다운로드</a>}
      />
      {open ? <div className="scax-fcard-row">{files.map((f) => <FileCard key={f.name} file={f} />)}</div> : null}
    </div>
  );
}

/* PDF 하나 — 큰 카드: 위 아이콘·이름·유형, 아래 첫 페이지 미리보기(잘린 채) */
function PdfBlock({ pdf }) {
  const [open, setOpen] = React.useState(true);
  return (
    <div className="scax-attach">
      <FoldHead label="PDF" open={open} onToggle={() => setOpen((v) => !v)} />
      {open ? (
        <div className="scax-pdf">
          <div className="scax-pdf__head">
            <FileMark type="pdf" />
            <span className="scax-fcard__text">
              <span className="scax-fcard__name">{pdf.name}</span>
              <span className="scax-fcard__type">PDF · {pdf.pages}쪽 · {pdf.size}</span>
            </span>
            <IconButton name="arrow-down" size={18} label={`${pdf.name} 받기`} />
          </div>
          <div className="scax-pdf__page" aria-label={`${pdf.name} 첫 페이지 미리보기`}>
            <div className="scax-pdf__sheet">
              <p className="scax-pdf__title">{pdf.preview.title}</p>
              {pdf.preview.lines.map((l) => <p className="scax-pdf__line" key={l}>{l}</p>)}
              <span className="scax-pdf__bar" /><span className="scax-pdf__bar scax-pdf__bar--short" /><span className="scax-pdf__bar" />
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

/* 이미지 — 가짜 썸네일(목업). 실제로는 받은 이미지가 선다 */
function Thumb({ caption, size = 'lg' }) {
  return (
    <span className={`scax-thumb scax-thumb--${size}`}>
      <Icon name="blank" size={size === 'lg' ? 32 : 20} />
      <span className="scax-thumb__cap">{caption}</span>
    </span>
  );
}

function ImageBlock({ img }) {
  const [open, setOpen] = React.useState(true);
  return (
    <div className="scax-attach">
      <FoldHead label={img.name} open={open} onToggle={() => setOpen((v) => !v)} />
      {open ? <Thumb caption={img.caption} /> : null}
    </div>
  );
}

/* URL 미리보기(언퍼일) — 둥근 상자 · 사이트 · 굵은 제목 · 설명 2줄 · 도메인 · 오른쪽 썸네일 */
function Unfurl({ u }) {
  return (
    <div className={`scax-unfurl${u.thumb ? '' : ' scax-unfurl--text'}`}>
      <div className="scax-unfurl__text">
        <span className="scax-unfurl__site">{u.site}</span>
        <span className="scax-unfurl__title">{u.title}</span>
        <span className="scax-unfurl__desc">{u.desc}</span>
        <span className="scax-unfurl__domain">{u.domain}</span>
      </div>
      {u.thumb ? <Thumb caption={u.thumb.caption} size="sm" /> : null}
    </div>
  );
}

function Reactions({ list }) {
  return (
    <div className="scax-reacts" aria-label="리액션">
      {list.map((r) => (
        <span className="scax-react" key={r.emoji}>
          <span className="scax-react__emoji">{r.emoji}</span>
          <span className="scax-react__count">{r.count}</span>
        </span>
      ))}
    </div>
  );
}

/* ===== 슬랙 메시지 ===== */

function Avatar({ user, size = 'md' }) {
  return <span className={`scax-msg-avatar scax-msg-avatar--${user.tone} scax-msg-avatar--${size}`} aria-hidden="true">{user.initial}</span>;
}

function MessageExtras({ m }) {
  return (
    <React.Fragment>
      {m.unfurl ? <Unfurl u={m.unfurl} /> : null}
      {m.images ? m.images.map((img) => <ImageBlock key={img.name} img={img} />) : null}
      {m.files ? (m.files.length > 1 ? <FileGroup files={m.files} /> : <div className="scax-attach"><FileCard file={m.files[0]} /></div>) : null}
      {m.pdf ? <PdfBlock pdf={m.pdf} /> : null}
      {m.photo ? <ImageBlock img={m.photo} /> : null}
      {m.album ? <AlbumBlock album={m.album} /> : null}
      {m.video ? <MediaChip kind="video" label="동영상" length={m.video.length} /> : null}
      {m.voice ? <MediaChip kind="voice" label="음성 메시지" length={m.voice.length} /> : null}
      {m.emoticon ? <span className="scax-msg-emoticon">(이모티콘)</span> : null}
      {m.expired ? <ExpiredCard item={m.expired} /> : null}
      {m.reactions ? <Reactions list={m.reactions} /> : null}
    </React.Fragment>
  );
}

/* ===== 카톡 첨부 (2026-10-06) =====
   사진·앨범·파일은 수집할 때 받아 우리 쪽에 저장해 보여 준다(카톡 CDN 링크가 며칠이면 끊기므로).
   동영상·음성은 받지 않고 표시만 · 이모티콘은 「(이모티콘)」 글자 · 수집 전에 이미 끊긴 옛 첨부는 「만료됨」. */

/* 앨범 — 여러 장을 격자로. 다섯 장째부터는 마지막 칸에 「+N」 */
function AlbumBlock({ album }) {
  const [open, setOpen] = React.useState(true);
  const shown = album.captions.slice(0, 4);
  const rest = album.count - shown.length;
  return (
    <div className="scax-attach">
      <FoldHead label={`사진 ${album.count}장`} open={open} onToggle={() => setOpen((v) => !v)} />
      {open ? (
        <div className={`scax-album scax-album--${Math.min(album.count, 4)}`}>
          {shown.map((c, i) => (
            <span className="scax-album__cell" key={c}>
              <Thumb caption={c} size="cell" />
              {i === shown.length - 1 && rest > 0 ? <span className="scax-album__more">+{rest}</span> : null}
            </span>
          ))}
        </div>
      ) : null}
    </div>
  );
}

/* 동영상·음성 — 받지 않는다. 회색 칩으로 무엇이 왔는지만 */
function MediaChip({ kind, label, length }) {
  return (
    <div className="scax-attach">
      <span className={`scax-media-chip scax-media-chip--${kind}`}>
        <Icon name={kind === 'video' ? 'play' : 'pending'} size={16} />
        <span className="scax-media-chip__label">{label}</span>
        {length ? <span className="scax-media-chip__len">{length}</span> : null}
        <span className="scax-media-chip__note">받지 않음 — 카카오톡에서 보기</span>
      </span>
    </div>
  );
}

/* 만료됨 — 수집하기 전에 카톡 링크가 이미 끊긴 옛 첨부. 복구하지 않는다 */
function ExpiredCard({ item }) {
  return (
    <div className="scax-attach">
      <div className="scax-fcard scax-fcard--expired" title={item.name}>
        <span className="scax-fmark scax-fmark--expired scax-fmark--size-md" aria-hidden="true">{item.kind === '사진' ? 'IMG' : 'FILE'}</span>
        <span className="scax-fcard__text">
          <span className="scax-fcard__name">{item.name}</span>
          <span className="scax-fcard__type">{item.kind} · 만료됨</span>
        </span>
      </div>
    </div>
  );
}

/* ===== 슬랙 입력창 — 채널 맨 아래 · 스레드 패널 아래 둘 다 이것 =====
   서식 막대(굵게 · 기울임 · 링크 · 목록 · 코드) · 왼쪽 「+」 = 첨부 창 · 오른쪽 보내기.
   파일을 입력창 위로 끌어오면 칸 전체가 DS DropZone 의 `--over` 모양이 된다. 고른 파일은 칸 안에 DS FileList 로 선다. */
const FORMAT_TOOLS = [
  { id: 'b', label: '굵게', glyph: 'B' },
  { id: 'i', label: '기울임', glyph: 'I' },
  { id: 'link', label: '링크', icon: 'link' },
  { id: 'list', label: '목록', icon: 'list-category' },
  { id: 'code', label: '코드', glyph: '</>' },
];

function SlackComposer({ placeholder, onSend, demo }) {
  const [text, setText] = React.useState(demo === 'draft' ? '교육 자료 확인했습니다. 3장 수정본 같이 올려요' : '');
  const [files, setFiles] = React.useState(() => (demo === 'draft' ? stage([{ name: '교육자료_심화편_3장_수정.md', size: 21 * 1024 }]) : []));
  const [over, setOver] = React.useState(demo === 'drag');
  const add = (list) => setFiles((l) => l.concat(stage(list)));
  const [picker, openPicker] = useFilePicker(add);
  const canSend = text.trim() || files.length;
  const send = () => {
    if (!canSend) return;
    onSend(text.trim(), files);
    setText(''); setFiles([]);
  };
  return (
    <div
      className={`scax-composer-box${over ? ' scax-dropzone scax-dropzone--over' : ''}`}
      onDragOver={(e) => { e.preventDefault(); setOver(true); }}
      onDragLeave={() => setOver(false)}
      onDrop={(e) => { e.preventDefault(); setOver(false); if (e.dataTransfer.files.length) add(Array.from(e.dataTransfer.files)); }}
    >
      {over ? (
        <div className="scax-composer-box__drop">
          <span aria-hidden="true" className="scax-dropzone__cursor"><Icon name="document" size={20} /></span>
          <span className="scax-composer-box__drop-text">여기에 놓으면 첨부됩니다</span>
        </div>
      ) : null}
      <div className="scax-composer-box__tools" role="toolbar" aria-label="서식">
        {FORMAT_TOOLS.map((t) => (
          <button key={t.id} type="button" className={`scax-composer-box__tool scax-composer-box__tool--${t.id}`} aria-label={t.label} title={t.label}>
            {t.icon ? <Icon name={t.icon} size={16} /> : t.glyph}
          </button>
        ))}
      </div>
      <textarea
        className="scax-composer-box__input"
        rows={2}
        value={text}
        placeholder={placeholder}
        aria-label={placeholder}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } }}
      />
      {files.length && FileList ? (
        <div className="scax-composer-box__files">
          <FileList label="보낼 첨부" rows={fileRows(files, (key) => setFiles((l) => l.filter((f) => f.key !== key)))} />
        </div>
      ) : null}
      <div className="scax-composer-box__foot">
        <IconButton name="plus" size={18} label="파일 첨부" onClick={openPicker} />
        <span className="scax-composer-box__hint">Enter 보내기 · Shift+Enter 줄바꿈</span>
        <button type="button" className="scax-composer-box__send" aria-label="보내기" disabled={!canSend} onClick={send}>
          <Icon name="send" size={16} />
        </button>
      </div>
      {picker}
    </div>
  );
}

/* 내가 보낸 메시지 — 보내는 중 · 실패(다시 보내기) */
function SendState({ m, onResend }) {
  if (m.status === 'sending') return <span className="scax-msg-state">보내는 중…</span>;
  if (m.status === 'failed') {
    return (
      <span className="scax-msg-state scax-msg-state--failed">
        <Icon name="circle-exclamation" size={16} />보내지 못했습니다
        <button type="button" className="scax-msg-state__retry" onClick={() => onResend(m.id)}>다시 보내기</button>
      </span>
    );
  }
  return null;
}

/* 스레드 줄 — 부모 아래 「답글 N개 · 마지막 답글」. 누르면 오른쪽 스레드 패널이 열린다(진짜 슬랙처럼 3열) */
function ThreadLine({ thread, open, onOpen }) {
  const replies = thread.replies;
  return (
    <div className="scax-thread">
      <button type="button" className={`scax-thread__line${open ? ' scax-thread__line--open' : ''}`} aria-expanded={open} onClick={onOpen}>
        <span className="scax-thread__faces">
          {Array.from(new Set(replies.map((r) => r.user))).slice(0, 3).map((u) => <Avatar key={u} user={userOf(u)} size="xs" />)}
        </span>
        <span className="scax-thread__count">답글 {replies.length}개</span>
        <span className="scax-thread__last">마지막 답글 {thread.last}</span>
        <Icon name="chevron-right" size={16} />
      </button>
    </div>
  );
}

function Message({ m, grouped, onResend, onOpenThread, activeThread, inPanel }) {
  const user = userOf(m.user);
  return (
    <div className={`scax-msg${grouped ? ' scax-msg--grouped' : ''}${m.status ? ` scax-msg--${m.status}` : ''}${activeThread === m.id && !inPanel ? ' scax-msg--active' : ''}`}>
      <div className="scax-msg__gutter">
        {grouped ? <span className="scax-msg__at-side">{m.at}</span> : <Avatar user={user} />}
      </div>
      <div className="scax-msg__main">
        {grouped ? null : (
          <div className="scax-msg__head">
            <span className="scax-msg__name">{user.name}</span>
            {user.bot ? <span className="scax-msg__app">앱</span> : null}
            <span className="scax-msg__at">{m.at}</span>
          </div>
        )}
        {m.body.length ? <div className="scax-msg__body"><Blocks body={m.body} /></div> : null}
        <MessageExtras m={m} />
        {m.status ? <SendState m={m} onResend={onResend} /> : null}
        {m.thread && !inPanel ? <ThreadLine thread={m.thread} open={activeThread === m.id} onOpen={() => onOpenThread(m.id)} /> : null}
      </div>
    </div>
  );
}

const toMin = (at) => { const [h, mm] = at.split(':').map(Number); return h * 60 + mm; };

/* 같은 날 · 같은 사람 · 5분 안이면 묶는다 (아바타·이름 없이 왼쪽에 시각만). 보내는 중·실패 줄은 묶지 않는다 */
function isGrouped(prev, m) {
  return !!prev && !prev.status && !m.status && prev.day === m.day && prev.user === m.user && toMin(m.at) - toMin(prev.at) <= 5;
}

/* 보낸 것 → 내 이름의 메시지 한 줄 (사용자 토큰으로 보내므로 슬랙에서도 내 이름이다) */
let sendSeq = 0;
function myMessage(text, files, status) {
  sendSeq += 1;
  const m = { id: `mine-${sendSeq}`, user: ME, day: 'd3', at: '09:52', status, body: text ? [{ p: [text] }] : [] };
  if (files.length) m.files = files.map((f) => ({ name: f.name, type: extOf(f.name), size: fmtSize(f.bytes) }));
  return m;
}

/* 시안 전용 — 답장 상태를 대화에 미리 깔아 둔다 */
const THREAD_PARENT = 'r1-3';
function seedRoom(item, demo) {
  const msgs = item.messages.map((m) => (m.thread ? Object.assign({}, m, { thread: Object.assign({}, m.thread) }) : m));
  if (item.source === 'kakao') return msgs; /* 카톡은 조회 전용 — 답장 상태를 깔지 않는다 */
  if (demo === 'sending') msgs.push(myMessage('3장 수정본 올립니다', stage([{ name: '교육자료_심화편_3장_수정.md', size: 21 * 1024 }]), 'sending'));
  if (demo === 'failed') msgs.push(myMessage('3장 수정본 올립니다', [], 'failed'));
  if (demo === 'thread-sending' || demo === 'thread-failed') {
    const r = myMessage('중복 3건 목록 첨부합니다', demo === 'thread-sending' ? stage([{ name: '중복계정_3건.xlsx', size: 12 * 1024 }]) : [], demo === 'thread-sending' ? 'sending' : 'failed');
    return msgs.map((m) => (m.id === THREAD_PARENT ? Object.assign({}, m, { thread: Object.assign({}, m.thread, { replies: m.thread.replies.concat([r]) }) }) : m));
  }
  return msgs;
}
const THREAD_DEMOS = ['thread', 'thread-draft', 'thread-sending', 'thread-failed'];

/* 스레드 패널 — 머리 「스레드 · #채널명」 + 닫기 → 부모 → 답글 → 패널 아래 입력창 */
function ThreadPanel({ item, parent, onClose, onReply, onResend, demo }) {
  const replies = parent.thread.replies;
  return (
    <aside className="scax-thread-panel" aria-label={`스레드 · ${item.title}`}>
      <header className="scax-thread-panel__head">
        <h3 className="scax-thread-panel__title">스레드 <span className="scax-thread-panel__room">· {item.title}</span></h3>
        <IconButton name="close" size={20} label="스레드 닫기" onClick={onClose} />
      </header>
      <div className="scax-thread-panel__log">
        <Message m={parent} inPanel onResend={onResend} />
        <div className="scax-thread-panel__count"><span>답글 {replies.length}개</span></div>
        {replies.map((r, i) => <Message key={r.id} m={r} inPanel grouped={isGrouped(replies[i - 1], r)} onResend={onResend} />)}
      </div>
      <div className="scax-thread-panel__compose">
        <SlackComposer key={`${parent.id}-${demo}`} placeholder="답글 달기…" onSend={onReply} demo={demo === 'thread-draft' ? 'draft' : null} />
      </div>
    </aside>
  );
}

function RoomView({ item, demo }) {
  const [msgs, setMsgs] = React.useState(() => seedRoom(item, demo));
  const [threadId, setThreadId] = React.useState(THREAD_DEMOS.includes(demo) && item.messages.some((m) => m.id === THREAD_PARENT) ? THREAD_PARENT : null);
  const timers = React.useRef([]);
  React.useEffect(() => () => timers.current.forEach(clearTimeout), []);

  /* 보내기 → 「보내는 중」 → 잠시 뒤 보냄 (시안에선 늘 성공. 실패는 DevSwitch 로 본다) */
  const settle = (id, patch) => timers.current.push(setTimeout(() => patch(id), 1200));
  const patchAny = (id, patch) => setMsgs((l) => l.map((m) => {
    if (m.id === id) return Object.assign({}, m, patch);
    if (m.thread) return Object.assign({}, m, { thread: Object.assign({}, m.thread, { replies: m.thread.replies.map((r) => (r.id === id ? Object.assign({}, r, patch) : r)) }) });
    return m;
  }));
  const markSent = (id) => patchAny(id, { status: null });
  const send = (text, files) => {
    const m = myMessage(text, files, 'sending');
    setMsgs((l) => l.concat([m]));
    settle(m.id, markSent);
  };
  const reply = (text, files) => {
    const r = myMessage(text, files, 'sending');
    setMsgs((l) => l.map((m) => (m.id === threadId ? Object.assign({}, m, { thread: Object.assign({}, m.thread, { replies: m.thread.replies.concat([r]), last: '오늘 오전 9:52' }) }) : m)));
    settle(r.id, markSent);
  };
  const resend = (id) => { patchAny(id, { status: 'sending' }); settle(id, markSent); };

  const dayLabel = Object.fromEntries(item.days.map((d) => [d.key, d.label]));
  const rows = [];
  msgs.forEach((m, i) => {
    const prev = msgs[i - 1];
    if (!prev || prev.day !== m.day) rows.push(<div className="scax-day-divider" key={`d-${m.day}`}><span className="scax-day-divider__pill">{dayLabel[m.day]}</span></div>);
    rows.push(<Message key={m.id} m={m} grouped={isGrouped(prev, m)} onResend={resend} onOpenThread={setThreadId} activeThread={threadId} />);
  });
  const parent = msgs.find((m) => m.id === threadId) || null;
  const kakao = item.source === 'kakao';
  const kind = kakao ? (item.roomType === 'direct' ? '1:1' : '단체방') : item.roomType === 'channel' ? '채널' : item.roomType === 'dm' ? 'DM' : '그룹 DM';
  const placeholder = item.roomType === 'channel' ? `${item.title}에 메시지 보내기` : `${item.title}에게 메시지 보내기`;
  return (
    <div className={`scax-inbox-main scax-inbox-main--room${parent ? ' scax-inbox-main--thread' : ''}`}>
      <div className="scax-room-col">
        <header className="scax-room-head">
          <div className="scax-room-head__lead">
            <h2 className="scax-room-head__title">{item.title}</h2>
            <div className="scax-room-head__meta">
              <span>{kakao ? '카카오톡' : '슬랙'} · {kind}</span>
              <span className="scax-inbox-card__meta-sep" />
              <span>참여 {item.members}명</span>
              {kakao ? <React.Fragment><span className="scax-inbox-card__meta-sep" /><span>조회 전용 · Mac 앱에서 수집</span></React.Fragment> : null}
            </div>
          </div>
          {kakao ? null : (
            <a className="scax-room-head__open" href={item.openUrl} target="_blank" rel="noreferrer">
              <Icon name="link" size={16} />슬랙에서 열기
            </a>
          )}
        </header>
        <div className="scax-room-log">
          <div className="scax-room-log__inner">{rows}</div>
          {item.newCount ? (
            <div className="scax-room-log__new" role="status">
              <span className="scax-room-log__new-pill"><Icon name="arrow-down" size={16} />새 메시지 {item.newCount}개</span>
            </div>
          ) : null}
        </div>
        {/* 카톡은 조회 전용 — 입력창이 없다 */}
        {kakao ? null : (
          <div className="scax-room-compose">
            <SlackComposer placeholder={placeholder} onSend={send} demo={demo === 'draft' || demo === 'drag' ? demo : null} />
          </div>
        )}
      </div>
      {parent ? <ThreadPanel item={item} parent={parent} onClose={() => setThreadId(null)} onReply={reply} onResend={resend} demo={demo} /> : null}
    </div>
  );
}

/* ===== 메일 ===== */

const people = (list) => list.map((p) => `${p.name} <${p.addr}>`).join(', ');
const MY_ADDR = 'haram@company.example';

/* 받는 사람 · 참조 칩 — 빼고, 주소를 쳐서 더한다 */
function PeopleField({ label, list, onChange }) {
  const [draft, setDraft] = React.useState('');
  const add = () => {
    const v = draft.trim().replace(/,$/, '');
    if (!v) return;
    onChange(list.concat([{ name: v.split('@')[0], addr: v }]));
    setDraft('');
  };
  return (
    <div className="scax-reply__row">
      <span className="scax-reply__label">{label}</span>
      <div className="scax-reply__chips">
        {list.map((p) => (
          <span className="scax-reply__chip" key={p.addr} title={p.addr}>
            {p.name}<span className="scax-reply__chip-addr">{p.addr}</span>
            <button type="button" className="scax-reply__chip-x" aria-label={`${p.name} 빼기`} onClick={() => onChange(list.filter((x) => x.addr !== p.addr))}>
              <Icon name="close" size={14} />
            </button>
          </span>
        ))}
        <input
          className="scax-reply__chip-input"
          value={draft}
          placeholder={list.length ? '' : '주소 입력'}
          aria-label={`${label} 주소 더하기`}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ',') { e.preventDefault(); add(); } }}
          onBlur={add}
        />
      </div>
    </div>
  );
}

function recipients(item, mode) {
  if (mode === 'all') {
    return {
      to: [item.from].concat(item.to.filter((p) => p.addr !== MY_ADDR)),
      cc: item.cc.filter((p) => p.addr !== MY_ADDR),
    };
  }
  return { to: [item.from], cc: [] };
}

/* 답장 작성 칸 — 원문 아래에 펼친다(모달 아님). 보내는 중 · 실패는 이 칸 안에서, 보냄은 칸을 닫고 「보낸 답장」으로 */
function ReplyBox({ item, mode, phase, seed, onCancel, onSend, onRetry }) {
  const init = recipients(item, mode);
  const [to, setTo] = React.useState(init.to);
  const [cc, setCc] = React.useState(init.cc);
  const [body, setBody] = React.useState(seed ? seed.body : '');
  const [files, setFiles] = React.useState(seed ? seed.files : []);
  const [quoteOpen, setQuoteOpen] = React.useState(false);
  const busy = phase === 'sending';
  const tooBig = files.some((f) => f.bytes > MAIL_LIMIT);
  const canSend = to.length && (body.trim() || files.length) && !tooBig && !busy;
  return (
    <section className={`scax-reply${busy ? ' scax-reply--busy' : ''}`} aria-label={mode === 'all' ? '전체 답장 쓰기' : '답장 쓰기'}>
      <header className="scax-reply__head">
        <span className="scax-reply__kind">{mode === 'all' ? '전체 답장' : '답장'}</span>
        <span className="scax-reply__from">보내는 계정 {item.account}</span>
      </header>
      <PeopleField label="받는 사람" list={to} onChange={setTo} />
      <PeopleField label="참조" list={cc} onChange={setCc} />
      <div className="scax-reply__row">
        <span className="scax-reply__label">제목</span>
        <span className="scax-reply__subject">Re: {item.title}</span>
      </div>
      <textarea
        className="scax-reply__body"
        value={body}
        placeholder="답장 내용을 쓰세요"
        aria-label="답장 내용"
        disabled={busy}
        onChange={(e) => setBody(e.target.value)}
      />
      <div className="scax-reply__quote">
        <button type="button" className="scax-mail__quote-toggle" aria-expanded={quoteOpen} onClick={() => setQuoteOpen((v) => !v)}>
          {quoteOpen ? '이전 내용 접기' : '··· 이전 내용'}
        </button>
        {quoteOpen ? (
          <div className="scax-mail-html scax-mail-html--quoted">
            <p className="quote-head">{item.date}, {item.from.name} &lt;{item.from.addr}&gt; 작성:</p>
            <blockquote dangerouslySetInnerHTML={{ __html: item.html }} />
          </div>
        ) : null}
      </div>
      {DropZone ? (
        <DropZone
          drop="첨부할 파일을 끌어다 놓거나 추가하세요"
          pickLabel="파일 추가"
          hint="한 번에 25MB까지"
          disabled={busy}
          onFiles={(list) => setFiles((l) => l.concat(stage(list)))}
        >
          {files.length && FileList ? <FileList label="보낼 첨부" rows={fileRows(files, busy ? null : (key) => setFiles((l) => l.filter((f) => f.key !== key)), MAIL_LIMIT)} /> : null}
        </DropZone>
      ) : null}
      {phase === 'failed' ? (
        <StatusNote inline title="답장을 보내지 못했습니다" desc="연결이 끊겼거나 Gmail 이 받지 않았습니다. 쓴 내용은 그대로 남아 있습니다." action={<Button size="sm" variant="outlined" tone="neutral" label="다시 보내기" onClick={onRetry} />} />
      ) : null}
      <footer className="scax-reply__foot">
        <Button variant="outlined" tone="neutral" label="취소" disabled={busy} onClick={onCancel} />
        <Button variant="solid" tone="primary" iconBefore="send" label={busy ? '보내는 중…' : '보내기'} disabled={!canSend} onClick={() => onSend({ to, cc, body, files })} />
      </footer>
    </section>
  );
}

/* 보낸 답장 — 원문 아래 한 덩어리 */
function SentReply({ sent }) {
  return (
    <section className="scax-sent" aria-label="보낸 답장">
      <header className="scax-sent__head">
        <span className="scax-sent__badge"><Icon name="send" size={16} />보낸 답장</span>
        <span className="scax-sent__meta">받는 사람 {sent.to.map((p) => p.name).join(', ')}{sent.cc.length ? ` · 참조 ${sent.cc.map((p) => p.name).join(', ')}` : ''} · 방금</span>
      </header>
      {sent.body ? <p className="scax-sent__body">{sent.body}</p> : null}
      {sent.files.length ? <div className="scax-fcard-row">{sent.files.map((f) => <FileCard key={f.key} file={{ name: f.name, type: f.type, size: fmtSize(f.bytes) }} />)}</div> : null}
    </section>
  );
}

const MAIL_DEMO_SEED = { body: '지안님, 일정표 잘 받았습니다.\n3주차 변경 반영해서 내부 일정도 맞추겠습니다.', files: stage([{ name: '내부_일정_조정안.xlsx', size: 64 * 1024 }, { name: '현장_도면_원본.pdf', size: 31 * 1024 * 1024 }]) };

/* 작성 중 시안에만 25MB 를 넘는 파일을 하나 섞어 「못 붙은 이유」를 보인다 */
const demoSeed = (demo) => (demo === 'draft' ? MAIL_DEMO_SEED : { body: MAIL_DEMO_SEED.body, files: MAIL_DEMO_SEED.files.slice(0, 1) });

function MailView({ item, demo }) {
  const [quoteOpen, setQuoteOpen] = React.useState(false);
  /* 답장 칸: mode = 'reply' | 'all' | null, phase = 'draft' | 'sending' | 'failed' */
  const demoOn = ['draft', 'sending', 'failed'].includes(demo);
  const [compose, setCompose] = React.useState(demoOn ? { mode: 'all', phase: demo } : null);
  const [sent, setSent] = React.useState(demo === 'sent' ? [Object.assign({ to: [item.from], cc: [] }, MAIL_DEMO_SEED, { files: MAIL_DEMO_SEED.files.slice(0, 1) })] : []);
  const [draft, setDraft] = React.useState(null);
  const timer = React.useRef(null);
  React.useEffect(() => () => clearTimeout(timer.current), []);
  const open = (mode) => setCompose({ mode, phase: 'draft' });
  const send = (payload) => {
    setDraft(payload);
    setCompose((c) => Object.assign({}, c, { phase: 'sending' }));
    timer.current = setTimeout(() => { setSent((l) => l.concat([payload])); setCompose(null); setDraft(null); }, 1200);
  };
  const files = item.attachments.filter((a) => !a.image);
  const images = item.attachments.filter((a) => a.image);
  return (
    <div className="scax-inbox-main">
      <article className="scax-mail">
        <div className="scax-mail__top">
          <h2 className="scax-mail__title">{item.title}</h2>
          <div className="scax-mail__actions">
            <Button size="sm" variant="outlined" tone="neutral" label="답장" disabled={!!compose} onClick={() => open('reply')} />
            <Button size="sm" variant="outlined" tone="neutral" label="전체 답장" disabled={!!compose} onClick={() => open('all')} />
          </div>
        </div>
        <dl className="scax-mail__head">
          <dt>보낸 사람</dt><dd><strong>{item.from.name}</strong> <span className="scax-mail__addr">&lt;{item.from.addr}&gt;</span></dd>
          <dt>받는 사람</dt><dd>{people(item.to)}</dd>
          {item.cc.length ? <React.Fragment><dt>참조</dt><dd>{people(item.cc)}</dd></React.Fragment> : null}
          <dt>날짜</dt><dd>{item.date}</dd>
          <dt>받은 계정</dt><dd>{item.account}</dd>
        </dl>
        {/* 원문은 HTML 메일 그대로 담는다 — 표·목록·서명·인용의 모양을 지운 채 평문으로 바꾸지 않는다 */}
        <div className="scax-mail-html" dangerouslySetInnerHTML={{ __html: item.html }} />
        {item.quoted ? (
          <div className="scax-mail__quote">
            <button type="button" className="scax-mail__quote-toggle" aria-expanded={quoteOpen} onClick={() => setQuoteOpen((v) => !v)}>
              {quoteOpen ? '이전 내용 접기' : '··· 이전 내용 보기'}
            </button>
            {quoteOpen ? <div className="scax-mail-html scax-mail-html--quoted" dangerouslySetInnerHTML={{ __html: item.quoted }} /> : null}
          </div>
        ) : null}
        {item.attachments.length ? (
          <section className="scax-mail__files">
            <h3 className="scax-mail__files-title">첨부 {item.attachments.length}개</h3>
            {images.length ? (
              <div className="scax-mail__images">
                {images.map((img) => (
                  <figure className="scax-mail__image" key={img.name}>
                    <Thumb caption={img.caption} size="md" />
                    <figcaption className="scax-fcard">
                      <FileMark type={img.type} size="sm" />
                      <span className="scax-fcard__text">
                        <span className="scax-fcard__name">{img.name}</span>
                        <span className="scax-fcard__type">{img.size}</span>
                      </span>
                      <IconButton name="arrow-down" size={18} label={`${img.name} 받기`} />
                    </figcaption>
                  </figure>
                ))}
              </div>
            ) : null}
            {files.length ? <div className="scax-fcard-row">{files.map((f) => <FileCard key={f.name} file={f} />)}</div> : null}
          </section>
        ) : null}
        {sent.map((s, i) => <SentReply key={i} sent={s} />)}
        {compose ? (
          <ReplyBox
            key={`${compose.mode}-${demo}`}
            item={item}
            mode={compose.mode}
            phase={compose.phase}
            seed={draft || (demoOn ? demoSeed(demo) : null)}
            onCancel={() => setCompose(null)}
            onSend={send}
            onRetry={() => send(draft || Object.assign(recipients(item, compose.mode), demoSeed(demo)))}
          />
        ) : null}
      </article>
    </div>
  );
}

/* ===== 레일 카드 — 시안 그대로의 모양에서 행동만 걷어냈다 ===== */

function cardProps(item, selected, onSelect) {
  return {
    className: `scax-inbox-card scax-inbox-card--${item.unread ? 'unread' : 'read'}${selected ? ' scax-inbox-card--selected' : ''}`,
    role: 'button',
    tabIndex: 0,
    'aria-pressed': selected,
    onClick: () => onSelect(item.id),
    onKeyDown: (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onSelect(item.id); } },
  };
}

/* 메일 = 단건. 제목 · 본문 두 줄 · 보낸 사람 · 시각 */
function MailCard({ item, selected, onSelect }) {
  return (
    <article {...cardProps(item, selected, onSelect)}>
      <div className="scax-inbox-card__content">
        <div className="scax-inbox-card__top">
          <Badge tone="neutral">메일</Badge>
          {item.unread ? <span className="scax-inbox-card__dot" aria-label="안 읽음" /> : null}
        </div>
        <h3 className="scax-inbox-card__title">{item.title}</h3>
        <p className="scax-inbox-card__excerpt">{item.excerpt}</p>
        <div className="scax-inbox-card__meta">
          <span className="scax-inbox-card__meta-who">{item.from.name}</span>
          <span className="scax-inbox-card__meta-sep" />
          <span>{item.dateShort}</span>
          {item.attachments.length ? (
            <React.Fragment>
              <span className="scax-inbox-card__meta-sep" />
              <span className="scax-inbox-card__source"><Icon name="paperclip" size={16} />{item.attachments.length}</span>
            </React.Fragment>
          ) : null}
        </div>
      </div>
    </article>
  );
}

/* 슬랙 = 대화방 한 장. 마지막 3줄 미리보기 */
function RoomCard({ item, selected, onSelect }) {
  const shown = item.messages.slice(-3);
  const rest = item.unreadCount > shown.length ? item.unreadCount - shown.length : 0;
  const last = item.messages[item.messages.length - 1];
  const lastDay = (item.days.find((d) => d.key === last.day) || {}).label;
  return (
    <article {...cardProps(item, selected, onSelect)}>
      <div className="scax-inbox-card__content">
        <div className="scax-inbox-card__top">
          <Badge tone="neutral">{item.sourceLabel}</Badge>
          {item.unreadCount ? <Badge variant="count">{item.unreadCount}</Badge> : null}
        </div>
        <h3 className="scax-inbox-card__title">{item.title}</h3>
        <ul className="scax-room-preview">
          {shown.map((m) => (
            <li className="scax-room-preview__line" key={m.id}>
              <span className="scax-room-preview__who">{userOf(m.user).name}</span>
              <span className="scax-room-preview__text">{previewText(m)}</span>
              <span className="scax-room-preview__at">{m.at}</span>
            </li>
          ))}
          {rest ? <li className="scax-room-preview__more">그 밖에 {rest}건 더</li> : null}
        </ul>
        <div className="scax-inbox-card__meta">
          <span className="scax-inbox-card__meta-who">참여 {item.members}명</span>
          <span className="scax-inbox-card__meta-sep" />
          <span>마지막 {lastDay} {last.at}</span>
        </div>
      </div>
    </article>
  );
}

/* ===== 네 상태 ===== */

function RailBody({ state, shown, selected, onSelect, onRetry }) {
  if (state === 'loading') return <div className="scax-skeleton-stack">{[0, 1, 2, 3, 4].map((i) => <Skeleton key={i} variant="card" />)}</div>;
  if (state === 'error') return <StatusNote title="메시지함을 불러오지 못했습니다" desc="잠시 후 다시 시도해 주세요." action={<Button size="sm" variant="outlined" tone="neutral" label="다시 시도" onClick={onRetry} />} />;
  if (state === 'empty') return <Empty title="쌓인 메시지가 없습니다" desc="설정에서 메일·슬랙을 연결하면 받은 메시지가 여기에 쌓입니다." />;
  if (!shown.length) return <Empty icon="tune" title="이 출처에는 메시지가 없습니다" desc="다른 출처를 골라 보세요." />;
  return (
    <div className="scax-inbox-list">
      {shown.map((i) => (i.kind === 'mail'
        ? <MailCard key={i.id} item={i} selected={i.id === selected} onSelect={onSelect} />
        : <RoomCard key={i.id} item={i} selected={i.id === selected} onSelect={onSelect} />))}
    </div>
  );
}

function MainBody({ state, item, onRetry, demo }) {
  if (state === 'loading') {
    return (
      <div className="scax-inbox-main">
        <div className="scax-inbox-skel">
          <Skeleton variant="title" width="60" />
          {[0, 1, 2, 3, 4].map((i) => <Skeleton key={i} variant="text" width={i % 2 ? '80' : 'full'} />)}
        </div>
      </div>
    );
  }
  if (state === 'error') {
    return <div className="scax-inbox-main scax-inbox-main--empty"><StatusNote title="원문을 불러오지 못했습니다" desc="잠시 후 다시 시도해 주세요." action={<Button size="sm" variant="outlined" tone="neutral" label="다시 시도" onClick={onRetry} />} /></div>;
  }
  if (state === 'empty' || !item) {
    return <div className="scax-inbox-main scax-inbox-main--empty"><Empty title="고른 메시지가 없습니다" desc="왼쪽 카드를 누르면 여기에 원문이 섭니다." /></div>;
  }
  return item.kind === 'mail' ? <MailView key={`${item.id}-${demo}`} item={item} demo={demo} /> : <RoomView key={`${item.id}-${demo}`} item={item} demo={demo} />;
}

/* 시안 전용 상태 토글 — 화면 네 상태 · 답장 상태. 제품 화면이 아니다 (DS .scax-state-switch 모양) */
const SCREEN_STATES = [
  { value: 'default', label: '기본' },
  { value: 'empty', label: '빈' },
  { value: 'loading', label: '로딩' },
  { value: 'error', label: '오류' },
];
const REPLY_STATES = [
  { value: 'none', label: '없음' },
  { value: 'draft', label: '작성 중' },
  { value: 'thread', label: '스레드 열림' },
  { value: 'thread-draft', label: '스레드 작성' },
  { value: 'thread-sending', label: '스레드 보내는 중' },
  { value: 'thread-failed', label: '스레드 실패' },
  { value: 'drag', label: '끌어오기' },
  { value: 'sending', label: '보내는 중' },
  { value: 'sent', label: '보냈음' },
  { value: 'failed', label: '실패' },
];

function DevSwitch({ groups }) {
  return (
    <div className="scax-state-switch scax-inbox-dev">
      {groups.map((g) => (
        <React.Fragment key={g.label}>
          <span className="scax-state-switch__label">{g.label}</span>
          {g.options.map((o) => (
            <button key={o.value} type="button" className={`scax-state-switch__btn${o.value === g.value ? ' scax-state-switch__btn--on' : ''}`} onClick={() => g.onChange(o.value)}>
              {o.label}
            </button>
          ))}
        </React.Fragment>
      ))}
    </div>
  );
}

function InboxPage() {
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [screenState, setScreenState] = React.useState('default');
  const [source, setSource] = React.useState('all');
  const [items, setItems] = React.useState(() => INBOX_ITEMS.map((x) => (x.id === 'r1' ? Object.assign({}, x, { unread: false, unreadCount: 0 }) : x)));
  const [selected, setSelected] = React.useState('r1');
  const [replyDemo, setReplyDemo] = React.useState('none');

  /* 카드를 열면 읽음 */
  const open = (id) => {
    setSelected(id);
    setItems((l) => l.map((x) => (x.id === id ? Object.assign({}, x, { unread: false, unreadCount: 0 }) : x)));
  };
  const readAll = () => setItems((l) => l.map((x) => Object.assign({}, x, { unread: false, unreadCount: 0 })));
  const retry = () => setScreenState('default');

  const shown = items.filter((i) => source === 'all' || i.source === source);
  const current = items.find((i) => i.id === selected) || null;
  const unread = items.filter((i) => i.unread).length;

  return (
    <React.Fragment>
      <AppShell nav={<SideNav user={{ name: '유하람님', role: '기획자', avatar: './assets/avatar-person.png' }} activeId="inbox" collapsed={navCollapsed} onCollapse={() => setNavCollapsed((v) => !v)} />}>
        <AppHeader title="메시지함" actions={screenState === 'default' ? <Button size="sm" label="모두 읽음으로" onClick={readAll} /> : null} />
        <AppBody
          railLeft={(
            <GutterList
              title="메시지함"
              count={screenState === 'default' ? unread : undefined}
              headerEnd={<SegmentedControl value={source} options={SOURCE_TABS} onChange={setSource} ariaLabel="출처" />}
            >
              <RailBody state={screenState} shown={shown} selected={selected} onSelect={open} onRetry={retry} />
            </GutterList>
          )}
        >
          <MainBody state={screenState} item={current} onRetry={retry} demo={replyDemo} />
        </AppBody>
      </AppShell>
      <DevSwitch groups={[
        { label: '화면', value: screenState, options: SCREEN_STATES, onChange: setScreenState },
        { label: '답장', value: replyDemo, options: REPLY_STATES, onChange: setReplyDemo },
      ]} />
    </React.Fragment>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<InboxPage />);
