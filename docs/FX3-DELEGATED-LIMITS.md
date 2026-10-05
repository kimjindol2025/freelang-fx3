# FX3 위임 경로 · 알려진 한계

```text
RUNTIME_OWNED=NONE
RUN=DELEGATED
DOC=LOCKED_FRICTION
```

이 문서는 **전용 VM을 만들지 않은 채** `.fx3` → `fx3_lower` → eval/native 로
작은 도구를 돌릴 때 반복해서 만나는 경계를 고정한다.
새 Core 문법을 마음대로 열지 않는다. 한계를 숨기지 않는다.

## 레이아웃 (POC 레일)

```text
src/<tool>.fx3                 # 업무 로직 본체 (단일 top-level F)
poc/<tool>/poc.json            # source / pass_tag / min_cases
poc/<tool>/fixtures/*.call
poc/<tool>/fixtures/*.expect.json
poc/<tool>/fixtures/*.meta.json
poc/<tool>/scripts/verify.sh   # → python3 tools/check_poc.py
```

검증:

```bash
python3 tools/check_poc.py all
# 또는
bash poc/<tool>/scripts/verify.sh
```

## 문법·lowering 마찰

| 한계 | 현상 | 실무 대응 |
|------|------|-----------|
| 단일 top-level `F` | `fx3_lower`가 F 둘 이상이면 `E_UNSUPPORTED_NODE` | 헬퍼를 인라인·중첩 조건으로 |
| `?` 분기에 바인딩 불가 | 분기 `{yes}/{no}`는 단일 식 | 선두 `$x=...;` let만 사용 |
| `string?` / `vector?` 표면 | `?` 토큰이 if와 충돌 | `type-of($x)=="string"` 등 |
| empty map lower | Core lower가 빈 `{}` 거부 | 결과 맵에 키를 항상 둠 |
| FX3 `==` vs native `=` | 내린 `.fl`의 `(==` 는 CGC가 모름 | `fx3 run --engine=native`가 `(=` 로 적응 |

## 실행·CLI 마찰

| 한계 | 현상 | 실무 대응 |
|------|------|-----------|
| eval 부분집합 | `eval_fl_min`에 `keys`/`length`/`type-of` 없음 | `eval_fl_ext` 심 (min 파일 미수정) |
| `--call` 맵 키 | bare `name`은 eval에선 심볼→문자열, native 원문은 깨짐 | CLI가 native용 문자열 키로 재방출 |
| 버전 문자열 비교 | `>=`/`<`는 사전식 | 단일 자릿수 세그먼트 또는 문서화된 구간 |
| 임의 길이 루프 없음 | 배열·키 순회를 일반 for로 못 씀 | 고정 상한 언롤 / 작은 스키마 |
| I/O 금지 | 파일·네트워크·process 없음 | 순수 검증/변환만 |

## 의도적으로 열지 않는 것

- 전용 FX3 VM / IR executor
- capability 실 파일 I/O
- self-hosting
- Core 문법 임의 확장·golden 기대값 완화
- `eval_fl_min.py` 본문 수정

## 관련 문서

- [FX3-RUN.md](FX3-RUN.md) — 위임 run 계약
- [FX3-CLI.md](FX3-CLI.md) — CLI
- [poc/README.md](../poc/README.md) — POC 추가 방법
