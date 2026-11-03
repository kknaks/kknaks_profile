import json,re,sys
W='/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend'
d=json.load(open(f'{W}/product-master-draft.json'))
mods={m['id']:m['name'] for m in json.load(open(f'{W}/taxonomy-classify-v2.json'))['modalities']}
U=r'(단위|유니트|유닛|U|mg|mL|ml|cc|g|IU)'
LEG=r'\(주\)|㈜|주식회사|유한회사|\(유\)|inc\.?|co\.,?\s*ltd\.?|ltd\.?|korea|코리아|한국|[\s·,]'
norm=lambda s: re.sub(LEG,'',(s or '').lower())
def rank(c):
    return (not c.get('model_equal'), not c.get('name_contains_ledger'), not c.get('name_contains_query'), not c.get('family_ok'), c.get('state')!='정상', -(int(re.sub(r'\D','',c.get('license_date') or '0')[:8] or 0)))
def tag(c):
    return '모델명 같음' if c.get('model_equal') else '이름 포함' if (c.get('name_contains_ledger') or c.get('name_contains_query')) else '계열만 맞음' if c.get('family_ok') else '잡음'
def base(n):
    n=re.sub(r'\(.*?\)|\[.*?\]','',n or ''); n=re.sub(r'\s*[\d.,]+\s*'+U+r'(/[\d.,]+\s*'+U+r')?','',n); n=re.sub(r'외\s*\d+건','',n)
    return re.sub(r'\s+','',n).lower()
def spec(c):
    sp=c.get('spec')
    s=json.dumps(sp,ensure_ascii=False) if isinstance(sp,(dict,list)) else (sp or '')
    m=re.search(r'\[([^\]]+)\]',s)
    if m: v=m.group(1)
    else:
        m=re.search(r'PACK_UNIT"?:\s*"([^"]+)',s); v=m.group(1) if m else ''
        if not v:
            m=re.search(r'([\d.,]+\s*'+U+r')',c.get('official_name') or ''); v=m.group(1) if m else ''
    return re.sub(r'바이알\(([\d.,]+\s*(?:단위|유니트|유닛|U))\)',r'1바이알당 \1',v)
VIA={'photo':'사진','web':'웹','hub_en':'Hub 영문명','guess':'추측','company_list':'업체 목록'}
def vias(c):
    v=c.get('via')
    v=v if isinstance(v,list) else ([v] if v else [])
    if c.get('via_guess') and 'guess' not in v: v.append('guess')
    if c.get('via_company_list') and 'company_list' not in v: v.append('company_list')
    return [VIA.get(x,x) for x in v]
def groups(cs):
    gs={}
    for c in sorted(cs,key=rank):
        k=(c.get('company') or '')+'|'+base(c.get('official_name'))+'|'+tag(c)+'|'+(c.get('state') or '')
        g=gs.get(k)
        if not g:
            g=gs[k]={'k':c['key'],'keys':[],'n':c.get('official_name'),'en':c.get('name_en'),'co':c.get('company'),'mo':c.get('manufacturer_original'),
              'dt':c.get('license_date'),'st':c.get('state'),'md':c.get('model_name'),'pu':(c.get('purpose_or_efficacy') or '')[:90],'lk':c.get('license_kind'),
              'tag':tag(c),'via':vias(c),'src':(c.get('source_urls') or c.get('sources') or [])[:2],'specs':[],'nos':[]}
        g['keys'].append(c['key']); s=spec(c)
        if s and s not in g['specs']: g['specs'].append(s)
        if c.get('license_no'): g['nos'].append(c['license_no'])
        for x in vias(c):
            if x not in g['via']: g['via'].append(x)
    out=[]
    for g in gs.values():
        g['sp']=('규격: '+' · '.join(g.pop('specs'))) if g['specs'] else (g.pop('specs') and '')
        nos=g.pop('nos'); g['no']=', '.join(nos[:3])+(' 외' if len(nos)>3 else '')
        if len(g['keys'])>1: g['n']=re.sub(r'\s*[\d.,]+\s*'+U,'',g['n'] or '',count=1).strip()+f'  — 용량별 허가 {len(g["keys"])}개'
        out.append(g)
    return out[:25], len(out)
