# FX3 CLI

```text
STATUS=P5_USABLE_GATE_PLUS_DELEGATED_RUN
RUNTIME_OWNED=NONE
RUN=DELEGATED
RUN_ENGINE_DEFAULT=eval
SUCCESS=check/lower/ir/cap/run/test/package verify
EXECUTION=DELEGATED_EVAL_OR_NATIVE
```

「쓸 만한」CLI다. 전용 FX3 VM·IR executor·capability 대상 파일 I/O는 없다.
실행은 위임: [FX3-RUN.md](FX3-RUN.md).

## 실행

```bash
./bin/fx3 --help
python3 tools/fx3_cli.py --help
```

## 종료코드

| code | 의미 |
|------|------|
| 0 | 성공 (cap은 allow; run은 실행 성공) |
| 1 | 검증/판정/실행 실패 (진단 stderr; cap은 deny JSON도 stdout) |
| 2 | 사용법/인자 오류 / native BLOCKED / 잘못된 engine |

## 명령

| 명령 | 동작 |
|------|------|
| `fx3 check FILE.fx3` | lex+parse → `OK` |
| `fx3 lower FILE.fx3 [--out PATH]` | 결정적 `.fl` |
| `fx3 ir FILE.fx3 [--out PATH]` | 결정적 `fx3-ir@1` JSON |
| `fx3 cap REQUEST.json --canonical-root ROOT` | capability 판정 JSON |
| `fx3 run FILE.fx3 --call '(fn args…)' [--engine=eval\|native]` | lower 후 위임 실행 |
| `fx3 test [--quick] [--legacy-lower]` | 게이트 묶음 |
| `fx3 package verify` | 문서/fixture/스키마 + quick test |

### `run`

- Lower 정본: `fx3_lower` (AST). `tools/lower.py` 미사용.
- 기본 엔진 `eval` → `tools/eval_fl_min.py`.
- `--engine=native` → `FX_ROOT/fl-build.sh --no-net`. 없으면 stderr `FX_NATIVE=BLOCKED`, exit 2.
- `--call` 필수. capability 판정은 자동으로 켜지지 않음.
- 스모크: `fixtures/run/sum.fx3` + `--call '(sum 2 3)'` → `5`.

### `cap` 주의

- 디스크에서 **요청 JSON만** 읽는다.
- `--canonical-root`는 서버 고정 root다. 요청의 `root`/`canonical_root`는 deny.
- capability 대상 path를 open/read 하지 않는다.

### `test`

- 기본: lex → parse → lower → ir → capability
- `--quick`: lex → parse → lower
- `--legacy-lower`: `tools/lower.py --check` 추가
- `run`은 `test`에 넣지 않는다 (`check_cli`만).

## 비범위

- 전용 FX3 runtime / owned VM
- IR interpreter
- 실 파일 capability I/O
- self-hosting
