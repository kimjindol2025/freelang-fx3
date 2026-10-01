# App 코퍼스 GAP 표

```text
AGENDA=CORPUS_APP_GAP
EXPRESS=NO
CORE_V0_GATE=NO
FX_TREE=/home/kim/kim/platform/freelang-v11-fx
FX_PIN=202c998
DATE=2026-10-01
```

app·템플릿 `.fl`을 FX3로 **표현하지 않는다.** Core 밖 기능을 GAP으로만 고정한다.  
이 표를 읽었다고 Core v0를 닫지 않는다 ([CORE-V0-PREP.md](../CORE-V0-PREP.md)).

## 조사 범위

| 경로 | 역할 |
|------|------|
| `fx-demo/server.fl` | 데모 앱 |
| `fx-kv/server.fl` | KV 서비스 |
| `templates/api-server/` | API 템플릿 |
| `templates/kim-notes/` | 노트 템플릿 |
| `templates/kim-short/` | 단축 URL |
| `templates/hello/` | 헬로 |

(스캔일 기준 `.fl` 8개. FX 트리는 수정하지 않음.)

## GAP (Core 표면 밖)

| GAP | 출현 예 | Core 조치 |
|-----|---------|-----------|
| `server_json` / `fx_server_json` | fx-demo, fx-kv, api-server, kim-notes, hello | 표현 금지. 별칭·builtin 경쟁 전 |
| `server_get` / `server_post` / `server_start` / `server_req_param` | 위 앱·템플릿 라우트 | 표현 금지 |
| `mariadb_*` | api-server, kim-notes | 표현 금지 |
| `fxb_sqlite_*` / sqlite 헬퍼 | fx-demo, fx-kv, hello, kim-short | 표현 금지 |
| `json_stringify` / `json_try_parse` | 다수 | 이름 그대로 호출은 이론상 가능하나 앱 묶음 미착수 |
| `(fn …)` 클로저 | fx-kv, kim-notes, kim-short | v0 미확정 |
| `loop` / `recur` | fx-kv | v0 미확정 |
| `try` | fx-kv | v0 미확정 |
| `future` | fx-kv | v0 미확정 |

## Core에 들어올 수 있는 것 (이번엔 추가하지 않음)

순수 `get` / `if` / `null?` / 산술만 쓰는 **작은 헬퍼**가 앱 안에 섞여 있어도, app 코퍼스 PASS로 올리지 않는다. stdlib 조각(`CORPUS_STDLIB=PASS`)이 그 역할을 한다.

## 판정 줄

```text
CORPUS_APP=GAP_ONLY
CORPUS_APP_EXPRESS=NO
CORPUS_SELFHOST=NOT_STARTED
```

다음으로 표현을 열려면 Core 표면 안의 순수 함수만 최소 폭으로 고르고, 이 GAP 표를 먼저 갱신한다.