prods=[]
for p in d['products']:
    m=p['match']; gl,total=groups(m.get('candidates',[]))
    st=m['status']; autoKeys=None
    if st=='auto':
        ak=m.get('auto_keys') or m.get('auto_pick'); ak=[ak] if isinstance(ak,str) else (ak or [])
        for g in gl:
            if ak and ak[0] in g['keys']: ak=g['keys']
        autoKeys=ak
        if not autoKeys:
            gg=[g for g in gl if g['tag'] in ('모델명 같음','이름 포함')]
            autoKeys=[k for g in gg for k in g['keys']] or None
            if not autoKeys: st='candidate'
    good=[g for g in gl if g['tag'] in ('모델명 같음','이름 포함') and not set(g['via'])&{'추측','사진','웹','업체 목록'}]
    makers=[norm(x) for mk in (p.get('maker_texts') or []) for x in re.split(r'[/,]',mk) if norm(x)]
    if st=='candidate' and len(good)==1 and makers:
        co=norm(good[0].get('co'))+norm(good[0].get('mo'))
        if any(mk in co or (co and co in mk) for mk in makers): st='auto'; autoKeys=good[0]['keys']
    if st=='auto': plain='자동 확정: 이름이 든 제품이 하나이고 업체가 같습니다. 틀리면 체크를 풀어 주세요.'
    elif st=='no_service': plain='의약품·의료기기 허가 DB에 없는 종류입니다(화장품·재료 등). 보통 「허가 대상 아님」.'+(' 무엇: '+(p.get('what_is_it') or m.get('what_is_it') or '') if (p.get('what_is_it') or m.get('what_is_it')) else '')
    elif st=='none': plain='식약처에서 찾지 못했습니다(사진·웹으로도). 영문명·업체를 아시면 메모에, 없으면 「해당 허가 없음」.'
    else:
        g2=[g for g in gl if g['tag'] in ('모델명 같음','이름 포함')]; fam=[g for g in gl if g['tag']=='계열만 맞음']
        bits=[]
        if g2: bits.append(f'이름이 든 제품 {len(g2)}개')
        if fam: bits.append(f'같은 업체·종류지만 이름이 다른 제품 {len(fam)}개')
        plain=('찾은 것: '+', '.join(bits)+'. 같은 제품이면 체크하세요.') if bits else '관련 있어 보이는 허가가 없습니다.'
    prods.append({'id':p['id'],'name':p['name'],'mod':p.get('modality'),'modn':mods.get(p.get('modality'),''),'maker':p.get('maker_texts') or [],
      'st':st,'autoKeys':autoKeys,'plain':plain,'total':total,'c':gl,'use':p.get('in_use_at_clinic') or []})
news=[]
for n in d.get('new_ledger_candidates',[]):
    mf=n.get('mfds') or {}; gl,total=groups(mf.get('candidates',[]))
    w=n.get('web') or {}
    news.append({'id':'new-'+n['photo_id'],'name':n.get('clinic_name'),'folder':n.get('folder'),'read':' / '.join(x for x in [n.get('read_maker'),n.get('read_model')] if x) or ('사진 판독 불가' if not n.get('readable') else ''),
      'web':' · '.join(x for x in [w.get('manufacturer'),w.get('device_type'),('수입사 '+w['importer_kr']) if w.get('importer_kr') else None] if x) if w.get('found') else '',
      'src':(w.get('sources') or [])[:2],'c':gl,'total':total})
data={'generated_at':d.get('generated_at'),'n':len(prods),'products':prods,'news':news}
s=json.dumps(data,ensure_ascii=False).replace('\ufffd','\\ufffd').replace('</','<\\/')
print('products',len(prods),'auto',sum(p['st']=='auto' for p in prods),'news',len(news),'KB',len(s)//1024)
# 게이트 축소 규칙(_RESUME 10-27): 이름 든 제품 하나+업체 일치 → auto · 여럿 → 라인 auto · 하나+업체 다름 → 직접 확인 · 없음/못 찾음 → 허가 미확인 · DB 없음 → 허가 대상 아님
for p in prods:
    if p['st']=='none': p['st']='unknown'; p['plain']='허가 미확인(식약처에서 못 찾음 — 웹 조사 포함). 아는 정보가 있으면 메모에.'; continue
    if p['st']=='no_service': p['st']='na'; p['plain']='허가 대상 아님으로 자동 처리(의약품·의료기기 DB에 없는 종류). 틀리면 메모에.'; continue
    if p['st']!='candidate': continue
    good=[g for g in p['c'] if g['tag'] in ('모델명 같음','이름 포함')]
    makers=[norm(x) for mk in p['maker'] for x in re.split(r'[/,]',mk) if norm(x)]
    mok=lambda g: any(mk in norm(g.get('co'))+norm(g.get('mo')) or (norm(g.get('co')) and norm(g.get('co')) in mk) for mk in makers)
    if len(good)==1 and (not makers or mok(good[0])):
        p['st']='auto'; p['autoKeys']=good[0]['keys']; p['plain']='자동 확정: 이름이 든 제품이 하나이고 업체가 같습니다(또는 원장에 업체 없음). 틀리면 체크를 풀어 주세요.'
    elif len(good)>1:
        p['st']='auto'; p['autoKeys']=[k for g in good for k in g['keys']]; p['plain']=f'자동 확정(라인 제품): 이름이 든 제품 {len(good)}개를 이 라인의 하위 품목으로 모두 연결했습니다. 아닌 품목은 체크를 풀어 주세요.'
    elif len(good)==1:
        p['plain']='직접 확인: 이름은 맞는데 업체가 원장과 다릅니다(수입사가 바뀌었거나 다른 제품). 같은 제품이면 체크, 아니면 「해당 허가 없음」.'
    else:
        p['st']='unknown'; p['plain']='허가 미확인(이름이 든 허가 없음 — 아래는 같은 업체·종류의 다른 제품일 뿐). 맞는 게 있으면 체크하세요.'
data={'generated_at':d.get('generated_at'),'n':len(prods),'products':prods,'news':news}
s=json.dumps(data,ensure_ascii=False).replace('\ufffd','\\ufffd').replace('</','<\\/')
from collections import Counter
print(dict(Counter(p['st'] for p in prods)))
# 페이지에 주입
h=open(f'{W}/product-match-review.html').read()
mm=re.search(r'(<script id="data" type="application/json">)(.*?)(</script>)',h,re.S)
open(f'{W}/product-match-review.html','w').write(h[:mm.start(2)]+s+h[mm.end(2):])
