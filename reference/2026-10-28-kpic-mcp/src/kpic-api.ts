/**
 * KPIC (Korea Pharmaceutical Information Center) API Client
 */

import {
  DrugSearchResult,
  DrugDetailResult,
  IngredientItem,
  IngredientPage,
  IngredientSearchResult,
  KPICApiError,
  SearchDrugItem,
  SearchDrugPage,
} from './types.js';

/**
 * 약학정보원 API 호스트.
 *
 * `www.health.kr` 는 `health.kr` 로 301 리다이렉트되므로 non-www 호스트로 직접 호출한다.
 */
const BASE_URL = 'https://health.kr';

/** 새 검색 API 의 페이지당 최대 건수(서버가 100 으로 자른다) */
const PAGE_LIMIT = 100;

/** 한 번의 검색에서 가져올 최대 페이지 수 (= 최대 500건) */
const MAX_PAGES = 5;

/** 성분 검색에서 제품을 펼칠 최대 성분 수 */
const MAX_INGREDIENTS = 5;

const JSON_HEADERS = {
  accept: 'application/json',
  'accept-language': 'ko,en-US;q=0.9,en;q=0.8',
};

/**
 * health.kr 새 API 를 GET 으로 호출하고 JSON 을 파싱한다.
 *
 * @throws {KPICApiError} HTTP 오류, 파싱 실패, 네트워크 오류
 */
async function getJson<T>(path: string, params: Record<string, string>): Promise<T> {
  const url = `${BASE_URL}${path}?${new URLSearchParams(params).toString()}`;

  let response: Response;
  try {
    response = await fetch(url, { method: 'GET', headers: JSON_HEADERS });
  } catch (error) {
    throw new KPICApiError(
      `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`,
    );
  }

  if (!response.ok) {
    throw new KPICApiError(`API request failed: ${response.statusText}`, response.status);
  }

  const data = await response.text();
  try {
    return JSON.parse(data) as T;
  } catch (parseError) {
    throw new KPICApiError(
      `Failed to parse API response: ${parseError instanceof Error ? parseError.message : 'Unknown error'}`,
    );
  }
}

/**
 * `/api/searchDrug` 를 페이지 단위로 돌며 결과를 모은다.
 *
 * 서버는 모르는 파라미터를 무시하고 전체 목록을 돌려주므로, `filter` 는 반드시
 * `drugName` 또는 `ingdcode` 중 하나여야 한다.
 */
async function searchDrugPages(
  filter: { drugName: string } | { ingdcode: string },
): Promise<SearchDrugItem[]> {
  const items: SearchDrugItem[] = [];

  for (let page = 1; page <= MAX_PAGES; page++) {
    const result = await getJson<SearchDrugPage>('/api/searchDrug', {
      ...filter,
      page: String(page),
      limit: String(PAGE_LIMIT),
    });

    if (!result || !Array.isArray(result.items)) {
      throw new KPICApiError('Invalid response format: expected items array');
    }

    items.push(...result.items);
    if (page >= (result.totalPages ?? 1)) {
      break;
    }
  }

  return items;
}

/**
 * 새 API 항목을 기존 검색 결과 형태로 옮긴다.
 *
 * 새 API 에 없는 `effect`·`dosage`·`total_cnt` 는 빈 값으로 두고(상세 조회에 있음),
 * 기존 `cls_code` 자리에는 분류명(`cls_name`)을 넣는다.
 */
function toDrugSearchResult(item: SearchDrugItem): DrugSearchResult {
  return {
    pack_img: item.pack_img ?? '',
    drug_pic: item.drug_pic ?? '',
    drug_name: item.drug_name ?? '',
    drug_enm: item.drug_enm ?? '',
    drug_code: item.drug_code ?? '',
    sunb_count: item.sunb_count ?? 0,
    list_sunb_name: (item.list_sunb_name ?? '').trim(),
    ingr_mg: item.ingr_mg ?? '',
    dosage: '',
    effect: '',
    upso_name_kfda: item.upso_name_kfda ?? '',
    cls_code: item.cls_name ?? '',
    drug_form: item.drug_form ?? '',
    drug_class: item.drug_class ?? '',
    etc: item.etc ?? '',
    produce: item.produce ?? '',
    boh_price: item.boh_price ?? '',
    total_cnt: 0,
    kfda_code: item.kfda_code ?? '',
    confirm_flag: item.confirm_flag ?? '',
    cls_name: item.cls_name ?? '',
    dosage_route_name: item.dosage_route_name ?? '',
    boh_code: item.boh_code ?? '',
  };
}

/**
 * 약학정보원에서 의약품 이름으로 대략적인 정보들을 가져온다.
 * 이름이 유사한 의약품 여러개가 나올 수 있다.
 *
 * @param drugname 검색할 의약품의 이름 (영문 또는 한글)
 * @returns JSON 문자열 형태의 검색 결과
 * @throws {KPICApiError} API 요청 실패 시
 */
