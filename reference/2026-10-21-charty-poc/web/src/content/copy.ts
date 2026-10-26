// 화면 문구 — 한 파일에 모은다(SPEC §2-3). 원본 analyze 설명문은 쓰지 않는다.
// 규칙: 진단·질환·치료·환자 말 금지 · 쉬운 이름 · 한 문장 30자 안팎 「~요」 · 겁주지 않는다.
import { withJosa } from '@medisolve-ai/medikit';
import type { CategoryKey, Grade, ItemKey, RegionKey, SkinCategory } from '@/domain/skin-report';

export const ITEM_COPY: Record<ItemKey, { label: string; meaning: string }> = {
  redness: { label: '붉은기', meaning: '피부 속 붉은 기운이 얼마나 퍼져 있는지예요' },
  porphyrin: { label: '피지 속 세균 흔적', meaning: '모공 속 피지에 생기는 세균 흔적의 양이에요' },
  pigment: { label: '색소', meaning: '기미·잡티처럼 갈색 색소가 얼마나 있는지예요' },
  brightness: { label: '밝기', meaning: '피부가 얼마나 맑고 환해 보이는지예요' },
  pore: { label: '모공', meaning: '넓어진 모공이 얼마나 있는지예요' },
  dermatoglyph: { label: '피부결', meaning: '피부 표면 골이 얼마나 고른지예요' },
  fineWrinkle: { label: '잔주름', meaning: '눈가·미간·이마의 가는 주름이에요' },
  deepWrinkle: { label: '굵은 주름', meaning: '팔자·눈물고랑처럼 깊게 팬 주름이에요' },
};

export const CATEGORY_COPY: Record<CategoryKey, { label: string; meaning: string }> = {
  inflammation: { label: '염증·민감', meaning: '붉은기와 피지 세균 흔적을 함께 봐요' },
  tone: { label: '피부톤', meaning: '색소와 밝기로 피부색이 고른지 봐요' },
  texture: { label: '피부결', meaning: '모공과 피부결 골로 매끄러움을 봐요' },
  aging: { label: '노화', meaning: '잔주름과 굵은 주름을 함께 봐요' },
};

export const REGION_LABEL: Record<RegionKey, string> = {
  TT: '이마',
  MJ: '미간',
  BG: '코뿌리',
  YD: '눈밑',
  YW: '눈가',
  LG: '눈물고랑',
  FL: '팔자',
  QJ: '광대고랑',
};

export const GRADE_PHRASE: Record<Grade, string> = {
  good: '좋은 상태예요',
  mild: '조금만 신경 쓰면 돼요',
  moderate: '지금부터 관리하면 좋아요',
  severe: '집중 관리가 필요해요',
  none: '점수는 나오지 않았어요',
};

/** 점수가 가장 낮은 대분류 2개 → 「{A}와 {B}부터 관리하면 좋아요」 */
export function summaryLine(categories: SkinCategory[]): string {
  const scored = categories.filter((c) => c.score != null).sort((a, b) => (a.score as number) - (b.score as number));
  if (scored.length === 0) return '';
  if (scored.length === 1) return `${withJosa(scored[0].label, '은/는')} 관리하면 좋아요`;
  return `${withJosa(scored[0].label, '와/과')} ${scored[1].label}부터 관리하면 좋아요`;
}

export function porphyrinScoreNote(count: number | null): string {
  return count == null ? GRADE_PHRASE.none : `${GRADE_PHRASE.none} · ${count.toLocaleString('ko-KR')}개 발견`;
}

export const COPY = {
  screenTitle: '피부 상담',
  tabletTitle: '피부 상담 · 상담사',
  linkOn: '상담사 화면 연결됨',
  linkWait: '상담사 화면 연결 대기',
  screenOn: '큰 화면 연결됨',
  screenOff: '큰 화면 없음',
  cartEmpty: '상담사가 시술을 고르면 여기에 보여요',
  priceHidden: '가격은 상담사가 안내해 드려요',
  assetsMissing: '3D 에셋이 없습니다 — npm run prepare:assets 를 먼저 실행하세요',
  reportMissing: '측정 데이터가 없습니다 — npm run prepare:assets 를 먼저 실행하세요',
  reportMissingShort: '측정 데이터 없음',
  faceLoading: '얼굴을 불러오는 중',
  sideNote: '원본 리포트의 좌우 표기와 다를 수 있어요',
  mockNote: '목업 · 의학적 근거 아님',
} as const;
