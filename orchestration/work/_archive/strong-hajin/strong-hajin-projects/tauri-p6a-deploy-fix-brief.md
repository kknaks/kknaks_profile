# Phase 6a 설계 보정

대상 `tauri-deploy-design.md` 한 파일만 수정한다.

검수 F-1·W-1~W-5를 반영한다.

1. §3-1 수치를 게이트 안 159개로 정정하고, 게이트 밖은 `/health` 하나(`http.py:2530`)이며 `/api/*`·WS는 전부 게이트 안이라고 쓴다.
2. §4-2 또는 §7 I-1에 liveness/readiness probe 기본 경로 `/health`를 추가한다.
3. §5-1 및 §7에 Strong Hajin용 `argocd/applications/datastores-strong-hajin.yaml`, `charts/datastores/values-strong-hajin.yaml` 산출물을 추가한다. 기존 Mediness 파일은 수정하지 않는다.
4. 좌표 F-6, F-13, App.tsx를 실제 행으로 보정한다.
5. §5 제목의 다섯/여덟 불일치를 고치고, 딥링크 예시를 `?interaction=`로 정정하며, F-2 소유 표기에 Phase8 기본·6b 코디 판단을 명시한다.

사실/사용자 결정·도메인 placeholder·P-5는 유지한다. 제품 코드·인프라 레포·SPEC·WORK는 수정하지 않는다. 검증 후 worker_done.
