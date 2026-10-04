# App GAP 관측 보강 · 2026-10-04

```text
AGENDA=APP_GAP_OBSERVE
EXPRESS=NO
CORE_CUT=NO
FIXTURE_05=NO
HOT_ALIAS=NO
RUNTIME=NO
CORE_V1_FINAL=PASS
OUTSIDE_CORE_V1=YES
FX_PIN=1d217f5
FL_FILES=9
GAP_SYMBOLS=43
```

## 목적

Core v1이 잠근 **현재 표면 밖**의 FX 앱·템플릿 사용을 **관측만** 갱신한다.  
FX3로 표현·구현하지 않는다. FX 트리는 수정하지 않는다.

## 스캔 범위

FX 트리 `/home/kim/kim/platform/freelang-v11-fx` @ `1d217f5`

- `fx-demo/server.fl`
- `fx-kv/server.fl`
- `fx-queue/server.fl`
- `templates/api-server/server.fl`
- `templates/api-server/test-db.fl`
- `templates/kim-notes/server.fl`
- `templates/kim-short/server.fl`
- `templates/hello/server.fl`
- `templates/hello/test-sqlite.fl`

(이전 APP-GAP 기록 8개 → 이번 **9**개. `fx-queue/server.fl`, `templates/*/test-*.fl` 포함.)

## 가족별 관측

### HTTP / server_*
| 심볼 | 횟수 | 파일 수 |
|------|-----:|-------:|
| `server_json` | 29 | 6 |
| `server_get` | 27 | 7 |
| `server_post` | 11 | 6 |
| `server_html` | 8 | 3 |
| `server_req_param` | 8 | 3 |
| `server_start` | 7 | 7 |
| `server_redirect` | 5 | 2 |
| `fx_server_json` | 4 | 1 |
| `server_req_body` | 4 | 3 |
| `server_status` | 4 | 3 |
| `server_delete` | 2 | 2 |
| `fx_respond` | 1 | 1 |
| `server_ws` | 1 | 1 |


### SQLite
| 심볼 | 횟수 | 파일 수 |
|------|-----:|-------:|
| `fxb_sqlite_exec` | 16 | 3 |
| `fxb_sqlite_query` | 11 | 3 |
| `sqlite_exec` | 6 | 2 |
| `fxb_sqlite_open` | 3 | 3 |
| `sqlite_exec_p` | 3 | 1 |
| `sqlite_query` | 3 | 2 |
| `sqlite_open` | 2 | 2 |
| `sqlite_close` | 1 | 1 |
| `sqlite_one` | 1 | 1 |
| `sqlite_one_p` | 1 | 1 |


### MariaDB
| 심볼 | 횟수 | 파일 수 |
|------|-----:|-------:|
| `mariadb_exec` | 6 | 2 |
| `mariadb_query` | 4 | 3 |
| `mariadb_connect` | 3 | 3 |
| `mariadb_one` | 3 | 2 |
| `mariadb_close` | 1 | 1 |


### JSON
| 심볼 | 횟수 | 파일 수 |
|------|-----:|-------:|
| `json_stringify` | 31 | 7 |
| `json_parse` | 1 | 1 |


### WebSocket
| 심볼 | 횟수 | 파일 수 |
|------|-----:|-------:|
| `ws_send` | 3 | 1 |
| `server_ws` | 1 | 1 |
| `ws_recv` | 1 | 1 |


### form / math
| 심볼 | 횟수 | 파일 수 |
|------|-----:|-------:|
| `form_parse` | 3 | 2 |
| `math_floor` | 1 | 1 |
| `math_random` | 1 | 1 |


### 언어 형태 (fn / try / future …)
| 심볼 | 횟수 | 파일 수 |
|------|-----:|-------:|
| `fn` | 9 | 4 |
| `catch` | 4 | 2 |
| `try` | 4 | 2 |
| `future` | 3 | 2 |


참고: 예전 표의 `loop`/`recur` 특수형은 이번 스캔에서 **호출 헤드로 재현되지 않았다**. `expire-loop` 같은 **이름**만 있다.

## 새로 눈에 띄는 GAP (이전 표 보강)

| GAP | 비고 |
|-----|------|
| `server_html` / `server_redirect` / `server_status` / `server_req_body` / `server_delete` | HTTP 표면 확장 |
| `server_ws` / `ws_send` / `ws_recv` | 웹소켓 |
| `form_parse` | 폼 |
| `math_floor` / `math_random` | 단축 URL |
| `sqlite_*` (비 `fxb_` 접두) | hello/kim-short 테스트·앱 |
| `catch` | `try`와 쌍 |

## 판정

```text
CORPUS_APP=GAP_ONLY
CORPUS_APP_EXPRESS=NO
CORPUS_APP_PURE=fib (기존 유지)
CORE_V1_SCOPE_UNCHANGED=YES
```

상세 원시 표: `scan.tsv`
