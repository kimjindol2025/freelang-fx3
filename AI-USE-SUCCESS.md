# FX3 AI 사용 성공 정의

기준일: 2026-09-29

```text
LOCK=AI_USE_SUCCESS_V0
STATUS=FIXED
DIALECT=FX3_CORE
AUDIENCE=AI_AUTHOR
GENEALOGY_FRAMING=MINIMIZED
COMPARE_TO_OTHER_LANGS=NOT_NOW
REFERENCE_ONLY=USER-STUDY,CORE_NOTES,BENCH_HISTORY
```

이 문서는 **앞으로의 방향 고정**이다. 리서치·사용자 리뷰·벤치 기록은 참고다. 충돌하면 이 파일의 PASS/FAIL이 이긴다.

목표는 “기존 언어와 견줄 만한가”가 아니다. 목표는 이것이다.

> AI가 이 언어를 **쓰고**, **고치고**, **오래 다시 써도** 되는가.

FX3는 FX 계보 설명으로 정당화하지 않는다. 실행 다리는 필요할 때만 쓰고, 성공 판정은 AI 사용 루프로 한다.

---

## 성공의 세 줄

| ID | 문장 | 한 줄 |
|----|------|-------|
| U1 | 써도 문제없다 | 첫 출력이 이 방언으로 내려가고 기대한 뜻을 깨지 않는다 |
| U2 | 쓰면서 고칠 수 있다 | 틀린 곳이 그 자리에서 끝나고, 파일 뒤로 밀리지 않는다 |
| U3 | 오래 써도 질리지 않는다 | 다시 열 때 사전이 필요 없고, 같은 밀도·같은 이름이 유지된다 |

세 줄이 모두 PASS여야 “AI가 쓰는 언어”로 판정한다. 한 줄이라도 FAIL이면 성공이 아니다.

---

## U1 — 써도 문제없다

**뜻:** 계약이 눈앞에 있을 때, AI가 낸 첫 유효 출력이 FX3 Core로 성립하고 의미가 깨지지 않는다.

**필수 조건**

1. 방언은 FX3 Core다. 생성 전 [AI-ENTRY.md](AI-ENTRY.md) 최소 조각을 붙인다.
2. 첫 출력이 `tools/lower.py`에 통과한다.
3. 기대한 canonical `.fl`(또는 잠긴 테스트)과 의미가 맞는다. 바이트 비교가 있는 과제면 바이트가 이긴다.
4. AFJ·FX Lisp 철자·다른 방언을 섞지 않는다.

**PASS**

- 동일 과제 N회 중 첫 시도 유효 비율이 합의 임계 이상.
- 기본 임계: **첫 시도 유효 ≥ 2/3** (과제 묶음마다 기록). 더 높은 임계는 이 파일을 개정할 때만 올린다.

**FAIL**

- 안내 없는 생성에서 `{}`·`;`·바인딩 위치를 반복해서 발명·생략한다.
- lower 전에 다른 방언 문법이 섞인다.
- “실행은 나중에”를 이유로 첫 출력 유효를 PASS로 적는다.

**측정**

- [bench/metrics](bench/metrics/README.md): `FIRST_PASS_HINT`, lowering 로그, 기대 비교.
- 타이밍·파이썬 대비 승리는 U1 조건이 아니다.

---

## U2 — 쓰면서 고칠 수 있다

**뜻:** 틀린 뒤에도 AI가 같은 표면에서 고치고, 수정 범위가 국소적이다.

**필수 조건**

1. 수리 프롬프트는 같은 FX3 Core 계약을 유지한다.
2. 한 글자·한 기호 실수가 파일 전체 해석을 밀지 않는다.
3. 수정 횟수와 수정 폭을 기록한다.

**PASS**

- 최종 유효에 도달한다 (과제 포기 없음).
- `EDIT_SPAN` / `EDIT_LOCALITY`를 남긴다.
- 기본 임계: 최종 유효 **≥ 3/3** (또는 합의 N) 이면서, 통과 trial의 `EDIT_LOCALITY` 중앙값이 **≤ 0.25**. 임계 변경은 개정으로만.

**FAIL**

- 수리가 방언을 바꾸거나 파이썬·FX Lisp로 탈출한다.
- 같은 오류 타입이 반복만 되고 국소 수정이 안 된다 (`CORRECTION_HINT=CHANGED`인데 위치가 매번 흩어짐).
- 수정 폭을 재지 않고 “고쳤다”고 적는다.

**측정**

- `EDIT_SPAN`, `EDIT_LOCALITY`, `CORRECTION_HINT`, repair 라운드 수.
- [DIALECT-FX3-CORE.md](DIALECT-FX3-CORE.md)의 바인딩·`;`·맵/블록 규칙을 깨는 수정은 실패로 분류한다.

---

## U3 — 오래 써도 질리지 않는다

