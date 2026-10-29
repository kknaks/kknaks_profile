/**
 * KPIC API Tests
 *
 * 외부 약학정보원 API 를 실제로 호출하지 않도록 global.fetch 를 mock 처리한다.
 * 이렇게 하면 네트워크/외부 API 상태와 무관하게 결정적으로 동작을 검증할 수 있다.
 */

import { describe, it, expect, jest, beforeEach } from '@jest/globals';
import {
  search_drugs_by_name,
  search_drugs_by_ingredient,
  get_drug_detail_by_id,
} from '../kpic-api.js';
import { KPICApiError } from '../types.js';

// 새 검색 API(/api/searchDrug) 항목 픽스처 (테스트가 확인하는 필드만 포함)
const SEARCH_ITEM = {
  rnum: '1',
  drug_code: '2013062800004',
  drug_name: '가스딘2mg',
  drug_enm: 'Gasdin Tab. 2mg',
  sunb_count: 1,
  list_sunb_name: 'Irsogladine Maleate 2mg',
  upso_name_kfda: '영진약품',
  drug_class: '전문',
  cls_name: '소화성궤양용제',
  kfda_code: '201300000',
  boh_code: '642403700',
  boh_price: '141원/1정',
};

function searchPage(items: unknown[], page = 1, totalPages = items.length ? 1 : 0) {
  return { items, total: items.length, page, limit: 100, totalPages };
}

// 성분 검색 API(/api/ingredient) 픽스처
const INGREDIENT_EXACT = {
  items: [
    {
      ingd_code: 'I005045',
      ingd_name: '이소트레티노인',
      ingd_ename: 'Isotretinoin',
      drug_count: 1,
    },
  ],
  total: 1,
  page: 1,
  limit: 5,
  totalPages: 1,
};
const INGREDIENT_PARTIAL = {
  items: [
    {
      ingd_code: 'I007305',
      ingd_name: '데옥시콜산',
      ingd_ename: 'Deoxycholic acid',
      drug_count: 1,
    },
    {
      ingd_code: 'I005733',
      ingd_name: '우르소데옥시콜산',
      ingd_ename: 'Ursodeoxycholic Acid',
      drug_count: 1,
    },
  ],
  total: 2,
  page: 1,
  limit: 5,
  totalPages: 1,
};
const EMPTY_INGREDIENT = { items: [], total: 0, page: 1, limit: 5, totalPages: 0 };

// 상세 정보 픽스처 (테스트가 확인하는 필드만 포함)
const DETAIL_FIXTURE = [
  {
    idx: 73363,
    drug_code: '2013062800004',
    drug_name: '가스딘2mg',
    drug_enm: 'Gasdin Tab. 2mg',
    effect: '위염, 위궤양',
    dosage: '1일 2회 경구투여한다.',
    caution: '이 약에 과민반응이 있는 환자',
    additives: '유당수화물',
    stmt: '실온보관',
  },
];

/**
 * 목 Response 헬퍼: JSON 본문
 */
function makeJsonResponse(
  data: unknown,
  init: { ok?: boolean; status?: number; statusText?: string } = {},
): Response {
  return {
    ok: init.ok ?? true,
    status: init.status ?? 200,
    statusText: init.statusText ?? 'OK',
    text: () => Promise.resolve(typeof data === 'string' ? data : JSON.stringify(data)),
    headers: { getSetCookie: () => [] },
  } as unknown as Response;
}

const mockFetch = jest.fn<(url: string, init?: RequestInit) => Promise<Response>>();

/**
 * URL 패턴에 따라 목 응답을 라우팅한다. 각 엔드포인트는 개별적으로 override 가능.
 */
function installFetch(
  overrides: {
    search?: (url: string) => Promise<Response>;
    ingredient?: (url: string) => Promise<Response>;
    detail?: () => Promise<Response>;
  } = {},
): void {
  mockFetch.mockImplementation((url: string) => {
    if (url.includes('/api/searchDrug')) {
      return (
        overrides.search ?? (() => Promise.resolve(makeJsonResponse(searchPage([SEARCH_ITEM]))))
      )(url);
    }
    if (url.includes('/api/ingredient')) {
      return (overrides.ingredient ?? (() => Promise.resolve(makeJsonResponse(INGREDIENT_EXACT))))(
        url,
      );
    }
    if (url.includes('ajax_result_drug2.asp')) {
      return (overrides.detail ?? (() => Promise.resolve(makeJsonResponse(DETAIL_FIXTURE))))();
    }
    return Promise.reject(new Error(`Unexpected URL: ${url}`));
  });
}

beforeEach(() => {
  mockFetch.mockReset();
  global.fetch = mockFetch as unknown as typeof fetch;
  installFetch();
});

