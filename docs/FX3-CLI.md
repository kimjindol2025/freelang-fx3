# FX3 CLI

```text
STATUS=P5_USABLE_GATE
RUNTIME=NONE
SUCCESS=check/lower/ir/cap/test/package verify
EXECUTION=EXISTING_FX_VIA_.fl
```

「쓸 만한」1차 길의 CLI다. 전용 runtime·IR executor·capability 대상 파일 I/O는 없다.

## 실행

```bash
./bin/fx3 --help
python3 tools/fx3_cli.py --help
```

## 종료코드

| code | 의미 |
|------|------|
| 0 | 성공 (cap은 allow) |
| 1 | 검증/판정 실패 (진단 stderr; cap은 deny JSON도 stdout) |
| 2 | 사용법/인자 오류 |

## 명령

| 명령 | 동작 |
|------|------|
| `fx3 check FILE.fx3` | lex+parse → `OK` |
| `fx3 lower FILE.fx3 [--out PATH]` | 결정적 `.fl` |
| `fx3 ir FILE.fx3 [--out PATH]` | 결정적 `fx3-ir@1` JSON |
| `fx3 cap REQUEST.json --canonical-root ROOT` | capability 판정 JSON |
| `fx3 test [--quick] [--legacy-lower]` | 게이트 묶음 |
| `fx3 package verify` | 문서/fixture/스키마 + quick test |

### `cap` 주의

- 디스크에서 **요청 JSON만** 읽는다.
- `--canonical-root`는 서버 고정 root다. 요청의 `root`/`canonical_root`는 deny.
- capability 대상 path를 open/read 하지 않는다.

### `test`

- 기본: lex → parse → lower → ir → capability
- `--quick`: lex → parse → lower
- `--legacy-lower`: `tools/lower.py --check` 추가

## 비범위

- `fx3 run` / 전용 runtime
- IR interpreter
- 실 파일 capability I/O
- self-hosting
