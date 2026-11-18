# stg 반입 절차서 — 데이터 메달리온 gold (사용자가 VM 에서 직접)

근거: SPEC-003 0.2.0 §11 · `research-stg-seed.md` · 코드 검수 `review-code-hub-stg.md`(C-1 · C-2). 값은 자리표시 — 실제 호스트 · 접속 값은 여기 적지 않는다.
허브 PR: #32(release/v1.2.0 머지 aa46a86) · stg 승격 PR #34(`kknaksss/promote-stg-gold` — 트리 = release 그대로).

## ⓪ 머지 전 (VM · 지금)

```bash
# 1) DB 백업(문서 관례 — deployment.md)
# 2) 지금 상태 기록
sudo docker inspect --format '{{.Config.Image}} {{.State.StartedAt}}' procedure-hub
# 3) env 파일에 세 줄 더함 (docker restart 는 env 를 다시 안 읽음 → CD 가 컨테이너를 새로 만들기 전에)
sudo vi /opt/procedure-hub/config/stg.env
#   GOLD_REPOSITORY=db
#   GOLD_MCP_ALLOWED_HOSTS=<Gateway 공개 호스트>      # 없으면 MCP 가 421
#   GOLD_LOAD_TIMEOUT_SECONDS=30                       # (선택) 기본 60 · CD 확인 창 ~100초 — 로컬 적재 0.5초
```

→ 코디에게 「env 넣음」 알림 → 코디가 PR #34 머지 → CD(verify · 빌드 · deploy.sh · Gateway health · products).

## ① CD 뒤 확인 (gold 는 아직 꺼짐이 정상)

```bash
curl -fsS http://127.0.0.1:10000/procedure-hub/health            # 200 (기존 그대로)
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:10000/procedure-hub/gold/health   # 503 (F2 — 적재 전)
sudo docker exec procedure-hub .venv/bin/alembic current          # b202611170002 (head)
IMG=$(sudo docker inspect --format '{{.Config.Image}}' procedure-hub)   # :stg-<sha>
```

## ② 데이터 올리기 (레포 같은 커밋의 data/medallion · assets/procedure-images)

```bash
D=/opt/procedure-hub/import/$(date +%Y%m%d)-medallion
sudo mkdir -p $D
# 로컬에서 Bastion 경유로 복사: <레포>/data/medallion → $D/data/medallion · <레포>/assets/procedure-images → $D/procedure-images
```

## ③ dry-run (DB 쓰기 0)

```bash
sudo docker run --rm --env-file /opt/procedure-hub/config/stg.env \
  -v $D/data/medallion:/data/medallion:ro \
  -v $D/procedure-images:/images:ro -e GOLD_IMAGE_DIR=/images \
  -e GOLD_EXPECTED_HASH=8accbb213ac5327d8675f8156bc57d87c12a3245c383c8239074444da7f6228c \
  --entrypoint .venv/bin/python $IMG scripts/load_medallion.py --dry-run
# 기대: exit 0 · 표 76 · 행 130,446 · gold_hash 8accbb21… · aux_hash 93ec89fd… · image_files 103 checked
```

**멈출 곳**: exit 2(입력 · 검사 거부) → 출력 그대로 코디에게.

## ④ 적재 (한 트랜잭션 · 실패하면 롤백 · 앞 판 그대로)

같은 명령에서 `--dry-run` 만 뺀다. 기대: exit 0 · `loaded tables 76 · rows 130446`. exit 3 → 롤백됨 · 출력 그대로 코디에게. **alembic downgrade 는 쓰지 않는다.**

## ⑤ 켜기

```bash
sudo docker restart procedure-hub
# 켜짐 판정은 gold/health 200 (로그만 보지 않는다 — 검수 C-2)
curl -fsS http://127.0.0.1:10000/procedure-hub/gold/health | head -c 400   # build.gold_hash 8accbb21… · aux_hash 93ec89fd…
curl -fsS http://127.0.0.1:10000/procedure-hub/health                         # 200 그대로
sudo docker stats --no-stream procedure-hub                                   # 메모리 기록 (로컬 기준 gold +약 125MB)
```

**멈출 곳**: gold/health 503 이 계속이면 `sudo docker logs --tail 100 procedure-hub | grep "gold off"` 의 이유(F 코드)만 코디에게. 메모리가 VM 한도에 가까우면 끄기(아래) 먼저.

## ⑥ Gateway 경유 확인

- REST: `GET https://<Gateway>/procedure-hub/gold/resolve?text=턱살` → CON-168
- MCP: `https://<Gateway>/procedure-hub/gold-mcp/mcp` tools/list 9 (421 이면 `GOLD_MCP_ALLOWED_HOSTS` 확인 → env 고친 뒤 컨테이너 새로 만들기)

## 끄기 (gold 만 되돌리기)

`stg.env` 에서 `GOLD_REPOSITORY` 줄을 빼고 컨테이너를 새로 만든다(deploy.sh) → gold 꺼짐 · 기존 허브 그대로 · 표 · 데이터는 둔다.

## 실행 기록 (2026-11-18 · 코디가 Bastion 경유로 직접)

- 백업: `/opt/procedure-hub/backup/stg-pre-medallion-20261118.dump`(custom · 168 표) · `stg.env.pre-medallion-20261118`
- **MCP 허용 호스트**: Gateway 는 Host 를 VM 내부 주소(`<VM 내부 IP>:10000`)로 넘긴다 — 공개 호스트만 두면 421. 두 값을 모두 둔다. 확인 = `docker logs | grep "Invalid Host header"`.
- env 를 고친 뒤 컨테이너 재생성 = Bastion 에서 `./deploy.sh procedure-hub stg`(`docker restart` 아님).
- 적재 6.3초 · 재시작 뒤 health 약 8초 · 컨테이너 메모리 154MB → 225MB · VM 여유 약 210MB(전체 891MB · swap 0).