export async function search_drugs_by_name(drugname: string): Promise<string> {
  if (!drugname || drugname.trim().length === 0) {
    throw new KPICApiError('Drug name cannot be empty');
  }

  const items = await searchDrugPages({ drugName: drugname.trim() });
  const results = items.map(toDrugSearchResult);
  results.forEach((r) => (r.total_cnt = results.length));

  return JSON.stringify(results, null, 2);
}

/**
 * 약학정보원에서 성분명으로 그 성분을 가진 의약품 목록을 가져온다(성분 → 제품 역조회).
 *
 * 성분명이 정확히 일치하는 성분이 있으면 그것만, 없으면 부분 일치 성분들(최대
 * MAX_INGREDIENTS 개)의 제품을 성분별로 묶어 돌려준다.
 *
 * @param ingredient 성분명 (한글 또는 영문, 예: "데옥시콜산", "Isotretinoin")
 * @returns JSON 문자열 형태의 성분별 제품 목록
 * @throws {KPICApiError} API 요청 실패 시
 */
export async function search_drugs_by_ingredient(ingredient: string): Promise<string> {
  if (!ingredient || ingredient.trim().length === 0) {
    throw new KPICApiError('Ingredient name cannot be empty');
  }

  const keyword = ingredient.trim();
  const findIngredients = async (match: '0' | '1'): Promise<IngredientItem[]> => {
    const result = await getJson<IngredientPage>('/api/ingredient', {
      keyword,
      match,
      hasDrug: '1',
      page: '1',
      limit: String(MAX_INGREDIENTS),
    });
    if (!result || !Array.isArray(result.items)) {
      throw new KPICApiError('Invalid response format: expected items array');
    }
    return result.items;
  };

  let matchType: 'exact' | 'partial' = 'exact';
  let ingredients = await findIngredients('1');
  if (ingredients.length === 0) {
    matchType = 'partial';
    ingredients = await findIngredients('0');
  }

  const results: IngredientSearchResult[] = [];
  for (const ingd of ingredients.slice(0, MAX_INGREDIENTS)) {
    if (!ingd.ingd_code) {
      continue;
    }
    const drugs = (await searchDrugPages({ ingdcode: ingd.ingd_code })).map(toDrugSearchResult);
    results.push({
      ingd_code: ingd.ingd_code,
      ingd_name: ingd.ingd_name ?? '',
      ingd_ename: ingd.ingd_ename ?? '',
      match_type: matchType,
      drug_count: ingd.drug_count ?? drugs.length,
      drugs,
    });
  }

  return JSON.stringify(results, null, 2);
}

/**
 * 약학정보원의 의약품 코드로 의약품의 상세정보를 가져온다.
 * search_drugs_by_name()로 조회한 정보가 부족할 때 사용할 수 있다.
 *
 * @param drugcode search_drugs_by_name()의 결과 값에 기재된 의약품의 drug_code 값
 * @returns JSON 문자열 형태의 상세 정보
 * @throws {KPICApiError} API 요청 실패 시
 */
export async function get_drug_detail_by_id(drugcode: string): Promise<string> {
  if (!drugcode || drugcode.trim().length === 0) {
    throw new KPICApiError('Drug code cannot be empty');
  }

  const now = Date.now();
  const query = new URLSearchParams({ drug_cd: drugcode, _: String(now) });
  const url = `${BASE_URL}/searchDrug/ajax/ajax_result_drug2.asp?${query.toString()}`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        accept: 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ko,en-US;q=0.9,en;q=0.8,ru;q=0.7',
        'cache-control': 'no-cache',
        pragma: 'no-cache',
        Referer: `${BASE_URL}/searchDrug/result_drug.asp?drug_cd=${encodeURIComponent(drugcode)}`,
      },
    });

    if (!response.ok) {
      throw new KPICApiError(`API request failed: ${response.statusText}`, response.status);
    }

    const data = await response.text();

    // 응답 데이터 검증
    try {
      const parsed = JSON.parse(data) as DrugDetailResult[];

      if (!Array.isArray(parsed)) {
        throw new KPICApiError('Invalid response format: expected array');
      }

      if (parsed.length === 0) {
        throw new KPICApiError(`No drug found with code: ${drugcode}`);
      }

      // 결과를 보기 좋게 포맷팅하여 반환
      return JSON.stringify(parsed, null, 2);
    } catch (parseError) {
      if (parseError instanceof KPICApiError) {
        throw parseError;
      }
      throw new KPICApiError(
        `Failed to parse API response: ${parseError instanceof Error ? parseError.message : 'Unknown error'}`,
      );
    }
  } catch (error) {
    if (error instanceof KPICApiError) {
      throw error;
    }

    if (error instanceof Error) {
      throw new KPICApiError(`Network error: ${error.message}`);
    }

    throw new KPICApiError('Unknown error occurred');
  }
}
