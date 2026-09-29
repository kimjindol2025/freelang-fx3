# U1 스모크 결과 — 2026-09-29

```text
AGENDA=U1_SMOKE
LOCK=AI_USE_SUCCESS_V0
MODEL=GROK_BUILD_SESSION
AI_ENTRY=YES
REPAIR=NO
PYTHON_WALL_CLOCK=NO
PACK=CASE_01_06
VALID=6/6
PACK_VERDICT=PASS
```

## 방법

1. [AI-ENTRY.md](../../../AI-ENTRY.md) 최소 규칙을 생성 전에 둔다.
2. `bench/tasks/case-01`…`case-06`의 `TASK_PROMPT`만 읽는다.
3. 각 과제에 첫 `.fx3` 한 파일만 쓴다. 수리 없음.
4. `python3 tools/lower.py` 후 `bench/expected/case-0N.fl`과 바이트 비교.

채점 전에 `expected/*.fx3` 내용은 열지 않았다. 채점 후 동일성만 표시한다.

## 결과

| CASE | LOWER | FL_BYTES | U1_VALID | FX3_IDENTICAL |
|------|-------|----------|----------|---------------|
| 01 | PASS | PASS | PASS | YES |
| 02 | PASS | PASS | PASS | YES |
| 03 | PASS | PASS | PASS | YES |
| 04 | PASS | PASS | PASS | YES |
| 05 | PASS | PASS | PASS | YES |
| 06 | PASS | PASS | PASS | YES |

묶음 임계 ≥ 4/6 → **PASS (6/6)**.

## 한계 (솔직)

- 모델은 이 세션의 Grok Build다. 다른 모델·CLI 재현은 아직이다.
- 과제가 서명이 강한 편이라 정답 모양이 한쪽으로 모인다. FX3_IDENTICAL=YES 6개는 그 제약과, 이 세션이 FX3 문서를 이미 읽은 상태의 영향이 있을 수 있다.
- U2(수정 국소성)·U3(질림)는 측정하지 않았다.
- 파이썬 대비 속도는 재지 않았다.

## 다음

U1 묶음은 닫는다. 다음 후보는 같은 계약으로 **다른 모델/CLI 재현**이거나 **U2 작은 실측**(일부러 깨진 첫 출력을 고쳐 EDIT_LOCALITY)이다.
