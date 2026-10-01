# Core v0 준비 체크리스트

```text
DOC=CORE_V0_PREP
CORE_V0_FINAL=NOT_YET
DECLARE=FORBIDDEN
DATE=2026-10-01
```

이 문서는 **확정 선언이 아니다.** Core v0를 닫기 전에 무엇이 PASS인지·무엇이 남았는지·무엇을 열지 않는지만 고정한다.  
PLAN 8 / 로드맵 8에 도달하기 전에는 `CORE_V0_FINAL=PASS`를 쓰지 않는다.

## 이미 잠긴 것 (다시 열지 않음)

| 항목 | 상태 | 재현 |
|------|------|------|
| Core 밀도·이름 보존 | LOCKED | [CORE.md](CORE.md) |
| Lowering 계약 | LOCKED | [LOWERING_CONTRACT.md](LOWERING_CONTRACT.md) |
| fixture 01–04 golden 바이트 | PASS | `python3 tools/lower.py --check` |
| 식 뒤 바인딩 거부 | PASS | lowerer |
| delimiter / `$a-$b` 하이픈 | PASS | `python3 tools/check_delimiter.py` |
| AI 사용 바닥 (U1/U2/U3·weak·ops) | FLOOR PASS | bench/results/* |
| semantic_min | PASS | `python3 tools/check_semantic_min.py` |
| native FX ELF (좁은 산술) | PASS | `bash tools/check_semantic_native.sh` |
| stdlib 코퍼스 조각 | PASS | `python3 tools/check_corpus.py` |
| AI-ENTRY / 방언 | LOCKED | [AI-ENTRY.md](AI-ENTRY.md), [DIALECT-FX3-CORE.md](DIALECT-FX3-CORE.md) |
| 성공 정의 | LOCKED | [AI-USE-SUCCESS.md](AI-USE-SUCCESS.md) |

## Core v0를 닫으려면 필요한 PASS (아직 전부는 아님)

확정 직전에 아래가 **모두** 기록되어야 한다. 하나라도 없으면 `CORE_V0_FINAL=NOT_YET`를 유지한다.

1. **문법·내리기** — fixture 01–04 + delimiter 회귀 유지 (`lower.py --check`, `check_delimiter.py`)
2. **의미** — Core 부분집합에 대해 min + native 재현 (`check_semantic_min.py`, `check_semantic_native.sh`)
3. **코퍼스** — stdlib 조각 유지 + app/self-host는 **GAP으로 명시**되거나 Core 표면 안으로 들어온 표본만 PASS
4. **AI 사용** — U1·U2·U3 바닥이 회귀로 깨지지 않음 (ENTRY 바이트 불변 원칙)
5. **세 사용자** — Core v0 닫기에 대한 표 (PLAN 채택·확정은 별 안건). 지피티 표가 비어 있으면 닫지 않음
6. **금지 준수** — 아래 「열지 않는 것」을 어긴 커밋이 없어야 함

## 의도적 GAP (Core v0 관문으로 올리지 않음)

보류·밖 기능을 읽기 테스트했다고 해서 Core v0를 닫지 않는다 ([PLAN.md](PLAN.md) 그록 수정).

| GAP | 이유 |
|-----|------|
| 동적 인덱스 / 반복 `?~` | 관찰만. 관문 아님 |
| `fn` / 클로저 | FX에 있으나 v0 표면 미확정 |
| `loop` / `recur` / `try` | 미확정 |
| `server_json` / `mariadb_*` / 라우트 | app 코퍼스 밖 |
| self-host / CGC 소스 | FX3로 가져오지 않음 |
| Hot Alias (`U`/`J` 등) | 후보만. Core 밀도 변경 금지 |
| fixture 05 | `NO_FIXTURE_05` |
| 표면 전용 런타임 | 금지 |
| FX2 import | 금지 |

app 코퍼스: `CORPUS_APP=NOT_STARTED` — 표현 시도 전에 GAP 표만 유지해도 된다.

## 열지 않는 것 (이 문서가 열려 있는 동안)

- `CORE_V0_FINAL=PASS` 또는 “Core v0 확정” 문구를 STATUS에 넣는 것
- fixture 05·축약어 채택·새 방언
- FX 런타임/앱을 이 저장소로 복사
- 보류 표면을 확정 관문으로 승격

## 한 줄 게이트 (준비 완료 ≠ 확정)

로컬에서 아래가 모두 초록이면 **준비는 됐다.** 확정은 아니다.

```bash
python3 tools/lower.py --check
python3 tools/check_delimiter.py
python3 tools/check_semantic_min.py
bash tools/check_semantic_native.sh
python3 tools/check_corpus.py
```

기대 요약 줄:

```text
BYTE fixture PASS
DELIMITER PASS
SEMANTIC_MIN=PASS
FX_NATIVE=PASS
CORPUS_STDLIB=PASS
CORE_V0_FINAL=NOT_YET
```

## 다음 안건 후보 (하나만 연다)

1. app 코퍼스 GAP 표 고정 (표현 없이)
2. 세 사용자 Core v0 닫기 표결 안건
3. 코퍼스 app 중 Core에 들어오는 순수 함수만 추가 (폭 최소)

확정 커밋은 위 PASS·표결이 모인 뒤에만 한다.