**뜻:** 며칠·여러 과제 뒤에도 같은 표면으로 다시 열고 쓰고 싶어지는가. 사전·예외·계보 설명이 늘어나지 않는다.

**필수 조건**

1. 의미 있는 이름은 유지한다. `str_upper` → `U` 금지 (Core).
2. 새 기호·Hot Alias·극단 압축을 Core에 넣지 않는다. 후보는 후보로만 경쟁한다.
3. 다시 읽기 단위는 `;` 분할 표시까지다. 줄바꿈을 문법으로 추가하지 않는다.
4. 매 세션 필요한 사전은 [AI-ENTRY.md](AI-ENTRY.md) 한도다. 그 이상 코드북이 필요하면 U3 실패 후보.

**PASS**

- 연속 과제 묶음에서 AI-ENTRY 조각을 **늘리지 않고** U1·U2를 유지한다.
- 사용자(AI 사용자 포함)가 “다시 열 때 사전이 더 필요해졌다”를 FAIL로 기록하지 않는다.
- Core 밀도 문장([CORE.md](CORE.md) 기준 줄)을 더 짧게 만들지 않는다.

**FAIL**

- 예외 규칙이 쌓여 AI-ENTRY가 한 화면을 넘기도록 비대해진다.
- 이름 축약·문맥 의존 기호가 Core로 들어온다.
- “계보상 FX라서”만으로 불편한 표면을 유지한다. 불편하면 측정하고, 다리는 다리로만 남긴다.

**측정**

- AI-ENTRY 바이트/줄 수 추이.
- 재독 과제: 이전 성공 소스를 가린 채 같은 과제 재생성·수정 비용.
- 주관 판정은 [USER-STUDY.md](USER-STUDY.md)에 쌓되, **채택 문장은 이 파일 개정으로만** 들어온다.

---

## 지금 하지 않는 판정

다음을 성공으로 치지 않는다. 참고만 한다.

- 파이썬·Rust보다 벽시계가 빠르다
- FX `.fl`보다 바이트가 짧다 (이미 본 절감은 참고)
- 셀프호스트·앱 이식·FX 실행 단계 통과
- 다른 방언(AFJ/Script/Front) 통합 목록

그것들은 별도 안건이다. U1·U2·U3가 닫히기 전에 성공 선언에 넣지 않는다.

---

## 실행 다리 (최소화)

```text
.ai writes .fx3
   → lower.py
   → .fl bytes / FX run (bridge)
```

- 다리(FX 실행)는 의미가 깨졌는지 확인하는 수단이 될 수 있다.
- 다리가 목표 문구가 되지 않는다. 목표 문구는 U1·U2·U3다.
- 자체 런타임·계보 확장은 이 잠금을 개정하거나 새 안건을 열 때만 한다.

---

## 개정 규칙

1. 이 파일의 `LOCK` 이름을 바꾸지 않고 본문만 살짝 고치지 않는다. 임계·문장 변경은 `AI_USE_SUCCESS_V1`처럼 버전을 올린다.
2. USER-STUDY의 의견이 달라도 자동으로 이 파일을 덮지 않는다. 중계자가 좁힌 뒤 개정 안건으로만 반영한다.
3. Core 문법 잠금([CORE.md](CORE.md))과 충돌하면 Core 문법을 조용히 바꾸지 않는다. 충돌을 안건으로 적는다.

---

## 다음 작업이 이 잠금을 쓰는 법

1. 새 벤치·프롬프트·문서의 성공 문구는 U1·U2·U3 중 어디에 속하는지 적는다.
2. 측정 결과는 `bench/metrics` 표에 남기고, 이 파일의 임계와 비교한다.
3. FAIL이면 기능 추가보다 계약·표면·수리 국소성을 먼저 고친다.

## 기록된 묶음

| 묶음 | 대상 | 결과 | 경로 |
|------|------|------|------|
| u1-smoke-20260929 | U1, case 01–06 | PASS 6/6 | [bench/results/u1-smoke-20260929/REPORT.md](bench/results/u1-smoke-20260929/REPORT.md) |
| u2-smoke-20260929 | U2, case 01–03 repair | PASS 3/3, locality median 0.016 | [bench/results/u2-smoke-20260929/REPORT.md](bench/results/u2-smoke-20260929/REPORT.md) |
| u3-smoke-20260929 | U3, regen 01–06 | PASS 6/6, ENTRY same 3204B | [bench/results/u3-smoke-20260929/REPORT.md](bench/results/u3-smoke-20260929/REPORT.md) |
| u1-weak-20260929 | U1 weak signature 01–06 | PASS 6/6, shapes 6 | [bench/results/u1-weak-20260929/REPORT.md](bench/results/u1-weak-20260929/REPORT.md) |
| other-model-20260929 | U1→U3 via gpt-5.6-luna | PACK PASS (U1 5/6, U2 3/3, U3 6/6) | [bench/results/other-model-20260929/REPORT.md](bench/results/other-model-20260929/REPORT.md) |
