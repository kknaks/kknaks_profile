# S05 — /categories/M5

[← review.md 목차](./review.md)

- 읽기 상태: read_direct · 마지막 읽은 Pointer `/categories/M5/effects/0/patient_ja`
- 공동 참조 문맥(소유 아님): `/source_method`, `/accuracy_summary`, `/categories/M5/name`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 JSON 리터럴 그대로다(이스케이프 포함). 관찰은 이 표에 섞지 않고 §2 에 둔다. 표현 ID 는 expressions.json.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/M5` | M5 | object | (object, 자식 4) | 29858–35754 |  |  |
| `/categories/M5/name` | name | string | "Platelet-rich plasma (PRP) and exosome therapies" | 29866–29916 | excluded | E0257 |
| `/categories/M5/moa` | moa | array | (array, 자식 4) | 29923–33242 |  |  |
| `/categories/M5/moa/0` | [0] | object | (object, 자식 8) | 29924–30786 |  |  |
| `/categories/M5/moa/0/statement` | statement | string | "PRP delivers concentrated platelet-derived growth factors (PDGF, TGF-β, VEGF, EGF) that stimulate fibroblast proliferation and collagen synthesis." | 29937–30085 | excluded | E0258, E0259 |
| `/categories/M5/moa/0/citations` | citations | array | (array, 자식 1) | 30098–30408 |  |  |
| `/categories/M5/moa/0/citations/0` | [0] | object | (object, 자식 8) | 30099–30407 |  |  |
| `/categories/M5/moa/0/citations/0/authors` | authors | string | "Alves R, Grimalt R" | 30110–30130 | excluded |  |
| `/categories/M5/moa/0/citations/0/title` | title | string | "A Review of Platelet-Rich Plasma: History, Biology, Mechanism of Action, and Classification." | 30139–30233 | excluded |  |
| `/categories/M5/moa/0/citations/0/journal` | journal | string | "Skin appendage disorders" | 30244–30270 | excluded |  |
| `/categories/M5/moa/0/citations/0/year` | year | number_int | 2018 | 30278–30282 | excluded |  |
| `/categories/M5/moa/0/citations/0/pmid` | pmid | string | "29457008" | 30290–30300 | excluded |  |
| `/categories/M5/moa/0/citations/0/doi` | doi | string | "10.1159/000477353" | 30307–30326 | excluded |  |
| `/categories/M5/moa/0/citations/0/pmc` | pmc | string | "PMC5806188" | 30333–30345 | excluded |  |
| `/categories/M5/moa/0/citations/0/oa_url` | oa_url | string | "https://pmc.ncbi.nlm.nih.gov/articles/PMC5806188/" | 30355–30406 | excluded |  |
| `/categories/M5/moa/0/accuracy_score` | accuracy_score | number_int | 100 | 30426–30429 | excluded |  |
| `/categories/M5/moa/0/accuracy_note` | accuracy_note | string | "PRP 내 성장인자들의 섬유아세포 증식 및 콜라겐 합성 유도 효과는 명확함." | 30446–30490 | applied | E0260 |
| `/categories/M5/moa/0/patient_ko` | patient_ko | string | "혈액에서 추출한 농축된 재생 성분들이 피부 세포의 활동을 돕고 탄력을 유지하는 단백질 생성을 촉진합니다." | 30504–30564 | applied | E0261 |
| `/categories/M5/moa/0/patient_en` | patient_en | string | "PRP provides concentrated growth factors that help skin cells stay active and boost collagen production." | 30578–30684 | excluded |  |
| `/categories/M5/moa/0/patient_zh` | patient_zh | string | "您的血小板浓缩液富含生长因子，能激活皮肤细胞并促进胶原蛋白再生。" | 30698–30732 | excluded |  |
| `/categories/M5/moa/0/patient_ja` | patient_ja | string | "濃縮された成長因子が細胞を活性化し、コラーゲンの生成を促して肌を整えます。" | 30746–30785 | excluded |  |
| `/categories/M5/moa/1` | [1] | object | (object, 자식 8) | 30787–31626 |  |  |
| `/categories/M5/moa/1/statement` | statement | string | "Extracellular vesicles (exosomes) carry proteins, lipids, and microRNAs that modulate recipient cell signaling and extracellular matrix remodeling." | 30800–30949 | excluded | E0262, E0263, E0264 |
| `/categories/M5/moa/1/citations` | citations | array | (array, 자식 1) | 30962–31230 |  |  |
| `/categories/M5/moa/1/citations/0` | [0] | object | (object, 자식 8) | 30963–31229 |  |  |
| `/categories/M5/moa/1/citations/0/authors` | authors | string | "Kalluri R" | 30974–30985 | excluded |  |
| `/categories/M5/moa/1/citations/0/title` | title | string | "The biology and function of exosomes in cancer." | 30994–31043 | excluded | E0265 |
| `/categories/M5/moa/1/citations/0/journal` | journal | string | "The Journal of clinical investigation" | 31054–31093 | excluded |  |
| `/categories/M5/moa/1/citations/0/year` | year | number_int | 2016 | 31101–31105 | excluded |  |
| `/categories/M5/moa/1/citations/0/pmid` | pmid | string | "27035812" | 31113–31123 | excluded |  |
| `/categories/M5/moa/1/citations/0/doi` | doi | string | "10.1172/JCI81135" | 31130–31148 | excluded |  |
| `/categories/M5/moa/1/citations/0/pmc` | pmc | string | "PMC4811149" | 31155–31167 | excluded |  |
| `/categories/M5/moa/1/citations/0/oa_url` | oa_url | string | "https://pmc.ncbi.nlm.nih.gov/articles/PMC4811149/" | 31177–31228 | excluded |  |
| `/categories/M5/moa/1/accuracy_score` | accuracy_score | number_int | 95 | 31248–31250 | excluded |  |
| `/categories/M5/moa/1/accuracy_note` | accuracy_note | string | "엑소좀의 세포 간 신호 전달 및 ECM 리모델링 조절 기전은 현대 재생의학의 핵심임." | 31267–31316 | applied | E0266 |
| `/categories/M5/moa/1/patient_ko` | patient_ko | string | "엑소좀이라 불리는 아주 작은 입자가 단백질과 유전 신호를 주변 세포에 전달해 재생과 콜라겐 재구성을 돕는 것으로 알려져 있습니다." | 31330–31404 | applied | E0267, E0268, E0269 |
| `/categories/M5/moa/1/patient_en` | patient_en | string | "Tiny particles called exosomes carry vital signals to surrounding cells to support natural skin renewal." | 31418–31524 | excluded |  |
| `/categories/M5/moa/1/patient_zh` | patient_zh | string | "被称为外泌体的微小颗粒将重要信号传递给周边细胞，协助皮肤自然更新。" | 31538–31573 | excluded |  |
| `/categories/M5/moa/1/patient_ja` | patient_ja | string | "エクソソームと呼ばれる微小粒子が細胞間で信号を送り、肌の再生を助けます。" | 31587–31625 | excluded |  |
| `/categories/M5/moa/2` | [2] | object | (object, 자식 7) | 31627–32454 |  |  |
| `/categories/M5/moa/2/statement` | statement | string | "Exosomes contain growth factors, lipids, amino acids, peptides, and RNA that promote fibroblast growth and collagen production." | 31640–31769 | excluded | E0270, E0271 |
| `/categories/M5/moa/2/citations` | citations | array | (array, 자식 1) | 31782–32147 |  |  |
| `/categories/M5/moa/2/citations/0` | [0] | object | (object, 자식 8) | 31783–32146 |  |  |
| `/categories/M5/moa/2/citations/0/authors` | authors | string | "Dai J, Su Y, Zhong S, Cong L, Liu B, Yang J, Tao Y, He Z, Chen C, Jiang Y" | 31794–31869 | excluded |  |
| `/categories/M5/moa/2/citations/0/title` | title | string | "Exosomes: key players in cancer and potential therapeutic strategy." | 31878–31947 | excluded | E0272 |
| `/categories/M5/moa/2/citations/0/journal` | journal | string | "Signal transduction and targeted therapy" | 31958–32000 | excluded |  |
| `/categories/M5/moa/2/citations/0/year` | year | number_int | 2020 | 32008–32012 | excluded |  |
| `/categories/M5/moa/2/citations/0/pmid` | pmid | string | "32759948" | 32020–32030 | excluded |  |
| `/categories/M5/moa/2/citations/0/doi` | doi | string | "10.1038/s41392-020-00261-0" | 32037–32065 | excluded |  |
| `/categories/M5/moa/2/citations/0/pmc` | pmc | string | "PMC7406508" | 32072–32084 | excluded |  |
| `/categories/M5/moa/2/citations/0/oa_url` | oa_url | string | "https://pmc.ncbi.nlm.nih.gov/articles/PMC7406508/" | 32094–32145 | excluded |  |
| `/categories/M5/moa/2/patient_ko` | patient_ko | string | "엑소좀은 섬유아세포 성장을 돕고 콜라겐 생성을 촉진하는 다양한 물질을 함유합니다." | 32161–32208 | applied |  |
| `/categories/M5/moa/2/patient_en` | patient_en | string | "These specialized particles contain essential nutrients that help firm the skin by encouraging growth." | 32222–32326 | excluded | E0273 |
| `/categories/M5/moa/2/patient_zh` | patient_zh | string | "这些特殊的颗粒含有必需营养成分，通过促进细胞生长来帮助紧致您的肌肤。" | 32340–32376 | excluded |  |
| `/categories/M5/moa/2/patient_ja` | patient_ja | string | "成長を助ける栄養素を含む粒子が、ハリのある健やかな肌作りをサポートします。" | 32390–32429 | excluded |  |
| `/categories/M5/moa/2/added_at` | added_at | string | "2026-04-19" | 32441–32453 | excluded |  |
| `/categories/M5/moa/3` | [3] | object | (object, 자식 7) | 32455–33241 |  |  |
| `/categories/M5/moa/3/statement` | statement | string | "Platelet-rich plasma stimulates tissue repair and new blood vessel formation." | 32468–32547 | excluded | E0274 |
| `/categories/M5/moa/3/citations` | citations | array | (array, 자식 1) | 32560–32949 |  |  |
| `/categories/M5/moa/3/citations/0` | [0] | object | (object, 자식 8) | 32561–32948 |  |  |
| `/categories/M5/moa/3/citations/0/authors` | authors | string | "Etulain J, Mena HA, Meiss RP, Frechtel G, Gutt S, Negrotto S, Schattner M" | 32572–32647 | excluded |  |
| `/categories/M5/moa/3/citations/0/title` | title | string | "An optimised protocol for platelet-rich plasma preparation to improve its angiogenic and regenerative properties." | 32656–32771 | excluded |  |
| `/categories/M5/moa/3/citations/0/journal` | journal | string | "Scientific reports" | 32782–32802 | excluded |  |
| `/categories/M5/moa/3/citations/0/year` | year | number_int | 2018 | 32810–32814 | excluded |  |
| `/categories/M5/moa/3/citations/0/pmid` | pmid | string | "29367608" | 32822–32832 | excluded |  |
| `/categories/M5/moa/3/citations/0/doi` | doi | string | "10.1038/s41598-018-19419-6" | 32839–32867 | excluded |  |
| `/categories/M5/moa/3/citations/0/pmc` | pmc | string | "PMC5784112" | 32874–32886 | excluded |  |
| `/categories/M5/moa/3/citations/0/oa_url` | oa_url | string | "https://pmc.ncbi.nlm.nih.gov/articles/PMC5784112/" | 32896–32947 | excluded |  |
| `/categories/M5/moa/3/patient_ko` | patient_ko | string | "혈소판풍부혈장은 조직 수복과 새로운 혈관 형성을 촉진합니다." | 32963–32998 | applied |  |
| `/categories/M5/moa/3/patient_en` | patient_en | string | "Concentrated blood components help repair damaged tissues and encourage healthy circulation in the skin." | 33012–33118 | excluded | E0275 |
| `/categories/M5/moa/3/patient_zh` | patient_zh | string | "浓缩的血液成分有助于修复受损组织，并促进您皮肤内的健康循环与代谢。" | 33132–33167 | excluded |  |
| `/categories/M5/moa/3/patient_ja` | patient_ja | string | "濃縮された血液成分が、組織の修復と健やかなめぐりをサポートします。" | 33181–33216 | excluded |  |
| `/categories/M5/moa/3/added_at` | added_at | string | "2026-04-19" | 33228–33240 | excluded |  |
| `/categories/M5/adverse_effects` | adverse_effects | array | (array, 자식 2) | 33261–34881 |  |  |
| `/categories/M5/adverse_effects/0` | [0] | object | (object, 자식 8) | 33262–34072 |  |  |
| `/categories/M5/adverse_effects/0/statement` | statement | string | "Post-procedure pain, swelling, and bruising at injection sites are the most frequently reported PRP adverse events." | 33275–33392 | excluded | E0276, E0277, E0278, E0279 |
| `/categories/M5/adverse_effects/0/citations` | citations | array | (array, 자식 1) | 33405–33715 |  |  |
| `/categories/M5/adverse_effects/0/citations/0` | [0] | object | (object, 자식 8) | 33406–33714 |  |  |
| `/categories/M5/adverse_effects/0/citations/0/authors` | authors | string | "Alves R, Grimalt R" | 33417–33437 | excluded |  |
| `/categories/M5/adverse_effects/0/citations/0/title` | title | string | "A Review of Platelet-Rich Plasma: History, Biology, Mechanism of Action, and Classification." | 33446–33540 | excluded |  |
| `/categories/M5/adverse_effects/0/citations/0/journal` | journal | string | "Skin appendage disorders" | 33551–33577 | excluded |  |
| `/categories/M5/adverse_effects/0/citations/0/year` | year | number_int | 2018 | 33585–33589 | excluded |  |
| `/categories/M5/adverse_effects/0/citations/0/pmid` | pmid | string | "29457008" | 33597–33607 | excluded |  |
| `/categories/M5/adverse_effects/0/citations/0/doi` | doi | string | "10.1159/000477353" | 33614–33633 | excluded |  |
| `/categories/M5/adverse_effects/0/citations/0/pmc` | pmc | string | "PMC5806188" | 33640–33652 | excluded |  |
| `/categories/M5/adverse_effects/0/citations/0/oa_url` | oa_url | string | "https://pmc.ncbi.nlm.nih.gov/articles/PMC5806188/" | 33662–33713 | excluded |  |
| `/categories/M5/adverse_effects/0/accuracy_score` | accuracy_score | number_int | 100 | 33733–33736 | excluded |  |
| `/categories/M5/adverse_effects/0/accuracy_note` | accuracy_note | string | "통증, 부기, 멍은 주사 시술에서 가장 빈번한 부작용임." | 33753–33786 | applied | E0280, E0281 |
| `/categories/M5/adverse_effects/0/patient_ko` | patient_ko | string | "시술을 받은 부위에 통증이나 붓기, 멍이 일시적으로 나타날 수 있으며 이는 가장 흔하게 발생하는 현상입니다." | 33800–33862 | applied | E0282, E0283, E0284, E0285, E0286 |
| `/categories/M5/adverse_effects/0/patient_en` | patient_en | string | "You may experience temporary discomfort, swelling, or minor bruising at the site of treatment." | 33876–33972 | excluded | E0287, E0288, E0289 |
| `/categories/M5/adverse_effects/0/patient_zh` | patient_zh | string | "您在治疗部位可能会感到暂时的不适、肿胀或出现轻微的淤青，这些都很常见。" | 33986–34023 | excluded |  |
| `/categories/M5/adverse_effects/0/patient_ja` | patient_ja | string | "施術した部分に、一時的な痛みや腫れ、内出血が出ることがあります。" | 34037–34071 | excluded |  |
| `/categories/M5/adverse_effects/1` | [1] | object | (object, 자식 8) | 34073–34880 |  |  |
| `/categories/M5/adverse_effects/1/statement` | statement | string | "Transmission of infection is a theoretical risk when exogenous (non-autologous) blood products are used." | 34086–34192 | excluded | E0290, E0291, E0292, E0293 |
| `/categories/M5/adverse_effects/1/citations` | citations | array | (array, 자식 1) | 34205–34515 |  |  |
| `/categories/M5/adverse_effects/1/citations/0` | [0] | object | (object, 자식 8) | 34206–34514 |  |  |
| `/categories/M5/adverse_effects/1/citations/0/authors` | authors | string | "Alves R, Grimalt R" | 34217–34237 | excluded |  |
| `/categories/M5/adverse_effects/1/citations/0/title` | title | string | "A Review of Platelet-Rich Plasma: History, Biology, Mechanism of Action, and Classification." | 34246–34340 | excluded |  |
| `/categories/M5/adverse_effects/1/citations/0/journal` | journal | string | "Skin appendage disorders" | 34351–34377 | excluded |  |
| `/categories/M5/adverse_effects/1/citations/0/year` | year | number_int | 2018 | 34385–34389 | excluded |  |
| `/categories/M5/adverse_effects/1/citations/0/pmid` | pmid | string | "29457008" | 34397–34407 | excluded |  |
| `/categories/M5/adverse_effects/1/citations/0/doi` | doi | string | "10.1159/000477353" | 34414–34433 | excluded |  |
| `/categories/M5/adverse_effects/1/citations/0/pmc` | pmc | string | "PMC5806188" | 34440–34452 | excluded |  |
| `/categories/M5/adverse_effects/1/citations/0/oa_url` | oa_url | string | "https://pmc.ncbi.nlm.nih.gov/articles/PMC5806188/" | 34462–34513 | excluded |  |
| `/categories/M5/adverse_effects/1/accuracy_score` | accuracy_score | number_int | 100 | 34533–34536 | excluded |  |
| `/categories/M5/adverse_effects/1/accuracy_note` | accuracy_note | string | "비자가 혈액 제제 사용 시 감염 전파 위험은 이론적, 실제적으로 존재함." | 34553–34595 | applied | E0294, E0295, E0296 |
| `/categories/M5/adverse_effects/1/patient_ko` | patient_ko | string | "외부의 혈액 성분을 사용하는 경우 이론적으로 감염 우려가 있으나 본인의 혈액을 활용하면 매우 안전합니다." | 34609–34669 | applied | E0297, E0298, E0299 |
| `/categories/M5/adverse_effects/1/patient_en` | patient_en | string | "Using your own blood components makes this treatment very compatible with your body's system." | 34683–34778 | excluded | E0300 |
| `/categories/M5/adverse_effects/1/patient_zh` | patient_zh | string | "使用您自身的血液成分使得这种疗法与您的身体系统具有极高的兼容性。" | 34792–34826 | excluded |  |
| `/categories/M5/adverse_effects/1/patient_ja` | patient_ja | string | "ご自身の血液成分を使用するため、体へのなじみが良く、とても自然なケアです。" | 34840–34879 | excluded |  |
| `/categories/M5/effects` | effects | array | (array, 자식 1) | 34892–35753 |  |  |
| `/categories/M5/effects/0` | [0] | object | (object, 자식 8) | 34893–35752 |  |  |
| `/categories/M5/effects/0/statement` | statement | string | "PRP application supports wound healing in chronic and post-procedural wounds." | 34906–34985 | excluded | E0301 |
| `/categories/M5/effects/0/citations` | citations | array | (array, 자식 1) | 34998–35391 |  |  |
| `/categories/M5/effects/0/citations/0` | [0] | object | (object, 자식 8) | 34999–35390 |  |  |
| `/categories/M5/effects/0/citations/0/authors` | authors | string | "Martinez-Zapata MJ, Martí-Carvajal AJ, Solà I, Expósito JA, Bolíbar I, Rodríguez L, Garcia J, Zaror C" | 35010–35113 | excluded |  |
| `/categories/M5/effects/0/citations/0/title` | title | string | "Autologous platelet-rich plasma for treating chronic wounds." | 35122–35184 | excluded | E0302 |
| `/categories/M5/effects/0/citations/0/journal` | journal | string | "The Cochrane database of systematic reviews" | 35195–35240 | excluded |  |
| `/categories/M5/effects/0/citations/0/year` | year | number_int | 2016 | 35248–35252 | excluded |  |
| `/categories/M5/effects/0/citations/0/pmid` | pmid | string | "27223580" | 35260–35270 | excluded |  |
| `/categories/M5/effects/0/citations/0/doi` | doi | string | "10.1002/14651858.CD006899.pub3" | 35277–35309 | excluded |  |
| `/categories/M5/effects/0/citations/0/pmc` | pmc | string | "PMC9308064" | 35316–35328 | excluded |  |
| `/categories/M5/effects/0/citations/0/oa_url` | oa_url | string | "https://pmc.ncbi.nlm.nih.gov/articles/PMC9308064/" | 35338–35389 | excluded |  |
| `/categories/M5/effects/0/accuracy_score` | accuracy_score | number_int | 95 | 35409–35411 | excluded |  |
| `/categories/M5/effects/0/accuracy_note` | accuracy_note | string | "만성 상처 및 시술 후 상처 치유를 돕는 보조 요법으로 가치가 큼." | 35428–35467 | applied | E0303 |
| `/categories/M5/effects/0/patient_ko` | patient_ko | string | "상처가 난 곳이나 시술로 인해 자극받은 피부가 자연스럽게 치유되는 과정을 도와 회복을 원활하게 해줍니다." | 35481–35541 | applied |  |
| `/categories/M5/effects/0/patient_en` | patient_en | string | "This approach supports the natural healing of the skin after other procedures or for dry areas." | 35555–35652 | excluded | E0304, E0305 |
| `/categories/M5/effects/0/patient_zh` | patient_zh | string | "这种方法有助于支持皮肤在其他疗程后或在干燥部位进行的自然修复过程。" | 35666–35701 | excluded |  |
| `/categories/M5/effects/0/patient_ja` | patient_ja | string | "施術後のデリケートな肌や、気になる部分の自然な修復をサポートします。" | 35715–35751 | excluded |  |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

- **S05-O1** [P] `/categories/M5/moa/0`, `/categories/M5/moa/1`, `/categories/M5/adverse_effects/0`, `/categories/M5/adverse_effects/1`, `/categories/M5/effects/0` — 점수 진술 5개(100·95·100·100·95)는 added_at 이 없고, moa/2·moa/3 은 added_at 만 있다. by_category_average M5=98.0 과 일치.
- **S05-O2** [P] `/categories/M5/name`, `/categories/M5/moa/1/statement`, `/categories/M5/moa/2/statement` — name 'Platelet-rich plasma (PRP) and exosome therapies' — 두 계열을 and 로 묶은 카테고리. 진술은 PRP(moa/0·3, AE 0·1, effects/0)와 exosome(moa/1·2)으로 나뉜다.
- **S05-O3** [P] `/categories/M5/moa/1/citations/0/title`, `/categories/M5/moa/2/citations/0/title` — exosome 진술 두 개의 인용 제목이 'The biology and function of exosomes in cancer.'·'Exosomes: key players in cancer and potential therapeutic strategy.' — 제목상 암 맥락 문헌. 미용 적용과의 관련성은 원문이 밝히지 않음.
- **S05-O4** [P] `/categories/M5/adverse_effects/0/statement` — 'Post-procedure pain, swelling, and bruising at injection sites are the most frequently reported PRP adverse events' — 시점(post-procedure)·부위(injection sites)·상대 빈도('most frequently reported', 보고 사건 기준). patient_ko '일시적으로'(경과)·'가장 흔하게 발생하는'(보고 빈도→발생 빈도로 바뀜), patient_en 'minor bruising'(정도 추가).
- **S05-O5** [P] `/categories/M5/adverse_effects/1/statement`, `/categories/M5/adverse_effects/1/patient_ko`, `/categories/M5/adverse_effects/1/patient_en` — statement 는 '외인성(비자가) 혈액 제제 사용 시 감염 전파는 이론적 위험'(조건+가능성). accuracy_note 는 '이론적, 실제적으로 존재함'으로 statement 보다 강하다. patient_ko 는 '본인의 혈액을 활용하면 매우 안전합니다' 를 더하고, patient_en/zh/ja 는 감염 위험을 전혀 언급하지 않고 자가 혈액의 적합성만 말한다.
- **S05-O6** [P] `/categories/M5/effects/0/statement`, `/categories/M5/effects/0/patient_en` — statement 'chronic and post-procedural wounds' 를 patient_en/zh 는 'after other procedures or for dry areas'·'干燥部位' 로 옮김 — chronic wounds 가 dry areas 로 바뀜. patient_ja '気になる部分'.
- **S05-O7** [P] `/categories/M5/moa/0/statement` — 성장인자 목록 '(PDGF, TGF-β, VEGF, EGF)' — 괄호 예시 나열. patient_ko 는 '혈액에서 추출한 농축된 재생 성분들' 로 일반화.

## 3. 수동 표현 (직접 읽기에서 수집)

| 표현 ID | Pointer | 구간 | 원문 구절 | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0257 | `/categories/M5/name` | 0–48 | Platelet-rich plasma (PRP) and exosome therapies | name_candidate, conjunction | P |  |
| E0258 | `/categories/M5/moa/0/statement` | 13–82 | concentrated platelet-derived growth factors (PDGF, TGF-β, VEGF, EGF) | ingredient, example, degree | P |  |
| E0259 | `/categories/M5/moa/0/statement` | 88–145 | stimulate fibroblast proliferation and collagen synthesis | mechanism | P |  |
| E0260 | `/categories/M5/moa/0/accuracy_note` | 38–41 | 명확함 | certainty | P |  |
| E0261 | `/categories/M5/moa/0/patient_ko` | 0–19 | 혈액에서 추출한 농축된 재생 성분들 | ingredient, source_material | P |  |
| E0262 | `/categories/M5/moa/1/statement` | 0–33 | Extracellular vesicles (exosomes) | name_candidate | P |  |
| E0263 | `/categories/M5/moa/1/statement` | 34–71 | carry proteins, lipids, and microRNAs | ingredient, example | P |  |
| E0264 | `/categories/M5/moa/1/statement` | 77–146 | modulate recipient cell signaling and extracellular matrix remodeling | mechanism | P |  |
| E0265 | `/categories/M5/moa/1/citations/0/title` | 37–46 | in cancer | context_scope | F |  |
| E0266 | `/categories/M5/moa/1/accuracy_note` | 34–46 | 현대 재생의학의 핵심임 | degree | P |  |
| E0268 | `/categories/M5/moa/1/patient_ko` | 10–18 | 아주 작은 입자 | size, degree | P |  |
| E0269 | `/categories/M5/moa/1/patient_ko` | 56–71 | 돕는 것으로 알려져 있습니다 | evidence_status, hedge | I | statement 는 단정 |
| E0270 | `/categories/M5/moa/2/statement` | 9–71 | contain growth factors, lipids, amino acids, peptides, and RNA | ingredient, example | P |  |
| E0271 | `/categories/M5/moa/2/statement` | 77–126 | promote fibroblast growth and collagen production | mechanism | P |  |
| E0272 | `/categories/M5/moa/2/citations/0/title` | 10–66 | key players in cancer and potential therapeutic strategy | context_scope, possibility | F |  |
| E0273 | `/categories/M5/moa/2/patient_en` | 36–55 | essential nutrients | ingredient | I | statement 성분 목록 일반화 |
| E0274 | `/categories/M5/moa/3/statement` | 21–76 | stimulates tissue repair and new blood vessel formation | mechanism | P |  |
| E0275 | `/categories/M5/moa/3/patient_en` | 62–103 | encourage healthy circulation in the skin | mechanism | I | 'new blood vessel formation' 이 circulation 으로 바뀜 |
| E0276 | `/categories/M5/adverse_effects/0/statement` | 0–14 | Post-procedure | time | P |  |
| E0277 | `/categories/M5/adverse_effects/0/statement` | 15–62 | pain, swelling, and bruising at injection sites | event, anatomy_site | P |  |
| E0278 | `/categories/M5/adverse_effects/0/statement` | 67–95 | the most frequently reported | frequency, comparison, evidence_status | P |  |
| E0280 | `/categories/M5/adverse_effects/0/accuracy_note` | 11–30 | 주사 시술에서 가장 빈번한 부작용임 | frequency, comparison, scope | P |  |
| E0282 | `/categories/M5/adverse_effects/0/patient_ko` | 23–38 | 일시적으로 나타날 수 있으며 | duration_quality, possibility | P |  |
| E0284 | `/categories/M5/adverse_effects/0/patient_ko` | 42–59 | 가장 흔하게 발생하는 현상입니다 | frequency, comparison | I | 'reported' 가 '발생'으로 |
| E0287 | `/categories/M5/adverse_effects/0/patient_en` | 0–18 | You may experience | possibility | P | 읽기 검토(정규식 미포함 후보 대조)에서 추가 |
| E0289 | `/categories/M5/adverse_effects/0/patient_en` | 19–68 | temporary discomfort, swelling, or minor bruising | event, duration_quality, degree | P |  |
| E0290 | `/categories/M5/adverse_effects/1/statement` | 0–47 | Transmission of infection is a theoretical risk | event, possibility | P |  |
| E0291 | `/categories/M5/adverse_effects/1/statement` | 48–103 | when exogenous (non-autologous) blood products are used | condition, negation, source_material | P |  |
| E0294 | `/categories/M5/adverse_effects/1/accuracy_note` | 0–14 | 비자가 혈액 제제 사용 시 | condition, negation, source_material | P | 읽기 검토(정규식 미포함 후보 대조)에서 추가 |
| E0296 | `/categories/M5/adverse_effects/1/accuracy_note` | 25–39 | 이론적, 실제적으로 존재함 | possibility, certainty | I | statement 는 theoretical 만 |
| E0297 | `/categories/M5/adverse_effects/1/patient_ko` | 0–35 | 외부의 혈액 성분을 사용하는 경우 이론적으로 감염 우려가 있으나 | condition, possibility, event | P |  |
| E0298 | `/categories/M5/adverse_effects/1/patient_ko` | 36–57 | 본인의 혈액을 활용하면 매우 안전합니다 | condition, safety_claim, degree | I | statement 에 없는 안전 주장 |
| E0300 | `/categories/M5/adverse_effects/1/patient_en` | 53–92 | very compatible with your body's system | safety_claim, degree | I | 감염 위험 탈락 |
| E0301 | `/categories/M5/effects/0/statement` | 16–76 | supports wound healing in chronic and post-procedural wounds | effect, scope, time | P |  |
| E0302 | `/categories/M5/effects/0/citations/0/title` | 0–60 | Autologous platelet-rich plasma for treating chronic wounds. | context_scope, source_material | P |  |
| E0303 | `/categories/M5/effects/0/accuracy_note` | 23–36 | 보조 요법으로 가치가 큼 | role, degree | P |  |
| E0304 | `/categories/M5/effects/0/patient_en` | 55–94 | after other procedures or for dry areas | time, scope | I | chronic wounds → dry areas |

## 4. 미결

- **S05-I1** [I] `/categories/M5/adverse_effects/1/patient_ko`, `/categories/M5/adverse_effects/1/patient_en`, `/categories/M5/adverse_effects/1/patient_zh`, `/categories/M5/adverse_effects/1/patient_ja`, `/categories/M5/adverse_effects/1/accuracy_note` — 감염 위험 진술의 언어별 내용 차이: ko 는 '매우 안전' 추가, en/zh/ja 는 위험 자체 탈락, accuracy_note 는 '실제적으로' 추가. I-LANG(안전 정보 방향이 달라지는 사례).
- **S05-I2** [I] `/categories/M5/effects/0/patient_en`, `/categories/M5/effects/0/patient_zh` — chronic wounds → dry areas/干燥部位. I-LANG.
- **S05-I3** [I] `/categories/M5/adverse_effects/0/patient_ko`, `/categories/M5/moa/1/patient_ko` — 'most frequently reported' → '가장 흔하게 발생'(보고 기준이 발생 기준으로), 단정 → '알려져 있습니다'. I-LANG.
- **S05-F1** [F] `/categories/M5/moa/1/citations/0/title`, `/categories/M5/moa/2/citations/0/title` — 암 맥락 문헌이 미용 exosome 기전 진술의 근거로 쓰인 적합성 — 원문 범위 밖 사실 확인이 필요, 후속(외부 자료로 채우지 않음).
- **S05-B1** [B] `/categories/M5/adverse_effects/0/statement` — 'most frequently reported' 의 수치·분모 없음. 지속 기간도 없음(patient_ko '일시적'의 근거 없음).
