# stdlib helper +1 · result-val-or

```text
AGENDA=STDLIB_HELPER_PLUS1
HELPER=result-val-or
FN_LOOP=NO
APP_GAP=NO
FIXTURE_05=NO
HOT_ALIAS=NO
RUNTIME=NO
CORE_V1_FINAL=PASS
```

## 안건

Core v1 잠금 안의 기존 표면만 써서 헬퍼 하나와 코퍼스 쌍만 추가한다.

## 선택

| 헬퍼 | 출처 | Core 대응 |
|------|------|-----------|
| **result-val-or** | `fx-std.fl` | `get` / `null?` / `if`만. `result-ok?` 이름(`?`) 미사용 |

```text
F result-val-or[$r,$d]{?~(get($r,1)){get($r,0)}{$d}}
```

Result 벡터 `[$v $err]`에서 에러 칸이 null이면 값을, 아니면 기본값을 돌려준다.

## 검증

```bash
python3 tools/check_corpus.py
# PASS result-val-or lower~ref · semantic_min · native
```

추가: 실패 경로 `[[null,"boom"],9] → 9` eval PASS.

## 열지 않음

`fn`/`loop` · app GAP · fixture 05 · Hot Alias · 전용 런타임

## 한 줄

```text
STDLIB_HELPER_PLUS1=PASS
HELPER=result-val-or
```
