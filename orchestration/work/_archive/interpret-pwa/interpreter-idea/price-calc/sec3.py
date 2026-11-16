"""price.md 3절 — 실제 원가만(마진 없음). 2절 산식: 독립변인 1개 이동 · 나머지 적정 고정."""
import json, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family']='AppleGothic'; plt.rcParams['axes.unicode_minus']=False
OUT='/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/reference/2026-11-12-interpreter-idea/'
S_STREAM, S_SPEECH, S_TTS, CONN = 0.023, 0.047, 0.272, 42.4     # 1.2
IDLE = 60                                                         # 무발화 1분 종료
# 1.5 실측 1발화: STT 연결 · 말 · 번역 음성(초)
U = {'상담': dict(stream=87.6, speech=36.7, tts=45.5), '간단': dict(stream=15.4, speech=15.4, tts=6.1)}
for u in U.values():
    u['cycle']=u['speech']+u['tts']                                # 발화 1회 시간(말 + 재생)
    u['a']=S_STREAM*u['stream']+S_SPEECH*u['speech']             # 발화 중 STT 연결 + 텍스트
    u['b']=S_TTS*u['tts']                                          # 번역 음성
DAYS=30
PARTS=['발화 중 STT · 텍스트(①②)','번역 음성(③)','무발화 연결 60초(①)','연결비(④)']
def kmax(t,d):
    return max(1.0, min(3600*d/U[t]['cycle'], 60*(1-d)))
def hour(t,d,p):
    if d<=0: return dict(zip(PARTS,[0,0,0,0]))|dict(k=0)
    u=U[t]; n=3600*d/u['cycle']; k=1+p*(kmax(t,d)-1)
    return dict(zip(PARTS,[n*u['a'],n*u['b'],S_STREAM*IDLE*k,CONN*k]))|dict(k=k)
def month(q):
    c=hour('상담',q['d'],q['p']); s=hour('간단',q['d'],q['p']); r=q['r']; h=DAYS*q['H']
    m={x:h*(r*c[x]+(1-r)*s[x]) for x in PARTS}
    m['cost']=sum(m[x] for x in PARTS); m['hours']=h; m['per_hour']=m['cost']/h
    m['k상담']=c['k']; m['k간단']=s['k']; m['월 연결']=h*(r*c['k']+(1-r)*s['k'])
    return m
BASE={'H':6.5,'r':0.5,'d':0.5,'p':0.5}
V=[('H','① 하루 실사용 시간 H (시간/일)',1,12),('r','② 상담 비율 r (0=간단만 · 1=상담만, 시간 기준)',0,1),
   ('p','③ 시간당 연결 횟수 (범위 위치 p: 0=1회 · 1=최대)',0,1),('d','④ 말 밀도 d (0=무발화 · 1=쉬지 않고)',0,1)]
COL=['#5dade2','#e67e22','#aab7b8','#8e44ad']
b=month(BASE); res={'base':b,'sweeps':{}}
fig,axs=plt.subplots(2,2,figsize=(14,12),dpi=130); axs=axs.flatten()
for ax,(key,name,a,z) in zip(axs,V):
    xs=[a+(z-a)*i/200 for i in range(201)]
    ms=[month({**BASE,key:x}) for x in xs]
    ax.stackplot(xs,*[[m[x]/1e4 for m in ms] for x in PARTS],colors=COL,labels=PARTS,alpha=.85)
    ax.plot(xs,[m['cost']/1e4 for m in ms],color='#000',lw=2,label='월 원가 합계')
    ax.axvline(BASE[key],color='#333',ls=':',lw=1)
    ax.annotate(f'적정 {b["cost"]/1e4:.1f}만원',(BASE[key],b['cost']/1e4),xytext=(6,-14),textcoords='offset points',fontsize=8)
    if key=='d':
        for dk,lab in ((60/(3600/U['간단']['cycle']+60),'간단 꺾임'),(60/(3600/U['상담']['cycle']+60),'상담 꺾임')):
            ax.axvline(dk,color='#c0392b',ls='--',lw=.8); ax.text(dk,.3,lab,fontsize=7,color='#c0392b',rotation=90,va='bottom')
    ax.set_title(name,fontsize=10); ax.set_xlabel(name.split(' (')[0][2:]+' ('+name.split(' (',1)[1]); ax.set_ylabel('월 원가 (만원 · 기기 1대)')
    FIX={'H':'하루 실사용 6.5h (월 195h)','r':'상담 비율 50%','d':'말 밀도 50%','p':'연결 = 범위 중간(상담 11.45 · 간단 15.5회/h)'}
    if key=='d': FIX['p']='연결 = 그 d 범위의 중간'
    ax.set_ylim(0,None); ax.grid(alpha=.3)
    ax.legend(fontsize=8,loc='upper center',bbox_to_anchor=(0.5,-0.16),ncol=3,title='고정 상수: '+' · '.join(v for k,v in FIX.items() if k!=key),title_fontsize=8)
    pts=[a,BASE[key],z]
    if key=='d':
        pts=sorted(set(pts+[round(60/(3600/U[t]['cycle']+60),4) for t in U]))
    res['sweeps'][key]=dict(name=name,points=[dict(x=x,**month({**BASE,key:x})) for x in pts])
fig.suptitle('독립변인 1개 이동 · 나머지 적정(중간값) 고정 — 월 Soniox 원가와 구성 (마진 없음 · 기기 1대 · 30일)',fontsize=11)
fig.tight_layout(rect=(0,0,1,.96)); fig.savefig(OUT+'price-s3-sweeps.png')
json.dump(res,open(OUT.replace('reference/2026-11-12-interpreter-idea/','orchestration/work/interpreter-idea/price-calc/')+'sec3.json','w'),ensure_ascii=False,indent=1)
f=lambda v:f'{v:,.0f}'
print('base',{k:(f(v) if v>100 else round(v,2)) for k,v in b.items()})
for key,s in res['sweeps'].items():
    for p in s['points']:
        print(key,round(p['x'],3),f(p['cost']),f(p['per_hour']),'k',round(p['k상담'],2),round(p['k간단'],2),'|',' | '.join(f"{f(p[x])}({p[x]/p['cost']*100 if p['cost'] else 0:.0f}%)" for x in PARTS))
