"""워커 부팅부 — 무출력 상한 덮어쓰기 (KDEV-WORK-017 결함 ①).

`app/worker/run.py` 는 back 패키지 밖이라 import 경로에 없다. 파일 경로로 싣는다.
컨테이너가 다르다고 검증을 빼면, 이 덮어쓰기가 조용히 죽어도 **잔디가 다시 안 도는
것으로만** 드러난다 — 그 실패는 원인에 닿기까지 오래 걸린다.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

WORKER_RUN = Path(__file__).resolve().parents[2] / "worker" / "run.py"


def _load_run():
    """`app/worker/run.py` 를 모듈로 싣는다. 부작용은 없다 — `main()` 은 안 부른다."""
    spec = importlib.util.spec_from_file_location("worker_run", WORKER_RUN)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def run_module():
    module = _load_run()
    original = module.okk_executor.IDLE_TIMEOUT
    yield module
    # 같은 프로세스의 다른 테스트에 새 상한이 새어 나가면 안 된다.
    module.okk_executor.IDLE_TIMEOUT = original
    sys.modules.pop("worker_run", None)


class TestApplyIdleTimeout:
    def test_default_raises_the_ceiling_well_past_the_okk_default(self, run_module):
        """기본값이 실제로 open-kknaks 상수를 덮는다.

        30 이 그대로면 `daily` 가 첫 토큰 전에 끊긴다 — 이 발주를 막았던 그 실패다.
        """
        applied = run_module.apply_idle_timeout(env={})
        assert applied == 180
        assert run_module.okk_executor.IDLE_TIMEOUT == 180

    def test_env_overrides_the_default(self, run_module):
        assert run_module.apply_idle_timeout(env={"IDLE_TIMEOUT_SEC": "240"}) == 240
        assert run_module.okk_executor.IDLE_TIMEOUT == 240

    def test_garbage_env_falls_back_instead_of_crashing_the_worker(self, run_module):
        """오타 하나로 워커가 통째로 안 뜨는 것보다 기본값으로 도는 편이 낫다."""
        assert run_module.apply_idle_timeout(env={"IDLE_TIMEOUT_SEC": "잘못"}) == 180
        assert run_module.okk_executor.IDLE_TIMEOUT == 180

    def test_missing_constant_fails_loud(self, run_module, monkeypatch):
        """open-kknaks 가 올라가며 상수가 사라지면 **부팅에서 죽는다.**

        조용히 넘어가면 상한이 30초로 되돌아가고, 그 사실은 잔디가 안 도는 것으로만
        드러난다. 이 가드가 없으면 다음 버전 bump 가 결함 ① 을 그대로 되살린다.
        """
        monkeypatch.delattr(run_module.okk_executor, "IDLE_TIMEOUT")
        with pytest.raises(RuntimeError, match="IDLE_TIMEOUT"):
            run_module.apply_idle_timeout(env={})


class TestInstalledContract:
    def test_executor_still_reads_the_constant_at_runtime(self):
        """설치된 open-kknaks 가 여전히 **루프 안에서** 그 전역을 읽는지.

        기본인자로 캡처하거나 `__init__` 에서 복사하도록 바뀌면 부팅 시점 대입이
        아무 효과가 없다. 덮어쓰기가 성립하는 근거 자체를 지킨다.
        """
        import inspect

        from open_kknaks.worker.executor import ClaudeCodeExecutor

        source = inspect.getsource(ClaudeCodeExecutor._read_pty_output)
        assert "IDLE_TIMEOUT" in source, (
            "executor 가 IDLE_TIMEOUT 을 읽지 않는다 — 무출력 상한 계약이 바뀌었다. "
            "app/worker/run.py 의 apply_idle_timeout 을 새 계약에 맞춰 고쳐야 한다."
        )
