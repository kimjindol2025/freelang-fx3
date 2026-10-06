# FX3 세션 미스테이크 · 인수인계 (2026-10-06 ~ 2026-10-07)

작성: Grok Build (이 세션)  
범위: Track1 이후 **위임 run → POC 레일 → 티어 종료(C)**  
상태 정본: `DELEGATED_SMALL_TOOLS=CLOSED_PASS` · `CHOICE=C_STOP` · `RUNTIME_OWNED=NONE`

이 문서는 **잘한 척하지 않고** 실수·못 한 일·다음 에이전트 주의를 남긴다.

---

## 1. 실수한 것 (Mistakes)

### 1.1 소통 · 의사결정

| # | 실수 | 결과 | 교정 |
|---|------|------|------|
| M1 | “다음 갈까요?” 식으로 **선택지를 물어보며** 끊음 | 사용자가 “가야 됩니다까지 분석해 제시”를 요구 | 증거가 있으면 **MUST_NEXT**로 단정 제시. 물은 뒤에만 선택 |
| M2 | “쓸 만해?”에 대한 답을 처음에 애매하게 둘 뻔함 | 기대와 런타임 완성도를 섞을 위험 | CLI/위임 도구 vs owned VM을 **문장에서 분리** |
| M3 | 커밋/푸시를 매번 물어보려 함 | 사용자가 “PASS면 너가 커밋·푸시” 규칙을 줌 | FX3 본인 작업 기록: **PASS → commit(+push), FAIL → 고칠 때까지** |

### 1.2 기술 · 구현

| # | 실수 | 결과 | 교정 |
|---|------|------|------|
| M4 | POC #1에서 `eval_fl_min`에 builtins를 **직접 넣으려다** 금지와 충돌 | 경계 흔들림 | `eval_fl_ext.py` 심으로 우회. **`eval_fl_min.py` 미수정** 유지 |
| M5 | FX3 `==` 가 native CGC `=` 와 다르다는 걸 **run 구현 후** 발견 | native build 실패 | CLI `_fl_for_native`: `(==` → `(=` |
| M6 | `--call` 맵 키 bare symbol이 native `.fl`에선 깨짐 | native 인자 오류 | CLI가 native용 **문자열 키**로 재방출 |
| M7 | 여러 `F` 헬퍼로 짜려다 **단일 top-level F**에 막힘 | 설계 재작성 | 헬퍼 인라인·조건 중첩. LIMITS에 고정 |
| M8 | `?` 분기에 `$x=...` 바인딩을 넣음 | parse 실패 | 선두 let만. 분기는 단일 식 |
| M9 | `string?` / `vector?` 호출 시도 | `?` 토큰이 if와 충돌 | `type-of(...)=="..."` |
| M10 | if 분기 값으로 `-1` → `{-1}` 이 **맵**으로 파싱 | `E_UNEXPECTED_TOKEN` | 센티널은 `99` 등, 음수는 `( -1 )` 또는 회피 |
| M11 | Core에 **벡터 리터럴 `[]`/`[a,b]`** 가 없다고 가정하지 않고 POC #3 설계 | “진짜 배열 정규화” 불가 | `count`+`t0..t2` 슬롯으로 우회하고 LIMITS에 **구멍으로 기록** |
| M12 | 선두에서 `@$t.id` / `get($tasks,i)` 를 nil tasks에 평가 | **eval PASS · native FAIL** (동등성 깨짐) | 배열 확정 후에만 get. nil-safe 바인딩. **native를 반드시 fixture에 포함** |
| M13 | empty map `{}` lower 불가·빈 벡터 식 불가를 늦게 학습 | 결과 맵/리스트 설계 재작업 | 결과 맵에 키를 항상 둠. 리스트는 슬롯 또는 입력 `$tasks` 재사용 |
| M14 | `check_poc` / verify를 돌리기 전에 “됐다”고 말하기 직전 단계가 있었음 | 08-missing-tasks native miss | **PASS 판정은 tool 출력 후에만**. FAIL이면 고치고 재실행 후 커밋 |

### 1.3 프로세스

