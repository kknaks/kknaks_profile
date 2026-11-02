import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { fromM3d } from '@/data/adapters/m3d';
import pricing from '@/data/mock/pricing.json';
import { summaryLine } from '@/content/copy';
import type { Procedure } from '@/domain/pricing';
import { recommend } from './recommend-rules';

const P = pricing.procedures as Procedure[];
const REAL = path.resolve(__dirname, '../../public/m3d/report');

describe.skipIf(!existsSync(path.join(REAL, 'measure.json')))('추천 규칙 — 실제 측정값(SPEC §3-5)', () => {
  const report = fromM3d(
    JSON.parse(readFileSync(path.join(REAL, 'measure.json'), 'utf8')),
    JSON.parse(readFileSync(path.join(REAL, 'render.json'), 'utf8')),
    { customer: { name: '이건학' } },
  );
  const rec = recommend(report, P);
  const names = rec.procedureIds.map((id) => P.find((p) => p.id === id)!.name);

  it('추천 칩 6개', () => {
    expect(rec.chips.map((c) => c.label).sort()).toEqual(['기기 리프팅', '레이저', '메디컬스킨케어', '보톡스', '스킨부스터', '필러'].sort());
  });
  it('「추천」 보기 행이 규칙대로', () => {
    expect(names).toEqual(
      expect.arrayContaining(['눈가 보톡스', '미간 보톡스', '이마 보톡스', '보톡스 3부위 패키지', '보톡스 풀페이스', '울쎄라 하안면', '신스킨 1회', '고주파리프팅 전체', '코필러', '리쥬란 HB 1회', '스킨보톡스 전체', '제네시스 1회', '피코토닝 1회', '르브란 1회', '올레이저 1회', '엑셀V 1회', '수소피부관리 1회']),
    );
    for (const no of ['사각턱 보톡스', '턱선 보톡스', '실리프팅 PDO 10줄', '인모드 10회', '얼굴 전체 제모']) expect(names).not.toContain(no);
    expect(names.length).toBeGreaterThanOrEqual(18);
    expect(names.length).toBeLessThanOrEqual(26);
  });
  it('레이저 칩은 이유 3개를 묶는다', () => {
    expect(rec.chips.find((c) => c.modality === 'M8')!.reasons).toEqual(['칙칙함·색소', '넓어진 모공', '붉은기']);
  });
  it('한 줄 요약 = 가장 낮은 대분류 2개', () => {
    expect(summaryLine(report.categories)).toBe('피부톤과 노화부터 관리하면 좋아요');
  });
});
