// Procedure Hub 스냅샷 읽기(SPEC §4). 실행 중 네트워크 요청 없음 — 스냅샷만 정적 import 한다.
// 원문을 고쳐 쓰지 않는다. 섹션마다 item → modality 순으로 그 필드가 있는 가장 구체적인 노드를 쓴다(§4-3 상향 대체).
import snapshot from './hub-snapshot.json';

export type HubLevel = 'modality' | 'subcategory' | 'item';

type Str = string | undefined;

export interface HubExtracted {
  overview?: string;
  mechanism?: string;
  indications?: { primary?: string[]; extended?: string[] };
  contraindications?: { absolute?: string[]; relative?: string[] };
  safety?: { common?: string[]; uncommon?: string[]; serious?: string[]; long_term?: string[]; note?: string | string[] };
  onset_duration?: { onset?: Str; peak?: Str; peak_effect?: Str; duration?: Str; maintenance?: Str };
  aftercare?: string[];
  related_techniques?: string[];
}

export interface HubProfile {
  id: string;
  name: string;
  durationMin: number | null;
  durationMax: number | null;
  needsAnesthesia: string | null;
}

export interface HubNode {
  level: HubLevel;
  modalityId: string;
  path: string[];
  extracted: HubExtracted | null;
}

export interface HubModality {
  category: string;
  extracted: HubExtracted | null;
  profile: HubProfile;
}

export interface HubSnapshot {
  meta: {
    source: string;
    endpoints: string[];
    fetchedAt: string;
    versions: { taxonomy: string | null; procedureProfiles: string };
    sha256: { taxonomy: string; procedureProfiles: string };
  };
  modalities: Record<string, HubModality>;
  nodes: Record<string, HubNode>;
  problems: Record<string, { label: string; items: string[] }>;
}

export const HUB = snapshot as unknown as HubSnapshot;

export function hubNode(id: string): HubNode | null {
  return HUB.nodes[id] ?? null;
}

export type SectionKey = 'overview' | 'mechanism' | 'indications' | 'onset' | 'procedure' | 'safety' | 'contraindications' | 'aftercare';

export type SectionBody =
  | { kind: 'text'; text: string }
  | { kind: 'list'; items: string[]; ordered?: boolean }
  | { kind: 'pairs'; pairs: { label: string; text: string }[] }
  | { kind: 'groups'; groups: { label: string; items: string[] }[] };

export interface ModalSection {
  key: SectionKey;
  title: string;
  /** 이 섹션 값을 가져온 노드 id */
  sourceId: string;
  /** 상위(modality)에서 가져왔으면 「레이저 전체 기준」, 아니면 null */
  inheritedLabel: string | null;
  body: SectionBody;
}

export const SECTION_TITLE: Record<SectionKey, string> = {
  overview: '',
  mechanism: '어떻게 작용하나요',
  indications: '이런 고민에',
  onset: '효과는 언제부터 · 얼마나',
  procedure: '시술 시간 · 마취',
  safety: '알아 둘 반응',
  contraindications: '받으면 안 되는 경우',
  aftercare: '시술 후 관리',
};

/** §4-2 표 — 여기 없는 하위 키가 스냅샷에 생기면 hub-snapshot.test.ts 가 실패한다 */
export const ONSET_KEYS: [keyof NonNullable<HubExtracted['onset_duration']>, string][] = [
  ['onset', '시작'],
  ['peak', '최대'],
  ['peak_effect', '최대'],
  ['duration', '지속'],
  ['maintenance', '유지'],
];
export const SAFETY_KEYS: [keyof NonNullable<HubExtracted['safety']>, string][] = [
  ['common', '흔한 반응'],
  ['uncommon', '가끔'],
  ['serious', '드문 부작용'],
  ['long_term', '반복 시 주의'],
  ['note', '참고'],
];
const CONTRA_KEYS: [keyof NonNullable<HubExtracted['contraindications']>, string][] = [
  ['absolute', '받으면 안 돼요'],
  ['relative', '상담이 필요해요'],
];

export const ANESTHESIA_LABEL: Record<string, string> = {
  none: '마취 없음',
  topical: '바르는 마취',
  topical_or_none: '바르는 마취(필요할 때)',
  topical_or_block: '바르는 마취 또는 부분 마취',
  block: '부분 마취',
  block_or_sedation: '부분 마취 또는 수면',
};

const asList = (v: string | string[] | undefined): string[] => (v == null ? [] : Array.isArray(v) ? v : [v]);