| # | 실수 | 결과 | 교정 |
|---|------|------|------|
| M15 | 같은 맵 검증 POC를 반복할 뻔함 (#2 직후 #3 없이 공회전 위험) | 사용자가 “가야 됩니다” 분석으로 강제 | 티어 닫기 전 **미증명 LIMITS 문장만** 찌름 |
| M16 | memory topic 편집 시 concurrent write로 실패 | 인수 메모 일부 누락 | 재읽기 후 편집. 중요 사실은 **repo docs**에 남김 |
| M17 | native 케이스가 많은 verify는 수분~십수분 | 타임아웃/대기 필요 | `block_until` 충분히. 빠른 스모크 후 full gate |

---

## 2. 못 한 것 / 일부러 안 한 것 (Not done)

의도적으로 열지 않음 (계약 준수):

- 전용 FX3 VM (`RUNTIME_OWNED=NONE` 유지)
- IR executor
- capability **실** 파일 read/write I/O
- self-hosting
- `eval_fl_min.py` 본문 수정
- Core 문법 임의 확장 (벡터 리터럴 포함) — **안건 A로만** 남김
- 제품 본체를 FX3로 대체

티어 종료 후 선택 **C(정지)** 로 잠금:

- A Core vector literal — 미착수
- B capability read I/O — 미착수
- 추가 동형 POC — **금지** (`CLOSED_PASS`)

기술 부채로 남은 것 (못 함 = 아직 구멍):

1. Core에서 새 `[]` 를 만들어 반환하지 못함 → 슬롯 정규화 우회
2. eval과 native의 nil/`get`/`==` 의미가 다름 → CLI·작성 규약으로 보정 중
3. 단일 F · 분기 바인딩 금지 → 큰 로직이 한 함수에 팽창
4. `eval_fl_ext` 심 의존 — “진짜 FX stdlib”가 아님

---

## 3. 잘한 것 (What went well)

| # | 내용 |
|---|------|
| G1 | 위임 run 계약을 먼저 문서화 (`FX3-RUN.md`) 후 CLI 구현 |
| G2 | `eval_fl_min` 미수정 + `eval_fl_ext` 분리 |
| G3 | POC 레일: `poc.json` + fixtures + `tools/check_poc.py` |
| G4 | POC 3종으로 맵 → 레일 → 배열 언롤 경계를 **순서대로** 증명 |
| G5 | LIMITS / CLOSE 문서에 구멍을 **숨기지 않고** 기록 |
| G6 | eval≡native·결정성·usage·정적 I/O 금지를 게이트에 포함 |
| G7 | PASS 후 커밋·푸시, FAIL 시 재실행 (사용자 규칙 정착) |
| G8 | 티어 `CLOSED_PASS` + 선택 **C_STOP** 으로 세션을 실제로 닫음 |
| G9 | owned runtime 완성을 **과장하지 않음** |

---

## 4. 다음 에이전트에게 (Handoff)

### 4.1 현재 진실

```text
DELEGATED_SMALL_TOOLS=CLOSED_PASS
CHOICE=C_STOP
RUNTIME_OWNED=NONE
RUN=DELEGATED
IO_CHANGE=NO
IR_EXEC=NO
```

정본 문서:

- `docs/FX3-DELEGATED-SMALL-TOOLS-CLOSE.md`
- `docs/FX3-DELEGATED-LIMITS.md`
- `docs/FX3-RUN.md`
- `STATUS.md` / `ROADMAP.md` / `poc/README.md`

검증:

```bash
python3 tools/check_poc.py all
python3 tools/check_cli.py
./bin/fx3 test --quick
python3 tools/check_{lex,parse,lower,ir,capability}.py
git diff --check
```

### 4.2 하지 말 것

1. 동형 업무 POC를 “하나 더” 만들지 말 것 (티어 닫힘).
2. `eval_fl_min.py` 고치지 말 것. 심은 `eval_fl_ext.py`.
3. `tools/lower.py`(레거시)를 run 경로에 쓰지 말 것. AST `fx3_lower`만.
4. PASS 없이 “완료” 말하지 말 것. native 빠진 eval-only PASS를 동등성으로 치지 말 것.
5. A/B를 사용자 새 안건·새 gate 없이 자동으로 열지 말 것.

### 4.3 다시 열 때 (NEW_ROAD만)

| 안건 | 열 조건 | 첫 증거 |
|------|---------|---------|
| **A** Core vector literal | 사용자가 NEW_ROAD로 명시 | `[]`/`[a,b]` parse+lower+golden + task-list가 **슬롯 없이** `tasks` 배열 반환 |
| **B** capability read I/O | 사용자가 NEW_ROAD로 명시 | 계약 문서 → deny-first 유지한 **읽기 스모크만** (쓰기/exec/net 금지) |
| **C** 유지 | 기본 | 제품은 Script/AFJ/FX, FX3는 위임 도구만 |

### 4.4 재발 방지 체크리스트

- [ ] `--engine=native` fixture 포함했는가
- [ ] nil/`get` 선두 평가 없는가
- [ ] 단일 top-level `F`인가
- [ ] `?` 분기에 바인딩 없는가
- [ ] 결과 empty map / vector literal 없는가
- [ ] `check_poc` 또는 해당 gate 출력이 PASS인가
- [ ] LIMITS에 새 구멍을 적었는가

---

## 5. 한 줄 요약

**위임 작은 도구 티어는 닫혔고(C), 런타임은 없다.**  
오늘 최대 실수는 “동등성·Core 한계를 나중에 발견”한 것과 “갈까요?” 소통이다.  
다음 에이전트는 **닫힌 티어를 존중**하고, A/B는 새 안건으로만 열어라.
