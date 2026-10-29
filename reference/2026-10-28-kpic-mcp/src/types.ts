/**
 * KPIC (Korea Pharmaceutical Information Center) API Types
 */

/**
 * 약품 검색 결과 타입 (search_drugs_by_name)
 */
export interface DrugSearchResult {
  pack_img: string;
  drug_pic: string;
  drug_name: string;
  drug_enm: string;
  drug_code: string;
  sunb_count: number;
  list_sunb_name: string;
  ingr_mg: string;
  dosage: string;
  effect: string;
  upso_name_kfda: string;
  cls_code: string;
  drug_form: string;
  drug_class: string;
  etc: string;
  produce: string;
  boh_price: string;
  total_cnt: number;
  kfda_code: string;
  confirm_flag: string;
  /** 식약처 분류명 (새 API) */
  cls_name: string;
  /** 투여경로 (새 API) */
  dosage_route_name: string;
  /** 보험 코드 (새 API, 비급여면 빈 값) */
  boh_code: string;
}

/**
 * health.kr 새 검색 API(`/api/searchDrug`) 항목
 */
export interface SearchDrugItem {
  rnum: string;
  drug_code: string;
  drug_name: string;
  drug_enm: string;
  confirm_flag: string;
  kfda_code: string;
  sunb_count: number;
  list_sunb_name: string;
  upso_name_kfda: string;
  drug_form: string;
  dosage_route_name: string;
  drug_class: string;
  cls_name: string;
  boh_code: string;
  pack_img: string;
  drug_pic: string;
  ingr_mg: string;
  etc: string;
  produce: string;
  list_boh: string;
  boh_price: string;
}

/**
 * `/api/searchDrug` 응답 한 페이지
 */
export interface SearchDrugPage {
  items: SearchDrugItem[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

/**
 * health.kr 성분 검색 API(`/api/ingredient`) 항목
 */
export interface IngredientItem {
  rnum: string;
  ingd_code: string;
  ingd_name: string;
  ingd_ename: string;
  igcode: string;
  drug_count: number;
  has_detail: string;
}

/**
 * `/api/ingredient` 응답 한 페이지
 */
export interface IngredientPage {
  items: IngredientItem[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

/**
 * 성분 검색 결과 타입 (search_drugs_by_ingredient)
 */
export interface IngredientSearchResult {
  ingd_code: string;
  ingd_name: string;
  ingd_ename: string;
  /** 성분명이 정확히 일치했는지(exact), 부분 일치로 찾았는지(partial) */
  match_type: 'exact' | 'partial';
  drug_count: number;
  drugs: DrugSearchResult[];
}

/**
 * 약품 상세 정보 타입 (get_drug_detail_by_id)
 */
export interface DrugDetailResult {
  idx: number;
  drug_code: string;
  drug_name: string;
  drug_enm: string;
  noins: string | null;
  narcotic_kind_code: string;
  list_sunb_name: string;
  cls_code_num: string;
  sunb: string;
  drug_cls: string;
  sunb_count: number;
  upso_name: string;
  upso1: string;
  drug_form: string;
  dosage_route: string;
  charact: string;
  charact_new: string;
  cls_code: string;
  atc_cd: string;
  boh_history: string;
  boh_hiracode: string;
  item_permit_date: string;
  cancel_date: string;
  newdrug_class_code: string;
  bioeq_prodt_yn: string;
  comp_drug_yn_biology: string;
  comp_drug_yn_effect: string;
  comp_drug_yn: string;
  comp_drug_yn_physicochemical: string;
  kpic_atc: string;
  kpic_atc_cd: string;
  insertpaper: string;
  paper_dt: string;
  dur_age: string;
  dur_contra: string;
  dur_preg: string;
  dur_senior: string;
  dur_dose: string;
  dur_period: string;
  dur_donate: string;
  dur_form: string;
  fdacode: string;
  fdacontent: string;
  sunbcontent: string;
  drug_box: string;
  stmt: string;
  drug_pic: string;
  pack_img: string;
  picto_img: string;
  medititle: string;
  mediguide: string;
  effect: string;
  dosage: string;
  caution: string;
  idfylength: string;
  boh: string;
  etc: string;
  idfyidx: number;
  reexam: string | null;
  reexam_start_date: string;
  reexam_end_date: string;
  item_ingr_type: string;
  additives: string;
}

/**
 * API 에러 타입
 */
export class KPICApiError extends Error {
  constructor(
    message: string,
    public readonly statusCode?: number,
    public readonly response?: string,
  ) {
    super(message);
    this.name = 'KPICApiError';
  }
}