function bodyOf(key: SectionKey, e: HubExtracted): SectionBody | null {
  switch (key) {
    case 'overview':
      return e.overview ? { kind: 'text', text: e.overview } : null;
    case 'mechanism':
      return e.mechanism ? { kind: 'text', text: e.mechanism } : null;
    case 'indications': {
      const items = (e.indications?.primary ?? []).slice(0, 6);
      return items.length ? { kind: 'list', items } : null;
    }
    case 'onset': {
      const o = e.onset_duration ?? {};
      const pairs = ONSET_KEYS.flatMap(([k, label]) => (o[k] ? [{ label, text: o[k] as string }] : []));
      return pairs.length ? { kind: 'pairs', pairs } : null;
    }
    case 'safety': {
      const s = e.safety ?? {};
      const groups = SAFETY_KEYS.flatMap(([k, label]) => {
        const items = asList(s[k]);
        return items.length ? [{ label, items }] : [];
      });
      return groups.length ? { kind: 'groups', groups } : null;
    }
    case 'contraindications': {
      const c = e.contraindications ?? {};
      const groups = CONTRA_KEYS.flatMap(([k, label]) => {
        const items = asList(c[k]);
        return items.length ? [{ label, items }] : [];
      });
      return groups.length ? { kind: 'groups', groups } : null;
    }
    case 'aftercare': {
      const items = e.aftercare ?? [];
      return items.length ? { kind: 'list', items, ordered: true } : null;
    }
    case 'procedure':
      return null;
  }
}

function procedureBody(p: HubProfile): SectionBody | null {
  const pairs: { label: string; text: string }[] = [];
  if (p.durationMin != null && p.durationMax != null) {
    pairs.push({ label: '시술 시간', text: p.durationMin === p.durationMax ? `${p.durationMin}분` : `${p.durationMin}–${p.durationMax}분` });
  }
  if (p.needsAnesthesia) pairs.push({ label: '마취', text: ANESTHESIA_LABEL[p.needsAnesthesia] ?? p.needsAnesthesia });
  return pairs.length ? { kind: 'pairs', pairs } : null;
}

const SECTION_ORDER: SectionKey[] = ['overview', 'mechanism', 'indications', 'onset', 'procedure', 'safety', 'contraindications', 'aftercare'];

/** 노드 하나의 모달 섹션 — 비어 있는 섹션은 뺀다 */
export function modalSections(id: string): ModalSection[] {
  const node = hubNode(id);
  if (!node) return [];
  const mod = HUB.modalities[node.modalityId];
  const inherited = `${mod.category} 전체 기준`;
  // 상향 대체 순서: item → (subcategory 는 extracted 가 없어 건너뜀) → modality
  const chain: { id: string; e: HubExtracted }[] = [];
  if (node.level !== 'modality' && node.extracted) chain.push({ id, e: node.extracted });
  if (mod.extracted) chain.push({ id: node.modalityId, e: mod.extracted });

  const out: ModalSection[] = [];
  for (const key of SECTION_ORDER) {
    if (key === 'procedure') {
      const body = procedureBody(mod.profile);
      if (body) out.push({ key, title: SECTION_TITLE[key], sourceId: node.modalityId, inheritedLabel: node.modalityId === id ? null : inherited, body });
      continue;
    }
    for (const src of chain) {
      const body = bodyOf(key, src.e);
      if (!body) continue;
      out.push({ key, title: SECTION_TITLE[key], sourceId: src.id, inheritedLabel: src.id === id ? null : inherited, body });
      break;
    }
  }
  return out;
}

/** 모달 머리 경로 「레이저 › 혈관 › 브이빔」 */
export function hubPath(id: string): string {
  return hubNode(id)?.path.join(' › ') ?? '';
}

/** 모달 바닥 출처 줄 */
export function hubSourceLine(): string {
  const day = new Date(HUB.meta.fetchedAt).toLocaleDateString('sv-SE', { timeZone: 'Asia/Seoul' }); // YYYY-MM-DD(한국 시각)
  return `출처: Procedure Hub(stg) · ${day} 받음 · 목업 · 의학적 근거 아님`;
}

/** 카드 안 간단 설명(U-1) — 모달 머리 요약과 같은 값(`extracted.overview`, item → modality 상향 대체) */
export function procedureSummary(id: string): { text: string; sourceId: string; inheritedLabel: string | null } | null {
  const s = modalSections(id).find((x) => x.key === 'overview');
  if (!s || s.body.kind !== 'text') return null;
  return { text: s.body.text, sourceId: s.sourceId, inheritedLabel: s.inheritedLabel };
}