describe('KPIC API Functions', () => {
  describe('search_drugs_by_name', () => {
    it('should return drug search results for valid drug name (Korean)', async () => {
      const result = await search_drugs_by_name('가스딘');

      const parsed = JSON.parse(result);
      expect(Array.isArray(parsed)).toBe(true);
      expect(parsed.length).toBeGreaterThan(0);

      const firstDrug = parsed[0];
      expect(firstDrug).toHaveProperty('drug_name', '가스딘2mg');
      expect(firstDrug).toHaveProperty('drug_code', '2013062800004');
      expect(firstDrug).toHaveProperty('drug_enm');
      expect(firstDrug).toHaveProperty('upso_name_kfda', '영진약품');
      expect(firstDrug).toHaveProperty('list_sunb_name', 'Irsogladine Maleate 2mg');
      // 기존 필드 유지 — 새 API 에 없는 것은 빈 값
      expect(firstDrug).toHaveProperty('effect', '');
      expect(firstDrug).toHaveProperty('dosage', '');
      // 분류명은 기존 cls_code 자리와 새 cls_name 둘 다
      expect(firstDrug).toHaveProperty('cls_code', '소화성궤양용제');
      expect(firstDrug).toHaveProperty('cls_name', '소화성궤양용제');
      expect(firstDrug).toHaveProperty('boh_code', '642403700');
    });

    it('should call the new search API with GET and drugName only', async () => {
      await search_drugs_by_name('  가스딘 ');

      expect(mockFetch).toHaveBeenCalledTimes(1);
      const [url, init] = mockFetch.mock.calls[0];
      expect(url.startsWith('https://health.kr/api/searchDrug?')).toBe(true);
      expect(new URL(url).searchParams.get('drugName')).toBe('가스딘');
      expect(init?.method).toBe('GET');
    });

    it('should follow pagination up to totalPages', async () => {
      installFetch({
        search: (url) => {
          const page = Number(new URL(url).searchParams.get('page'));
          return Promise.resolve(
            makeJsonResponse(searchPage([{ ...SEARCH_ITEM, rnum: String(page) }], page, 2)),
          );
        },
      });

      const parsed = JSON.parse(await search_drugs_by_name('가스딘'));
      expect(mockFetch).toHaveBeenCalledTimes(2);
      expect(parsed).toHaveLength(2);
      expect(parsed[0].total_cnt).toBe(2);
    });

    it('should throw error for empty drug name without making a request', async () => {
      await expect(search_drugs_by_name('')).rejects.toThrow(KPICApiError);
      await expect(search_drugs_by_name('   ')).rejects.toThrow(KPICApiError);
      expect(mockFetch).not.toHaveBeenCalled();
    });

    it('should return empty array for non-existent drug', async () => {
      installFetch({ search: () => Promise.resolve(makeJsonResponse(searchPage([]))) });

      const parsed = JSON.parse(await search_drugs_by_name('xyznonexistentdrug123456'));
      expect(Array.isArray(parsed)).toBe(true);
      expect(parsed).toHaveLength(0);
    });

    it('should throw KPICApiError on HTTP error (403)', async () => {
      installFetch({
        search: () =>
          Promise.resolve(
            makeJsonResponse('', { ok: false, status: 403, statusText: 'Forbidden' }),
          ),
      });

      await expect(search_drugs_by_name('가스딘')).rejects.toMatchObject({
        name: 'KPICApiError',
        statusCode: 403,
      });
    });

    it('should throw KPICApiError when the response has no items array', async () => {
      installFetch({ search: () => Promise.resolve(makeJsonResponse([])) });

      await expect(search_drugs_by_name('가스딘')).rejects.toThrow(KPICApiError);
    });

    it('should wrap network errors as KPICApiError', async () => {
      installFetch({ search: () => Promise.reject(new Error('connection refused')) });

      await expect(search_drugs_by_name('가스딘')).rejects.toThrow(/Network error/);
    });
  });

  describe('search_drugs_by_ingredient', () => {
    it('should use exact match first and list drugs by ingdcode', async () => {
      const parsed = JSON.parse(await search_drugs_by_ingredient('이소트레티노인'));

      expect(parsed).toHaveLength(1);
      expect(parsed[0]).toMatchObject({ ingd_code: 'I005045', match_type: 'exact' });
      expect(parsed[0].drugs[0]).toHaveProperty('drug_code', '2013062800004');

      const [ingUrl] = mockFetch.mock.calls[0];
      expect(new URL(ingUrl).searchParams.get('match')).toBe('1');
      const [drugUrl] = mockFetch.mock.calls[1];
      expect(new URL(drugUrl).searchParams.get('ingdcode')).toBe('I005045');
      expect(new URL(drugUrl).searchParams.has('drugName')).toBe(false);
    });

    it('should fall back to partial match when there is no exact match', async () => {
      installFetch({
        ingredient: (url) =>
          Promise.resolve(
            makeJsonResponse(
              new URL(url).searchParams.get('match') === '1'
                ? EMPTY_INGREDIENT
                : INGREDIENT_PARTIAL,
            ),
          ),
      });

      const parsed = JSON.parse(await search_drugs_by_ingredient('Deoxycholic'));
      expect(parsed.map((r: { ingd_code: string }) => r.ingd_code)).toEqual(['I007305', 'I005733']);
      expect(parsed[0].match_type).toBe('partial');
    });

    it('should return empty array when no ingredient matches', async () => {
      installFetch({ ingredient: () => Promise.resolve(makeJsonResponse(EMPTY_INGREDIENT)) });

      const parsed = JSON.parse(await search_drugs_by_ingredient('없는성분'));
      expect(parsed).toEqual([]);
      // 성분이 없으면 제품 검색을 부르지 않는다(필터 없는 전체 목록 방지)
      expect(mockFetch.mock.calls.some(([u]) => u.includes('/api/searchDrug'))).toBe(false);
    });

    it('should throw error for empty ingredient without making a request', async () => {
      await expect(search_drugs_by_ingredient(' ')).rejects.toThrow(KPICApiError);
      expect(mockFetch).not.toHaveBeenCalled();
    });
  });

  describe('get_drug_detail_by_id', () => {
    it('should return drug detail for valid drug code via GET', async () => {
      const result = await get_drug_detail_by_id('2013062800004');

      expect(result).toBeTruthy();

      const parsed = JSON.parse(result);
      expect(Array.isArray(parsed)).toBe(true);
      expect(parsed.length).toBeGreaterThan(0);

      const detail = parsed[0];
      expect(detail).toHaveProperty('drug_code', '2013062800004');
      expect(detail).toHaveProperty('drug_name');
      expect(detail).toHaveProperty('effect');
      expect(detail).toHaveProperty('dosage');
      expect(detail).toHaveProperty('caution');
      expect(detail).toHaveProperty('additives');
      expect(detail).toHaveProperty('stmt');

      // 상세 조회는 CSRF 없이 단일 GET 요청
      expect(mockFetch).toHaveBeenCalledTimes(1);
      const [, init] = mockFetch.mock.calls[0];
      expect(init?.method).toBe('GET');
    });

    it('should throw error for empty drug code without making a request', async () => {
      await expect(get_drug_detail_by_id('')).rejects.toThrow(KPICApiError);
      await expect(get_drug_detail_by_id('   ')).rejects.toThrow(KPICApiError);
      expect(mockFetch).not.toHaveBeenCalled();
    });

    it('should throw error for invalid drug code (empty result)', async () => {
      installFetch({ detail: () => Promise.resolve(makeJsonResponse([])) });

      await expect(get_drug_detail_by_id('invalid_code_12345')).rejects.toThrow(KPICApiError);
    });

    it('should throw KPICApiError on HTTP error (404)', async () => {
      installFetch({
        detail: () =>
          Promise.resolve(
            makeJsonResponse('', { ok: false, status: 404, statusText: 'Not Found' }),
          ),
      });

      await expect(get_drug_detail_by_id('2013062800004')).rejects.toMatchObject({
        name: 'KPICApiError',
        statusCode: 404,
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle KPICApiError correctly', () => {
      const error = new KPICApiError('Test error', 404, 'Not found');

      expect(error).toBeInstanceOf(Error);
      expect(error).toBeInstanceOf(KPICApiError);
      expect(error.message).toBe('Test error');
      expect(error.statusCode).toBe(404);
      expect(error.response).toBe('Not found');
      expect(error.name).toBe('KPICApiError');
    });
  });

  describe('Integration Test', () => {
    it('should perform complete workflow: search -> get detail', async () => {
      // 1. 약품 검색
      const searchResult = await search_drugs_by_name('가스딘');
      const searchParsed = JSON.parse(searchResult);

      expect(searchParsed.length).toBeGreaterThan(0);

      // 2. 첫 번째 결과의 상세 정보 조회
      const firstDrug = searchParsed[0];
      const detailResult = await get_drug_detail_by_id(firstDrug.drug_code);
      const detailParsed = JSON.parse(detailResult);

      expect(detailParsed.length).toBeGreaterThan(0);

      // 3. 상세 정보가 검색 결과와 일치하는지 확인
      const detail = detailParsed[0];
      expect(detail.drug_code).toBe(firstDrug.drug_code);
      expect(detail.drug_name).toBe(firstDrug.drug_name);
    });
  });
});
