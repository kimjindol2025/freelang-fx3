# FX3 코퍼스 (좁은 폭)

```text
AGENDA=CORPUS_STDLIB_SLICE
FX_TREE=/home/kim/kim/platform/freelang-v11-fx
FX_PIN=202c998
COPY_RUNTIME=NO
FIXTURE_05=NO
```

로드맵 5–6의 **첫 조각**이다. FX 트리를 수정하지 않는다. 참조 `.fl`은 여기로만 복사한다.

## 포함 (stdlib)

| 이름 | 출처 | `.fx3` | 비고 |
|------|------|--------|------|
| identity | `fx-std.fl` | `stdlib/identity.fx3` | Core 최소 |
| req-body | `fx-std.fl` | `stdlib/req-body.fx3` | `@$req.body` |
| str-coerce | `fx-std.fl` | `stdlib/str-coerce.fx3` | `?~` + `str` |

## app GAP (표현 없음)

표: [APP-GAP.md](APP-GAP.md) · `CORPUS_APP=GAP_ONLY`

## 아직 아님

- **app 표현**: `server_json`, `mariadb_*`, 라우트 등 — GAP만
- **self-host**: `self/cgc-main.fl` — 가져오지 않음
- fixture 05 추가 금지 (`NO_FIXTURE_05`)

## 검사

```bash
python3 tools/check_corpus.py
```

PASS 줄: `CORPUS_STDLIB=PASS`. app는 `GAP_ONLY`, self-host는 `NOT_STARTED`.
