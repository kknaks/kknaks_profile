// 차트 본문 — LLM 없이 템플릿으로 만든다(SPEC §3-3). 가격 블록은 차티 형식 그대로(stg features/chart/utils/build-pricing-summary.ts:9-40).
import { buildCategoryPath, calcTotals, itemPrice } from '@/domain/pricing';
import { CONSULT_TYPE_LABEL, type SessionState } from '@/domain/session';
import { formatScore, GRADE_META } from '@/domain/grade';
import type { SkinReport } from '@/domain/skin-report';

const won = (n: number) => `${n.toLocaleString()}원`;

export function buildPricingSummary(session: Pick<SessionState, 'cart' | 'discountRate'>): string {
  const checked = session.cart.filter((i) => i.checked !== false);
  if (checked.length === 0) return '';
  const { total, totalVat, final } = calcTotals(session.cart, session.discountRate);
  let text = '■ 시술 가격 안내\n';
  text += '══════════════════════════════════════════\n';
  checked.forEach((item, i) => {
    const tag = item.free ? '[무료]' : `[${item.priceType || '정규가'}]`;
    const discountTag = !item.free && item.discount > 0 ? ` (${item.discount}% 할인)` : '';
    const path = buildCategoryPath({ category: item.category, sub_category: item.subCategory }, 2);
    text += `  ${i + 1}. ${tag}${discountTag} ${path} | ${item.name}\n`;
    text += `     ${item.free ? '무료 (서비스)' : won(itemPrice(item))}\n`;
  });
  text += '  ──────────────────────────────────────\n';
  text += `  합계 (VAT 별도): ${won(total)}\n`;
  text += `  합계 (VAT 포함): ${won(totalVat)}\n`;
  if (session.discountRate > 0) {
    text += session.discountRate === 100 ? '  협찬 (100% 할인): 0원\n' : `  추가 ${session.discountRate}% 할인: ${won(final)}\n`;
  }
  return text;
}

export function buildAnalysisSummary(report: SkinReport | null): string {
  if (!report) return '';
  let text = '■ 피부 분석 요약\n';
  text += `  측정일: ${report.measuredAt.replace(/-/g, '.')}\n`;
  text += `  대분류: ${report.categories.map((c) => `${c.label} ${formatScore(c.score)}(${GRADE_META[c.grade].label})`).join(' · ')}\n`;
  const low = report.items.filter((i) => i.score != null).sort((a, b) => (a.score as number) - (b.score as number)).slice(0, 3);
  text += `  낮은 항목: ${low.map((i) => `${i.label} ${formatScore(i.score)}`).join(' · ')}\n`;
  if (report.tone) text += `  피부톤: ${report.tone.name}(${report.tone.code})\n`;
  return text;
}

export function buildChartText(report: SkinReport | null, session: SessionState, includeMemo: boolean): string {
  const parts = [`[${CONSULT_TYPE_LABEL[session.consultType]} 상담]`, buildAnalysisSummary(report), buildPricingSummary(session)].filter(Boolean);
  if (includeMemo) parts.push('■ 내부 메모\n  통증에 민감함 · 예산 200만 원 안쪽 희망 (목 메모)\n');
  return parts.join('\n');
}
