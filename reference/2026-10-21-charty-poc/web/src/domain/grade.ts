import type { BadgeVariant } from '@medisolve-ai/medikit';
import type { Grade } from './skin-report';

// 원본 리포트 안내문 「85 이상 건강 · 70–85 경도 · 60–70 중등도 · 60 이하 중도」를 점수로 적용(SPEC §2-1).
export function gradeOf(score: number | null | undefined): Grade {
  if (score == null || score < 0) return 'none';
  if (score >= 85) return 'good';
  if (score >= 70) return 'mild';
  if (score >= 60) return 'moderate';
  return 'severe';
}

export interface GradeMeta {
  label: string;
  /** 원본 이름(태블릿 보조 표기용) */
  original: string;
  /** 차트 채움 색 */
  color: string;
  badge: { variant: BadgeVariant; className?: string };
}

export const GRADE_META: Record<Grade, GradeMeta> = {
  good: { label: '좋아요', original: '건강', color: 'var(--ms-primary)', badge: { variant: 'primary', className: 'bg-primary text-ms-white' } },
  mild: { label: '조금 신경 써요', original: '경도', color: 'var(--ms-primary-500)', badge: { variant: 'primary' } },
  moderate: { label: '관리 시작', original: '중등도', color: 'var(--ms-yellow)', badge: { variant: 'warning' } },
  severe: { label: '집중 관리', original: '중도', color: 'var(--ms-red)', badge: { variant: 'danger' } },
  none: { label: '점수 없음', original: '무', color: 'var(--ms-gray-400)', badge: { variant: 'neutral' } },
};

/** 레이더·막대의 등급 띠 눈금 */
export const GRADE_TICKS = [60, 70, 85] as const;

export function formatScore(score: number | null): string {
  if (score == null) return '–';
  return Number.isInteger(score) ? String(score) : score.toFixed(1);
}
