# FX3 위임 실행 (`fx3 run`)

```text
RUN=DELEGATED
RUN_ENGINE_DEFAULT=eval
RUN_ENGINE_NATIVE=OPTIONAL
RUNTIME_OWNED=NONE
```

FX3는 전용 VM을 갖지 않는다. `fx3 run`은 Core를 **AST lower → `.fl` → 기존 실행 경로**로 위임한다.

## 모델

```text
.fx3
  │  fx3_lower (AST 경로; tools/lower.py 미사용)
  ▼
.fl
  ├── --engine=eval   (기본) → tools/eval_fl_min.py  (Core 부분집합)
  └── --engine=native        → freelang-v11-fx/fl-build.sh --no-net → ELF
```

## 규칙

1. 위임만. 새 bytecode VM·IR interpreter 금지.
2. Lower 정본은 `fx3_lower`. `tools/lower.py`는 회귀용만.
3. `--call '(name args…)'` 필수 (FX S-expr). 생략 시 exit 2.
4. native는 항상 `--no-net`. eval은 네트워크 builtin 없음.
5. run은 capability 판정을 자동으로 켜지 않는다. cap은 `fx3 cap`.
6. 층 분리: lower FAIL ≠ run FAIL ≠ native BLOCKED.
7. Core 문법·golden `.fl` 임의 변경 금지.

## 엔진

| 엔진 | 경로 | 없을 때 |
|------|------|---------|
| `eval` (기본) | `tools/eval_fl_ext.py` (over `eval_fl_min`; adds `keys`/`length`/`type-of`/`str_length`, safe vector get). `eval_fl_min.py` 파일은 수정하지 않음 | — (repo 내) |
| `native` | `$FX_ROOT/fl-build.sh` (기본 `/home/kim/kim/platform/freelang-v11-fx`). CLI adapts lowered `(==` → `(=` and emits string map keys for `--call` | stderr `FX_NATIVE=BLOCKED`, exit 2 |

## 사용

```bash
./bin/fx3 run FILE.fx3 --call '(sum 2 3)'
./bin/fx3 run FILE.fx3 --call '(sum 2 3)' --engine=eval
./bin/fx3 run FILE.fx3 --call '(sum 2 3)' --engine=native
```

eval 성공 시 stdout에 결과 한 줄 (JSON이면 `sort_keys` compact).
native 성공 시 ELF stdout 마지막 줄을 같은 JSON 규약으로 정규화할 수 있다.

실사용 POC: [poc/manifest-validator/README.md](../poc/manifest-validator/README.md).

## 종료코드

| code | 의미 |
|------|------|
| 0 | 실행 성공 |
| 1 | parse/lower 실패 또는 실행 의미 오류 |
| 2 | 사용법 / 잘못된 `--engine` / native 도구 없음(BLOCKED) |

## 비범위 (이번 계약)

- FX3 전용 runtime 소스 트리
- IR 실행기
- capability 실 파일 read/write
- `runtime.execute` allow
- self-hosting

상세 CLI: [FX3-CLI.md](FX3-CLI.md).
