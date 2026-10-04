# App 코퍼스 GAP 표

```text
AGENDA=CORPUS_APP_GAP
EXPRESS=NO
CORE_V0_GATE=NO
CORE_V1_GATE=NO
OUTSIDE_CORE_V1=YES
FX_TREE=/home/kim/kim/platform/freelang-v11-fx
FX_PIN=1d217f5
DATE=2026-10-04
OBSERVE=bench/results/app-gap-observe-20261004/
```

app·템플릿 `.fl`을 FX3로 **표현하지 않는다.** Core 밖 기능을 GAP으로만 고정한다.  
Core v1(`CORE_V1_FINAL=PASS`)이 잠근 것은 **현재 표면**뿐이다. 이 표의 GAP은 계속 **OUTSIDE**다.  
FX 트리는 수정하지 않는다.

## 조사 범위

| 경로 | 역할 |
|------|------|
| `fx-demo/server.fl` | 데모 앱 |
| `fx-kv/server.fl` | KV 서비스 |
| `fx-queue/server.fl` | 큐 서비스 (이번 관측 포함) |
| `templates/api-server/` | API 템플릿 (+ `test-db.fl`) |
| `templates/kim-notes/` | 노트 템플릿 |
| `templates/kim-short/` | 단축 URL |
| `templates/hello/` | 헬로 (+ `test-sqlite.fl`) |

스캔 @ `1d217f5`: **`.fl` 9개**. 증거: [bench/results/app-gap-observe-20261004/](../bench/results/app-gap-observe-20261004/).

## GAP (Core 표면 밖)

| GAP | 출현 예 | Core 조치 |
|-----|---------|-----------|
| `server_json` / `fx_server_json` | fx-demo, fx-kv, fx-queue, api-server, kim-notes, kim-short, hello | 표현 금지 |
| `server_get` / `server_post` / `server_start` / `server_req_param` | 위 + demo/kv/queue | 표현 금지 |
| `server_html` / `server_redirect` / `server_status` / `server_req_body` / `server_delete` | notes/short/api/hello/queue | 표현 금지 (2026-10-04 보강) |
| `server_ws` / `ws_send` / `ws_recv` | fx-queue | 표현 금지 (신규 관측) |
| `mariadb_*` | api-server, kim-notes | 표현 금지 |
| `fxb_sqlite_*` / `sqlite_*` | demo/kv/queue · hello/short 테스트 | 표현 금지 |
| `json_stringify` / `json_parse` | 다수 | 앱 묶음 표현 금지 (관측만) |
| `form_parse` | kim-notes, kim-short | 표현 금지 |
| `math_floor` / `math_random` | kim-short | 표현 금지 |
| `(fn …)` 클로저 | fx-kv, fx-queue, kim-notes, kim-short | Core v1 밖 |
| `try` / `catch` | fx-kv, fx-queue | Core v1 밖 |
| `future` | fx-kv, fx-queue | Core v1 밖 |

`loop`/`recur` **특수형**은 이번 스캔에서 호출 헤드로 재현되지 않았다 (`expire-loop` 등 이름만 존재).

원시 심볼 표: `bench/results/app-gap-observe-20261004/scan.tsv` (GAP 심볼 43).

## Core 안 순수 헬퍼 (최소 폭으로만)

GAP 표를 유지한 채, Core `get`/`if`/`null?`/산술·호출만 쓰는 헬퍼를 `corpus/app/`에 둔다.  
`server_json` / `mariadb` / `fn` / `loop` 는 여전히 넣지 않는다.

| 이름 | 출처 | 상태 |
|------|------|------|
| fib | `fx-queue/server.fl` | `corpus/app/fib.fx3` · lower/semantic 검사 |

## stdlib 추가 (Core 안 · GAP 아님)

`fx-std.fl`에서 get만 쓰는 헬퍼를 `corpus/stdlib`에 더한다. app 표현이 아니다.

| 이름 | 출처 | 상태 |
|------|------|------|
| req-param | `fx-std.fl` | `corpus/stdlib/req-param.fx3` |
| req-query | `fx-std.fl` | `corpus/stdlib/req-query.fx3` |
| get-or | `fx-std.fl` | `corpus/stdlib/get-or.fx3` (null?-get 동등형; let 없음) |
| nested-get | `fx-std.fl` get-in-2 Core 동등 | `corpus/stdlib/nested-get.fx3` (이름 `get-in-2`는 하이픈+숫자로 lower 불가) |
| get-in-or | Core 확장 (null-safe 2단) | `corpus/stdlib/get-in-or.fx3` (`?~` + nested get + default) |

스킵(관찰만): `first-or`(빈 get IndexError), `last-item`(length), `result-ok?`(`?` 이름), `blank?`(trim), `safe-int`(let), 원본 `get-in-2`(`json_safe_get`).

## 좁은 표현 (APP_GAP_NARROW_01)

전면 이식 없이 **json** 가족만 최소 표현:

| 예제 | 내용 | 검증 |
|------|------|------|
| `corpus/app-gap/json-ok-obj` | `json_stringify({ok:true})` → FX `json_stringify` 형태 | lower≡ref PASS |

`server_*` / `sqlite` / `mariadb` / `fn` / `loop` 는 여전히 표현하지 않는다.  
증거: [bench/results/app-gap-narrow-01-20261004/](../bench/results/app-gap-narrow-01-20261004/)

## 판정 줄

```text
CORPUS_APP=GAP_ONLY
CORPUS_APP_PURE=fib
CORPUS_APP_EXPRESS=NARROW_JSON_ONLY
CORPUS_APP_GAP_NARROW=PASS
CORPUS_SELFHOST=NOT_STARTED
OUTSIDE_CORE_V1=YES
OBSERVE_2026_10_04=PASS
APP_GAP_NARROW_01=PASS
```
