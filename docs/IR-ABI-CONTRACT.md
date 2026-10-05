# FX3 IR / ABI Contract

```text
ABI=fx3-ir
VERSION=1
STATUS=LOCKED_SCHEMA
EXECUTOR=NONE
CAPABILITY=NONE
RUNTIME=NONE
PURPOSE=CONTRACT_ONLY
```

기준일: 2026-10-05

이 문서는 **FX3 located AST와 FX backend 사이의 공통 IR/ABI 계약**이다.
이번 단계는 계약을 잠그는 것이다. 실행기·capability·native runtime·CLI·self-hosting은 범위 밖이다.

```text
.fx3 → lexer → AST → IR (이 계약) → (나중) FX backend
                 ↘ .fl lowering (기존 P2, 별층)
```

IR은 `.fl` 텍스트가 아니다. `.fl` lowering과 IR은 같은 Core 의미를 다른 층에서 표현한다.

## 1. 버전

| 필드 | 값 | 규칙 |
|------|----|------|
| `abi` | `"fx3-ir"` | 고정 문자열 |
| `version` | `1` | 정수. 비호환 변경 시 증가 |

알 수 없는 `abi`/`version`은 검증 실패다.

## 2. 직렬화 (deterministic)

- 형식: UTF-8 JSON
- `json.dumps(..., ensure_ascii=False, sort_keys=True, separators=(",", ":"))`
- 객체 키는 사전순. **배열 원소 순서는 소스/AST 순서** (맵 entry 포함)
- 동일 AST → 동일 IR 바이트
- trailing newline 없음 (바이트 비교는 dumps 결과 그대로)

## 3. 위치 (location)

모든 IR 노드는 `loc`를 가진다.

```json
"loc": {"column": 1, "line": 1}
```

- `line` ≥ 1, `column` ≥ 1
- span 확장은 예약: `span` 필드는 VERSION 1에서 선택·미사용. 있으면 `start`/`end` 각각 `loc`와 동일 형태
- 오류 보고는 `loc.line` / `loc.column`을 쓴다

## 4. 루트: Program

```json
{
  "abi": "fx3-ir",
  "version": 1,
  "op": "program",
  "loc": {"column": 1, "line": 1},
  "functions": [ /* Function+ */ ]
}
```

- Core v0/v1 lower 폭과 같이 **함수 1개**를 기본 fixture로 둔다
- 함수 0개는 검증 오류
- 함수 2개 이상은 schema상 허용하되, 현재 Core lower 게이트와 별개다

## 5. Function

```json
{
  "op": "function",
  "name": "handle-rate-single",
  "params": ["$req"],
  "bindings": [ /* Binding* */ ],
  "body": [ /* Expr+ */ ],
  "result": { "op": "result", "value": /* Expr */, "loc": { } },
  "loc": { }
}
```

- `params`: `$` 이름 문자열 배열 (순서 유지)
- `bindings`: leading binding만 (AST와 동일)
- `body`: 본문 식 전부. 길이 ≥ 1
- `result.value`는 **`body`의 마지막 식과 구조적으로 동일**한 트리 (결정적 복제)

## 6. Binding

```json
{
  "op": "binding",
  "name": "$cur",
  "value": /* Expr */,
  "loc": { }
}
```

## 7. 식 (Expr) 노드

| `op` | 필드 | 의미 |
|------|------|------|
| `variable` | `name` | `$x` |
| `literal` | `kind`: `number` \| `string` \| `symbol`, `text` | 숫자 토큰 / 문자열 토큰(따옴표 포함) / 심볼 이름 |
| `call` | `name`, `args` | 일반 호출. builtin 이름 해석은 backend 몫 |
| `operator` | `name`, `left`, `right` | `+ - * / == != > < >= <=` |
| `conditional` | `cond`, `then`, `else` | `?cond{then}{else}` |
| `null_check` | `value` | `~primary` → FX `(null? …)` 대응 |
| `get` | `target`, `key` | `@` 경로 / 인덱스 → FX `(get …)` 대응 |
| `map` | `entries` | 맵. entry 순서 = 소스 순서 |
| `map_entry` | `key`, `value` | `key`는 문자열 리터럴 형태 (`"ok"`) |
| `result` | `value` | 함수 결과. function.result 전용 |

## 8. 값 타입 (논리)

VERSION 1 논리 타입 (런타임 태그 아님):

```text
number | string | symbol | boolean-as-symbol | null-as-runtime
map | list(RESERVED) | function-value(RESERVED)
```

- `true`/`false`는 Core 표면에서 심볼로 내려가므로 IR `literal.kind=symbol`
- 배열 리터럴 IR `op=list`는 **RESERVED**. 출현 시 `E_UNSUPPORTED_NODE`
- capability / error / process 노드는 schema에만 이름을 예약하고 VERSION 1 생성기는 방출하지 않는다

## 9. 예약·미구현 op (생성 금지)

```text
list
capability_request
error
array
loop
fn
```

AST나 수동 IR에 나타나면 `E_UNSUPPORTED_NODE` + loc.

## 10. 검증 규칙 (요약)

1. `abi`/`version`/`op`/`loc` 필수
2. 모든 노드 `loc.line`/`loc.column` ≥ 1
3. 허용 `op`만
4. function: `body` 비어 있지 않음, `result.value` ≡ `body[-1]` (JSON 동등)
5. map `entries`는 `map_entry`만
6. 알 수 없는 필드 키는 VERSION 1에서 거부 (결정적 스키마)

## 11. AST → IR 매핑

| AST kind | IR op |
|----------|-------|
| module | program |
| defn | function |
| binding | binding |
| var | variable |
| num | literal number |
| str | literal string |
| sym | literal symbol |
| call | call |
| op | operator |
| if | conditional |
| null? | null_check |
| get | get |
| map | map |
| pair | map_entry |
| body | function.bindings + function.body + function.result |
| (기타) | E_UNSUPPORTED_NODE |

## 12. 비범위

- IR 실행
- capability 허용/거부 실행
- FX native ELF
- `fx3` CLI
- self-hosting
- Core 문법 변경
- `tools/lower.py` 변경

## 13. 게이트

```bash
python3 tools/check_ir.py
```

PASS 조건: schema validate · golden fixture IR byte-match · determinism · location · unsupported reject.
